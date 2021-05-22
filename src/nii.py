"""
classes for manipulating nifti files

Tom Roberts
"""

import numpy as np
import nibabel as nib
# import pydicom
# from pydicom.dataset  import Dataset, FileDataset, FileMetaDataset
# from pydicom.datadict import DicomDictionary, keyword_dict
# from pydicom.sequence import Sequence

class NII:

    def assessNii(nii):
        """
        Determine nSeries
        :nii - nii loaded with nibabel
        :nii_parameters - parameters to transfer to dicom header

        """    

    def getNiiParameters(nii):
        
        """
        Get parameters from nifti to transfer to dicom
        :nii - nii loaded with nibabel
        :nii_parameters - parameters to transfer to dicom header

        """

        nii_img = nii.get_fdata()

        if nii.header['dim'][0] == 3:
            nX, nY, nZ, nF         = nii.header['dim'][1], nii.header['dim'][2], nii.header['dim'][3], 1
            dimX, dimY, dimZ, dimT = nii.header['pixdim'][1], nii.header['pixdim'][2], nii.header['pixdim'][3], nii.header['pixdim'][4]

        if nii.header['dim'][0] == 4:
            nX, nY, nZ, nF         = nii.header['dim'][1], nii.header['dim'][2], nii.header['dim'][3], nii.header['dim'][4]
            dimX, dimY, dimZ, dimT = nii.header['pixdim'][1], nii.header['pixdim'][2], nii.header['pixdim'][3], nii.header['pixdim'][4]

        # number of instances
        nInstances = nZ*nF

        # slice location arrays
        sliceIndices = np.repeat(range(1, nZ+1), nF)

        # slice locations array
        voxelSpacing = dimZ
        zLocLast = (voxelSpacing * nZ) - voxelSpacing
        sliceLoca = np.repeat( np.linspace(0, zLocLast, num=nZ), nF)

        # TODO: windowing
        # windowCenter = []
        # windowWidth = []
        # rescaleIntercept = []
        # rescaleSlope = []

        # nii parameters to transfer to dicom
        nii_parameters = []
        for iInstance in range(0,nInstances):
            nii_parameters.append({
                'SliceThickness': str(dimZ),
                'SpacingBetweenSlices': str(dimZ),
                'AcquisitionMatrix': [0, nX, nY, 0],
                'InstanceNumber': sliceIndices[iInstance],
                'SliceLocation': sliceLoca[iInstance],
                'Rows': nX,
                'Columns': nY,
                'NumberOfSlices': nZ,
                'PixelSpacing': [dimX, dimY],
                'WindowCenter': str(1000),
                'WindowWidth': str(1800),
                'RescaleIntercept': str(0),
                'RescaleSlope': str(21),
            })

        return nii_parameters
        