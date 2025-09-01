from aiohttp import ClientSession


class KoreanbotsRequester:
    BASE = "https://koreanbots.dev/api/"
    VERSION = "v2"

    KOREANBOTS_URL = BASE + VERSION

    def __init__(self, api_key: str):
        self.api_key = api_key
