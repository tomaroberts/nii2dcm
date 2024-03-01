# Use the official Python image as the base image
FROM python:3.9-slim

LABEL org.opencontainers.image.source https://github.com/tomaroberts/nii2dcm

# Setup
COPY . /home/nii2dcm
WORKDIR /home/nii2dcm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    bash git \
    && apt-get clean

# Update base packages
RUN pip install --upgrade pip && \
    pip install setuptools wheel

# Install nii2dcm requirements
RUN pip install -r requirements.txt

# Build package from source
RUN pip install .

# Test nii2dcm install
# To see output locally during build process: docker build -t nii2dcm --progress=plain .
RUN nii2dcm -h

ENTRYPOINT ["nii2dcm"]