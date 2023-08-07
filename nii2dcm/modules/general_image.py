"""
IOD Module – General Image

C.7.6.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.html#sect_C.7.6.1
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    dcm.ds.InstanceNumber = ''
    dcm.ds.PatientOrientation = ''
    dcm.ds.ContentDate = ''
    dcm.ds.ContentTime = ''
    dcm.ds.ImageType = ''

