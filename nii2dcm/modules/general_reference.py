"""
IOD Module – General Reference

C.12.4
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.12.4.html
"""

from nii2dcm.module import Module


class GeneralReference(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'GeneralReference'

        # TODO update placeholder class
        pass

