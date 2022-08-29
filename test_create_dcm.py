import nii2dcm.dcm

TestDicom = nii2dcm.dcm.Dicom('testDicom.dcm')
TestDicom.save_as()

TestDicomMRI = nii2dcm.dcm.DicomMRI('testDicomMri.dcm')
TestDicomMRI.save_as()

TestDicomMRISVR = nii2dcm.dcm.DicomMRISVR('testDicomMriSVR.dcm')
TestDicomMRISVR.save_as()