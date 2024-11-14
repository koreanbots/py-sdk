import pytest

from koreanbots.client import Koreanbots
from koreanbots.model import KoreanbotsBot, KoreanbotsUser


@pytest.mark.asyncio
async def test_botinfo(session: Koreanbots):
    response = await session.get_bot_info(653534001742741552)
    assert response.code == 200
    assert response.data.name == "KODL"
    assert isinstance(response.data.owners[0], KoreanbotsUser)
    assert isinstance(response.data.owners[0].bots[0], str)


@pytest.mark.asyncio
async def test_get_user_info(session: Koreanbots):
    response = await session.get_user_info(285185716240252929)

    assert response.code == 200
    assert isinstance(response.data.bots[0], KoreanbotsBot)
    assert isinstance(response.data.bots[0].owners[0], str)


@pytest.mark.asyncio
async def test_get_server_info(session: Koreanbots):
    response = await session.get_server_info(653083797763522580)

    assert response.code == 200
    assert isinstance(response.data.owner, KoreanbotsUser)


@pytest.mark.asyncio
async def test_get(session: Koreanbots):
    response = await session.get_widget("votes", 653534001742741552)
    assert (
        response
        == "https://koreanbots.dev/api/v2/widget/bots/votes/653534001742741552.svg?style=flat&scale=1.0&icon=False"
    )
