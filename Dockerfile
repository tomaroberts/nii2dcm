# Use the official Python image as the base image
FROM scilus/scilus:1.6.0

LABEL maintainer="Onset-Lab"

ENV NII2DCM_REVISION=0.1.0

WORKDIR /
RUN apt-get update && apt-get -y install git unzip dcm2niix
RUN pip install dcm2bids

# Install nii2dcm
RUN python3 -m pip install --upgrade pip && \
    pip install git+https://github.com/onset-lab/nii2dcm.git@${NII2DCM_REVISION}

ADD rbx.tar.gz /
WORKDIR /
