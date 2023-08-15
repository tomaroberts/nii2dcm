"""
IOD Module – SOP Common

C.12.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.12.html#sect_C.12.1
"""

from nii2dcm.module import Module


class SOPCommon(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'SOPCommon'

        self.ds.SOPClassUID = ''  # initiated, should be defined by Dicom subclass
        self.ds.SOPInstanceUID = ''
    
        # SpecificCharacterSet
        # Default set to ISO_IR 100 = Latin alphabet No. 1
        # https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.12.html#sect_C.12.1.1.2
        self.ds.SpecificCharacterSet = 'ISO_IR 100'
        self.ds.InstanceCreationDate = ''
        self.ds.InstanceCreationTime = ''
    
        self.ds.InstanceCreatorUID = ''
