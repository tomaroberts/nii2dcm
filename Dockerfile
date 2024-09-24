# Use the official Python image as the base image
FROM scilus/scilus:1.6.0

# Set the working directory in the container
WORKDIR /

# Clone nii2dcm repository
RUN git clone https://github.com/Onset-lab/nii2dcm.git
WORKDIR /nii2dcm

# Install nii2dcm requirements
RUN pip install -r requirements.txt

# Build package from source
RUN pip install -e .

# Test nii2dcm installation
RUN nii2dcm -h
