"""
IOD Module – General Series

C.7.3.1
https://dicom.nema.org/medical/Dicom/current/output/chtml/part03/sect_C.7.3.html#sect_C.7.3.1
"""

from nii2dcm.module import Module


class GeneralSeries(Module):

    def __init__(self):
        super().__init__()

        self.module_type = 'GeneralSeries'

        self.ds.Modality = ''  # initiated, should be defined by Dicom subclass
        self.ds.SeriesInstanceUID = ''  # initiated, but value set by Dicom.init_series_tags()
        self.ds.SeriesNumber = ''  # initiated, but value set by Dicom.init_series_tags()
        self.ds.ProtocolName = "nii2dcm_DICOM"

        # PatientPosition
        # From NEMA: required for images where Patient Orientation Code Sequence (0054,0410) is not present and whose
        # SOP Class is one of the following:
        # CT ("1.2.840.10008.5.1.4.1.1.2") or
        # MR ("1.2.840.10008.5.1.4.1.1.4") or
        # Enhanced CT ("1.2.840.10008.5.1.4.1.1.2.1") or
        # Enhanced MR Image ("1.2.840.10008.5.1.4.1.1.4.1") or
        # Enhanced Color MR Image ("1.2.840.10008.5.1.4.1.1.4.3") or
        # MR Spectroscopy ("1.2.840.10008.5.1.4.1.1.4.2")
        self.ds.PatientPosition = ''

        self.ds.AccessionNumber = "ABCXYZ"
