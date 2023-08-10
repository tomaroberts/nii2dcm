"""
IOD Module – MR Image

C.8.3.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.8.3.html#sect_C.8.3.1

Note: Tags labelled ":missing:" are defined in the NEMA MR standard, but I have not found in real DICOMs exported from
an MRI scanner.
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    # ImageType
    # NEMA defines MR-specific ImageType terms here:
    # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.8.3.html#sect_C.8.3.1.1.1
    # For now, will inherit
    dcm.ds.ImageType = dcm.ds.ImageType

    dcm.ds.SamplesPerPixel = 1

    # PhotometricInterpretation
    # TODO: decide MONOCHROME1 or MONOCHROME2 as default
    # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.3.html#sect_C.7.6.3.1.2
    dcm.ds.PhotometricInterpretation = 'MONOCHROME2'

    # PresentationLUTShape
    # depends on PhotometricInterpretation: https://dicom.innolitics.com/ciods/mr-image/general-image/20500020
    if dcm.ds.PhotometricInterpretation == 'MONOCHROME2':
        dcm.ds.PresentationLUTShape = 'IDENTITY'
    elif dcm.ds.PhotometricInterpretation == 'MONOCHROME1':
        dcm.ds.PresentationLUTShape = 'INVERSE'

    # Bits Allocated
    # defined to equal 16 for MR Image Module
    # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.8.3.html#sect_C.8.3.1.1.4
    dcm.ds.BitsAllocated = 16
    dcm.ds.BitsStored = 12
    dcm.ds.HighBit = dcm.ds.BitsStored - 1

    dcm.ds.ScanningSequence = 'RM'  # :missing:, 'RM' = Research Mode
    dcm.ds.SequenceVariant = ''  # :missing:
    dcm.ds.ScanOptions = ''  # :missing:
    dcm.ds.MRAcquisitionType = ''  # 2D or 3D
    dcm.ds.RepetitionTime = ''
    dcm.ds.EchoTime = ''
    dcm.ds.EchoTrainLength = ''
    dcm.ds.InversionTime = ''
    dcm.ds.TriggerTime = ''
    dcm.ds.SequenceName = ''
    dcm.ds.AngioFlag = ''  # :missing:
    dcm.ds.NumberOfAverages = ''
    dcm.ds.ImagingFrequency = ''
    dcm.ds.ImagedNucleus = ''
    dcm.ds.EchoNumbers = ''
    dcm.ds.MagneticFieldStrength = ''
    dcm.ds.NumberOfPhaseEncodingSteps = ''  # :missing:
    dcm.ds.PercentSampling = ''  # TODO set?
    dcm.ds.PercentPhaseFieldOfView = ''  # TODO set?
    dcm.ds.PixelBandwidth = ''
    dcm.ds.NominalInterval = ''  # :missing:
    dcm.ds.BeatRejectionFlag = ''  # :missing:
    dcm.ds.LowRRValue = ''  # :missing:
    dcm.ds.HighRRValue = ''  # :missing:
    dcm.ds.IntervalsAcquired = ''  # :missing:
    dcm.ds.IntervalsRejected = ''  # :missing:
    dcm.ds.PVCRejection = ''  # :missing:
    dcm.ds.SkipBeats = ''  # :missing:
    dcm.ds.HeartRate = ''
    dcm.ds.CardiacNumberOfImages = ''
    dcm.ds.TriggerWindow = ''
    dcm.ds.ReconstructionDiameter = ''  # :missing:
    dcm.ds.ReceiveCoilName = ''
    dcm.ds.TransmitCoilName = ''
    dcm.ds.AcquisitionMatrix = ''  # :missing:
    dcm.ds.InPlanePhaseEncodingDirection = ''  # ROW or COLUMN
    dcm.ds.FlipAngle = ''
    dcm.ds.SAR = ''
    dcm.ds.VariableFlipAngleFlag = ''  # :missing:
    dcm.ds.dBdt = ''
    dcm.ds.TemporalPositionIdentifier = ''  # :missing:
    dcm.ds.NumberOfTemporalPositions = ''
    dcm.ds.TemporalResolution = ''  # :missing:

    # Currently omitting, but part of NEMA MR Image module:
    # NEMA Table 10-7 “General Anatomy Optional Macro Attributes”

    # Currently omitting, but part of NEMA MR Image module:
    # NEMA Table 10-25 “Optional View and Slice Progression Direction Macro Attributes”

    dcm.ds.IsocenterPosition = ''  # :missing:
    dcm.ds.B1rms = ''

