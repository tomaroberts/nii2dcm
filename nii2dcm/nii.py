"""
Classes for manipulating NIfTI files

Tom Roberts
"""

import numpy as np


class Nifti:

    def get_nii2dcm_parameters(nib_nii):
        """
        Get general NIfTI header parameters relevant for DICOM tag transferal.
        :nib_nii - NIfTI loaded with nibabel
        :nii_parameters - parameters to transfer to DICOM header
        """

        def fnT1N(A, N):
            # Subfn: calculate T1N vector
            # A = affine matrix [4x4]
            # N = slice number (counting from 1)
            T1N = A.dot([0, 0, N - 1, 1])
            return T1N

        # load nifti
        nii_img = nib_nii.get_fdata()

        # volume dimensions
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
        sliceLoca = np.repeat(np.linspace(0, zLocLast, num=nZ), nF)

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

        # slice positioning in 3-D space
        # nb: -1 for dir cosines gives consistent orientation between Nifti and DICOM in ITK-Snap
        A = nib_nii.affine
        dircosX = -1 * A[:3, 0] / dimX
        dircosY = -1 * A[:3, 1] / dimY

        image_pos_patient_array = []
        for iInstance in range(0, nInstances):
            T1N = fnT1N(A, iInstance)
            image_pos_patient_array.append([T1N[0], T1N[1], T1N[2]])

        # output dictionary
        nii2dcm_parameters = {

            # series parameters
            'dimX': dimX,
            'dimY': dimY,
            'SliceThickness': str(dimZ),
            'SpacingBetweenSlices': str(dimZ),
            'AcquisitionMatrix': [0, nX, nY, 0],
            'Rows': nX,
            'Columns': nY,
            'NumberOfSlices': nZ,
            'NumberOfInstances': nZ*nF,
            'PixelSpacing': [dimX, dimY],
            'FOV': [fovX, fovY, fovZ],
            'SmallestImagePixelValue': minI,
            'LargestImagePixelValue': maxI,
            'WindowCenter': str(windowCenter),
            'WindowWidth': str(windowWidth),
            'RescaleIntercept': str(rescaleIntercept),
            'RescaleSlope': str(rescaleSlope),
            'SpacingBetweenSlices': round(float(dimZ), 2),
            'ImageOrientationPatient': [dircosY[0], dircosY[1], dircosY[2], dircosX[0], dircosX[1], dircosX[2]],
            # alternative:
            # 'ImageOrientationPatient': [dircosX[0], dircosX[1], dircosX[2], dircosY[0], dircosY[1], dircosY[2]],

            # instance parameters
            'InstanceNumber': sliceIndices,
            'SliceLocation': sliceLoca,
            'ImagePositionPatient': image_pos_patient_array

        }

        return nii2dcm_parameters
