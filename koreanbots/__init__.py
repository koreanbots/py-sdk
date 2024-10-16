from typing import Literal, NamedTuple

from .client import Koreanbots as Koreanbots
from .errors import *
from .http import KoreanbotsRequester as KoreanbotsRequester


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


versioninfo = VersionInfo(2, 1, 2, "final", 0)

__version__ = "2.1.2"
