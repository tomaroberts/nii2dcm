import dunamai as _dunamai
__version__ = _dunamai.get_version("nii2dcm", third_choice=_dunamai.Version.from_any_vcs).serialize()
