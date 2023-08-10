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

        self.ds.PatientPosition = ''  # does this affect 3D display? inherit from ref_dicom (e.g. [HFS]) or leave blank?

        self.ds.RequestingPhysician = ''
        self.ds.RequestingService = ''
        self.ds.RequestedProcedureDescription = ''
        self.ds.RequestedContrastAgent = ''
        self.ds.PerformedStationAETitle = ''
        self.ds.PerformedStationName = ''
        self.ds.PerformedLocation = ''

        # # Omit for now:
        # 'PositionReferenceIndicator': '',  # MC said v important, can be undefined
        # 'InstitutionAddress': 'InstitutionAddress',
        # 'ReferringPhysicianName': 'ReferringPhysicianName',
        # 'CodeValue': 'CodeValue',
        # 'CodingSchemeDesignator': 'CodingSchemeDesignator',
        # 'CodeMeaning': 'CodeMeaning',
        # 'StationName': 'StationName',
        # 'InstitutionalDepartmentName': 'InstitutionalDepartmentName',
        # 'PerformingPhysicianName': 'PerformingPhysicianName',
        # 'OperatorsName': 'OperatorsName',


