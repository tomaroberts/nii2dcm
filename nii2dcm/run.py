"""
nii2dcm runner
"""
from os.path import abspath

import nibabel as nib
import pydicom as pyd
import numpy as np
import nii2dcm.nii
import nii2dcm.svr
from nii2dcm.dcm_writer import (
    transfer_nii_hdr_series_tags,
    transfer_nii_hdr_instance_tags,
    transfer_ref_dicom_series_tags,
    write_slice
)


def run_nii2dcm(input_nii_path, output_dcm_path, dicom_type=None, ref_dicom_file=None, centered=False, use_float=False):
    """
    Execute NIfTI to DICOM conversion

    :param input_nii_path: input .nii/.nii.gz file
    :param output_dcm_path: output DICOM directory
    :param dicom_type: specified by user on command-line
    :param ref_dicom_file: reference DICOM file for transferring Attributes
    :param centered: whether to apply centered scaling
    :param use_float: whether to preserve float values (32-bit) instead of converting to uint16. 
                     Can be True (automatic scale) or float (user-specified scale factor)
    """

    # load NIfTI
    nii = nib.load(input_nii_path)

    # get pixel data from NIfTI
    # TODO: create method in nii class
    nii_img = nii.get_fdata()

    if centered:
        # Normalize the data
        mean_val = nii_img.mean()
        std_val = nii_img.std()
        normalized_img = (nii_img - mean_val) / std_val

        # Rescale the normalized data to fit within the desired range
        # Adjust the factor to fit your specific data
        rescaled_img = normalized_img * 50 + 2048

        # Clip values to prevent overflow
        rescaled_img = np.clip(rescaled_img, 0, 65535)

        # Assign the rescaled image to nii_img
        nii_img = rescaled_img

    if use_float:
        # Use integer scaling for floating-point representation
        # Use 32-bit signed integers with a rescale parameter
        data_min = nii_img.min()
        data_max = nii_img.max()
        
        if data_min < data_max:
            if isinstance(use_float, bool):
                # Automatic mode: optimize scale factor for this dataset
                int32_min = -2**30
                int32_max = 2**30 - 1
                scale_factor = (data_max - data_min) / (int32_max - int32_min)
                print(f"nii2dcm: Auto-selected scale factor {scale_factor:.2e} for data range [{data_min:.6f}, {data_max:.6f}]")
            else:
                # User-specified scale factor
                scale_factor = float(use_float)
                print(f"nii2dcm: Using user-specified scale factor {scale_factor:.2e}")
                # Calculate integer range based on user's scale factor
                max_abs_value = max(abs(data_min), abs(data_max))
                int_range_needed = max_abs_value / scale_factor
                if int_range_needed > 2**30:
                    print(f"nii2dcm: Warning - scale factor may be too small for data range. Some clipping may occur.")
                
                int32_min = -2**30
                int32_max = 2**30 - 1
            
            # Scale data to integer range
            nii_img_scaled = ((nii_img - data_min) / scale_factor + int32_min).astype(np.int32)
            
            # DICOM rescale parameters to map back to original float values
            rescale_slope = scale_factor
            rescale_intercept = data_min - int32_min * scale_factor
            
            nii_img = nii_img_scaled
        else:
            # Handle constant data
            nii_img = np.full_like(nii_img, 0, dtype=np.int32)
            rescale_intercept = data_min
            rescale_slope = 1.0
    elif centered:
        # Centered data is already prepared for DICOM - no additional scaling needed
        nii_img = np.clip(nii_img, 0, 65535).astype(np.uint16)
        rescale_intercept = 0
        rescale_slope = 1
    else:
        # Scale float data to appropriate uint16 range
        # Find min/max values in the data
        data_min = nii_img.min()
        data_max = nii_img.max()
        
        if data_min < data_max:  # Avoid division by zero
            # Scale to 16-bit unsigned integer range (0-65535)
            # Use a reasonable range that avoids the extremes
            scaled_img = ((nii_img - data_min) / (data_max - data_min)) * 4000 + 1000
            nii_img = scaled_img.astype(np.uint16)
        else:
            # Handle case where all values are the same
            nii_img = np.full_like(nii_img, 1000, dtype=np.uint16)
        
        # Standard scaling parameters
        rescale_intercept = 0
        rescale_slope = 1

    # get NIfTI parameters
    nii2dcm_parameters = nii2dcm.nii.Nifti.get_nii2dcm_parameters(nii)
    
    # Override rescale parameters for float mode
    if use_float:
        nii2dcm_parameters['RescaleIntercept'] = str(rescale_intercept)
        nii2dcm_parameters['RescaleSlope'] = str(rescale_slope)

    # initialise nii2dcm.dcm object
    # --dicom_type specified on command line
    if dicom_type is None:
        if use_float:
            dicom = nii2dcm.dcm.DicomMRIFloat('nii2dcm_dicom_float.dcm')  # Default to MRI Float when using float
        else:
            dicom = nii2dcm.dcm.Dicom('nii2dcm_dicom.dcm')

    if dicom_type is not None and dicom_type.upper() in ['MR', 'MRI']:
        if use_float:
            dicom = nii2dcm.dcm.DicomMRIFloat('nii2dcm_dicom_mri_float.dcm')
        else:
            dicom = nii2dcm.dcm.DicomMRI('nii2dcm_dicom_mri.dcm')

    if dicom_type is not None and dicom_type.upper() in ['SVR']:
        dicom = nii2dcm.svr.DicomMRISVR('nii2dcm_dicom_mri_svr.dcm')
        nii_img = nii.get_fdata()
        nii_img[nii_img < 0] = 0  # set background pixels = 0 (negative in SVRTK)
        
        if use_float:
            # Preserve floating-point values as float32 for SVR
            nii_img = nii_img.astype(np.float32)
        else:
            # Scale float data to appropriate uint16 range for SVR
            data_min = nii_img.min()
            data_max = nii_img.max()
            
            if data_min < data_max:
                scaled_img = ((nii_img - data_min) / (data_max - data_min)) * 4000 + 1000
                nii_img = scaled_img.astype("uint16")
            else:
                nii_img = np.full_like(nii_img, 1000, dtype=np.uint16)

    # load reference DICOM object
    # --ref_dicom_file specified on command line
    if ref_dicom_file is not None:
        ref_dicom = pyd.dcmread(ref_dicom_file)

    # transfer Series tags from NIfTI
    transfer_nii_hdr_series_tags(dicom, nii2dcm_parameters)

    # transfer tags from reference DICOM
    # IMPORTANT: this deliberately happens last in the DICOM tag manipulation process so that any tag values transferred
    # from the reference DICOM override any values initialised by nii2dcm
    if ref_dicom_file is not None:
        transfer_ref_dicom_series_tags(dicom, ref_dicom)

    """
    Write DICOM files
    - Transfer NIfTI parameters and write slices, instance-by-instance
    """
    print('nii2dcm: writing DICOM files ...')  # TODO use logger

    for instance_index in range(0, nii2dcm_parameters['NumberOfInstances']):

        # Transfer Instance tags
        transfer_nii_hdr_instance_tags(dicom, nii2dcm_parameters, instance_index)

        # Write slice
        write_slice(dicom, nii_img, instance_index, output_dcm_path)

    print(f'nii2dcm: DICOM files written to: {abspath(output_dcm_path)}')  # TODO use logger
