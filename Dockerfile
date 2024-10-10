# Use the official Python image as the base image
FROM scilus/scilus:1.6.0

LABEL maintainer="Onset-Lab"

ENV NII2DCM_REVISION=${NII2DCM_REVISION:-main}

WORKDIR /
RUN apt-get update && apt-get -y install git

# Install nii2dcm
RUN python3 -m pip install --upgrade pip && \
    pip install git+https://github.com/onset-lab/nii2dcm.git@${NII2DCM_REVISION} && \
    apt-get -y remove git && \
    apt-get -y autoremove

# Test nii2dcm installation
RUN convert_nii2dcm.py -h
