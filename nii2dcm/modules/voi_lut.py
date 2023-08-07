"""
IOD Module – VOI LUT

C.11.2
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.11.2.html
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    # WindowCenter
    # From NEMA: Required if VOI LUT Sequence (0028,3010) is not present. May be present otherwise.
    dcm.ds.WindowCenter = ''

    # WindowWidth
    # Required if Window Center (0028,1050) is present.
    dcm.ds.WindowWidth = ''
