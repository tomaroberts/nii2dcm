"""
Create 3D Fetal Brain MRI SVRTK single-frame DICOM dataset NIfTI file

Tested with data from the following scanners:
- 1.5T Philips Ingenia
- 1.5T Siemens Sola
"""
import os
import nibabel as nib

import nii2dcm.dcm_writer
import nii2dcm.nii
import nii2dcm.svr


NII2DCM_DIR = r'/Users/tr17/code/nii2dcm'
INPUT_DIR   = r'/Users/tr17/code/nii2dcm/input/'
OUTPUT_DIR  = r'/Users/tr17/code/nii2dcm/output'

if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Load Nifti file
niiInPath = os.path.join(INPUT_DIR, 'SVR-output.nii.gz')
nii = nib.load(niiInPath)

# Set output directory
dcmOutPath = OUTPUT_DIR
if os.path.exists(dcmOutPath):
    if not os.path.isdir(dcmOutPath):
        raise ValueError('The DICOM output path must be a directory.')
else:
    os.makedirs(dcmOutPath)

# Get NIfTI parameters to transfer to DICOM
nii2dcm_parameters = nii2dcm.nii.Nifti.get_nii2dcm_parameters(nii)


# Write single DICOM

# Initialise
TestDicomMRISVR = nii2dcm.svr.DicomMRISVR('testDicomMriSVR.dcm')

# Transfer Series tags
nii2dcm.dcm_writer.transfer_nii_hdr_series_tags(TestDicomMRISVR, nii2dcm_parameters)

# Get NIfTI pixel data
# TODO: create method in Nifti class – need to think about -1 value treatment
nii_img = nii.get_fdata()
nii_img[nii_img < 0] = 0  # set background pixels = 0 (negative in SVRTK)
nii_img = nii_img.astype("uint16")  # match DICOM datatype

# Set custom tags
# - currently none

# Write DICOM Series, instance-by-instance
for instance_index in range(0, nii2dcm_parameters['NumberOfInstances']):

    # Transfer Instance tags
    nii2dcm.dcm_writer.transfer_nii_hdr_instance_tags(TestDicomMRISVR, nii2dcm_parameters, instance_index)

    # Write slice
    nii2dcm.dcm_writer.write_slice(TestDicomMRISVR, nii_img, instance_index, dcmOutPath)

print(TestDicomMRISVR.ds)
