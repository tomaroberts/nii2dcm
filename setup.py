from setuptools import setup

setup(
    name="nii2dcm",
    version="0.1.0",
    packages=["nii2dcm"],
    entry_points={
        "console_scripts": [
            "nii2dcm = nii2dcm.__main__:run"
        ]
    },
)