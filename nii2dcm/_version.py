from dunamai import Version, Style
__version__ = Version.from_git().serialize(metadata=False, style=Style.SemVer)
