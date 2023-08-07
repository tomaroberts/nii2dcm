"""
IOD Module – General Study

C.7.2.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.2.html#sect_C.7.2.1
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    dcm.ds.StudyInstanceUID = ''  # attribute initialised but value initialised in Dicom class
    dcm.ds.StudyDescription = ''
    dcm.ds.ReferringPhysicianName = ''


