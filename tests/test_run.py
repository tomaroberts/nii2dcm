import pytest
import os, shutil
import pydicom as pyd

from nii2dcm.run import run_nii2dcm


NII_FILE_PATH = "tests/data/DicomMRISVR/t2-svr-atlas-35wk.nii.gz"
OUTPUT_DIR = "tests/data/tmp_dcm_dir"
OUTPUT_DCM_PATH = os.path.join(os.getcwd(), OUTPUT_DIR)
NUM_DICOM_FILES = 180
SINGLE_DICOM_FILENAME = "IM_0001.dcm"

class TestRun:
    def setup_method(self):
        os.makedirs(OUTPUT_DCM_PATH, exist_ok=True)

    @pytest.mark.parametrize(
        "TEST_DICOM_TYPE, TEST_DCM_MODALITY",
        [
            (None, ''),  # basic DICOM with undefined modality
            ("MR", "MR"),  # MRI DICOM
            ("SVR", "MR")  # SVR DICOM hence MR modality
        ]
    )
    def test_run_dicom_types(self, TEST_DICOM_TYPE, TEST_DCM_MODALITY):
        """
        Test run_nii2dcm with different dicom_types
        """
        run_nii2dcm(
            NII_FILE_PATH,
            OUTPUT_DCM_PATH,
            dicom_type=TEST_DICOM_TYPE
        )
        assert os.path.exists(os.path.join(OUTPUT_DCM_PATH, SINGLE_DICOM_FILENAME))
        assert len(os.listdir(OUTPUT_DCM_PATH)) == NUM_DICOM_FILES

        ds = pyd.dcmread(os.path.join(OUTPUT_DCM_PATH, SINGLE_DICOM_FILENAME))
        assert ds.Modality == TEST_DCM_MODALITY

        shutil.rmtree(OUTPUT_DCM_PATH)

    def test_run_reference_dicom(self):
        """
        Test run_nii2dcm with different ref_dicom option
        """
        # TODO: implement - will involve adding reference DICOM test dataset
        pass

    def teardown_method(self):
        """
        Remove output DICOM directory in event of test failure
        """
        if os.path.exists(OUTPUT_DCM_PATH):
            shutil.rmtree(OUTPUT_DCM_PATH)
