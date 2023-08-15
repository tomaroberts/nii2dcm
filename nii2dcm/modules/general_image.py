"""
IOD Module – General Image

C.7.6.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.html#sect_C.7.6.1
"""

from nii2dcm.module import Module


class GeneralImage(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'GeneralImage'

        self.ds.InstanceNumber = ''
        self.ds.PatientOrientation = ''
        self.ds.ContentDate = ''
        self.ds.ContentTime = ''
        self.ds.ImageType = ['SECONDARY', 'DERIVED']

        # LossyImageCompression
        # Enumerated values either:
        # 00 = no lossy compression
        # 01 = lossy compression
        self.ds.LossyImageCompression = '00'

