from .client import Koreanbots
from .http import KoreanbotsRequester
from .errors import *
from .model import KoreanbotsBot, KoreanbotsUser

from typing import Literal, NamedTuple


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


versioninfo = VersionInfo(1, 0, 2, "final", 0)

__version__ = "1.0.2"
