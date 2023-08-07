"""
IOD Module – Patient

C.7.1.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.html#sect_C.7.1.1
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    dcm.ds.PatientName = 'Lastname^Firstname'
    dcm.ds.PatientID = '12345678'
    dcm.ds.PatientSex = ''
    dcm.ds.PatientBirthDate = ''

