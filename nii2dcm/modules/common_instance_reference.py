"""
IOD Module – Common Instance Reference

C.12.2
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.12.2.html
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    # ReferencedSeriesSequence
    # omit for now, but can be important for references Instances/Series with other Series
    # dcm.ds.ReferencedSeriesSequence = ''
    pass
