"""
IOD Module – Image Pixel

C.7.6.3
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.3.html

and

C.7-11c
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.3.3.html#table_C.7-11c
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    dcm.ds.Rows = ''
    dcm.ds.Columns = ''
    dcm.ds.BitsAllocated = ''
    dcm.ds.BitsStored = ''
    dcm.ds.HighBit = ''
    dcm.ds.PixelRepresentation = ''

    # PixelData written in dcm_writer via Pydicom
    dcm.ds.PixelData = ''
