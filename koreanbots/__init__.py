#-*- coding: utf-8 -*-
"""
KoreanBots API Wrapper
~~~~~~~~~~~~~~~~~~~
A Simple Python API wrapper for KoreanBots.
:license: MIT, 자세한 내용은 LISENCE를 확인해주세요.
"""

__title__ = 'koreanbots'
__author__ = 'kijk2869'
__lisence__ = 'MIT'
__version__ = '0.2.1'

from collections import namedtuple

from .client import Client
from .http import HTTPClient
from .model import Category, Library
from .errors import *

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=2, micro=1, releaselevel='final', serial=0)