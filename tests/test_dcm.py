import pytest
import os
import datetime

from pydicom.dataset import FileMetaDataset, FileDataset

from nii2dcm.dcm import Dicom
from nii2dcm.modules.patient import Patient


TRANSFER_SYNTAX_UID = '1.2.840.10008.1.2.1'
DATE = datetime.datetime.now().strftime('%Y%m%d')
PATIENT_ID = '12345678'
PATIENT_SEX = ''
IMAGE_TYPE = ['SECONDARY', 'DERIVED']
CHARACTER_SET = 'ISO_IR 100'

MIN_UID_LENGTH = 10  # arbitrary just to check UID has some characters
MAX_UID_LENGTH = 64  # DICOM standard max length

class TestDicom:
    def setup_method(self):
        self.dicom = Dicom()

    def test_dicom(self):
        """
        Tests some metadata in basic Dicom object
        """
        assert self.dicom.file_meta.TransferSyntaxUID == TRANSFER_SYNTAX_UID
        assert self.dicom.ds.ContentDate == DATE
        assert self.dicom.ds.AcquisitionDate == DATE
        assert self.dicom.ds.SeriesDate == DATE
        assert self.dicom.ds.StudyDate == DATE

    def test_add_module(self):
        """
        Tests add_module() method
        """
        self.dicom.add_module(Patient())
        assert self.dicom.ds.PatientID == PATIENT_ID
        assert self.dicom.ds.PatientSex == PATIENT_SEX

    def test_add_base_modules(self):
        """
        Test metadata present following bulk method invocation via add_base_modules()
        """
        self.dicom.add_base_modules()
        assert self.dicom.ds.SpecificCharacterSet == CHARACTER_SET
        assert self.dicom.ds.ImageType[0] == 'SECONDARY'
        assert self.dicom.ds.ImageType[1] == 'DERIVED'

    def test_get_file_meta(self):
        fm = self.dicom.get_file_meta()
        assert isinstance(fm, FileMetaDataset)

    def test_get_dataset(self):
        ds = self.dicom.get_dataset()
        assert isinstance(ds, FileDataset)

    def test_save_as(self):
        """
        Test DICOM save (default save location: cwd)
        """
        self.dicom.ds.save_as(self.dicom.filename)
        assert os.path.exists(self.dicom.filename)
        os.remove(self.dicom.filename)
        if os.path.exists(self.dicom.filename):
            raise Exception("Failed to delete temporary DICOM created during pytest process.")

    def test_init_study_tags(self):
        self.dicom.init_study_tags()
        assert isinstance(self.dicom.ds.StudyInstanceUID, str)
        assert self.dicom.ds.StudyInstanceUID.find(".")
        assert MIN_UID_LENGTH < len(self.dicom.ds.StudyInstanceUID) <= MAX_UID_LENGTH

    def test_init_series_tags(self):
        self.dicom.init_study_tags()
        assert isinstance(self.dicom.ds.SeriesInstanceUID, str)
        assert self.dicom.ds.SeriesInstanceUID.find(".")
        assert MIN_UID_LENGTH < len(self.dicom.ds.SeriesInstanceUID) <= MAX_UID_LENGTH

        assert len(str(self.dicom.ds.SeriesNumber)) == 4
