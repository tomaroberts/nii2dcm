"""
IOD Module – Image Plane

C.7.6.2
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.2.html
"""

from nii2dcm.module import Module


class ImagePlane(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'ImagePlane'

        self.ds.PixelSpacing = ''
        self.ds.ImageOrientationPatient = ''  # TODO set here or in Dicom class?
        self.ds.ImagePositionPatient = ''  # TODO set here or in Dicom class?
        self.ds.SliceThickness = ''
        self.ds.SpacingBetweenSlices = ''
        self.ds.SliceLocation = ''  # maths: https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.2.html#sect_C.7.6.2.1.2
