"""
IOD Module – General Acquisition

C.7.10.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.10.html#sect_C.7.10.1
"""


def add_module(dcm):
    """
    Adds Module to Pydicom Dataset object
    :param dcm: input Pydicom Dataset object
    :return: updated Pydicom Dataset object
    """

    # TODO generate Acquisition values here - perhaps with date/time subfunction - or perform within Dicom class
    #  (as currently doing)?
    dcm.ds.AcquisitionNumber = ''
    dcm.ds.AcquisitionDate = ''
    dcm.ds.AcquisitionTime = ''
