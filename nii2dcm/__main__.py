"""
nii2dcm entrypoint code and command line interface (CLI)
"""

import sys
import argparse
from pathlib import Path
from nii2dcm.run import run_nii2dcm


def cli(args=None):
    """
    Run nii2dcm via command line
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="nii2dcm",
        description="nii2dcm - NIfTI file to DICOM conversion"
    )

    parser.add_argument("input_file", type=str, help="[.nii/.nii.gz] input NIfTI file")
    parser.add_argument("output_dir", type=str, help="[directory] output DICOM path")
    parser.add_argument("-d", "--dicom_type", type=str, help="[string] type of DICOM. e.g. MR, CT, US, XR, etc.")
    parser.add_argument("-r", "--ref_dicom", type=str, help="[.dcm] Reference DICOM file for Attribute transfer")
    parser.add_argument("-v", "--version", action="version", version="0.1.0")

    args = parser.parse_args()

    input_file = Path(args.input_file)  # TODO: add check that file is .nii/.nii.gz
    output_dir = Path(args.output_dir)  # TODO: add check that this is directory
    ref_dicom_file = Path(args.ref_dicom)   # TODO: add check that file is DICOM

    if not input_file.exists():
        print(f"Input file '{input_file}' not found")
        raise SystemExit(1)

    if not output_dir.exists():
        print(f"Output directory '{output_dir}' does not exist")
        raise SystemExit(1)

    if not ref_dicom_file.exists():
        print(f"Reference DICOM file '{ref_dicom}' not found.")
        raise SystemExit(1)

    # execute nii2dcm
    run_nii2dcm(
        input_file,
        output_dir,
        args.dicom_type,
        ref_dicom_file
    )


if __name__ == "__main__":
    sys.exit(cli())
