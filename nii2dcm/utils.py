"""
Utility functions for nii2dcm
"""

# TODO(tomaroberts) create DicomDict class/functions which enable user to add custom attributes to nii2dcm Dicom
#  subclasses. Code below is currently non-functioning, but retained as reminder for future development.

from typing import Dict
from pydicom.datadict import DicomDictionary, keyword_dict


def dcm_dictionary_update(new_dict_items: Dict):
    """
    Update Pydicom DicomDictionary object with non-standard Private tags. Note: these tags are not added to the
    instantiated nii2dcm Dicom object; the DicomDictionary object is just updated meaning that these tags are now
    available to be written if the user desires.

    Tuple definitions: (VR, VM, description, is_retired flag, keyword)

    See: https://pydicom.github.io/pydicom/stable/auto_examples/metadata_processing/plot_add_dict_entries.html
    """

    # TODO temporary pass – implement functionality and remove later
    pass

    # Update the dictionary itself
    DicomDictionary.update(new_dict_items)

    # Update the reverse mapping from name to tag
    new_names_dict = dict([(val[4], tag) for tag, val in new_dict_items.items()])
    keyword_dict.update(new_names_dict)


# Example dictionary
# Supply as: dcm_dictionary_update(new_dict_items_PRIDESVR)
new_dict_items_PRIDESVR = {
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
