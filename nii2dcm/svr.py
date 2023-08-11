"""
Classes for creating 3D MRI SVR DICOMs

Tom Roberts
"""

from nii2dcm.dcm import DicomMRI, nii2dcm_temp_filename


class DicomMRISVR(DicomMRI):
    """
    Creates 3D Slice-to-Volume Registration reconstruction DICOM
    """

    def __init__(self, filename=nii2dcm_temp_filename):
        super().__init__(filename)

        self.ds.MRAcquisitionType = '3D'
        self.ds.AcquisitionDuration = ''

        self.ds.ProtocolName = 'SVRTK_RESEARCH_RECONSTRUCTION'
        self.ds.SeriesDescription = 'SVRTK_RESEARCH_RECONSTRUCTION'

        """
        DICOM Attributes to transfer from DICOM supplied using --ref_dicom CLI option        
        IMPORTANT: this list overrides the equivalent list in DicomMRI class
        """

        # Not transferring PatientPosition
        # - Does this affect 3D display? Leave empty for now
        self.attributes_to_transfer.remove('PatientPosition')
