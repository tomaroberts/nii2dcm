"""
IOD Module – Frame of Reference

C.7.4.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.4.html#sect_C.7.4.1
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    dcm.ds.FrameOfReferenceUID = ''
    # dcm.ds.PositionReferenceIndicator = ''  # TODO add robustly
