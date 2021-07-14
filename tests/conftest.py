from os import getenv

from pytest import fixture

from koreanbots import Koreanbots


@fixture
async def client():
    yield Koreanbots(api_key=getenv("API_KEY"))
