import pytest

from koreanbots.client import Koreanbots
from koreanbots.model import KoreanbotsBot, KoreanbotsUser


@pytest.mark.asyncio
async def test_botinfo(session: Koreanbots):
    response = await session.botinfo(653534001742741552)
    assert response.code == 200
    assert response.name == "KODL"
    assert isinstance(response.owners[0], KoreanbotsUser)
    assert isinstance(response.owners[0].bots[0], str)


@pytest.mark.asyncio
async def test_get_user_info(session: Koreanbots):
    response = await session.userinfo(285185716240252929)

    assert response.code == 200
    assert isinstance(response.bots[0], KoreanbotsBot)
    assert isinstance(response.bots[0].owners[0], str)


@pytest.mark.asyncio
async def test_get_server_info(session: Koreanbots):
    response = await session.serverinfo(653083797763522580)

    assert response.code == 200
    assert isinstance(response.bots[0], KoreanbotsBot)
    assert isinstance(response.bots[0].owners[0], str)


@pytest.mark.asyncio
async def test_get(session: Koreanbots):
    response = await session.widget("votes", 653534001742741552)
    assert (
        response
        == "https://koreanbots.dev/api/v2/widget/bots/votes/653534001742741552.svg?style=flat&scale=1.0&icon=False"
    )
