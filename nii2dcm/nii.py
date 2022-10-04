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


class Nifti:

    def get_nii2dcm_general_parameters(nii):
        """
        Get general NIfTI file parameters relevant for DICOM creation.
        :nii - NIfTI loaded with nibabel
        :nii_parameters - parameters to transfer to DICOM header
        """

        nii_img = nii.get_fdata()

        # Dimensions
        if nii.header['dim'][4] == 1:
            nX, nY, nZ, nF = nii.header['dim'][1], nii.header['dim'][2], nii.header['dim'][3], 1
            dimX, dimY, dimZ = nii.header['pixdim'][1], nii.header['pixdim'][2], nii.header['pixdim'][3]

        elif nii.header['dim'][4] > 1:
            print("Warning: Nifti is not 3-dimensional.")

        # Instances & Slice Spacing
        nInstances = nZ*nF

        sliceIndices = np.repeat(range(1, nZ+1), nF)

        voxelSpacing = dimZ
        zLocLast = (voxelSpacing * nZ) - voxelSpacing
        sliceLoca = np.repeat( np.linspace(0, zLocLast, num=nZ), nF)

        # Windowing & Signal Intensity
        maxI = np.amax(nii_img)
        minI = np.amin(nii_img)
        windowCenter = round((maxI - minI) / 2)
        windowWidth = round(maxI - minI)
        rescaleIntercept = 0
        rescaleSlope = 1

        # FOV
        fovX = nX * dimX
        fovY = nY * dimY
        fovZ = nZ * dimZ

        nii2dcm_general_parameters = {
            'dimX': dimX,
            'dimY': dimY,
            'SliceThickness': str(dimZ),
            'SpacingBetweenSlices': str(dimZ),
            'AcquisitionMatrix': [0, nX, nY, 0],
            'InstanceNumber': sliceIndices,
            'SliceLocation': sliceLoca,
            'Rows': nX,
            'Columns': nY,
            'NumberOfSlices': nZ,
            'PixelSpacing': [dimX, dimY],
            'FOV': [fovX, fovY, fovZ],
            'WindowCenter': str(windowCenter),
            'WindowWidth': str(windowWidth),
            'RescaleIntercept': str(rescaleIntercept),
            'RescaleSlope': str(rescaleSlope),
        }

        return nii2dcm_general_parameters

