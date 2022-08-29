import nii2dcm.dcm

TestDicom = nii2dcm.dcm.Dicom('testfile.dcm')
TestDicom.save_as()