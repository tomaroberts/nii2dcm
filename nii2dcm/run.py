"""
nii2dcm runner
"""
from os.path import abspath

import nibabel as nib
import pydicom as pyd

import nii2dcm.nii
import nii2dcm.svr
from nii2dcm.dcm_writer import (
    transfer_nii_hdr_series_tags,
    transfer_nii_hdr_instance_tags,
    transfer_ref_dicom_series_tags,
    write_slice
)


def run_nii2dcm(input_nii_path, output_dcm_path, dicom_type=None, ref_dicom_file=None):
    """
    Execute NIfTI to DICOM conversion

    :param input_nii_path: input .nii/.nii.gz file
    :param output_dcm_path: output DICOM directory
    :param dicom_type: specified by user on command-line
    :param ref_dicom: reference DICOM file for transferring Attributes
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
