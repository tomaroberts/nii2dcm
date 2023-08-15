"""
IOD Module – MR Image

C.8.3.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.8.3.html#sect_C.8.3.1

Note: Tags labelled ":missing:" are defined in the NEMA MR standard, but I have not found in real DICOMs exported from
an MRI scanner.
"""


from nii2dcm.module import Module


class MRImage(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'MRImage'

        # ImageType
        # NEMA defines MR-specific ImageType terms here:
        # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.8.3.html#sect_C.8.3.1.1.1
        # For now, will omit thereby inheriting parent value
        # self.ds.ImageType = ''
    
        self.ds.SamplesPerPixel = 1
    
        # PhotometricInterpretation
        # TODO: decide MONOCHROME1 or MONOCHROME2 as default
        # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.3.html#sect_C.7.6.3.1.2
        self.ds.PhotometricInterpretation = 'MONOCHROME2'
    
        # PresentationLUTShape
        # depends on PhotometricInterpretation: https://dicom.innolitics.com/ciods/mr-image/general-image/20500020
        if self.ds.PhotometricInterpretation == 'MONOCHROME2':
            self.ds.PresentationLUTShape = 'IDENTITY'
        elif self.ds.PhotometricInterpretation == 'MONOCHROME1':
            self.ds.PresentationLUTShape = 'INVERSE'
    
        # Bits Allocated
        # defined to equal 16 for MR Image Module
        # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.8.3.html#sect_C.8.3.1.1.4
        self.ds.BitsAllocated = 16
        self.ds.BitsStored = 12
        self.ds.HighBit = self.ds.BitsStored - 1
    
        self.ds.ScanningSequence = 'RM'  # :missing:, 'RM' = Research Mode
        self.ds.SequenceVariant = ''  # :missing:
        self.ds.ScanOptions = ''  # :missing:
        self.ds.MRAcquisitionType = ''  # 2D or 3D
        self.ds.RepetitionTime = ''
        self.ds.EchoTime = ''
        self.ds.EchoTrainLength = ''
        self.ds.InversionTime = ''
        self.ds.TriggerTime = ''
        self.ds.SequenceName = ''
        self.ds.AngioFlag = ''  # :missing:
        self.ds.NumberOfAverages = ''
        self.ds.ImagingFrequency = ''
        self.ds.ImagedNucleus = ''
        self.ds.EchoNumbers = ''
        self.ds.MagneticFieldStrength = ''
        self.ds.NumberOfPhaseEncodingSteps = ''  # :missing:
        self.ds.PercentSampling = ''  # TODO set?
        self.ds.PercentPhaseFieldOfView = ''  # TODO set?
        self.ds.PixelBandwidth = ''
        self.ds.NominalInterval = ''  # :missing:
        self.ds.BeatRejectionFlag = ''  # :missing:
        self.ds.LowRRValue = ''  # :missing:
        self.ds.HighRRValue = ''  # :missing:
        self.ds.IntervalsAcquired = ''  # :missing:
        self.ds.IntervalsRejected = ''  # :missing:
        self.ds.PVCRejection = ''  # :missing:
        self.ds.SkipBeats = ''  # :missing:
        self.ds.HeartRate = ''
        self.ds.CardiacNumberOfImages = ''
        self.ds.TriggerWindow = ''
        self.ds.ReconstructionDiameter = ''  # :missing:
        self.ds.ReceiveCoilName = ''
        self.ds.TransmitCoilName = ''
        self.ds.AcquisitionMatrix = ''  # :missing:
        self.ds.InPlanePhaseEncodingDirection = ''  # ROW or COLUMN
        self.ds.FlipAngle = ''
        self.ds.SAR = ''
        self.ds.VariableFlipAngleFlag = ''  # :missing:
        self.ds.dBdt = ''
        self.ds.TemporalPositionIdentifier = ''  # :missing:
        self.ds.NumberOfTemporalPositions = ''
        self.ds.TemporalResolution = ''  # :missing:
    
        # Currently omitting, but part of NEMA MR Image module:
        # NEMA Table 10-7 “General Anatomy Optional Macro Attributes”
    
        # Currently omitting, but part of NEMA MR Image module:
        # NEMA Table 10-25 “Optional View and Slice Progression Direction Macro Attributes”
    
        self.ds.IsocenterPosition = ''  # :missing:
        self.ds.B1rms = ''

