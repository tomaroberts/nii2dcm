"""
module.py
"""

from pydicom.dataset import Dataset


class Module:

    def __init__(self):
        """
        Creates generic Module object with empty Pydicom Dataset object

        nb: below somewhat superfluous – building out for future
        """
        self.module_type = 'GenericModule'

        self.ds = Dataset()
