"""
IOD Module – General Equipment

C.7.5.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.5.html#sect_C.7.5.1
"""

from nii2dcm.module import Module


class GeneralEquipment(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'GeneralEquipment'

        self.ds.Manufacturer = ''
        self.ds.InstitutionName = 'INSTITUTION_NAME_UNDEFINED'
        self.ds.ManufacturerModelName = ""
        self.ds.SoftwareVersions = ''
