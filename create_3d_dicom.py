"""
Create 3D, single-frame DICOM dataset from NIfTI file
"""
import numpy as np
import nibabel as nib
import nii2dcm.nii

# Load Nifti file
niiPath = r'/Users/tr17/data/DicomRecon/previous-recon/SVR-output.nii.gz'
nii = nib.load(niiPath)
nii_parameters = nii2dcm.nii.Nifti.get_nii2dcm_general_parameters(nii)
print(nii_parameters)

geo_parameters = nii2dcm.nii.Nifti.get_nii2dcm_geometry_parameters(nii)
print(geo_parameters)

# Initialise DICOM

# DICOM tags
# - transfer
# - create
