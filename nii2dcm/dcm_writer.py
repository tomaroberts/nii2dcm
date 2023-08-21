"""
creates a DICOM Series
"""

import os
import pydicom as pyd


def write_slice(dcm, img_data, instance_index, output_dir):
    """
    write a single DICOM slice

    dcm – nii2dcm DICOM object
    img_data - [nX, nY, nSlice] image pixel data, such as from NIfTI file
    instance_index – instance index (important: counts from 0)
    output_dir – output DICOM file save location
    """

    output_filename = r'IM_%04d.dcm' % (instance_index + 1)  # begin filename from 1, e.g. IM_0001.dcm

    img_slice = img_data[:, :, instance_index]

    # Instance UID – unique to current slice
    dcm.ds.SOPInstanceUID = pyd.uid.generate_uid(None)

    # write pixel data
    dcm.ds.PixelData = img_slice.tobytes()

    # write DICOM file
    dcm.ds.save_as(os.path.join(output_dir, output_filename), write_like_original=False)


def transfer_nii_hdr_series_tags(dcm, nii2dcm_parameters):
    """
    Transfer NIfTI header parameters applicable across Series

    dcm – nii2dcm DICOM object
    nii2dcm_parameters - parameters from NIfTI file
    """

    dcm.ds.Rows = nii2dcm_parameters['Rows']
    dcm.ds.Columns = nii2dcm_parameters['Columns']
    dcm.ds.PixelSpacing = [round(float(nii2dcm_parameters['dimX']), 2), round(float(nii2dcm_parameters['dimY']), 2)]
    dcm.ds.SliceThickness = nii2dcm_parameters['SliceThickness']
    dcm.ds.SpacingBetweenSlices = round(float(nii2dcm_parameters['SpacingBetweenSlices']), 2)
    dcm.ds.ImageOrientationPatient = nii2dcm_parameters['ImageOrientationPatient']
    dcm.ds.AcquisitionMatrix = nii2dcm_parameters['AcquisitionMatrix']
    dcm.ds.SmallestImagePixelValue = int(nii2dcm_parameters['SmallestImagePixelValue']) \
        if int(nii2dcm_parameters['SmallestImagePixelValue']) > 0 else 0  # SmallestImagePixelValue must be >= 0
    dcm.ds.LargestImagePixelValue = int(nii2dcm_parameters['LargestImagePixelValue'])
    dcm.ds.WindowCenter = nii2dcm_parameters['WindowCenter']
    dcm.ds.WindowWidth = nii2dcm_parameters['WindowWidth']
    dcm.ds.RescaleIntercept = nii2dcm_parameters['RescaleIntercept']
    dcm.ds.RescaleSlope = nii2dcm_parameters['RescaleSlope']


def transfer_nii_hdr_instance_tags(dcm, nii2dcm_parameters, instance_index):
    """
    Transfer NIfTI header parameters applicable to Instance

    dcm – nii2dcm DICOM object
    nii2dcm_parameters - parameters from NIfTI file
    instance_index - slice number in NIfTI file
    """

    # Possible per Instance Tags
    # SOPInstanceUID (set within write_slice function)
    # InstanceNumber
    # SliceLocation
    # ImagePositionPatient

    dcm.ds.InstanceNumber = nii2dcm_parameters['InstanceNumber'][instance_index]
    dcm.ds.SliceLocation = nii2dcm_parameters['SliceLocation'][instance_index]
    dcm.ds.ImagePositionPatient = [
        str(nii2dcm_parameters['ImagePositionPatient'][instance_index][0]),
        str(nii2dcm_parameters['ImagePositionPatient'][instance_index][1]),
        str(nii2dcm_parameters['ImagePositionPatient'][instance_index][2]),
    ]


def transfer_ref_dicom_series_tags(dcm, ref_dcm):
    """
    Transfer Series level DICOM Attributes from reference DICOM to nii2dcm DICOM

    dcm – nii2dcm DICOM object
    ref_dcm - reference DICOM object
    """

    for current_attribute in dcm.attributes_to_transfer:
        try:
            attribute_value = getattr(ref_dcm, current_attribute)
            setattr(dcm.ds, current_attribute, attribute_value)
        except AttributeError as e:
            # TODO once logger implemented, replace print statement with log warning
            print(f'Warning: ref_dicom {e} therefore could not transfer')
