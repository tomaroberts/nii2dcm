"""
Test DICOM creation from different classes/subclasses
"""

import nii2dcm.dcm
import nii2dcm.svr

TestDicom = nii2dcm.dcm.Dicom('testDicom.dcm')
TestDicom.save_as()

TestDicomMRI = nii2dcm.dcm.DicomMRI('testDicomMri.dcm')
TestDicomMRI.save_as()

TestDicomMRISVR = nii2dcm.svr.DicomMRISVR('testDicomMriSVR.dcm')
TestDicomMRISVR.save_as()