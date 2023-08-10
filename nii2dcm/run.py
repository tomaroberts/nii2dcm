"""
nii2dcm runner
"""
import nibabel as nib

import nii2dcm.nii
import nii2dcm.svr
from nii2dcm.dcm_writer import (
    transfer_nii_hdr_series_tags,
    transfer_nii_hdr_instance_tags,
    write_slice
)


def run_nii2dcm(input_nii_path, output_dcm_path, dicom_type=None):
    """
    Execute NIfTI to DICOM conversion

    :param input_nii_path: input .nii/.nii.gz file
    :param output_dcm_path: output DICOM directory
    :param dicom_type: specified by user on command-line
    """

    # load NIfTI
    nii = nib.load(input_nii_path)

    # get pixel data from NIfTI
    # TODO: create method in nii class
    nii_img = nii.get_fdata()
    nii_img = nii_img.astype("uint16")  # match DICOM datatype

    # get NIfTI parameters
    nii2dcm_parameters = nii2dcm.nii.Nifti.get_nii2dcm_parameters(nii)

    # initialise nii2dcm.dcm object
    # --dicom_type specified on command line
    if dicom_type is None:
        dicom = nii2dcm.dcm.Dicom('nii2dcm_dicom.dcm')

    if dicom_type is not None and dicom_type.upper() in ['MR', 'MRI']:
        dicom = nii2dcm.dcm.DicomMRI('nii2dcm_dicom_mri.dcm')

    if dicom_type is not None and dicom_type.upper() in ['SVR']:
        dicom = nii2dcm.svr.DicomMRISVR('nii2dcm_dicom_mri_svr.dcm')
        nii_img = nii.get_fdata()
        nii_img[nii_img < 0] = 0  # set background pixels = 0 (negative in SVRTK)
        nii_img = nii_img.astype("uint16")

    # transfer Series tags from NIfTI
    transfer_nii_hdr_series_tags(dicom, nii2dcm_parameters)

    # write DICOM files, instance-by-instance

    print('nii2dcm: writing DICOM files ...')  # TODO use logger

    for instance_index in range(0, nii2dcm_parameters['NumberOfInstances']):

        # Transfer Instance tags
        transfer_nii_hdr_instance_tags(dicom, nii2dcm_parameters, instance_index)

        # Write slice
        write_slice(dicom, nii_img, instance_index, output_dcm_path)