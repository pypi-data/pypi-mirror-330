"""Python Requests addon to support accessing data from a Pelican federation.

See https://docs.pelicanplatform.org/ for details of the Pelican platform.
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

from .adapters import PelicanAdapter
from .director import (
    DirectorResponse,
    get_urls,
)
from .requests import *
from .sessions import Session

try:
    from ._version import version as __version__
except ModuleNotFoundError:  # development mode
    __version__ = ""
