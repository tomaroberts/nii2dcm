from setuptools import setup, find_packages
from pathlib import Path


# import README.md for long_description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="nii2dcm",
    version="0.1.1",
    description='nii2dcm: NIfTI to DICOM creation with Python',
    author='Tom Roberts',
    url='https://github.com/tomaroberts/nii2dcm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['nii2dcm', 'nii2dcm.*']),
    install_requires=[
        'numpy',
        'matplotlib',
        'nibabel',
        'pydicom'
    ],
    setup_requires=['flake8'],
    entry_points={
        "console_scripts": [
            "nii2dcm = nii2dcm.__main__:cli"
        ]
    },
)