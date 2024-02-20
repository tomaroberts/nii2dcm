import pytest

from nii2dcm.nii import Nifti
import nibabel as nib


NII_FILE_PATH = "tests/data/DicomMRISVR/t2-svr-atlas-35wk.nii.gz"
NII_VOXEL_DIMS = (180, 221, 180)
NII_VOXEL_SPACING = (0.5, 0.5, 0.5)

class TestNifti:
    def setup_method(self):
        self.nii = nib.load(NII_FILE_PATH)

    def test_get_nii2dcm_parameters(self):
        nii_parameters = Nifti.get_nii2dcm_parameters(self.nii)
        assert nii_parameters["Rows"] == NII_VOXEL_DIMS[0]
        assert nii_parameters["Columns"] == NII_VOXEL_DIMS[1]
        assert nii_parameters["NumberOfSlices"] == NII_VOXEL_DIMS[2]
        assert nii_parameters["AcquisitionMatrix"] == [0, NII_VOXEL_DIMS[0], NII_VOXEL_DIMS[1], 0]
        assert nii_parameters["dimX"] == NII_VOXEL_SPACING[0]
        assert nii_parameters["dimY"] == NII_VOXEL_SPACING[1]
        assert nii_parameters["SliceThickness"] == str(NII_VOXEL_SPACING[2])
