"""
IOD Module – Patient

C.7.1.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.html#sect_C.7.1.1
"""

from nii2dcm.module import Module


class Patient(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'PatientModule'

        self.ds.PatientName = 'Lastname^Firstname'
        self.ds.PatientID = '12345678'
        self.ds.PatientSex = ''
        self.ds.PatientBirthDate = ''
