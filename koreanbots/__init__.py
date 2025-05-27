from typing import Literal, NamedTuple

from .client import Koreanbots as Koreanbots
from .errors import *
from .http import KoreanbotsRequester as KoreanbotsRequester
from .model import KoreanbotsBot as KoreanbotsBot
from .model import KoreanbotsServer as KoreanbotsServer
from .model import KoreanbotsUser as KoreanbotsUser


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


versioninfo = VersionInfo(3, 1, 0, "final", 0)

__version__ = "3.0.0"
