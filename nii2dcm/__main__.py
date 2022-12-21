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
    parser.add_argument("-d", "--dicom_type", type=str, help="type of DICOM. e.g. MR, CT, US, XR, etc.")
    parser.add_argument("-v", "--version", action="version", version="0.1.0")

    args = parser.parse_args()

    input_file = Path(args.input_file)  # TODO: add check that file is .nii/.nii.gz
    output_dir = Path(args.output_dir)

    if not input_file.exists():
        print(f"The input file '{input_file}' does not exist")
        raise SystemExit(1)

    if not output_dir.exists():
        print(f"The output directory '{output_dir}' does not exist")
        raise SystemExit(1)

    # execute nii2dcm
    run_nii2dcm(input_file, output_dir, args.dicom_type)


if __name__ == "__main__":
    sys.exit(cli())
