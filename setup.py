from setuptools import setup
from dunamai import Version, Style

setup(
    name="nii2dcm",
    version=Version.from_any_vcs().serialize(metadata=False, style=Style.SemVer),
)