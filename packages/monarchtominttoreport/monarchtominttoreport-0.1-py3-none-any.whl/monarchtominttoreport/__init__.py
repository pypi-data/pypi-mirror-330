"""
monarchtominttoreport
"""
__version__ = "0.1"
__all__ = ["convert"]

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("monarchtominttoreport")
except PackageNotFoundError:
    # package is not installed
    pass