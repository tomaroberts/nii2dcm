"""
classes for creating a dicom from scratch

Tom Roberts
"""

import tempfile
import pydicom
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from pydicom.uid import UID
from pydicom.datadict import DicomDictionary, keyword_dict
from pydicom.sequence import Sequence
import nibabel as nib


class Dicom:
    """
    Creates basic DICOM structure
    """

    def __init__(self, filename=tempfile.NamedTemporaryFile(suffix='.dcm').name):

        self.filename = filename

        # Creates minimal FileMeta
        self.file_meta = FileMetaDataset()
        self.file_meta.MediaStorageSOPClassUID = ''
        self.file_meta.MediaStorageSOPInstanceUID = ''
        self.file_meta.ImplementationClassUID = ''

        # Creates minimal DataSet
        self.ds = FileDataset(filename, {}, file_meta=self.file_meta, preamble=b"\0" * 128)
        self.ds.PatientName = "Test^Firstname"
        self.ds.PatientID = "12345678"

    def get_file_meta(self):
        return self.file_meta

    def get_dataset(self):
        return self.ds

    # def initDcmHdr(self):
    #     """ create minimal dicom header
    #     - essential fields found in all MRI dicoms
    #     - many fields can be left blank
    #     - some initialised with MRI-related tags
    #     """
    #
    #     # fm - file_meta
    #     self.file_meta.FileMetaInformationVersion = b'\x00\x01'
    #     self.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
    #     self.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
    #     self.file_meta.ImplementationClassUID = '1.2.276.0.7230010.3.0.3.6.1'
    #     self.file_meta.ImplementationVersionName = 'dicom_created_with_nii2dcm'
    #
    #     # ds - main data elements
    #     self.ds.SpecificCharacterSet = 'ISO_IR 100'
    #     self.ds.ImageType = ['', '', '', '', '']
    #     self.ds.InstanceCreationDate = ''
    #     self.ds.InstanceCreationTime = ''
    #     self.ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
    #     self.ds.StudyDate = ''
    #     self.ds.SeriesDate = ''
    #     self.ds.AcquisitionDate = ''
    #     self.ds.ContentDate = ''
    #     self.ds.StudyTime = ''
    #     self.ds.SeriesTime = ''
    #     self.ds.AcquisitionTime = ''
    #     self.ds.ContentTime = ''
    #     self.ds.AccessionNumber = ''
    #     self.ds.Modality = 'MR'
    #     self.ds.Manufacturer = ''
    #     self.ds.CodeValue = ''
    #     self.ds.CodingSchemeDesignator = 'DCM'
    #     self.ds.CodeMeaning = ''
    #     self.ds.OperatorsName = ''
    #     self.ds.AdmittingDiagnosesDescription = ''
    #     self.ds.ManufacturerModelName = ''
    #     self.ds.StudyDescription = ''
    #     self.ds.SeriesDescription = ''
    #
    #     # self.ds.PrivateCreator = 'Philips Imaging DD 001' # Tag must be this string to propagate 2001x private fields.
    #     self.ds.PatientName = 'Default Patient Name'
    #     self.ds.PatientID = 'Default Patient ID'
    #     self.ds.IssuerOfPatientID = ''
    #     self.ds.PatientBirthDate = ''
    #     self.ds.OtherPatientIDs = ''
    #     self.ds.OtherPatientNames = ''
    #     self.ds.PatientMotherBirthName = ''
    #     self.ds.PregnancyStatus = 4 # 4 = unknown pregnancy status
    #     self.ds.BodyPartExamined = ''
    #     self.ds.ScanningSequence = ''
    #     self.ds.SequenceVariant = ''
    #     self.ds.ScanOptions = ''
    #     self.ds.MRAcquisitionType = ''
    #     self.ds.SequenceName = ''
    #     self.ds.SliceThickness = ''
    #     self.ds.RepetitionTime = ''
    #     self.ds.EchoTime = ''
    #     self.ds.NumberOfAverages = "1"
    #     self.ds.ImagingFrequency = "127.768401"
    #     self.ds.ImagedNucleus = '1H'
    #     self.ds.EchoNumbers = "1"
    #     self.ds.MagneticFieldStrength = "1.5"
    #     self.ds.SpacingBetweenSlices = ""
    #     self.ds.NumberOfPhaseEncodingSteps = ""
    #     self.ds.EchoTrainLength = ""
    #     self.ds.PercentSampling = ""
    #     self.ds.PercentPhaseFieldOfView = ""
    #     self.ds.PixelBandwidth = ""
    #     self.ds.SoftwareVersions = ''
    #     self.ds.ProtocolName = 'Not Specified'
    #     self.ds.TriggerTime = "" ### REQUIRES DEFINITION
    #     self.ds.LowRRValue = ""
    #     self.ds.HighRRValue = ""
    #     self.ds.IntervalsAcquired = ""
    #     self.ds.IntervalsRejected = ""
    #     self.ds.HeartRate = ""
    #     self.ds.ReconstructionDiameter = ""
    #     self.ds.ReceiveCoilName = '' # 'MULTI COIL'
    #     self.ds.TransmitCoilName = '' # 'B'
    #     # self.ds.AcquisitionMatrix = [0, 148, 143, 0] # Think not required
    #     self.ds.InPlanePhaseEncodingDirection = ''
    #     self.ds.FlipAngle = ""
    #     self.ds.SAR = ""
    #     self.ds.dBdt = ""
    #     self.ds.PatientPosition = ''
    #     self.ds.AcquisitionDuration = ''
    #     self.ds.DiffusionBValue = 0.0
    #     self.ds.DiffusionGradientOrientation = [0.0, 0.0, 0.0]
    #     self.ds.StudyID = 'Default Study ID'
    #     self.ds.SeriesNumber = ''
    #     self.ds.AcquisitionNumber = ''
    #     self.ds.TemporalPositionIdentifier = "1"
    #     self.ds.NumberOfTemporalPositions = "1"
    #     self.ds.PositionReferenceIndicator = ''
    #     self.ds.SamplesPerPixel = 1
    #     self.ds.PhotometricInterpretation = 'MONOCHROME2'
    #     self.ds.BitsAllocated = 16
    #     self.ds.BitsStored = 12
    #     self.ds.HighBit = 11
    #     self.ds.PixelRepresentation = 0
    #     # ds.WindowCenter = "213.04" ### REQUIRES DEFINITION
    #     # ds.WindowWidth = "370.49" ### REQUIRES DEFINITION
    #     self.ds.PresentationLUTShape = 'IDENTITY'
    #     self.ds.LossyImageCompression = '00'
    #     self.ds.RequestingPhysician = ''
    #     self.ds.RequestingService = ''
    #     self.ds.RequestedProcedureDescription = ''
    #     self.ds.PerformedStationAETitle = ''
    #     self.ds.PerformedProcedureStepStartDate = ''
    #     self.ds.PerformedProcedureStepStartTime = ''
    #     self.ds.PerformedProcedureStepEndDate = ''
    #     self.ds.PerformedProcedureStepEndTime = ''
    #     self.ds.PerformedProcedureStepID = ''
    #     self.ds.PerformedProcedureStepDescription = ''
    #     self.ds.RequestedProcedureID = ''
    #
    #     # Required Fields
    #     # - fields required of ALL MRI dicoms
    #     # - initialise as None
    #     # - these depend on image properties, i.e: resolution, FOV, etc.
    #     self.ds.SOPInstanceUID = None
    #     self.ds.InstanceCreatorUID = None ### TODO: determine if required
    #     self.ds.Rows = None
    #     self.ds.Columns = None
    #     self.ds.PixelSpacing = None # ['float','float']
    #     self.ds.SliceLocation = None
    #     self.ds.StudyInstanceUID = None
    #     self.ds.SeriesInstanceUID = None
    #     self.ds.InstanceNumber = None
    #     self.ds.ImagePositionPatient = None # ['float','float','float']
    #     self.ds.ImageOrientationPatient = None # ['float','float','float','float','float','float'] ### TODO: decide if need to match Nifti affine
    #     self.ds.FrameOfReferenceUID = None # constant across all
    #
    #
    # def niiHdr2Dcm(self, nii_hdr):
    #     self.ds.Rows = nii_hdr['dim'][1]
    #     self.ds.Columns = nii_hdr['dim'][2]


class DicomMRI(Dicom):
    """
    Creates basic MRI DICOM structure
    """
