# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import glob

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = 0  # use '' for first of series, number for 1 and above
_version_extra = ""  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = ".".join(map(str, _ver))

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Scientific/Engineering",
]

# Description should be a one-liner:
description = "nii2dcm - NIfTI file to DICOM conversion."
# Long description will go up on the pypi page
long_description = """
This repository is a fork of the original nii2dcm repository by onset-lab.
The original repository can be found at https://github.com/tomaroberts/nii2dcm/
"""

NAME = "nii2dcm"
MAINTAINER = "Tom Roberts"
MAINTAINER_EMAIL = "t.roberts@kcl.ac.uk"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/onset-lab/nii2dcm"
DOWNLOAD_URL = ""
LICENSE = "BSD 3-Clause License"
AUTHOR = "The developers"
AUTHOR_EMAIL = ""
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
SCRIPTS = glob.glob("scripts/*.py")
