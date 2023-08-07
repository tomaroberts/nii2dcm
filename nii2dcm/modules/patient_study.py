"""
IOD Module – Patient Study

C.7.2.2
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.2.2.html
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    dcm.ds.PatientAge = ""
    dcm.ds.PatientWeight = ""
