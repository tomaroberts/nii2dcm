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

    def get_nii2dcm_general_parameters(nib_nii):
        """
        Get general NIfTI file parameters relevant for DICOM creation.
        :nib_nii - NIfTI loaded with nibabel
        :nii_parameters - parameters to transfer to DICOM header
        """

        nii_img = nib_nii.get_fdata()

        # Dimensions
        if nib_nii.header['dim'][4] == 1:
            nX, nY, nZ, nF = nib_nii.header['dim'][1], nib_nii.header['dim'][2], nib_nii.header['dim'][3], 1
            dimX, dimY, dimZ = nib_nii.header['pixdim'][1], nib_nii.header['pixdim'][2], nib_nii.header['pixdim'][3]

        elif nib_nii.header['dim'][4] > 1:
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

    def get_nii2dcm_geometry_parameters(nib_nii):
        """
        Create DICOM geometry tags from NIfTI affine
        :nib_nii - NIfTI loaded with nibabel
        :sliceIndex - index of slice within Nifti volume
        """

        def convert_nii2dcm_slice_parameters(nib_nii, sliceIndex):
            """
            Convert Nifti geometry parameters to DICOM geometry format
            :nib_nii - NIfTI loaded with nibabel
            :sliceIndex - index of slice within Nifti volume
            """

            def fnT1N(A, N):
                # Subfn: calculate T1N vector
                # A = affine matrix [4x4]
                # N = slice number (counting from 1)
                T1N = A.dot([[0], [0], [N - 1], [1]])
                return T1N

            dimX = nib_nii.header['pixdim'][1]
            dimY = nib_nii.header['pixdim'][2]
            dimZ = nib_nii.header['pixdim'][3]
            dimF = nib_nii.header['pixdim'][4]

            # Direction Cosines & Position Parameters
            # nb: -1 for dir cosines gives consistent orientation between Nifti and DICOM in ITK-Snap
            A = nib_nii.affine
            dircosX = -1 * A[:3, 0] / dimX
            dircosY = -1 * A[:3, 1] / dimY
            T1N = fnT1N(A, sliceIndex)

            dcm_geo_parameters = {
                'SpacingBetweenSlices': round(float(dimZ), 2),
                'ImagePositionPatient': [T1N[0], T1N[1], T1N[2]],

                # nb: consistent orientation between Nifti and DICOM in ITK-Snap
                'ImageOrientationPatient': [dircosY[0], dircosY[1], dircosY[2], dircosX[0], dircosX[1], dircosX[2]]

                # Alternative:
                # 'ImageOrientationPatient': [dircosX[0], dircosX[1], dircosX[2], dircosY[0], dircosY[1], dircosY[2]]
            }

            return dcm_geo_parameters

        nInstances = nib_nii.header['dim'][3] * nib_nii.header['dim'][4]

        nii2dcm_geometry_parameters = []
        for iInstance in range(0, nInstances):
            nii2dcm_geometry_parameters = convert_nii2dcm_slice_parameters(nib_nii, iInstance)

        return nii2dcm_geometry_parameters