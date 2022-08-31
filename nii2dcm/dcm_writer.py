"""
creates a DICOM Series
"""

import os


def write_slice(dcm, img_data, index_instance, output_dir):
    """
    write a single DICOM slice

    dcm – nii2dcm DICOM object
    img_data - [nX, nY, nSlice] image pixel data, such as from NIfTI file
    index_instance – slice index
    output_dir – output DICOM file save location
    """

    output_filename = r'IM_%04d' % index_instance

    img_slice = img_data[:, :, index_instance]

    dcm.ds.InstanceNumber = index_instance
    # InstanceUID

    dcm.ds.PixelData = img_slice.tobytes()
    dcm.ds.save_as( os.path.join( output_dir, output_filename ), write_like_original=False )





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