"""
Create 3D, single-frame DICOM dataset from NIfTI file
"""
import nibabel as nib
import nii2dcm.nii, nii2dcm.svr, nii2dcm.dcm_writer


# Load Nifti file
niiPath = r'/Users/tr17/data/DicomRecon/previous-recon/SVR-output.nii.gz'
nii = nib.load(niiPath)

# Get Nifti parameters for transferal to DICOM
nii_parameters = nii2dcm.nii.Nifti.get_nii2dcm_general_parameters(nii)
print(nii_parameters)

geo_parameters = nii2dcm.nii.Nifti.get_nii2dcm_geometry_parameters(nii)
print(geo_parameters)


# Write single DICOM

# Initialise
TestDicomMRISVR = nii2dcm.svr.DicomMRISVR('testDicomMriSVR.dcm')
print(TestDicomMRISVR.ds)

# Get Nifti pixel data
# TODO: create method in Nifti class – need to think about -1 value treatment
nii_img = nii.get_fdata()
iBkrd = nii_img == -1  # set background pixels = 0 (-1 in SVRTK)
nii_img[iBkrd] = 0
nii_img = nii_img.astype("uint16")  # match DICOM datatype

# Write slice
# TODO: lines below for overriding and testing DICOM creation.
#  Need to decide how best to implement properly, e.g.: force TransferSyntaxUID depending on Dicom subclass,
#  or give user option to edit. Think former, with possibility of latter.
TestDicomMRISVR.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'
TestDicomMRISVR.ds.BitsAllocated = 16

nii2dcm.dcm_writer.write_slice(TestDicomMRISVR, nii_img, 70, '')
print(TestDicomMRISVR.ds)

# - transfer
# - create

# Save DICOM
# TestDicomMRISVR.save_as()
