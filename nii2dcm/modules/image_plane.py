"""
IOD Module – Image Plane

C.7.6.2
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.2.html
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    dcm.ds.PixelSpacing = ''
    dcm.ds.ImageOrientationPatient = ''  # TODO set here or in Dicom class?
    dcm.ds.ImagePositionPatient = ''  # TODO set here or in Dicom class?
    dcm.ds.SliceThickness = ''
    dcm.ds.SpacingBetweenSlices = ''
    dcm.ds.SliceLocation = ''  # maths: https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.2.html#sect_C.7.6.2.1.2
