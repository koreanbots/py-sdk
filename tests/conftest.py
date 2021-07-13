from pytest import fixture
from koreanbots import Koreanbots
from os import getenv


@fixture
async def client():
    yield Koreanbots(api_key=getenv("API_KEY"))
