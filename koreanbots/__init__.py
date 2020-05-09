__title__ = 'koreanbots'
__author__ = 'kijk2869'
__version = '0.1.0'

from collections import namedtuple

from .client import Client
from .http import HTTPClient
from .model import Category, Libraries
from .errors import *

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=1, micro=0, releaselevel='final', serial=0)