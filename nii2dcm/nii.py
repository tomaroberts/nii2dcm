"""
Classes for manipulating NIfTI files

Tom Roberts

Updates by Bryan Luna with explicit NIfTI RAS → DICOM LPS for DICOM geometry consistency.
"""

import numpy as np


class Nifti:

    def get_nii2dcm_parameters(nib_nii):
        """
        Get general NIfTI header parameters relevant for DICOM tag transferal.
        Assumes NIfTI RAS orientation after canonicalization in run.py
        :nib_nii - NIfTI loaded with nibabel
        :nii_parameters - parameters to transfer to DICOM header
        """

        # NIfTI RAS --> DICOM LPS helper
        def ras_to_lps(v3):
            """Convert a 3-vector from RAS to LPS patient space.
            NIfTI uses RAS+ (R, A, S); DICOM uses LPS+ (L, P, S).
            """
            return np.array([-v3[0], -v3[1], v3[2]], dtype=float)
        
        # ---------------------------
        # Load NIfTI - RAS orientation after canonicalization in run.py
        # ---------------------------

        nii_img = nib_nii.get_fdata()

        # ---------------------------
        # Dimensions & Voxel Spacing
        # ---------------------------

        nii_hdr = nib_nii.header
        dim = nii_hdr['dim']
        pixdim = nii_hdr['pixdim']

        # NIfTI volume dimensions (I/J/K)
        # dim[1] = nI (rows), dim[2] = nJ (columns), dim[3] = nK (slices)
        # pixdim[1] = dI, pixdim[2] = dJ, pixdim[3] = dK (mm)
        if dim[4] == 1:
            # 3D volume
            nI, nJ, nK, nF = dim[1], dim[2], dim[3], 1
            dimI, dimJ, dimK = pixdim[1], pixdim[2], pixdim[3]

        elif dim[0] == 3 and all([x > 1 for x in dim[1:4]]):
            nI, nJ, nK, nF = (dim[1:4].tolist() + [1])
            dimI, dimJ, dimK = pixdim[1:4].tolist()

        else:
            raise ValueError("Error: NIfTI is not 3-dimensional.")
        
        # DICOM volume dimensions (X/Y/Z)
        # DICOM rows (X) = NIfTI rows (I)
        # DICOM columns (Y) = NIfTI columns (J)
        # DICOM slices = NIfTI slices (Z)
        rows = nI
        cols = nJ
        row_spacing = dimI
        col_spacing = dimJ

        # Instances & Slice Spacing
        nInstances = nK*nF
        sliceIndices = np.repeat(range(1, nK+1), nF)
        voxelSpacing = dimK
        zLocLast = (voxelSpacing * nK) - voxelSpacing
        sliceLoca = np.repeat(np.linspace(0, zLocLast, num=nK), nF)

        # -----------------------------
        # Windowing & Signal Intensity
        # -----------------------------

        maxI = np.amax(nii_img)
        minI = np.amin(nii_img)
        windowCenter = round((maxI - minI) / 2)
        windowWidth = round(maxI - minI)
        rescaleIntercept = 0
        rescaleSlope = 1

        # NIfTI FOV
        fovI = nI * dimI
        fovJ = nJ * dimJ
        fovK = nK * dimK

        # ---------------------------
        # ImageOrientationPatient
        # ---------------------------

        # NIfTI affine in RAS
        # RAS = A_ras @ [i, j, k, 1]
        A_ras = nib_nii.affine

        # NIfTI direction cosines in RAS normalized by voxel size
        # 1st column (I) is rows; 2nd column (J) is columns
        dircosI_ras =  A_ras[:3, 0] / dimI
        dircosJ_ras =  A_ras[:3, 1] / dimJ

        # convert RAS cosines to LPS cosines
        dircosI_lps = ras_to_lps(dircosI_ras)
        dircosJ_lps = ras_to_lps(dircosJ_ras)

        # normalize to be safe (should already be unit length)
        dircosI_lps = dircosI_lps / np.linalg.norm(dircosI_lps)
        dircosJ_lps = dircosJ_lps / np.linalg.norm(dircosJ_lps)

        # DICOM rows are NIfTI I axis, DICOM columns are NIfTI J axis
        dcm_rows = dircosJ_lps
        dcm_columns = dircosI_lps

        # ImageOrientationPatient
        # row value for x, y, z (respectively) followed by column value for x, y, z (respectively)
        # https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html
        image_orientation_patient = [
            float(dcm_rows[0]), float(dcm_rows[1]), float(dcm_rows[2]),
            float(dcm_columns[0]), float(dcm_columns[1]), float(dcm_columns[2]),
        ]

        # ---------------------------
        # ImagePositionPatient
        # ---------------------------

        image_pos_patient_array = []
        slice_ipps_lps = []

        # precompute IPPs for each slice k
        for k in range(nK):
            ijk = np.array([0, 0, k, 1], dtype=float)
            ras = A_ras.dot(ijk)[:3]
            lps = ras_to_lps(ras)
            slice_ipps_lps.append(lps)

        # if nF > 1, repeat IPPs for each frame
        for k in range(nK):
            for f in range(nF):
                image_pos_patient_array.append([
                    float(slice_ipps_lps[k][0]),
                    float(slice_ipps_lps[k][1]),
                    float(slice_ipps_lps[k][2]),
                ])

        # ---------------------------
        # Output Dictionary
        # ---------------------------

        nii2dcm_parameters = {
            # series parameters
            'dimX': dimI,
            'dimY': dimJ,
            'SliceThickness': str(dimK),
            'SpacingBetweenSlices': str(dimK),
            'AcquisitionMatrix': [0, rows, cols, 0],
            'Rows': rows,
            'Columns': cols,
            'NumberOfSlices': nK,
            'NumberOfInstances': nInstances,
            'PixelSpacing': [row_spacing, col_spacing],
            'FOV': [fovI, fovJ, fovK],
            'SmallestImagePixelValue': minI,
            'LargestImagePixelValue': maxI,
            'WindowCenter': str(windowCenter),
            'WindowWidth': str(windowWidth),
            'RescaleIntercept': str(rescaleIntercept),
            'RescaleSlope': str(rescaleSlope),
            'SpacingBetweenSlices': round(float(dimK), 2),
            'ImageOrientationPatient': image_orientation_patient,
            # instance parameters
            'InstanceNumber': sliceIndices,
            'SliceLocation': sliceLoca,
            'ImagePositionPatient': image_pos_patient_array

        }

        return nii2dcm_parameters
