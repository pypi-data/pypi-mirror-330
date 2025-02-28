"""
Pipeline for BFOSC Grisms
"""

import os, argparse, warnings, toml
from glob import glob

# NumPy
import numpy as np
# AstroPy
import astropy.units as u
from astropy.io import fits
from astropy.stats import mad_std
from astropy.nddata import CCDData
from astropy.config import reload_config
from astropy.utils.exceptions import AstropyUserWarning
# ccdproc
from ccdproc import ImageFileCollection, cosmicray_lacosmic
from ccdproc.utils.slices import slice_from_string
# specutils
from specutils import Spectrum1D
# drpy
from drpy.batch import CCDDataList
from drpy.image import concatenate
from drpy.utils import imstatistics
from drpy.plotting import plot2d, plotSpectrum1D
from drpy.twodspec import (response, illumination, align, fitcoords, transform, trace, 
                           background, profile, extract, calibrate2d)
from drpy.twodspec.utils import invertCoordinateMap
from drpy.onedspec import dispcor, sensfunc, calibrate1d# , saveSpectrum1D

from .. import conf
from ..utils import login, makeDirectory, getMask

# Load parameters from configuration file
reload_config(packageormod='plpy', rootname='plpy')


def pipeline(save_dir, data_dir, semester, grism, slit_width, standard, reference, 
             shouldCombine, keyword, shouldExtract, verbose):
    """BFOSC pipeline."""

    # Login message
    if verbose:
        login(f'2.16-m/BFOSC {grism}', 100)
    
    # Make directories
    if verbose:
        print('\n[MAKE DIRECTORIES]')
        print(f'  - Changing working directory to {save_dir}...')
    os.chdir(save_dir)

    # Check setup
    for directory in ['cal', 'fig', 'red']:
        if not os.path.isdir(directory):
            raise RuntimeError(f'Run command `plpy_setup` first to set up {save_dir}.')
    if not os.path.isfile('params.toml'):
        raise RuntimeError(f'Run command `plpy_setup` first to set up {save_dir}.')

    # Load inputs
    params = toml.load('params.toml')

    if params['slit_along'] == 'col':
        dispersion_axis = 'row'
    else:
        dispersion_axis = 'col'

    # Custom mask
    if grism == 'g3':
        custom_mask = np.zeros(params['shape'], dtype=bool)

    elif grism == 'g4':
        path_to_semester = os.path.join(os.path.split(__file__)[0], f'lib/{semester}')
        if not os.path.exists(path_to_semester):
            path_to_semester = sorted(glob(
                os.path.join(os.path.split(__file__)[0], f'lib/*/')))[-1]
            warnings.warn(
                f'Semester {semester} not found. Bad regions of '
                f"{path_to_semester.split('/')[-2]} (latest) will be used.", 
                RuntimeWarning)
            semester = path_to_semester.split('/')[-2]

        path_to_region = os.path.join(
            path_to_semester, f'bfosc_{grism}_slit{slit_width}_{semester}.reg')
        custom_mask = getMask(path_to_region=path_to_region, shape=params['shape'])

    # Better not to use slit18 for slit23. (at least for g3)
    if not reference:
        reference = sorted(glob(os.path.join(
            os.path.split(__file__)[0], f'lib/bfosc_{grism}_slit{slit_width}*.fits'
        )))[-1]
    else:
        reference = os.path.abspath(reference)
    if not os.path.exists(reference):
        raise ValueError('Reference not found.')

    # Construct image file collection
    ifc = ImageFileCollection(
        location=data_dir, keywords=params['keywords'], find_fits_by_reading=False, 
        filenames=None, glob_include=params['include'], glob_exclude=params['exclude'], 
        ext=params['hdu'])
        
    if verbose:
        print('\n[OVERVIEW]')
        ifc.summary.pprint_all()
    
    # Load gain and readout noise
    first_file = ifc.files_filtered(include_path=True)[0]
    gain = fits.getval(first_file, 'GAIN', ext=params['hdu']) * u.photon / u.adu
    rdnoise = fits.getval(first_file, 'RDNOISE', ext=params['hdu']) * u.photon
    
    if 'trim' in params['steps']:
        custom_mask = custom_mask[
            slice_from_string(params['fits_section'], fits_convention=True)
        ]
        trim = True
    else:
        trim = False
    
    # Bias combination
    if ('bias.combine' in params['steps']) or ('bias' in params['steps']):
        
        if verbose:
            print('\n[BIAS COMBINATION]')
        
        # Load bias
        if verbose:
            print('  - Loading bias...')
        ifc_bias = ifc.filter(regex_match=True, imagetyp='Bias Frame')
        bias_list = CCDDataList.read(
            file_list=ifc_bias.files_filtered(include_path=True), hdu=params['hdu'])

        # Trim
        if trim:
            if verbose:
                print('  - Trimming...')
            bias_list = bias_list.trim_image(fits_section=params['fits_section'])
        
        # Correct gain
        if verbose:
            print('  - Correcting gain...')
        bias_list_gain_corrected = bias_list.gain_correct(gain=gain)
        
        bias_list_gain_corrected.statistics(verbose=verbose)
        
        # Combine bias
        if verbose:
            print('  - Combining...')
        bias_combined = bias_list_gain_corrected.combine(
            method='average', mem_limit=conf.mem_limit, sigma_clip=True, 
            sigma_clip_low_thresh=3, sigma_clip_high_thresh=3, 
            sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std, 
            output_file='cal/bias_combined.fits', dtype=conf.dtype, 
            overwrite_output=True)
        
        imstatistics(bias_combined, verbose=verbose)
        
        # Plot combined bias
        plot2d(
            bias_combined.data, title='bias combined', show=conf.show, save=conf.save, 
            path='fig')
        
        # Release memory
        del bias_list

    # Flat combination
    if ('flat.combine' in params['steps']) or ('flat' in params['steps']):
        
        if verbose:
            print('\n[FLAT COMBINATION]')
        
        # Load flat
        if verbose:
            print('  - Loading flat...')
        ifc_flat = ifc.filter(regex_match=True, obstype='SPECLFLAT')
        flat_list = CCDDataList.read(
            file_list=ifc_flat.files_filtered(include_path=True), hdu=params['hdu'])
        
        # Trim
        if trim:
            if verbose:
                print('  - Trimming...')
            flat_list = flat_list.trim_image(fits_section=params['fits_section'])
        
        # Correct gain
        if verbose:
            print('  - Correcting gain...')
        flat_list_gain_corrected = flat_list.gain_correct(gain=gain)
        
        flat_list_gain_corrected.statistics(verbose=verbose)

        # Subtract bias
        # Uncertainties created here (equal to that of ``bias_combined``) are useless!!!
        if verbose:
            print('  - Subtracting bias...')
        if 'bias_combined' not in locals():
            bias_combined = CCDData.read('cal/bias_combined.fits')
        flat_list_bias_subtracted = flat_list_gain_corrected.subtract_bias(
            bias_combined
        )
        
        flat_list_bias_subtracted.statistics(verbose=verbose)

        # Combine flat
        #   Uncertainties created above are overwritten here!!!
        if verbose:
            print('  - Combining...')
        scaling_func = lambda ccd: 1 / np.ma.average(ccd)
        flat_combined = flat_list_bias_subtracted.combine(
            method='average', scale=scaling_func, mem_limit=conf.mem_limit, 
            sigma_clip=True, sigma_clip_low_thresh=3, sigma_clip_high_thresh=3, 
            sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std, 
            output_file='cal/flat_combined.fits', dtype=conf.dtype, 
            overwrite_output=True)

        imstatistics(flat_combined, verbose=verbose)

        # Plot combined flat
        plot2d(
            flat_combined.data, title='flat combined', show=conf.show, save=conf.save, 
            path='fig')

        # Release memory
        del flat_list, flat_list_bias_subtracted

    # Response
    if ('flat.normalize.response' in params['steps']) or \
       ('flat.normalize' in params['steps']) or \
       ('flat' in params['steps']):
        
        if verbose:
            print('\n[RESPONSE]')
        
        # Response calibration
        if 'flat_combined' not in locals():
            flat_combined = CCDData.read('cal/flat_combined.fits')
        flat_combined.mask |= custom_mask
        reflat = response(
            ccd=flat_combined, slit_along=params['slit_along'], 
            n_piece=params['flat']['n_piece'], maxiters=0, sigma_lower=None, 
            sigma_upper=None, grow=False, use_mask=True, plot=conf.save, path='fig')
        reflat = flat_combined.divide(reflat, handle_meta='first_found')
        
        imstatistics(reflat, verbose=verbose)
        
        # Plot response corrected flat
        plot2d(
            reflat.data, title='flat response corrected', show=conf.show, 
            save=conf.save, path='fig')
        
        # Plot response mask
        plot2d(
            reflat.mask.astype(int), vmin=0, vmax=1, title='mask response', 
            show=conf.show, save=conf.save, path='fig')
        
        # Write response calibrated flat to file
        reflat.write('cal/flat_response_corrected.fits', overwrite=True)
    
    # Illumination
    if ('flat.normalize.illumination' in params['steps']) or \
       ('flat.normalize' in params['steps']) or \
       ('flat' in params['steps']):

        if verbose:
            print('\n[ILLUMINATION]')
        
        # Illumination modeling
        if 'reflat' not in locals():
            reflat = CCDData.read('cal/flat_response_corrected.fits')
        ilflat = illumination(
            ccd=reflat, slit_along=params['slit_along'], method='Gaussian2D', 
            sigma=params['flat']['sigma'], bins=10, maxiters=5, sigma_lower=3, 
            sigma_upper=3, grow=5, use_mask=True, plot=conf.save, path='fig')

        # Plot illumination
        plot2d(
            ilflat.data, title='illumination', show=conf.show, save=conf.save, 
            path='fig')
        
        # Plot illumination mask
        plot2d(
            ilflat.mask.astype(int), vmin=0, vmax=1, title='mask illumination', 
            show=conf.show, save=conf.save, path='fig')
        
        # Write illumination to file
        ilflat.write('cal/illumination.fits', overwrite=True)

    # Flat normalization
    if ('flat.normalize' in params['steps']) or ('flat' in params['steps']):
        
        if verbose:
            print('\n[FLAT NORMALIZATION]')
        
        # Normalization
        if 'reflat' not in locals():
            reflat = CCDData.read('cal/flat_response_corrected.fits')
        if 'ilflat' not in locals():
            ilflat = CCDData.read('cal/illumination.fits')
        flat_normalized = reflat.divide(ilflat, handle_meta='first_found')
        
        # Plot normalized flat
        plot2d(
            flat_normalized.data, title='flat normalized', show=conf.show, 
            save=conf.save, path='fig')
        
        # Plot normalized flat mask
        plot2d(
            flat_normalized.mask.astype(int), title='mask flat normalized', 
            show=conf.show, save=conf.save, path='fig')
        
        flat_normalized.mask = None
        
        # Write normalized flat to file
        flat_normalized.write('cal/flat_normalized.fits', overwrite=True)
    
    # Lamp concatenation
    if ('lamp.concatenate' in params['steps']) or ('lamp' in params['steps']):
        
        if verbose:
            print('\n[LAMP CONCATENATION]')
        
        # Load lamp
        if verbose:
            print('  - Loading lamp...')
        ifc_lamp = ifc.filter(regex_match=True, obstype='SPECLLAMP')
        lamp_list = CCDDataList.read(
            file_list=ifc_lamp.files_filtered(include_path=True), hdu=params['hdu'])

        # Trim
        if trim:
            if verbose:
                print('  - Trimming...')
            lamp_list = lamp_list.trim_image(fits_section=params['fits_section'])
        
        # Correct gain
        if verbose:
            print('  - Correcting gain...')
        lamp_list_gain_corrected = lamp_list.gain_correct(gain=gain)
        
        lamp_list_gain_corrected.statistics(verbose=verbose)
        
        # Subtract bias
        #   Uncertainties created here (equal to that of ``bias_combined``) are useless!!!
        if verbose:
            print('  - Subtracting bias...')
        if 'bias_combined' not in locals():
            bias_combined = CCDData.read('cal/bias_combined.fits')
        lamp_list_bias_subtracted = lamp_list_gain_corrected.subtract_bias(
            bias_combined
        )
        
        lamp_list_bias_subtracted.statistics(verbose=verbose)
        
        # Create real uncertainty!!!
        if verbose:
            print('  - Creating deviation...')
        lamp_list_bias_subtracted_with_deviation = (
            lamp_list_bias_subtracted.create_deviation(
                gain=None, readnoise=rdnoise, disregard_nan=True)
        )
        
        # Concatenate if there are two lamp frames
        if len(lamp_list_bias_subtracted_with_deviation) == 2:
            if verbose:
                print('  - Concatenating...')
            # Ensure that the first is the short exposure
            exptime = ifc_lamp.summary['exptime'].data
            if exptime[0] > exptime[1]:
                lamp_list_bias_subtracted_with_deviation = (
                    lamp_list_bias_subtracted_with_deviation[::-1]
                )
            lamp_concatenated = concatenate(
                lamp_list_bias_subtracted_with_deviation, 
                fits_section=f"[:{params['index']}, :]", scale=None)

        else:
            lamp_concatenated = lamp_list_bias_subtracted_with_deviation[0]
        
        # Plot concatenated lamp
        plot2d(
            lamp_concatenated.data, title='lamp concatenated', show=conf.show, 
            save=conf.save, path='fig')
        
        # Write concatenated lamp to file
        lamp_concatenated.write('cal/lamp_concatenated.fits', overwrite=True)
        
        # Release memory
        del (lamp_list, lamp_list_bias_subtracted, 
             lamp_list_bias_subtracted_with_deviation)
    
    # Curvature rectification
    if ('lamp.rectify' in params['steps']) or ('lamp' in params['steps']):
        
        if verbose:
            print('\n[CURVATURE RECTIFICATION]')
        
        # Fit coordinates
        if verbose:
            print('  - Fitting coordinates...')
        if 'lamp_concatenated' not in locals():
            lamp_concatenated = CCDData.read('cal/lamp_concatenated.fits')
        U, _ = fitcoords(
            ccd=lamp_concatenated, slit_along=params['slit_along'], order=1, n_med=15, 
            n_piece=3, prominence=1e-3, maxiters=3, sigma_lower=3, sigma_upper=3, 
            grow=False, use_mask=False, plot=conf.save, path='fig', height=0, 
            threshold=0, distance=5, width=5, wlen=15, rel_height=1, plateau_size=1)
        
        # Invert coordinate map
        if verbose:
            print('  - Inverting coordinate map...')
        X, Y = invertCoordinateMap(params['slit_along'], U)
        np.save('cal/X.npy', X)
        np.save('cal/Y.npy', Y)
        
        # Rectify curvature
        if verbose:
            print('  - Rectifying curvature...')
        lamp_transformed = transform(ccd=lamp_concatenated, X=X, Y=Y)
        
        # Plot transformed lamp
        plot2d(
            lamp_transformed.data, title='lamp transformed', show=conf.show, 
            save=conf.save, path='fig')
        
        # Write transformed lamp to file
        lamp_transformed.write('cal/lamp_transformed.fits', overwrite=True)
    
    # Correct targets
    if ('targ' in params['steps']):
        
        if verbose:
            print('\n[CORRECTION]')
        
        # Load targ
        if verbose:
            print('  - Loading targ...')
        ifc_targ = ifc.filter(regex_match=True, obstype='SPECLTARGET|SPECLFLUXREF')
        targ_list = CCDDataList.read(
            file_list=ifc_targ.files_filtered(include_path=True), hdu=params['hdu'])
        
        # Trim
        if trim:
            if verbose:
                print('  - Trimming...')
            targ_list = targ_list.trim_image(fits_section=params['fits_section'])
        
        # Correct gain
        if verbose:
            print('  - Correcting gain...')
        targ_list_gain_corrected = targ_list.gain_correct(gain=gain)
        
        targ_list_gain_corrected.statistics(verbose=verbose)
        
        # Subtract bias
        #   Uncertainties created here (equal to that of ``bias_combined``) are useless!!!
        if verbose:
            print('  - Subtracting bias...')
        if 'bias_combined' not in locals():
            bias_combined = CCDData.read('cal/bias_combined.fits')
        targ_list_bias_subtracted = targ_list_gain_corrected.subtract_bias(
            bias_combined
        )
        
        targ_list_bias_subtracted.statistics(verbose=verbose)

        # Create real uncertainty!!!
        if verbose:
            print('  - Creating deviation...')
        targ_list_bias_subtracted_with_deviation = (
            targ_list_bias_subtracted.create_deviation(
                gain=None, readnoise=rdnoise, disregard_nan=True)
        )
        
        # Flat-fielding
        if verbose:
            print('  - Flat-fielding...')
        if 'flat_normalized' not in locals():
            flat_normalized = CCDData.read('cal/flat_normalized.fits')
        targ_list_flat_fielded = (
            targ_list_bias_subtracted_with_deviation.flat_correct(flat_normalized)
        )
        
        # Identify flux standard
        isStandard = ifc_targ.summary['obstype'].data == 'SPECLFLUXREF'

        if isStandard.sum() > 0:
            
            # if isStandard.sum() > 1:
            #     raise RuntimeError('More than one standard spectrum found.')
                
            # Only the first standard is used
            index_standard = np.where(isStandard)[0][0]

            key_standard = ifc_targ.summary['object'].data[index_standard]
            standard_flat_fielded = targ_list_flat_fielded[index_standard]

            # Plot
            plot2d(
                standard_flat_fielded.data, title=f'{key_standard} flat-fielded', 
                show=conf.show, save=conf.save, path='fig')

            # Write standard spectrum to file
            if verbose:
                print('\n[STANDARD]')
                print(
                    f'  - Saving flat-fielded spectrum of {key_standard} to red/...')
            standard_flat_fielded.write(
                f'red/{key_standard}_flat_fielded.fits', overwrite=True)

            if verbose:
                print(f'  - Tracing {key_standard}...')
        
            # Trace (trace the brightest spectrum)
            trace1d_standard = trace(
                ccd=standard_flat_fielded, dispersion_axis=dispersion_axis, fwhm=10, 
                mode='trace', method='gaussian', n_med=10, interval='[:]', n_piece=5, 
                maxiters=5, sigma_lower=2, sigma_upper=2, grow=False, 
                title=key_standard, show=conf.show, save=conf.save, path='fig')

            # Write standard trace to file (of type float64)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=AstropyUserWarning)
                trace1d_standard.write(
                    f'cal/trace1d_{key_standard}.fits', format='tabular-fits', 
                    overwrite=True)

            if verbose:
                print('  - Extracting 1-dimensional lamp spectra...')

            # Extract lamp spectrum for standard (of type float64)
            if 'lamp_concatenated' not in locals():
                lamp_concatenated = CCDData.read('cal/lamp_concatenated.fits')
            lamp1d_standard = extract(
                ccd=lamp_concatenated, dispersion_axis=dispersion_axis, method='sum', 
                trace1d=trace1d_standard, aper_width=150, n_aper=1, 
                title=f'lamp1d {key_standard}', show=conf.show, save=conf.save, 
                path='fig')

            if verbose:
                print('  - Correcting dispersion axis of lamp spectra...')

            # Correct dispersion of lamp spectrum for standard (of type float64)
            lamp1d_standard_calibrated = dispcor(
                spectrum1d=lamp1d_standard, reverse=True, reference=reference, 
                n_sub=20, refit=True, degree=1, maxiters=5, sigma_lower=3, 
                sigma_upper=3, grow=False, use_mask=True, title=key_standard, 
                show=conf.show, save=conf.save, path='fig')

            if verbose:
                print(f'  - Saving calibrated lamp spectra to cal/...')

            # Write calibrated lamp spectrum for standard to file (of type float64)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=AstropyUserWarning)
                lamp1d_standard_calibrated.write(
                    f'cal/lamp1d_{key_standard}.fits', format='tabular-fits', 
                    overwrite=True)

            if verbose:
                print(f'  - Modeling sky background of {key_standard}...')

            # Model sky background of standard
            background2d_standard = background(
                ccd=standard_flat_fielded, dispersion_axis=dispersion_axis, 
                trace1d=trace1d_standard, 
                location=params['background']['location_standard'], 
                aper_width=params['background']['width_standard'], 
                degree=params['background']['order_standard'], 
                maxiters=3, sigma_lower=4, sigma_upper=4, grow=False, 
                use_uncertainty=False, use_mask=True, title=key_standard, 
                show=conf.show, save=conf.save, path='fig')

            # Plot sky background of standard
            plot2d(
                background2d_standard.data, title=f'background2d {key_standard}', 
                show=conf.show, save=conf.save, path='fig')

            # Write sky background of standard to file
            background2d_standard.write(
                f'red/background2d_{key_standard}.fits', overwrite=True)

            if verbose:
                print(
                    f'  - Extracting sky background spectrum of {key_standard}...')

            # Extract background spectrum of standard
            background1d_standard = extract(
                ccd=background2d_standard, dispersion_axis=dispersion_axis, 
                method='sum', trace1d=trace1d_standard, aper_width=150, n_aper=1, 
                use_uncertainty=False, use_mask=True, 
                spectral_axis=lamp1d_standard_calibrated.spectral_axis, show=False, 
                save=False)

            # Plot background spectrum of standard
            plotSpectrum1D(
                background1d_standard, title=f'{key_standard} background1d', 
                show=conf.show, save=conf.save, path='fig')

            # Write sky background spectrum of standard to file (of type float64)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=AstropyUserWarning)
                background1d_standard.write(
                    f'cal/background1d_{key_standard}.fits', format='tabular-fits', 
                    overwrite=True)

            if verbose:
                print(f'  - Subtracting sky background from {key_standard}...')

            # Subtract sky background from standard
            standard_background_subtracted = standard_flat_fielded.subtract(
                background2d_standard, handle_meta='first_found')

            # Plot background subtracted standard
            plot2d(
                standard_background_subtracted.data, 
                title=f'{key_standard} background subtracted', show=conf.show, 
                save=conf.save, path='fig')

            # Write background subtracted standard to file
            standard_background_subtracted.write(
                f'red/{key_standard}_background_subtracted.fits', overwrite=True)

            # Extract standard spectrum
            if verbose:
                print(
                    f'  - Extracting spectrum of {key_standard} (standard) '
                    f"({params['extract']['method_standard']})..."
                )

            if params['extract']['method_standard'] == 'sum':

#                 standard_cosmicray_corrected, crmask = cosmicray_lacosmic(
#                     standard_background_subtracted.data, 
#                     gain=(1 * u.dimensionless_unscaled),  readnoise=rdnoise, 
#                     sigclip=4.5, sigfrac=0.3, objlim=1, niter=5, verbose=True)

#                 standard_background_subtracted.data = standard_cosmicray_corrected
#                 standard_background_subtracted.mask = crmask

                # Extract (sum)
                standard1d = extract(
                    ccd=standard_background_subtracted, 
                    dispersion_axis=dispersion_axis, method='sum', 
                    trace1d=trace1d_standard, 
                    aper_width=params['extract']['width_standard'], n_aper=1, 
                    spectral_axis=lamp1d_standard_calibrated.spectral_axis, 
                    use_uncertainty=True, use_mask=True, title=key_standard, 
                    show=conf.show, save=conf.save, path='fig')

            else:

                # Model spatial profile of standard
                profile2d_standard, _ = profile(
                    ccd=standard_background_subtracted, 
                    slit_along=params['slit_along'], trace1d=trace1d_standard, 
                    profile_width=params['extract']['width_standard'], 
                    window_length=params['extract']['pfl_window_standard'], 
                    polyorder=params['extract']['pfl_order_standard'], 
                    deriv=0, delta=1.0, title='profile', show=conf.show, 
                    save=conf.save, path='fig')

                # Extract (optimal)
                standard1d = extract(
                    ccd=standard_background_subtracted, 
                    dispersion_axis=dispersion_axis, method='optimal', 
                    profile2d=profile2d_standard, 
                    background2d=background2d_standard.data, rdnoise=rdnoise.value, 
                    maxiters=5, sigma_lower=5, sigma_upper=5, grow=False, 
                    spectral_axis=lamp1d_standard_calibrated.spectral_axis, 
                    use_uncertainty=True, use_mask=True, title=key_standard, 
                    show=conf.show, save=conf.save, path='fig')

            # Plot standard spectrum
            plotSpectrum1D(
                standard1d, title=f'{key_standard} extracted', show=conf.show, 
                save=conf.save, path='fig')

            # Write standard spectrum to file (of type float64)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=AstropyUserWarning)
                standard1d.write(
                    f'cal/{key_standard}_extracted.fits', format='tabular-fits', 
                    overwrite=True)

            if standard is not None:

                if verbose:
                    print('\n[SENSITIVITY]')
                    print('  - Fitting sensitivity function...')

                # Fit sensitivity function
                sens1d, spl = sensfunc(
                    spectrum1d=standard1d, exptime=params['calibrate']['exposure'], 
                    airmass=params['calibrate']['airmass'], 
                    extinct=params['calibrate']['extinct'], 
                    standard=standard, bandwid=params['calibrate']['band_width'], 
                    bandsep=params['calibrate']['band_separation'], 
                    n_piece=params['calibrate']['n_piece'], 
                    maxiters=params['calibrate']['maxiters'], 
                    sigma_lower=params['calibrate']['sigma_lower'], 
                    sigma_upper=params['calibrate']['sigma_upper'], grow=False, 
                    show=conf.show, save=conf.save, path='fig')
        
        if verbose:
            print('\n[TARGET]')

        # Remove flux standard
        targ_list_flat_fielded = targ_list_flat_fielded[~isStandard]

        # Group
        ifc_targ = ifc_targ.filter(regex_match=True, obstype='SPECLTARGET')
        ifc_targ_summary = ifc_targ.summary
        ifc_targ_summary_grouped = ifc_targ_summary.group_by(keyword)
        keys = ifc_targ_summary_grouped.groups.keys[keyword].data
        if verbose:
            print('  - Grouping')
            print(f'    - {keys.shape[0]} groups: ' + ', '.join(keys))

        key_list = list()
        targ_combined_list = list()

        for i, key in enumerate(keys):

            if verbose:
                print(
                    f'  - Dealing with group {key} ({(i + 1)}/{keys.shape[0]})...')
            mask = ifc_targ_summary[keyword].data == key

            if shouldCombine:

                if mask.sum() >= 3:

                    # Skip cosmic ray removal
                    targ_list_cosmicray_corrected = targ_list_flat_fielded[mask]

                else:

                    # Remove cosmic ray
                    if verbose:
                        print('    - Removing cosmic ray...')
                    targ_list_cosmicray_corrected = (
                        targ_list_flat_fielded[mask].cosmicray_lacosmic(
                            use_mask=False, gain=(1 * u.dimensionless_unscaled), 
                            readnoise=rdnoise, sigclip=4.5, sigfrac=0.3, objlim=1, 
                            niter=5, verbose=True)
                    )

                # Rectify curvature
                if verbose:
                    print('    - Rectifying curvature...')
                if 'X' not in locals():
                    X = np.load('cal/X.npy')
                if 'Y' not in locals():
                    Y = np.load('cal/Y.npy')
                targ_list_transformed = (
                    targ_list_cosmicray_corrected.apply_over_ccd(transform, X=X, Y=Y)
                )

                if mask.sum() > 1:

                    # Align
                    if verbose:
                        print('    - Aligning...')
                    targ_list_aligned = align(
                        targ_list_transformed, params['slit_along'], index=0, 
                        interval=params['align_interval'])

                    # Combine
                    if verbose:
                        print(f'    - Combining ({mask.sum()})...')
                    exptime = ifc_targ_summary['exptime'].data[mask]
                    scale = exptime.max() / exptime
                    targ_combined = targ_list_aligned.combine(
                        method='median', scale=scale, mem_limit=conf.mem_limit, 
                        sigma_clip=True, sigma_clip_low_thresh=3, 
                        sigma_clip_high_thresh=3, sigma_clip_func=np.ma.median, 
                        sigma_clip_dev_func=mad_std, 
                        output_file=f'red/{key}_combined.fits', 
                        dtype=conf.dtype, overwrite_output=True)

                else:

                    targ_combined = targ_list_transformed[0]
                    targ_combined.write(f'red/{key}_combined.fits', overwrite=True)

                if verbose:
                    print(f'    - Saving combined {key} to red/...')

                # Plot
                plot2d(
                    targ_combined.data, title=f'{key} combined', show=conf.show, 
                    save=conf.save, path='fig')
                
                key_list.append(key)
                targ_combined_list.append(targ_combined)

            else:

                # Remove cosmic ray
                if verbose:
                    print('  - Removing cosmic ray...')
                targ_list_cosmicray_corrected = (
                    targ_list_flat_fielded[mask].cosmicray_lacosmic(
                        use_mask=False, gain=(1 * u.dimensionless_unscaled), 
                        readnoise=rdnoise, sigclip=4.5, sigfrac=0.3, objlim=1, 
                        niter=5, verbose=True)
                )

                # Rectify curvature
                if verbose:
                    print('  - Rectifying curvature...')
                if 'X' not in locals():
                    X = np.load('cal/X.npy')
                if 'Y' not in locals():
                    Y = np.load('cal/Y.npy')
                targ_list_transformed = targ_list_cosmicray_corrected.apply_over_ccd(
                        transform, X=X, Y=Y
                )

                n = int(np.log10(mask.sum())) + 1

                for j, targ_transformed in enumerate(targ_list_transformed):

                    if mask.sum() == 1:
                        new_name = f'{key}'
                    else:
                        new_name = f'{key}_{(j + 1):0{n}d}'

                    # Write transformed spectrum to file
                    if verbose:
                        print(f'  - Saving corrected {new_name} to red/...')
                    targ_transformed.write(f'red/{key}_corrected.fits', overwrite=True)

                    # Plot
                    plot2d(
                        targ_transformed.data, title=f'{new_name} corrected', 
                        show=conf.show, save=conf.save, path='fig')

                    key_list.append(f'{key}_{(j + 1):0{n}d}')
                    targ_combined_list.append(targ_transformed)

        targ_combined_list = CCDDataList(targ_combined_list)

        if verbose:
            print('  - Extracting 1-dimensional lamp spectra...')

        # Extract lamp spectrum for target (of type float64)
        if 'lamp_transformed' not in locals():
            lamp_transformed = CCDData.read('cal/lamp_transformed.fits')
        # Here may cause an exception when the dimension is less than 200.
        lamp1d_target = extract(
            ccd=lamp_transformed, dispersion_axis=dispersion_axis, method='sum', 
            trace1d=200, aper_width=10, n_aper=1, title='lamp1d target', 
            show=conf.show, save=conf.save, path='fig')

        if verbose:
            print('  - Correcting dispersion axis of lamp spectra...')

        # Correct dispersion of lamp spectrum for target (of type float64)
        lamp1d_target_calibrated = dispcor(
            spectrum1d=lamp1d_target, reverse=True, reference=reference, n_sub=20, 
            refit=True, degree=1, maxiters=5, sigma_lower=3, sigma_upper=3, grow=False, 
            use_mask=True, title='target', show=conf.show, save=conf.save, 
            path='fig')

        if verbose:
            print(f'  - Saving calibrated lamp spectra to cal/...')

        # Write calibrated lamp spectrum for target to file (of type float64)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=AstropyUserWarning)
            lamp1d_target_calibrated.write(
                'cal/lamp1d_target.fits', format='tabular-fits', 
                overwrite=True)

        if 'sens1d' in locals():

            sens1d = Spectrum1D(
                spectral_axis=lamp1d_target_calibrated.spectral_axis, 
                flux=(
                    spl(lamp1d_target_calibrated.spectral_axis.value) * sens1d.flux.unit
                ), 
                uncertainty=sens1d.uncertainty, 
                meta=sens1d.meta
            )

            if verbose:
                print(f'  - Saving sensitivity function to cal/...')

            # Write sensitivity function to file (of type float64)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=AstropyUserWarning)
                sens1d.write(
                    'cal/sens1d.fits', format='tabular-fits', 
                    overwrite=True)

        for key, targ_combined in zip(key_list, targ_combined_list):

            # Trace (trace the brightest spectrum)
            if verbose:
                print(f'  - Tracing {key}...')

            if (params['trace']['mode_target'] is 'center') & (isStandard.sum() > 0):

                trace1d_target = trace(
                    ccd=targ_combined, dispersion_axis=dispersion_axis, fwhm=10, 
                    mode='center', method='gaussian', interval='[:]', title=key, 
                    show=conf.show, save=conf.save, path='fig')
                shift = (
                    trace1d_standard.meta['header']['TRCENTER'] 
                    - trace1d_target.meta['header']['TRCENTER']) * u.pixel
                trace1d_target = Spectrum1D(
                    flux=(trace1d_standard.flux - shift), meta=trace1d_target.meta)

            else:

                trace1d_target = trace(
                    ccd=targ_combined, dispersion_axis=dispersion_axis, fwhm=10, 
                    mode=params['trace']['mode_target'], method='gaussian', 
                    n_med=params['trace']['n_med'], interval='[:]', 
                    n_piece=params['trace']['n_piece'], maxiters=5, sigma_lower=2, 
                    sigma_upper=2, grow=False, title=key, show=conf.show, 
                    save=conf.save, path='fig')

            # Write target trace to file (of type float64)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=AstropyUserWarning)
                trace1d_target.write(
                    f'cal/trace1d_{key}.fits', format='tabular-fits', 
                    overwrite=True)

            if verbose:
                print(f'  - Modeling sky background of {key}...')

            # Model sky background of target
            background2d_target = background(
                ccd=targ_combined, dispersion_axis=dispersion_axis, 
                trace1d=trace1d_target, 
                location=params['background']['location_target'], 
                aper_width=params['background']['width_target'], 
                degree=params['background']['order_target'], maxiters=3, sigma_lower=4, 
                sigma_upper=4, grow=False, use_uncertainty=False, use_mask=True, 
                title=key, show=conf.show, save=conf.save, path='fig')

            # Write sky background of standard to file
            background2d_target.write(f'red/background_{key}.fits', overwrite=True)

            if verbose:
                print(f'  - Subtracting sky background from {key} (target)...')

            # Subtract sky background from target
            target_background_subtracted = targ_combined.subtract(
                background2d_target, handle_meta='first_found')

            # Plot background subtracted target
            plot2d(
                target_background_subtracted.data, 
                title=f'{key} background subtracted', show=conf.show, save=conf.save, 
                path='fig')

            # Write background subtracted target to file
            target_background_subtracted.write(
                f'red/{key}_background_subtracted.fits', overwrite=True)

            if shouldExtract:

                # Extract target spectrum
                if verbose:
                    print(
                        f'  - Extracting spectrum of {key} '
                        f"({params['extract']['method_target']})..."
                    )

                if params['extract']['method_target'] == 'sum':

                    # Extract (sum)
                    target1d = extract(
                        ccd=target_background_subtracted, 
                        dispersion_axis=dispersion_axis, method='sum', 
                        trace1d=trace1d_target, 
                        aper_width=params['extract']['width_target'], n_aper=1, 
                        spectral_axis=lamp1d_target_calibrated.spectral_axis, 
                        use_uncertainty=True, use_mask=True, title=key, show=conf.show, 
                        save=conf.save, path='fig')

                else:

                    # Model spatial profile of target
                    profile2d_target, _ = profile(
                        ccd=target_background_subtracted, 
                        slit_along=params['slit_along'], trace1d=trace1d_target, 
                        profile_width=params['extract']['width_target'], 
                        window_length=params['extract']['pfl_window_target'], 
                        polyorder=params['extract']['pfl_order_target'], deriv=0, 
                        delta=1.0, title='profile', show=conf.show, save=conf.save, 
                        path='fig')

                    # Extract (optimal)
                    target1d = extract(
                        ccd=target_background_subtracted, 
                        dispersion_axis=dispersion_axis, method='optimal', 
                        profile2d=profile2d_target, 
                        background2d=background2d_target.data, rdnoise=rdnoise.value, 
                        maxiters=5, sigma_lower=5, sigma_upper=5, grow=False, 
                        spectral_axis=lamp1d_target_calibrated.spectral_axis, 
                        use_uncertainty=True, use_mask=True, title=key, show=conf.show, 
                        save=conf.save, path='fig')

                # Plot target spectrum
                plotSpectrum1D(
                    target1d, title=f'{key} extracted', show=conf.show, 
                    save=conf.save, path='fig')

                # Write calibrated spectrum to file
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', category=AstropyUserWarning)
                    target1d.write(
                        f'red/{key}_extracted.fits', format='tabular-fits', 
                        overwrite=True)

                # Calibrate target spectrum
                if 'sens1d' in locals():

                    if verbose:
                        print(f'    - Calibrating {key}...')
                    target1d_calibrated = calibrate1d(
                        spectrum1d=target1d, exptime=params['calibrate']['exposure'], 
                        airmass=params['calibrate']['airmass'], 
                        extinct=params['calibrate']['extinct'], sens1d=sens1d, 
                        use_uncertainty=False)

                    # Plot calibrated target spectrum
                    plotSpectrum1D(
                        target1d_calibrated, title=f'{key} calibrated 1d', show=conf.show, 
                        save=conf.save, path='fig')

                    # Write calibrated spectrum to file
                    if verbose:
                        print(f'    - Saving calibrated {key} to red/...')
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore', category=AstropyUserWarning)
                        target1d_calibrated.write(
                            f'red/{key}_calibrated_1d.fits', format='tabular-fits', 
                            overwrite=True)

            elif 'sens1d' in locals():

                # Calibrate                    
                if verbose:
                    print(f'    - Calibrating {key}...')
                targ_calibrated = calibrate2d(
                    ccd=target_background_subtracted, slit_along=params['slit_along'], 
                    exptime=params['calibrate']['exposure'], 
                    airmass=params['calibrate']['airmass'], 
                    extinct=params['calibrate']['extinct'], sens1d=sens1d, 
                    use_uncertainty=False)

                # Write calibrated spectrum to file
                if verbose:
                    print(f'    - Saving calibrated {key} to red/...')
                targ_calibrated.write(f'red/{key}_calibrated_2d.fits', overwrite=True)


def debug():
    """Command line tool."""
    
    # External parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input_dir', required=True, type=str, 
        help='Input (data) directory.'
    )
    parser.add_argument(
        '-m', '--semester', required=True, type=str, 
        help='Observation semester.'
    )
    parser.add_argument(
        '-w', '--slit_width', required=True, type=float, choices=[1.8, 2.3], 
        help='Slit width.'
    )
    parser.add_argument(
        '-o', '--output_dir', default='', type=str, 
        help='Output (saving) directory.'
    )
    parser.add_argument(
        '-r', '--reference', default=None, type=str, 
        help='Reference spectrum for wavelength calibration.'
    )
    parser.add_argument(
        '-s', '--standard', default=None, type=str, 
        help='Path to the standard spectrum in the library.'
    )
    parser.add_argument(
        '-c', '--combine', action='store_true', 
        help='Combine or not.'
    )
    parser.add_argument(
        '-k', '--keyword', default='object', type=str, 
        help='Keyword for grouping.'
    )
    parser.add_argument(
        '-x', '--extract', action='store_true', 
        help='Extract 1-dimensional spectra or not.'
    )
    parser.add_argument(
        '-p', '--point', action='store_true', 
        help='Point source or not.'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', 
        help='Verbose or not.'
    )
        
    # Parse
    args = parser.parse_args()
    data_dir = os.path.abspath(args.input_dir)
    semester = args.semester
    slit_width = str(args.slit_width).replace('.', '')
    save_dir = os.path.abspath(args.output_dir)
    reference = args.reference
    standard = args.standard
    combine = args.combine
    keyword = args.keyword
    extract = args.extract
    verbose = args.verbose

    # Run pipeline
    pipeline(
        save_dir=save_dir, data_dir=data_dir, semester=semester, grism=grism, 
        slit_width=slit_width, standard=standard, reference=reference, 
        shouldCombine=combine, keyword=keyword, shouldExtract=extract, 
        verbose=verbose)

    
if __name__ == '__main__':
    debug()