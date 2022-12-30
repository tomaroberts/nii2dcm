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
        self.ds.NumberOfPhaseEncodingSteps = ''
        self.ds.PercentPhaseFieldOfView = ''
        self.ds.BitsAllocated = 16

