# Example:
# Convert 3D nifti to dicom

import os, pprint
import nibabel as nib
import pydicom
from pydicom.dataset  import Dataset, FileDataset, FileMetaDataset
from pydicom.datadict import DicomDictionary, keyword_dict
from pydicom.sequence import Sequence

# reference nifti
niiPath = r'example/nii_3d/brain.nii.gz'
nii     = nib.load(niiPath)
nii_hdr = nii.header
nii_img = nii.get_fdata()

# get nifti image data properties
import src.nii as NII
nii_params = NII.NII.getNiiParameters(nii)
pprint.pprint(nii_params[0])
print(len(nii_params))

# dicom shell
import src.dcm as DCM
dcm3d = DCM.DCM(Dataset(),Dataset())
dcm3d.initDcmHdr()



# dcm3d.niiHdr2Dcm(nii_hdr)

# print(dcm3d.ds.InstanceNumber is None)







### PIPELINE:

# Create DICOM Shell
# - Define ALL elements ?
# – Set to be defined important dicom elements = 'REQUIRED' upon initialisation ?
# - Could define these based on Classes?
# --- ie: 3D class
# ---     4D class
# ---     -- Mag
# ---     -- V0
# ---     -- V1
# ---     -- V2

# Set Tags Fixed across all Instances
# - extract from nii metadata 

# Determine Number of DICOMs to Create
# - nSlices
# - nFrames
# - nInstances = nSlices * nFrames

# Create huge array of Datasets and update individual parameters?
# OR:
# Work out looping structure, create Datasets one-by-one?




