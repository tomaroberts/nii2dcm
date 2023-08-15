"""
IOD Module – Common Instance Reference

C.12.2
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.12.2.html
"""

from nii2dcm.module import Module


class CommonInstanceReference(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'CommonInstanceReference'

        # ReferencedSeriesSequence
        # omit for now, but can be important for references Instances/Series with other Series
        # self.ds.ReferencedSeriesSequence = ''
        pass
