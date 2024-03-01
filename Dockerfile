# Use the official Python image as the base image
FROM python:3.9-slim

LABEL org.opencontainers.image.source https://github.com/tomaroberts/nii2dcm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    bash \
    && apt-get clean

RUN pip install --upgrade pip && \
    pip install setuptools wheel

RUN pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ nii2dcm==0.1.2-post.11

#RUN pip install nii2dcm

# Test nii2dcm install
# To see output locally during build process: docker build -t nii2dcm --progress=plain .
RUN nii2dcm -h

ENTRYPOINT ["nii2dcm"]