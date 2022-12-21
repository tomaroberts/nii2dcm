import sys
import argparse

from pathlib import Path


def run(args=None):
    """
    Run nii2dcm via command line
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()

    parser.add_argument("input_path")
    parser.add_argument("output_path")

    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    if not input_path.exists():
        print(f"The input directory '{input_path}' does not exist")
        raise SystemExit(1)

    if not output_path.exists():
        print(f"The output directory '{output_path}' does not exist")
        raise SystemExit(1)


if __name__ == "__main__":
    sys.exit(run())
