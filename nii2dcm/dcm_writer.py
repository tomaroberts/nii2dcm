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

    output_filename = r'IM_%04d' % (instance_index + 1)  # begin filename from 1, e.g. IM_0001

    img_slice = img_data[:, :, instance_index]

    # Instance UID – unique to current slice
    dcm.ds.SOPInstanceUID = pyd.uid.generate_uid(None)

    # write pixel data
    dcm.ds.PixelData = img_slice.tobytes()

    # write DICOM file
    dcm.ds.save_as( os.path.join( output_dir, output_filename ), write_like_original=False )


def transfer_nii_hdr_series_tags(dcm, nii2dcm_parameters):
    """
    Transfer NIfTI header parameters applicable across Series

    dcm – nii2dcm DICOM object
    nii2dcm_parameters - parameters from NIfTI file
    """

    dcm.ds.Rows = nii2dcm_parameters['Rows']
    dcm.ds.Columns = nii2dcm_parameters['Columns']
    dcm.ds.PixelSpacing = [round(float(nii2dcm_parameters['dimX']),2), round(float(nii2dcm_parameters['dimY']),2)]
    dcm.ds.SliceThickness = nii2dcm_parameters['SliceThickness']
    dcm.ds.SpacingBetweenSlices = round(float(nii2dcm_parameters['SpacingBetweenSlices']),2)
    dcm.ds.ImageOrientationPatient = nii2dcm_parameters['ImageOrientationPatient']
    # dcm.ds.AcquisitionMatrix = nii2dcm_parameters['AcquisitionMatrix']
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
    # SOPInstanceUID
    # InstanceNumber
    # ImagePositionPatient

    dcm.ds.InstanceNumber = nii2dcm_parameters['InstanceNumber'][instance_index]
    dcm.ds.SliceLocation = nii2dcm_parameters['SliceLocation'][instance_index]
    dcm.ds.ImagePositionPatient = [
        str(nii2dcm_parameters['ImagePositionPatient'][instance_index][0]),
        str(nii2dcm_parameters['ImagePositionPatient'][instance_index][1]),
        str(nii2dcm_parameters['ImagePositionPatient'][instance_index][2]),
    ]


# nii_parameters = get_nii_parameters( niiIn ); nInstances = nii_parameters['InstanceNumber'].size
#
# # uid_instance_creator   = pyd.uid.generate_uid(None) # think can transfer
# uid_series_instance    = pyd.uid.generate_uid(None) # per svr
# uid_frame_of_reference = pyd.uid.generate_uid(None) # per svr
#
# iFileCtr = 1
#
# for iInstance in range(0,nInstances):
#
#     uid_instance   = pyd.uid.generate_uid(None) # per slice
#     nii_parameters = get_nii_parameters( niiIn )
#
#     # override
#     nii_parameters['InstanceNumber'] = nii_parameters['InstanceNumber'][iInstance]
#     nii_parameters['SliceLocation'] = round(nii_parameters['SliceLocation'][iInstance], 2)
#
#     # initialise header elements
#     elements_to_define_meta, elements_to_transfer_meta, elements_to_define_ds, elements_to_transfer_ds, non_std_elements_to_define_ds = elem_initialise(uid_instance, uid_series_instance, uid_frame_of_reference, nii_parameters)
#
#     # file_meta
#     file_meta = Dataset()
#
#     for k, v in elements_to_define_meta.items():
#         setattr(file_meta, k, v)
#
#     for k, v in elements_to_transfer_meta.items():
#         try:
#             setattr(file_meta, k, getattr(dcmIn.file_meta, v))
#         except:
#             print(f"Could not transfer tag for keyword {k}")
#
#     # dataset
#     ds = Dataset()
#     ds.file_meta = file_meta
#     ds.is_implicit_VR = False
#     ds.is_little_endian = True
#
#     for k, v in elements_to_define_ds.items():
#         setattr(ds, k, v)
#
#     for k, v in elements_to_transfer_ds.items():
#         try:
#             setattr(ds, k, getattr(dcmIn, v))
#         except:
#             print(f"Could not transfer tag for keyword {k}")
#
#     for k, v in non_std_elements_to_define_ds.items():
#         setattr(ds, k, v)
#
#     # override elements
#     setattr(ds, 'SeriesNumber', str(int(str(getattr(dcmIn, 'SeriesNumber'))) + 1) ) # +1 to SeriesNumber
#     setattr(ds, 'AcquisitionNumber', str(getattr(dcmIn, 'SeriesNumber'))[:-2])
#     # setattr(ds, 'InstanceCreationDate', str(today_date) )
#     # setattr(ds, 'InstanceCreationTime', str(today_time) )
#     # setattr(ds, 'SeriesDate', str(today_date) )
#     # setattr(ds, 'ContentDate', str(today_date) )
#     # setattr(ds, 'SeriesTime', str(today_time) )
#     # setattr(ds, 'ContentTime', str(today_time + 1) )
#     setattr(ds, 'NumberOfSlicesMR', nInstances )
#     setattr(ds, 'SliceNumberMR', nii_parameters['InstanceNumber'] )
#
#     # Update Geometry
#     dcm_make_geometry_tags(ds, niiIn, iInstance+1)
#
#     # Add Stack Sequence to dataset
#     create_seq_stack()
#
#     # Overrides for Matthew
#     # setattr(ds, 'ImagePositionPatient', [str(49.5),str(-61.5694439709180),str(61.5694439709187)] )
#     # setattr(ds, 'ImageOrientationPatient', ['0','1','0','0','0','-1'] )
#
#     # create dicom
#     ds.PixelData = nii_img[:,:,iInstance].tobytes()
#     ds.save_as( os.path.join( dcmOutPath, r'IM_%04d'%(iFileCtr) ), write_like_original=False )
#     iFileCtr = iFileCtr + 1
#
#     del ds, file_meta, elements_to_define_meta, elements_to_transfer_meta, elements_to_define_ds, elements_to_transfer_ds, non_std_elements_to_define_ds
#