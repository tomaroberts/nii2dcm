"""
IOD Module – Image Pixel

C.7.6.3
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.3.html

and

C.7-11c
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.6.3.3.html#table_C.7-11c
"""


from nii2dcm.module import Module


class ImagePixel(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'ImagePixel'

        self.ds.Rows = ''
        self.ds.Columns = ''

        # BitsAllocated, BitsStored, HighBit
        # Setting default = 1 for purposes of basic DICOM creation. Should be overwritten by Dicom subclass.
        self.ds.BitsAllocated = 1
        self.ds.BitsStored = ''
        self.ds.HighBit = ''

        # PixelRepresentation
        # Enumerated values either: unsigned integer or two's complement
        # Setting = 0, as observed in real DICOM
        self.ds.PixelRepresentation = 0

        self.ds.SmallestImagePixelValue = ''
        self.ds.LargestImagePixelValue = ''

        # PixelData written in dcm_writer via Pydicom
        self.ds.PixelData = ''
