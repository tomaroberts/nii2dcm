"""
Create 3D, single-frame DICOM dataset from NIfTI file
"""
import nibabel as nib
import nii2dcm.nii, nii2dcm.svr, nii2dcm.dcm_writer


# Load Nifti file
niiPath = r'/Users/tr17/data/DicomRecon/previous-recon/SVR-output.nii.gz'
nii = nib.load(niiPath)

# Get Nifti parameters for transferal to DICOM
nii2dcm_parameters = nii2dcm.nii.Nifti.get_nii2dcm_parameters(nii)
# print(f'nii_parameters:\n {nii2dcm_parameters}')


# Write single DICOM

# Initialise
TestDicomMRISVR = nii2dcm.svr.DicomMRISVR('testDicomMriSVR.dcm')
# print(TestDicomMRISVR.ds)

# Transfer Series tags
nii2dcm.dcm_writer.transfer_nii_hdr_series_tags(TestDicomMRISVR, nii2dcm_parameters)

# Get Nifti pixel data
# TODO: create method in Nifti class – need to think about -1 value treatment
nii_img = nii.get_fdata()
iBkrd = nii_img == -1  # set background pixels = 0 (-1 in SVRTK)
nii_img[iBkrd] = 0
nii_img = nii_img.astype("uint16")  # match DICOM datatype

# Set custom tags
# TODO: lines below for overriding and testing DICOM creation.
#  Need to decide how best to implement properly, e.g.: force TransferSyntaxUID depending on Dicom subclass,
#  or give user option to edit. Think former, with possibility of latter.
TestDicomMRISVR.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'
TestDicomMRISVR.ds.BitsAllocated = 16

# Write DICOM Series, instance-by-instance
num_slices = nii.shape[2]
for slice_number in range(1, num_slices):

    # Transfer Instance tags
    nii2dcm.dcm_writer.transfer_nii_hdr_instance_tags(TestDicomMRISVR, nii2dcm_parameters, slice_number)

    # Write slice
    nii2dcm.dcm_writer.write_slice(TestDicomMRISVR, nii_img, slice_number, '')
    # print(TestDicomMRISVR.ds)
