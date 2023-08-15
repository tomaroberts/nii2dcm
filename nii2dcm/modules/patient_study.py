"""
IOD Module – Patient Study

C.7.2.2
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.2.2.html
"""

from nii2dcm.module import Module


class PatientStudy(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'PatientStudy'

        self.ds.PatientAge = ""
        self.ds.PatientWeight = ""
