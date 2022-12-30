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

1. Setup a Python virtual environment
   ```sh
   python -m venv nii2dcm-venv
   source nii2dcm-venv/bin/activate
   ```
2. Clone this repo
   ```sh
   git clone https://github.com/tomaroberts/nii2dcm.git
   ```
3. Install the Python requirements
   ```sh
   pip install -r requirements.txt
   ```
4. Install nii2dcm
   ```sh
   cd nii2dcm
   python setup.py install
   ```
5. Verify installation by displaying nii2dcm help information
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

Currently, nii2dcm provides three Python classes corresponding to different DICOM types. These are:
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

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- DISCLAIMER -->
## Disclaimer 
The Software has been developed for research purposes only and is not a clinical tool.


<!-- Licence -->
## Licence 

BSD 3-Clause License

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Copyright (c) 2021-2022 Tom Roberts. All rights reserved.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
