"""
IOD Module – General Equipment

C.7.5.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.5.html#sect_C.7.5.1
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    dcm.ds.Manufacturer = ''
    dcm.ds.InstitutionName = 'INSTITUTION_NAME_UNDEFINED'
    dcm.ds.ManufacturerModelName = ""
    dcm.ds.SoftwareVersions = ''
