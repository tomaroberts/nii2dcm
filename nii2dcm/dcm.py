"""
Classes for creating a DICOM from scratch

Tom Roberts
"""

import datetime
import os
from random import randint

import pydicom as pyd
from pydicom.dataset import FileDataset, FileMetaDataset

from nii2dcm.utils import dcm_dictionary_update
from nii2dcm.modules import (
    patient,
    general_study,
    patient_study,
    general_series,
    frame_of_reference,
    general_equipment,
    general_acquisition,
    general_image,
    general_reference,
    image_plane,
    image_pixel,
    mr_image,
    voi_lut,
    sop_common,
    common_instance_reference,
)

nii2dcm_temp_filename = 'nii2dcm_tempfile.dcm'


class Dicom:
    """
    Creates basic DICOM structure

    Assumptions:
    - is_implicit_VR = False
    - is_little_endian = True
    - ImageOrientationPatient hard-coded

    """

    def __init__(self, filename=nii2dcm_temp_filename):

        self.filename = filename

        # TODO implement dcm_dictionary_update() function, most likely at this location in code
        # dcm_dictionary_update()

        # Instantiates minimal Pydicom FileMetaDataset object
        self.file_meta = FileMetaDataset()
        self.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'  # Explicit VR Little Endian
        self.file_meta.ImplementationVersionName = 'nii2dcm_DICOM'

        # Instantiates minimal DataSet object
        self.ds = FileDataset(filename, {}, file_meta=self.file_meta, preamble=b"\0" * 128)
        self.ds.is_implicit_VR = False
        self.ds.is_little_endian = True
        self.ds.ImageType = ['DERIVED', 'SECONDARY']

        """
        Initialise Composite IOD by adding Modules to Dicom object
        
        Common Modules below taken by comparing A.3.3 (CT) and A.4.3 (MRI) CIODs to determine shared Modules. Other 
        modalities assumed to have similar composition. Modules unique to a specific imaging modality are added within 
        the respective subclass. e.g. MR Image Module is added within the nii2dcm DicomMRI class
        """
        patient.add_module(self)
        general_study.add_module(self)
        patient_study.add_module(self)
        general_series.add_module(self)
        frame_of_reference.add_module(self)
        general_equipment.add_module(self)
        general_acquisition.add_module(self)

        general_image.add_module(self)
        general_reference.add_module(self)
        image_plane.add_module(self)
        image_pixel.add_module(self)
        voi_lut.add_module(self)
        sop_common.add_module(self)
        common_instance_reference.add_module(self)

        """
        Set Dicom Date/Time
        Important: doing this once sets all Instances/Series/Study creation dates and times to the same values. Whereas, 
        doing this within the Modules would every so slightly offset the times
        """
        # TODO shift to utils.py and propagate to Modules, or, create method within this Dicom class
        dt = datetime.datetime.now()
        dateStr = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds

        self.ds.ContentDate = dateStr
        self.ds.ContentTime = timeStr
        self.ds.StudyDate = dateStr
        self.ds.StudyTime = timeStr
        self.ds.SeriesDate = dateStr
        self.ds.SeriesTime = timeStr
        self.ds.AcquisitionDate = dateStr
        self.ds.AcquisitionTime = timeStr
        self.ds.InstanceCreationDate = dateStr
        self.ds.InstanceCreationTime = timeStr

        """
        Set some default Attribute values for _all_ DICOM CIODs
        """
        # TODO
        #  - decide if this is the best way to implement setting default values of important Attributes
        #  - probably makes more sense to hard-code these in subclasses, e.g. DicomMRI, DicomCT, etc, so that they are
        #  not hard-coded across different imaging modalities, where some might be irrelevant

        # ImageOrientationPatient
        # hard-coded, probably better way to define based on NIfTI values
        self.ds.ImageOrientationPatient = ['1', '0', '0', '0', '1', '0']

        # Display Attributes
        # NB: RescaleIntercept and RescaleSlope do NOT appear to be in MR Image Module, but are in CT Image, Secondary
        # Capture and Enhanced MR Modules, hence for MRI must define in this class or within DicomMRI class
        self.ds.RescaleIntercept = ''
        self.ds.RescaleSlope = ''
        self.ds.WindowCenter = ''
        self.ds.WindowWidth = ''

        # per Instance Attributes
        # initialised with hard-coded value below, but overwritten with transfer_nii_hdr_instance_tags()
        self.ds.ImagePositionPatient = ['0', '0', '0']

        self.init_study_tags()
        self.init_series_tags()

    def get_file_meta(self):
        return self.file_meta

    def get_dataset(self):
        return self.ds

    def save_as(self):
        print("Writing DICOM to", os.path.join(os.getcwd(), self.filename))
        self.ds.save_as(self.filename)

    def init_study_tags(self):
        """
        Create Study Tags
        - these tags are fixed across Instances and Series
        """

        # Possible per Study Tags
        # StudyInstanceUID

        self.ds.StudyInstanceUID = pyd.uid.generate_uid(None)

    def init_series_tags(self):
        """
        Create Series Tags
        - these tags are fixed across Instances
        """

        # Possible per Series Tags
        # SeriesInstanceUID
        # FrameOfReferenceUID
        # SeriesDate
        # SeriesTime
        # AcquisitionDate
        # AcquisitionTime
        # SeriesNumber

        self.ds.SeriesInstanceUID = pyd.uid.generate_uid(None)
        self.ds.FrameOfReferenceUID = pyd.uid.generate_uid(None)
        self.ds.SeriesNumber = str(randint(1000, 9999))  # 4 digit number to avoid conflict
        self.ds.AcquisitionNumber = ''  # Innolitics says this is in General Image Module, but NEMA says it is not...


class DicomMRI(Dicom):
    """
    DicomMRI subclass
    - Sets appropriate SOPClass UIDs for MR
    - Adds MR Image Module to Dicom object
    """

    def __init__(self, filename=nii2dcm_temp_filename):
        super().__init__(filename)

        """
        Set DICOM attributes which are located outside of the MR Image Module to MR-specific values 
        """
        self.ds.Modality = 'MR'

        # MR Image Storage SOP Class
        # UID = 1.2.840.10008.5.1.4.1.1.4
        # https://dicom.nema.org/dicom/2013/output/chtml/part04/sect_I.4.html
        self.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        self.ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.4'

        """
        Initialise subclass CIOD Modules
        """
        mr_image.add_module(self)

        """
        DICOM Attributes to transfer from DICOM supplied using --ref_dicom CLI option
        """
        # TODO(tomaroberts) figure out whether transfer SQ Sequence blocks, e.g.:
        #  ProcedureCodeSequence,
        #  ReferencedStudySequence,
        #  ConversionSourceAttributesSequence
        #  - conflicts if _included_?

        self.attributes_to_transfer = [
            'StudyDate',
            'SeriesDate',
            'AcquisitionDate',
            'AccessionNumber',
            'InstitutionName',
            'InstitutionAddress',
            'ReferringPhysicianName',
            'StationName',
            'StudyDescription',
            'ProcedureCodeSequence',  # SQ Sequence
            'InstitutionalDepartmentName',
            'PerformingPhysicianName',
            'OperatorsName',
            'ManufacturerModelName',
            'ReferencedStudySequence',  # SQ Sequence
            'RelatedSeriesSequence',  # SQ Sequence

            'PatientName',
            'PatientID',
            'PatientBirthDate',
            'PatientSex',
            'PatientAge',
            'PatientSize',
            'PatientWeight',
            'BodyPartExamined',

            # MR Image Module Attributes
            'ScanningSequence',
            'SequenceVariant',
            'ScanOptions',
            'MRAcquisitionType',
            'SequenceName',
            'AngioFlag',
            'RepetitionTime',
            'EchoTime',
            'InversionTime',
            'NumberOfAverages',
            'ImagingFrequency',
            'ImagedNucleus',
            'MagneticFieldStrength',
            'NumberOfPhaseEncodingSteps',
            'EchoTrainLength',
            'PercentSampling',
            'PercentPhaseFieldOfView',
            'PixelBandwidth',
            'DeviceSerialNumber',
            'SoftwareVersions',
            'BeatRejectionFlag',
            'CardiacNumberOfImages',
            'ReceiveCoilName',
            'TransmitCoilName',
            'InPlanePhaseEncodingDirection',
            'FlipAngle',
            'SAR',
            'PatientPosition',

            # General Study Module Attributes
            'StudyInstanceUID',  # Important: enables new DICOM to be filed in original Study
            'StudyID',
            'AcquisitionNumber',  # include or set in Dicom subclass?
            'FrameOfReferenceUID',  # include?
            'NumberOfTemporalPositions',
            'ConversionSourceAttributesSequence',  # SQ Sequence
            'RequestAttributesSequence',  # SQ Sequence
            'RequestingPhysician',
            'RequestingService',
        ]


