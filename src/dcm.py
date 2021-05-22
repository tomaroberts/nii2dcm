"""
classes for creating a dicom from scratch

Tom Roberts
"""

import pydicom
from pydicom.dataset  import Dataset, FileDataset, FileMetaDataset
from pydicom.datadict import DicomDictionary, keyword_dict
from pydicom.sequence import Sequence
import nibabel as nib

class DCM:

    def __init__(self, ds, file_meta):
        self.ds = ds
        self.file_meta = file_meta

    def get_dataset(self):
        return self.ds

    def get_file_meta(self):
        return self.file_meta

    def initDcmHdr(self):
        """ create minimal dicom header
        - essential fields found in all MRI dicoms
        - many fields can be left blank
        - some initialised with MRI-related tags
        """

        # fm - file_meta
        self.file_meta.FileMetaInformationVersion = b'\x00\x01'
        self.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        self.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
        self.file_meta.ImplementationClassUID = '1.2.276.0.7230010.3.0.3.6.1'
        self.file_meta.ImplementationVersionName = 'dicom_created_with_nii2dcm'

        # ds - main data elements
        self.ds.SpecificCharacterSet = 'ISO_IR 100'
        self.ds.ImageType = ['', '', '', '', '']
        self.ds.InstanceCreationDate = ''
        self.ds.InstanceCreationTime = ''
        self.ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        self.ds.StudyDate = ''
        self.ds.SeriesDate = ''
        self.ds.AcquisitionDate = ''
        self.ds.ContentDate = ''
        self.ds.StudyTime = ''
        self.ds.SeriesTime = ''
        self.ds.AcquisitionTime = ''
        self.ds.ContentTime = ''
        self.ds.AccessionNumber = ''
        self.ds.Modality = 'MR'
        self.ds.Manufacturer = ''
        self.ds.CodeValue = ''
        self.ds.CodingSchemeDesignator = 'DCM'
        self.ds.CodeMeaning = ''
        self.ds.OperatorsName = ''
        self.ds.AdmittingDiagnosesDescription = ''
        self.ds.ManufacturerModelName = ''
        self.ds.StudyDescription = ''
        self.ds.SeriesDescription = ''
        
        # self.ds.PrivateCreator = 'Philips Imaging DD 001' # Tag must be this string to propagate 2001x private fields.
        self.ds.PatientName = 'Default Patient Name'
        self.ds.PatientID = 'Default Patient ID'
        self.ds.IssuerOfPatientID = ''
        self.ds.PatientBirthDate = ''
        self.ds.OtherPatientIDs = ''
        self.ds.OtherPatientNames = ''
        self.ds.PatientMotherBirthName = ''
        self.ds.PregnancyStatus = 4 # 4 = unknown pregnancy status
        self.ds.BodyPartExamined = ''
        self.ds.ScanningSequence = ''
        self.ds.SequenceVariant = ''
        self.ds.ScanOptions = ''
        self.ds.MRAcquisitionType = ''
        self.ds.SequenceName = ''
        self.ds.SliceThickness = ''
        self.ds.RepetitionTime = ''
        self.ds.EchoTime = ''
        self.ds.NumberOfAverages = "1"
        self.ds.ImagingFrequency = "127.768401"
        self.ds.ImagedNucleus = '1H'
        self.ds.EchoNumbers = "1"
        self.ds.MagneticFieldStrength = "1.5"
        self.ds.SpacingBetweenSlices = ""
        self.ds.NumberOfPhaseEncodingSteps = ""
        self.ds.EchoTrainLength = ""
        self.ds.PercentSampling = ""
        self.ds.PercentPhaseFieldOfView = ""
        self.ds.PixelBandwidth = ""
        self.ds.SoftwareVersions = ''
        self.ds.ProtocolName = 'Not Specified' 
        self.ds.TriggerTime = "" ### REQUIRES DEFINITION
        self.ds.LowRRValue = ""
        self.ds.HighRRValue = ""
        self.ds.IntervalsAcquired = ""
        self.ds.IntervalsRejected = ""
        self.ds.HeartRate = ""
        self.ds.ReconstructionDiameter = ""
        self.ds.ReceiveCoilName = '' # 'MULTI COIL'
        self.ds.TransmitCoilName = '' # 'B'
        # self.ds.AcquisitionMatrix = [0, 148, 143, 0] # Think not required
        self.ds.InPlanePhaseEncodingDirection = ''
        self.ds.FlipAngle = ""
        self.ds.SAR = ""
        self.ds.dBdt = ""
        self.ds.PatientPosition = ''
        self.ds.AcquisitionDuration = ''
        self.ds.DiffusionBValue = 0.0
        self.ds.DiffusionGradientOrientation = [0.0, 0.0, 0.0]
        self.ds.StudyID = 'Default Study ID'
        self.ds.SeriesNumber = ''
        self.ds.AcquisitionNumber = ''
        self.ds.TemporalPositionIdentifier = "1"
        self.ds.NumberOfTemporalPositions = "1"
        self.ds.PositionReferenceIndicator = ''
        self.ds.SamplesPerPixel = 1
        self.ds.PhotometricInterpretation = 'MONOCHROME2'
        self.ds.BitsAllocated = 16
        self.ds.BitsStored = 12
        self.ds.HighBit = 11
        self.ds.PixelRepresentation = 0
        # ds.WindowCenter = "213.04" ### REQUIRES DEFINITION
        # ds.WindowWidth = "370.49" ### REQUIRES DEFINITION
        self.ds.PresentationLUTShape = 'IDENTITY'
        self.ds.LossyImageCompression = '00'
        self.ds.RequestingPhysician = ''
        self.ds.RequestingService = ''
        self.ds.RequestedProcedureDescription = ''
        self.ds.PerformedStationAETitle = ''
        self.ds.PerformedProcedureStepStartDate = ''
        self.ds.PerformedProcedureStepStartTime = ''
        self.ds.PerformedProcedureStepEndDate = ''
        self.ds.PerformedProcedureStepEndTime = ''
        self.ds.PerformedProcedureStepID = ''
        self.ds.PerformedProcedureStepDescription = ''
        self.ds.RequestedProcedureID = ''

        # Required Fields
        # - fields required of ALL MRI dicoms
        # - initialise as None
        # - these depend on image properties, i.e: resolution, FOV, etc.
        self.ds.SOPInstanceUID = None
        self.ds.InstanceCreatorUID = None ### TODO: determine if required
        self.ds.Rows = None
        self.ds.Columns = None
        self.ds.PixelSpacing = None # ['float','float']
        self.ds.SliceLocation = None
        self.ds.StudyInstanceUID = None
        self.ds.SeriesInstanceUID = None
        self.ds.InstanceNumber = None
        self.ds.ImagePositionPatient = None # ['float','float','float']
        self.ds.ImageOrientationPatient = None # ['float','float','float','float','float','float'] ### TODO: decide if need to match Nifti affine
        self.ds.FrameOfReferenceUID = None # constant across all

    #     # # Procedure Code Sequence
    #     # procedure_code_sequence = Sequence()
    #     # ds.ProcedureCodeSequence = procedure_code_sequence
    #     # procedure_code1 = Dataset()
    #     # procedure_code1.CodeValue = ''
    #     # procedure_code1.CodingSchemeDesignator = ''
    #     # procedure_code1.CodeMeaning = ''
    #     # procedure_code1.ContextGroupExtensionFlag = 'N'
    #     # procedure_code_sequence.append(procedure_code1)

    #     # # Referenced Image Sequence
    #     # refd_image_sequence = Sequence()
    #     # ds.ReferencedImageSequence = refd_image_sequence

    #     # refd_image1 = Dataset()
    #     # refd_image1.ReferencedSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
    #     # refd_image1.ReferencedSOPInstanceUID = '' # '1.2.40.0.13.1.89078282904346598403696206113943676723' # Constant across M/V _only_ 
    #     # refd_image_sequence.append(refd_image1)

    #     # refd_image2 = Dataset()
    #     # refd_image2.ReferencedSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
    #     # refd_image2.ReferencedSOPInstanceUID = '' # '1.2.40.0.13.1.295129673873169057216869911833080985343' # Constant across M/V _only_ 
    #     # refd_image_sequence.append(refd_image2)

    #     # refd_image3 = Dataset()
    #     # refd_image3.ReferencedSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
    #     # refd_image3.ReferencedSOPInstanceUID = '' # '1.2.40.0.13.1.37560432539838529536104187971339317428' # Constant across R/M/V
    #     # refd_image_sequence.append(refd_image3)

    #     # # Real World Value Mapping Sequence
    #     # real_world_value_mapping_sequence = Sequence()
    #     # ds.RealWorldValueMappingSequence = real_world_value_mapping_sequence
    #     # real_world_value_mapping1 = Dataset()
    #     # real_world_value_mapping1.RealWorldValueIntercept = 0.0
    #     # real_world_value_mapping1.RealWorldValueSlope = 1.0 # Important this is non-zero!
    #     # real_world_value_mapping_sequence.append(real_world_value_mapping1)


    # def requiredParams(self):
        # ds.SOPInstanceUID = '1.2.40.0.13.1.75591523476291404472265359935487530723' ### REQUIRES DEFINITION
        # ds.InstanceCreatorUID = '1.2.40.0.13.1.203399489339977079628124438700844270739' ### TODO: determine if required
        # self.ds.Rows = 192 ### REQUIRES DEFINITION
        # self.ds.Columns = 192 ### REQUIRES DEFINITION
        # ds.PixelSpacing = ['1.97916662693023', '1.97916662693023'] ### REQUIRES DEFINITION
        # ds.SliceLocation = "38.9999961150011" ### REQUIRES DEFINITION
        # ds.StudyInstanceUID = '1.2.40.0.13.1.333311361771566580913219583914625766216'
        # ds.SeriesInstanceUID = '1.2.40.0.13.1.286595144572817015845933344548631223145'
        # ds.InstanceNumber = "319" ### REQUIRES DEFINITION
        # ds.ImagePositionPatient = ['-56.040032677094', '-189.81796011867', '225.026188065538'] ### REQUIRES DEFINITION
        # ds.ImageOrientationPatient = ['0.51319164037704', '0.85772150754928', '-0.0307911429554', '-0.0599991045892', '6.4554493292E-05', '-0.9981984496116'] ### TODO: decide if need to match Nifti affine
        # ds.FrameOfReferenceUID = '1.2.40.0.13.1.168070265634523572089252568290704983898' # constant across all

        # return ds

    def niiHdr2Dcm(self, nii_hdr):
        self.ds.Rows = nii_hdr['dim'][1]
        self.ds.Columns = nii_hdr['dim'][2]
