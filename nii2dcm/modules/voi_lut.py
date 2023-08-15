"""
IOD Module – VOI LUT

C.11.2
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.11.2.html
"""

from nii2dcm.module import Module


class VOILUT(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'VOILUT'

        # WindowCenter
        # From NEMA: Required if VOI LUT Sequence (0028,3010) is not present. May be present otherwise.
        self.ds.WindowCenter = ''
    
        # WindowWidth
        # Required if Window Center (0028,1050) is present.
        self.ds.WindowWidth = ''
