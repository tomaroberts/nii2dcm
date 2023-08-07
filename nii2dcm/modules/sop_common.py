"""
IOD Module – SOP Common

C.12.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.12.html#sect_C.12.1
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    dcm.ds.SOPClassUID = ''  # initiated, should be defined by Dicom subclass
    dcm.ds.SOPInstanceUID = ''

    # SpecificCharacterSet
    # Default set to ISO_IR 100 = Latin alphabet No. 1
    # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.12.html#sect_C.12.1.1.2
    dcm.ds.SpecificCharacterSet = 'ISO_IR 100'
    dcm.ds.InstanceCreationDate = ''
    dcm.ds.InstanceCreationTime = ''

    dcm.ds.InstanceCreatorUID = ''
