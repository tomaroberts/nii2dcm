import os

import pytest
import nibabel as nib

from nii2dcm import dcm_writer
from nii2dcm.dcm import Dicom
from nii2dcm.nii import Nifti


NII_FILE_PATH = "tests/data/DicomMRISVR/t2-svr-atlas-35wk.nii.gz"
INSTANCE_INDEX = 10  # dcm instances count from 1
SLICE_NUMBER = INSTANCE_INDEX - 1  # nibabel slice array counts from 0
OUTPUT_DIR = "tests/data"
OUTPUT_DCM_FILENAME = r"IM_%04d.dcm" % (INSTANCE_INDEX)
OUTPUT_DCM_PATH = os.path.join(os.getcwd(), OUTPUT_DIR, OUTPUT_DCM_FILENAME)


class TestDicomWriter:
    def setup_method(self):
        self.dicom = Dicom()
        self.nii = nib.load(NII_FILE_PATH)
        self.img_data = self.nii.get_fdata().astype("uint16")
        self.nii2dcm_parameters = Nifti.get_nii2dcm_parameters(self.nii)

    def test_write_slice(self):
        dcm_writer.write_slice(self.dicom, self.img_data, SLICE_NUMBER, OUTPUT_DIR)

        assert os.path.exists(OUTPUT_DCM_PATH)
        os.remove(OUTPUT_DCM_PATH)
        if os.path.exists(OUTPUT_DCM_PATH):
            raise Exception(
                "Failed to delete temporary DICOM created during pytest process."
            )

    def test_transfer_nii_hdr_series_tags(self):
        dcm_writer.transfer_nii_hdr_series_tags(self.dicom, self.nii2dcm_parameters)
        assert self.dicom.ds.Rows == self.nii.shape[0]
        assert self.dicom.ds.Columns == self.nii.shape[1]

    def test_transfer_nii_hdr_instance_tags(self):
        dcm_writer.transfer_nii_hdr_instance_tags(
            self.dicom, self.nii2dcm_parameters, SLICE_NUMBER
        )
        assert self.dicom.ds.InstanceNumber == INSTANCE_INDEX

    def test_transfer_ref_dicom_series_tags(self):
        """
        TODO: implement test
        """
        pass
