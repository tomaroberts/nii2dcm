# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

PACKAGES = find_packages()

with open("requirements.txt") as f:
    required_dependencies = f.read().splitlines()
    external_dependencies = []
    for dependency in required_dependencies:
        if dependency[0:2] == "-e":
            repo_name = dependency.split("=")[-1]
            repo_url = dependency[3:]
            external_dependencies.append("{} @ {}".format(repo_name, repo_url))
        else:
            external_dependencies.append(dependency)


# Get version and release info, which is all stored in nii2dcm/version.py
ver_file = os.path.join("nii2dcm", "version.py")
with open(ver_file) as f:
    exec(f.read())

opts = dict(
    name=NAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    platforms=PLATFORMS,
    version=VERSION,
    packages=PACKAGES,
    install_requires=external_dependencies,
    scripts=SCRIPTS,
    include_package_data=True,
)


if __name__ == "__main__":
    setup(**opts)
