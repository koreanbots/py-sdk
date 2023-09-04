from os import getenv

from pytest_asyncio import fixture

from koreanbots import Koreanbots


@fixture(name="session")
async def client():
    yield Koreanbots(api_key=getenv("API_KEY"))
