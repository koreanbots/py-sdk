from os import getenv

from pytest_asyncio import fixture

from koreanbots.client import Koreanbots


@fixture(name="session")
async def client():
    bot = Koreanbots(api_key=getenv("API_KEY"))
    yield bot
    if bot.session:
        await bot.session.close()
