"""
IOD Module – General Acquisition

C.7.10.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.10.html#sect_C.7.10.1
"""

from nii2dcm.module import Module


class GeneralAcquisition(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'GeneralAcquisition'

        # TODO generate Acquisition values here - perhaps with date/time subfunction - or perform within Dicom class
        #  (as currently doing)?
        self.ds.AcquisitionNumber = ''
        self.ds.AcquisitionDate = ''
        self.ds.AcquisitionTime = ''
