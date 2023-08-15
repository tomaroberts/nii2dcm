"""
IOD Module – Frame of Reference

C.7.4.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.4.html#sect_C.7.4.1
"""

from nii2dcm.module import Module


class FrameOfReference(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'FrameOfReference'

        self.ds.FrameOfReferenceUID = ''
        # self.ds.PositionReferenceIndicator = ''  # TODO add robustly
