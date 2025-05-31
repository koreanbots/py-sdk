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


version_info = VersionInfo(3, 1, 0, "final", 0)

__version__ = f"{version_info.major}.{version_info.minor}.{version_info.micro}"

if version_info.releaselevel != "final":
    __version__ = f"{__version__}-{version_info.releaselevel}.{version_info.serial}"
