from os import getenv

from pytest import fixture

from koreanbots import Koreanbots


@fixture
async def client():
    """
    client params in test.
    """
    yield Koreanbots(api_key=getenv("API_KEY"))
