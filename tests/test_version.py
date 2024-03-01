import pytest
from packaging import version

from nii2dcm._version import __version__


class TestVersion:
    def test_version(self):
        assert isinstance(version.parse(__version__), version.Version)
