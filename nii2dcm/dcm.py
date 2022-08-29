"""
classes for creating a dicom from scratch

Tom Roberts
"""

import tempfile
import datetime
import os
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import UID
from pydicom.datadict import DicomDictionary, keyword_dict
from pydicom.sequence import Sequence
import nibabel as nib


class Dicom:
    """
    Creates basic DICOM structure

    Assumptions:
    - is_implicit_VR = False
    - is_little_endian = True

    """

    def __init__(self, filename=tempfile.NamedTemporaryFile(suffix='.dcm').name):

        # TODO:
        # - add in correct UIDs
        # - arrange tags into Series/Instance tags

        self.dcm_dictionary_update()

        self.filename = filename

        # Creates minimal FileMeta
        self.file_meta = FileMetaDataset()
        self.file_meta.FileMetaInformationGroupLength = ''
        self.file_meta.FileMetaInformationVersion = ''
        # self.file_meta.FileMetaInformationVersion = b'\x00\x01'  # Think redundant
        self.file_meta.MediaStorageSOPClassUID = ''
        self.file_meta.MediaStorageSOPInstanceUID = ''
        self.file_meta.ImplementationClassUID = ''
        self.file_meta.ImplementationVersionName = 'nii2dcm_DICOM'

        # Creates minimal DataSet
        self.ds = FileDataset(filename, {}, file_meta=self.file_meta, preamble=b"\0" * 128)
        self.ds.is_implicit_VR = False
        self.ds.is_little_endian = True
        self.ds.SpecificCharacterSet = "ISO_IR 100"
        self.ds.ImageType = ['DERIVED', 'SECONDARY']
        self.ds.ProtocolName = "nii2dcm_DICOM"

        self.ds.PatientName = "Test^Firstname"
        self.ds.PatientID = "12345678"
        self.ds.AccessionNumber = "ABCXYZ"
        self.ds.PatientBirthDate = ""
        self.ds.PatientSex = ""
        self.ds.PatientAge = ""
        self.ds.PatientWeight = ""
        self.ds.BodyPartExamined = ""

        self.ds.InstitutionName = "INSTITUTION_NAME_NONE"
        self.ds.Manufacturer = ""
        self.ds.ManufacturerModelName = ""
        self.ds.StudyDescription = ""
        self.ds.InstanceCreatorUID = ''

        self.ds.SOPClassUID = ''
        self.ds.Modality = ''

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

        self.ds.Rows = ""
        self.ds.Columns = ""
        self.ds.PixelSpacing = ""
        self.ds.SamplesPerPixel = ""
        self.ds.ImageOrientationPatient = ['1', '0', '0', '0', '1', '0']

        self.ds.RescaleIntercept = ""
        self.ds.RescaleSlope = ""
        self.ds.WindowCenter = ""
        self.ds.WindowWidth = ""

        # per Instance tags
        self.ds.SOPInstanceUID = ""
        self.ds.InstanceNumber = ""
        self.ds.SliceThickness = ""
        self.ds.SpacingBetweenSlices = ""
        self.ds.SliceLocation = ""
        self.ds.ImagePositionPatient = ['0', '0', '0']

        # per Series tags
        self.ds.SeriesInstanceUID = ""
        self.ds.SeriesNumber = ""
        self.ds.AcquisitionNumber = ""

        # # MRI DICOM tags
        # # TODO: create MRI DICOM class
        # self.ds.Modality = 'MR'
        # self.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        # self.ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        # self.ds.MRAcquisitionType = '' # '3D' for SVR

        # # Omitted for now:
        # 'FrameOfReferenceUID': uid_frame_of_reference,  # per SVR – think to do with localizer
        # 'TemporalPositionIdentifier': '1',
        # 'NumberOfTemporalPositions': '1',
        # 'PositionReferenceIndicator': '',  # MC said v important, can be undefined
        # 'InstitutionAddress': 'InstitutionAddress',
        # 'ReferringPhysicianName': 'ReferringPhysicianName',
        # 'CodeValue': 'CodeValue',
        # 'CodingSchemeDesignator': 'CodingSchemeDesignator',
        # 'CodeMeaning': 'CodeMeaning',
        # 'StationName': 'StationName',
        # 'InstitutionalDepartmentName': 'InstitutionalDepartmentName',
        # 'PerformingPhysicianName': 'PerformingPhysicianName',
        # 'OperatorsName': 'OperatorsName',

    def get_file_meta(self):
        return self.file_meta

    def get_dataset(self):
        return self.ds

    def save_as(self):
        print("Writing DICOM to", os.path.join(os.getcwd(), self.filename))
        self.ds.save_as(self.filename)

    def dcm_dictionary_update(self):
        """
        Update Pydicom DicomDictionary object with non-standard Private tags.
        Tuple definitions: (VR, VM, description, is_retired flag, keyword)
        See: https://pydicom.github.io/pydicom/stable/auto_examples/metadata_processing/plot_add_dict_entries.html
        """

        new_dict_items = {
            0x20011002: ('IS', '1', "Chemical Shift Number MR", '', 'ChemicalShiftNumberMR'),
            0x20011008: ('IS', '1', "Phase Number", '', 'PhaseNumber'),
            0x2001100a: ('IS', '1', "Slice Number MR", '', 'SliceNumberMR'),
            0x2001100b: ('CS', '1', "Slice Orientation", '', 'SliceOrientation'),
            0x20011014: ('SL', '1', "Number Of Echoes", '', 'NumberOfEchoes'),
            0x20011015: ('SS', '1', "Number Of Locations", '', 'NumberOfLocations'),
            0x20011016: ('SS', '1', "Number Of PC Directions", '', 'NumberOfPCDirections'),
            0x20011017: ('SL', '1', "Number Of Phases MR", '', 'NumberOfPhasesMR'),
            0x20011018: ('SL', '1', "Number Of Slices MR", '', 'NumberOfSlicesMR'),
            0x20011020: ('LO', '1', "Scanning Technique", '', 'ScanningTechnique'),
            0x20011025: ('SH', '1', "Echo Time Display MR", '', 'EchoTimeDisplayMR'),
            0x20011060: ('SL', '1', "Number Of Stacks", '', 'NumberOfStacks'),
            0x20011063: ('CS', '1', "Examination Source", '', 'ExaminationSource'),
            # 0x2001107b: ('IS', '1', "Acquisition Number", '', 'AcquisitionNumber'), # Philips Private alternative
            0x20011081: ('IS', '1', "Number Of Dynamic Scans", '', 'NumberOfDynamicScans'),
            0x2001101a: ('FL', '3', "PC Velocity", '', 'PCVelocity'),
            0x2001101d: ('IS', '1', "Reconstruction Number MR", '', 'ReconstructionNumberMR'),
            0x20051035: ('CS', '1', '', '', 'unknowntag20051035'),
            # PIXEL --- this seems to also correspond to MRSeriesDataType?
            0x20051011: ('CS', '1', 'MR Image Type', '', 'MRImageType'),
            0x2005106e: ('CS', '1', 'MR Scan Sequence', '', 'MRScanSequence'),

            # Philips "Stack" Tags
            0x2001105f: ('SQ', '1', 'Stack', '', 'Stack'),
            0x20010010: ('LO', '1', "Private Creator", '', 'PrivateCreator20010010'),
            0x2001102d: ('SS', '1', 'StackNumberOfSlices', '', 'StackNumberOfSlices'),
            0x20011032: ('FL', '1', 'StackRadialAngle', '', 'StackRadialAngle'),
            0x20011033: ('CS', '1', 'StackRadialAxis', '', 'StackRadialAxis'),
            0x20011035: ('SS', '1', 'MRSeriesDataType', '', 'MRSeriesDataType'),  # SS - StackSliceNumber ?
            0x20011036: ('CS', '1', 'StackType', '', 'StackType'),
            0x20050010: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050010'),
            # Is this duplicate necessary with entry above?
            0x20050011: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050011'),
            0x20050012: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050012'),
            0x20050013: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050013'),
            0x20050014: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050014'),
            0x20050015: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050015'),
            0x20051071: ('FL', '1', 'MRStackAngulationAP', '', 'MRStackAngulationAP'),
            0x20051072: ('FL', '1', 'MRStackAngulationFH', '', 'MRStackAngulationFH'),
            0x20051073: ('FL', '1', 'MRStackAngulationRL', '', 'MRStackAngulationRL'),
            0x20051074: ('FL', '1', 'MRStackFovAP', '', 'MRStackFovAP'),
            0x20051075: ('FL', '1', 'MRStackFovFH', '', 'MRStackFovFH'),
            0x20051076: ('FL', '1', 'MRStackFovRL', '', 'MRStackFovRL'),
            0x20051078: ('FL', '1', 'MRStackOffcentreAP', '', 'MRStackOffcentreAP'),
            0x20051079: ('FL', '1', 'MRStackOffcentreFH', '', 'MRStackOffcentreFH'),
            0x2005107a: ('FL', '1', 'MRStackOffcentreRL', '', 'MRStackOffcentreRL'),
            0x2005107b: ('CS', '1', 'MRStackPreparationDirection', '', 'MRStackPreparationDirection'),
            0x2005107e: ('FL', '1', 'MRStackSliceDistance', '', 'MRStackSliceDistance'),
            0x20051081: ('CS', '1', 'MRStackViewAxis', '', 'MRStackViewAxis'),
            0x2005143c: ('FL', '1', 'MRStackTablePosLong', '', 'MRStackTablePosLong'),
            0x2005143d: ('FL', '1', 'MRStackTablePosLat', '', 'MRStackTablePosLat'),
            0x2005143e: ('FL', '1', 'MRStackPosteriorCoilPos', '', 'MRStackPosteriorCoilPos'),
            0x20051567: ('IS', '1', 'MRPhilipsX1', '', 'MRPhilipsX1'),

            # Phase Contrast/Velocity Tags
            0x00089209: ('CS', '1', "Acquisition Contrast", '', 'AcquisitionContrast'),
            0x00189014: ('CS', '1', "Phase Contrast", '', 'PhaseContrast'),
            0x00189090: ('FD', '3', "Velocity Encoding Direction", '', 'VelocityEncodingDirection'),
            0x00189091: ('FD', '1', "Velocity Encoding Minimum Value", '', 'VelocityEncodingMinimumValue'),
        }

        # Update the dictionary itself
        DicomDictionary.update(new_dict_items)

        # Update the reverse mapping from name to tag
        new_names_dict = dict([(val[4], tag) for tag, val in new_dict_items.items()])
        keyword_dict.update(new_names_dict)

    # def initDcmHdr(self):
    #     """ create minimal dicom header
    #     - essential fields found in all MRI dicoms
    #     - many fields can be left blank
    #     - some initialised with MRI-related tags
    #     """
    #
    #     # fm - file_meta
    #     self.file_meta.FileMetaInformationVersion = b'\x00\x01'
    #
    #
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
