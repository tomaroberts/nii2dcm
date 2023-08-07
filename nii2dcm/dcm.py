"""
Classes for creating a DICOM from scratch

Tom Roberts
"""

import datetime
import os
import pydicom as pyd
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.datadict import DicomDictionary, keyword_dict

from nii2dcm.modules import (
    patient,
    general_study,
    patient_study,
    general_series,
    frame_of_reference,
    general_equipment,
    general_acquisition,
    general_image,
    general_reference,
    image_plane,
    image_pixel,
    mr_image,
    voi_lut,
    sop_common,
    common_instance_reference,
)

nii2dcm_temp_filename = 'nii2dcm_tempfile.dcm'


class Dicom:
    """
    Creates basic DICOM structure

    Assumptions:
    - is_implicit_VR = False
    - is_little_endian = True
    - ImageOrientationPatient hard-coded

    """

    def __init__(self, filename=nii2dcm_temp_filename):

        self.filename = filename

        self.dcm_dictionary_update()

        # Instantiates minimal Pydicom FileMetaDataset object
        self.file_meta = FileMetaDataset()
        self.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'  # Explicit VR Little Endian
        self.file_meta.ImplementationVersionName = 'nii2dcm_DICOM'

        # Instantiates minimal DataSet object
        self.ds = FileDataset(filename, {}, file_meta=self.file_meta, preamble=b"\0" * 128)
        self.ds.is_implicit_VR = False
        self.ds.is_little_endian = True
        self.ds.ImageType = ['DERIVED', 'SECONDARY']

        """
        Create Composite IOD by adding Modules to Dicom object
        """
        # TODO
        #  - modules below are from MR Image IOD Module Table (A.4.3)
        #  - some are probably irrelevant to say, CT Image CIOD, therefore all/most of these should be shifted to
        #  DicomMRI subclass
        #  - equivalent list of add_module() calls should be created for CT, SC, US, etc.
        patient.add_module(self)
        general_study.add_module(self)
        patient_study.add_module(self)
        general_series.add_module(self)
        frame_of_reference.add_module(self)
        general_equipment.add_module(self)
        general_acquisition.add_module(self)

        general_image.add_module(self)
        general_reference.add_module(self)
        image_plane.add_module(self)
        image_pixel.add_module(self)
        voi_lut.add_module(self)
        sop_common.add_module(self)
        common_instance_reference.add_module(self)

        """
        Set Dicom Date/Time
        Important: doing this once sets all Instances/Series/Study creation dates and times to the same values. Whereas, 
        doing this within the Modules would every so slightly offset the times
        """
        # TODO shift to utils.py and propagate to Modules, or, create method within this Dicom class
        dt = datetime.datetime.now()
        dateStr = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds

        self.ds.ContentDate = dateStr
        self.ds.ContentTime = timeStr
        self.ds.StudyDate = dateStr
        self.ds.StudyTime = timeStr
        self.ds.SeriesDate = dateStr
        self.ds.SeriesTime = timeStr
        self.ds.AcquisitionDate = dateStr
        self.ds.AcquisitionTime = timeStr
        self.ds.InstanceCreationDate = dateStr
        self.ds.InstanceCreationTime = timeStr

        """
        Set some default Attribute values
        """
        # TODO
        #  - decide if this is the best way to implement setting default values of important Attributes
        #  - probably makes more sense to hard-code these in subclasses, e.g. DicomMRI, DicomCT, etc, so that they are
        #  not hard-coded across different imaging modalities, where some might be irrelevant

        # ImageOrientationPatient
        # hard-coded, probably better way to define based on NIfTI values
        self.ds.ImageOrientationPatient = ['1', '0', '0', '0', '1', '0']

        # Display Attributes
        # NB: RescaleIntercept and RescaleSlope do NOT appear to be in MR Image Module, but are in CT Image, Secondary
        # Capture and Enhanced MR Modules, hence for MRI must define in this class or within DicomMRI class
        self.ds.RescaleIntercept = ''
        self.ds.RescaleSlope = ''
        self.ds.WindowCenter = ''
        self.ds.WindowWidth = ''

        # per Instance Attributes
        # initialised with hard-coded value below, but overwritten with transfer_nii_hdr_instance_tags()
        self.ds.ImagePositionPatient = ['0', '0', '0']

        self.init_study_tags()
        self.init_series_tags()

    def get_file_meta(self):
        return self.file_meta

    def get_dataset(self):
        return self.ds

    def save_as(self):
        print("Writing DICOM to", os.path.join(os.getcwd(), self.filename))
        self.ds.save_as(self.filename)

    def init_study_tags(self):
        """
        Create Study Tags
        - these tags are fixed across Instances and Series
        """

        # Possible per Study Tags
        # StudyInstanceUID

        self.ds.StudyInstanceUID = pyd.uid.generate_uid(None)

    def init_series_tags(self):
        """
        Create Series Tags
        - these tags are fixed across Instances
        """

        # Possible per Series Tags
        # SeriesInstanceUID
        # FrameOfReferenceUID
        # SeriesDate
        # SeriesTime
        # AcquisitionDate
        # AcquisitionTime
        # SeriesNumber

        self.ds.SeriesInstanceUID = pyd.uid.generate_uid(None)
        self.ds.FrameOfReferenceUID = pyd.uid.generate_uid(None)
        self.ds.SeriesNumber = ''
        self.ds.AcquisitionNumber = ''  # Innolitics says this is in General Image Module, but NEMA says it is not...

    # TODO move this function to new utils file
    def dcm_dictionary_update(self):
        """
        Update Pydicom DicomDictionary object with non-standard Private tags. Note: these tags are not added to the
        instantiated nii2dcm Dicom object; the DicomDictionary object is just updated meaning that these tags are now
        available to be written if the user desires.

        Tuple definitions: (VR, VM, description, is_retired flag, keyword)

        See: https://pydicom.github.io/pydicom/stable/auto_examples/metadata_processing/plot_add_dict_entries.html
        """

        new_dict_items = {
            0x20011002: ('IS', '1', "Chemical Shift Number MR", '', 'ChemicalShiftNumberMR'),
            0x20011008: ('IS', '1', "Phase Number", '', 'PhaseNumber'),
            0x2001100a: ('IS', '1', "Slice Number MR", '', 'SliceNumberMR'),
            0x2001100b: ('CS', '1', "Slice Orientation", '', 'SliceOrientation'),
            0x20011014: ('SL', '1', "Number Of Echoes", '', 'NumberOfEchoes'),
            0x20011015: ('SS', '1', "Number Of Locations", '', 'NumberOfLocations'),
            0x20011016: ('SS', '1', "Number Of PC Directions", '', 'NumberOfPCDirections'),
            0x20011017: ('SL', '1', "Number Of Phases MR", '', 'NumberOfPhasesMR'),
            0x20011018: ('SL', '1', "Number Of Slices MR", '', 'NumberOfSlicesMR'),
            0x20011020: ('LO', '1', "Scanning Technique", '', 'ScanningTechnique'),
            0x20011025: ('SH', '1', "Echo Time Display MR", '', 'EchoTimeDisplayMR'),
            0x20011060: ('SL', '1', "Number Of Stacks", '', 'NumberOfStacks'),
            0x20011063: ('CS', '1', "Examination Source", '', 'ExaminationSource'),
            # 0x2001107b: ('IS', '1', "Acquisition Number", '', 'AcquisitionNumber'), # Philips Private alternative
            0x20011081: ('IS', '1', "Number Of Dynamic Scans", '', 'NumberOfDynamicScans'),
            0x2001101a: ('FL', '3', "PC Velocity", '', 'PCVelocity'),
            0x2001101d: ('IS', '1', "Reconstruction Number MR", '', 'ReconstructionNumberMR'),
            0x20051035: ('CS', '1', '', '', 'unknowntag20051035'),
            # PIXEL --- this seems to also correspond to MRSeriesDataType?
            0x20051011: ('CS', '1', 'MR Image Type', '', 'MRImageType'),
            0x2005106e: ('CS', '1', 'MR Scan Sequence', '', 'MRScanSequence'),

            # Philips "Stack" Tags
            0x2001105f: ('SQ', '1', 'Stack', '', 'Stack'),
            0x20010010: ('LO', '1', "Private Creator", '', 'PrivateCreator20010010'),
            0x2001102d: ('SS', '1', 'StackNumberOfSlices', '', 'StackNumberOfSlices'),
            0x20011032: ('FL', '1', 'StackRadialAngle', '', 'StackRadialAngle'),
            0x20011033: ('CS', '1', 'StackRadialAxis', '', 'StackRadialAxis'),
            0x20011035: ('SS', '1', 'MRSeriesDataType', '', 'MRSeriesDataType'),  # SS - StackSliceNumber ?
            0x20011036: ('CS', '1', 'StackType', '', 'StackType'),
            0x20050010: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050010'),
            # Is this duplicate necessary with entry above?
            0x20050011: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050011'),
            0x20050012: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050012'),
            0x20050013: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050013'),
            0x20050014: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050014'),
            0x20050015: ('LO', '1', 'Private Creator', '', 'PrivateCreator20050015'),
            0x20051071: ('FL', '1', 'MRStackAngulationAP', '', 'MRStackAngulationAP'),
            0x20051072: ('FL', '1', 'MRStackAngulationFH', '', 'MRStackAngulationFH'),
            0x20051073: ('FL', '1', 'MRStackAngulationRL', '', 'MRStackAngulationRL'),
            0x20051074: ('FL', '1', 'MRStackFovAP', '', 'MRStackFovAP'),
            0x20051075: ('FL', '1', 'MRStackFovFH', '', 'MRStackFovFH'),
            0x20051076: ('FL', '1', 'MRStackFovRL', '', 'MRStackFovRL'),
            0x20051078: ('FL', '1', 'MRStackOffcentreAP', '', 'MRStackOffcentreAP'),
            0x20051079: ('FL', '1', 'MRStackOffcentreFH', '', 'MRStackOffcentreFH'),
            0x2005107a: ('FL', '1', 'MRStackOffcentreRL', '', 'MRStackOffcentreRL'),
            0x2005107b: ('CS', '1', 'MRStackPreparationDirection', '', 'MRStackPreparationDirection'),
            0x2005107e: ('FL', '1', 'MRStackSliceDistance', '', 'MRStackSliceDistance'),
            0x20051081: ('CS', '1', 'MRStackViewAxis', '', 'MRStackViewAxis'),
            0x2005143c: ('FL', '1', 'MRStackTablePosLong', '', 'MRStackTablePosLong'),
            0x2005143d: ('FL', '1', 'MRStackTablePosLat', '', 'MRStackTablePosLat'),
            0x2005143e: ('FL', '1', 'MRStackPosteriorCoilPos', '', 'MRStackPosteriorCoilPos'),
            0x20051567: ('IS', '1', 'MRPhilipsX1', '', 'MRPhilipsX1'),

            # Phase Contrast/Velocity Tags
            0x00089209: ('CS', '1', "Acquisition Contrast", '', 'AcquisitionContrast'),
            0x00189014: ('CS', '1', "Phase Contrast", '', 'PhaseContrast'),
            0x00189090: ('FD', '3', "Velocity Encoding Direction", '', 'VelocityEncodingDirection'),
            0x00189091: ('FD', '1', "Velocity Encoding Minimum Value", '', 'VelocityEncodingMinimumValue'),
        }

        # Update the dictionary itself
        DicomDictionary.update(new_dict_items)

        # Update the reverse mapping from name to tag
        new_names_dict = dict([(val[4], tag) for tag, val in new_dict_items.items()])
        keyword_dict.update(new_names_dict)


class DicomMRI(Dicom):
    """
    DicomMRI subclass adds MR Image Module to Dicom object
    """

    def __init__(self, filename=nii2dcm_temp_filename):
        super().__init__(filename)

        """
        Set DICOM attributes which are located outside of the MR Image Module to MR-specific values 
        """
        self.ds.Modality = 'MR'

        # MR Image Storage SOP Class
        # UID = 1.2.840.10008.5.1.4.1.1.4
        # https://dicom.nema.org/dicom/2013/output/chtml/part04/sect_I.4.html
        self.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        self.ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.4'

        """
        Add MR Image Module to Dicom object
        """
        mr_image.add_module(self)


