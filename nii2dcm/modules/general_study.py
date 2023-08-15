"""
IOD Module – General Study

C.7.2.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.2.html#sect_C.7.2.1
"""


from nii2dcm.module import Module


class GeneralStudy(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'GeneralStudy'

        self.ds.StudyInstanceUID = ''  # attribute initialised but value initialised in Dicom class
        self.ds.StudyDescription = ''
        self.ds.ReferringPhysicianName = ''


