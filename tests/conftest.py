from os import getenv

from pytest_asyncio import fixture

from koreanbots import Koreanbots


@fixture
async def client():
    """
    client params in test.
    """
    yield Koreanbots(api_key=getenv("API_KEY"))
