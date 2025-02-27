#!/usr/bin/env python3

"""
nii2dcm entrypoint code and command line interface (CLI)
"""

import argparse
import os
from pathlib import Path
from nii2dcm.run import run_nii2dcm
from nii2dcm.version import VERSION


def main(args=None):
    """
    Run nii2dcm via command line
    """

    parser = argparse.ArgumentParser(
        prog="nii2dcm", description="nii2dcm - NIfTI file to DICOM conversion"
    )

    parser.add_argument(
        "input_file", nargs="+", type=str, help="[.nii/.nii.gz] input NIfTI file"
    )
    parser.add_argument("output_dir", type=str, help="[directory] output DICOM path")
    parser.add_argument(
        "-d",
        "--dicom_type",
        type=str,
        help="[string] type of DICOM. Available types: MR, SVR.",
    )
    parser.add_argument(
        "--study_description", type=str, help="[string] Study Description"
    )
    parser.add_argument(
        "--series_description", nargs="+", type=str, help="[string] Series Description"
    )
    parser.add_argument("--protocol_name", type=str, help="[string] Protocol Name")
    parser.add_argument(
        "-r",
        "--ref_dicom",
        type=str,
        help="[.dcm] Reference DICOM file for Attribute transfer",
    )
    parser.add_argument("-v", "--version", action="version", version=VERSION)

    args = parser.parse_args()
    output_dir = Path(args.output_dir)  # TODO: add check that this is directory

    for f in args.input_file:
        if not f:
            print(f"Input file '{f}' not found")
            raise SystemExit(1)

    if not output_dir.exists():
        os.makedirs(output_dir)

    if args.series_description:
        if len(args.input_file) != len(args.series_description):
            print(
                "Number of input files and series descriptions do not match. Please provide a "
                + "series description for each input file."
            )
            raise SystemExit(1)
    else:
        args.series_description = ["" for _ in range(len(args.input_file))]

    # Coding of optional file checks below is quite verbose
    if args.dicom_type is not None:
        dicom_type = (
            args.dicom_type
        )  # TODO: add check that supplied dicom_type is permitted
    elif args.dicom_type is None:
        dicom_type = None

    if args.ref_dicom is not None:
        ref_dicom_file = Path(args.ref_dicom)  # TODO: add check that file is DICOM
    elif args.ref_dicom is None:
        ref_dicom_file = None

    # execute nii2dcm
    run_nii2dcm(
        args.input_file,
        output_dir,
        dicom_type,
        ref_dicom_file,
        study_description=args.study_description,
        series_description=args.series_description,
        protocol_name=args.protocol_name,
    )


if __name__ == "__main__":
    main()
