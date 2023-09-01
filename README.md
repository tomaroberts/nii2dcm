<!-- back to top link -->
<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">

<h1 align="center">nii2dcm</h1>

  <p align="center">
    NIfTI to DICOM file creation with Python
    <br />
    <a href="https://github.com/tomaroberts/nii2dcm"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/tomaroberts/nii2dcm">View Repo</a>
    ·
    <a href="https://github.com/tomaroberts/nii2dcm/issues">Report Bug</a>
    ·
    <a href="https://github.com/tomaroberts/nii2dcm/issues">Request Feature</a>
  </p>
</div>


<!-- Overview -->
## Overview

[DICOM](https://www.dicomstandard.org/) is the international standard used to store, transfer and display medical images 
in clinical institutions. It is a vast and complicated standard. The 
[NIfTI](https://brainder.org/2012/09/23/the-nifti-file-format/) file format is widely used within medical imaging 
research because it is a comparatively simple data format, generally stripped of identifiable patient data and with far 
fewer metadata fields.

Researchers often convert DICOM files to NIfTI files using tools such as 
[dcm2niix](https://github.com/rordenlab/dcm2niix/). However, the reverse process is much harder.

**nii2dcm** is designed to convert a NIfTI file (.nii/.nii.gz) into a single-frame DICOM Series in one line, e.g.:

```sh
nii2dcm nifti-file.nii.gz dicom-output-directory/ --dicom-type MR
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Installation -->
## Installation

To install and run nii2dcm locally, you have two options:
- pip
- build from source

### pip

```shell
pip install nii2dcm
```

### build from source

Clone this repo:
```sh
git clone https://github.com/tomaroberts/nii2dcm.git
```

Setup a Python virtual environment (recommended):
```sh
cd nii2dcm/
python -m venv nii2dcm-venv
source nii2dcm-venv/bin/activate
python -m pip install --upgrade pip
```

Install dependencies and nii2dcm:
```sh
pip install setuptools wheel
pip install -r requirements.txt
pip install .
```

Verify installation by displaying nii2dcm help information
```sh
nii2dcm -h
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

nii2dcm is designed to be pointed at a single `.nii` or `.nii.gz` from which it generates a single-frame DICOM dataset. 

It is **recommended** to specify the output DICOM modality using the `-d` or `--dicom-type` flag (see examples below). 
Without this, a generic DICOM is created without complete imaging modality metadata.

### DicomMRI
Create an MRI 2D multi-slice DICOM dataset:
```sh
nii2dcm nifti-file.nii.gz dicom-output-directory/ -d MR
```

### DicomMRISVR
Create an MRI 3D [SVR](https://svrtk.github.io/) DICOM dataset:
```sh
nii2dcm SVR-output.nii.gz dicom-output-directory/ -d SVR
```

### Dicom
Create a generic DICOM dataset:
```sh
nii2dcm nifti-file.nii.gz dicom-output-directory/
```

### Other
Eventually, nii2dcm will be extended to cover other imaging modalities including CT, Ultrasound, X-Ray, etc.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- REFERENCE DICOM -->
## Reference DICOM metadata transferral

There are often situations where it can be useful to transfer information from an existing DICOM Study into a new DICOM 
Series. For example, if you want to store your new DICOM dataset alongside your original DICOM Study.

The `-r` or `--ref-dicom` flag attempts to transfer common DICOM attributes from a reference DICOM file into the 
output DICOM:

```shell
nii2dcm nifti-file.nii.gz dicom-output-directory/ -d MR -r reference-dicom-file.dcm
```

Currently, attributes to transfer are [listed here in the DicomMRI class](https://github.com/tomaroberts/nii2dcm/blob/b03b4aacce25eeb6a00756bdb47365034dced787/nii2dcm/dcm.py#L236).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

This project is in its infancy! Expect bugs :bug: :ant: :beetle:

There are many things I would like to test and implement. 
[Raise an Issue](https://github.com/tomaroberts/nii2dcm/issues) if you have ideas or suggestions.

#### Developer Note
If you would like to create another class of DICOM within nii2dcm, you can use the base 
[DicomMRI](https://github.com/tomaroberts/nii2dcm/blob/b03b4aacce25eeb6a00756bdb47365034dced787/nii2dcm/dcm.py#L201) 
class or the [DicomMRISVR](https://github.com/tomaroberts/nii2dcm/blob/main/nii2dcm/svr.py) class for inspiration. You 
will also need to extend the command line interface to utilise your class, i.e. `--dicom-type CT`.

Please [raise an Issue](https://github.com/tomaroberts/nii2dcm/issues) if you need developer support.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [SVRTK @ KCL](https://svrtk.github.io/) - the original motivation for this project
* [Chris Rorden for dcm2niix](https://github.com/rordenlab/dcm2niix/) - inspiration for the reverse process
* [NHS Topol Digital Fellowships scheme](https://topol.hee.nhs.uk/digital-fellowships/) - for the protected time to work 
on this
* [highdicom](https://github.com/ImagingDataCommons/highdicom) - beautiful and extensive Python library for various 
tasks, including DICOM creation
* [SimpleITK](https://simpleitk.org/) - comprehensive software including DICOM reading and writing

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LINKS -->
## Links
Some useful, free image viewing software:
* [ITK-Snap](http://www.itksnap.org/) - fast, simple interface. Opens NIfTI and DICOM
* [MITK Workbench](https://www.mitk.org/wiki/The_Medical_Imaging_Interaction_Toolkit_(MITK)) - excellent for viewing 
multiple image datasets in the same geometric space. Opens NIfTI and DICOM
* [3D Slicer](https://www.slicer.org/) - comprehensive imaging software
* [Horos](https://horosproject.org/) - similar to a hospital clinical information system

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- DISCLAIMER -->
## Disclaimer 
The Software has been developed for research purposes only and is not a clinical tool.


<!-- Licence -->
## Licence 

[BSD 3-Clause License can be found here](LICENCE)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
