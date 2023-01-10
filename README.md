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

[DICOM](https://www.dicomstandard.org/) is the international standard used to store and display medical images in 
clinical institutions. It is a vast and complicated standard. The 
[NIfTI](https://brainder.org/2012/09/23/the-nifti-file-format/) file format is widely used within medical imaging 
research because it is a comparatively simple data format, generally stripped of identifiable patient data and with far 
fewer metadata fields.

Researchers often convert DICOM files to NIfTI files using tools such as 
[dcm2niix](https://github.com/rordenlab/dcm2niix/). However, the reverse process is much harder.

**nii2dcm** is designed to convert a NIfTI file (.nii/.nii.gz) into a single-frame DICOM Series in one line, e.g.:

```sh
nii2dcm nifti-file.nii.gz dicom-output-directory
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To install and run nii2dcm locally follow these steps.

### Prerequisites

* Python (tested with v3.9)


### Installation

Setup a Python virtual environment (recommended)
   ```sh
   python -m venv nii2dcm-venv
   source nii2dcm-venv/bin/activate
   ```
Install nii2dcm
   ```sh
   pip install nii2dcm
   ```

Verify installation by displaying nii2dcm help information
   ```sh
   nii2dcm -h
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

nii2dcm is designed to be pointed at a single `.nii` or `.nii.gz` and generate a single-frame DICOM dataset:

```sh
nii2dcm nifti-file.nii.gz dicom-output-directory
```

Currently, nii2dcm provides three Python classes in order to build different DICOM types. These are:
* **Dicom** – generic DICOM class
* **DicomMRI** – MRI DICOM class
* **DicomMRISVR** – 3D [SVR](https://svrtk.github.io/) MRI DICOM class

The created DICOM type can be specified with the `-d` or `--dicom-type` flag. For example, the following will output a 
3D MRI SVR DICOM dataset
```sh
nii2dcm SVR-output.nii.gz path/to/output/dir/ -d SVR
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

This project is in its infancy! Expect :bug::ant::beetle:

There are many things I would like to test and implement. 
[Raise an Issue](https://github.com/tomaroberts/nii2dcm/issues) if you have ideas or suggestions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [SVRTK @ KCL](https://svrtk.github.io/) - the original motivation for this project
* [Chris Rorden for dcm2niix](https://github.com/rordenlab/dcm2niix/) - inspiration for the reverse process
* [NHS Topol Digital Fellowships scheme](https://topol.hee.nhs.uk/digital-fellowships/) - for the protected time to work 
on this


<!-- Links -->
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
