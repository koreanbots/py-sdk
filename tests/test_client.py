import pytest

from koreanbots.client import Koreanbots
from koreanbots.model import KoreanbotsBot, KoreanbotsUser, KoreanbotsServer


@pytest.mark.asyncio
async def test_botinfo(client: Koreanbots):
    response = await client.botinfo(653534001742741552)
    assert response.code == 200
    assert response.name == "IU"
    assert isinstance(response.owners[0], KoreanbotsUser)
    assert isinstance(response.owners[0].bots[0], str)


@pytest.mark.asyncio
async def test_get_user_info(client: Koreanbots):
    response = await client.userinfo(285185716240252929)

    assert response.code == 200
    assert isinstance(response.bots[0], KoreanbotsBot)
    assert isinstance(response.bots[0].owners[0], str)


@pytest.mark.asyncio
async def test_get_server_info(client: Koreanbots):
    response = await client.serverinfo(653083797763522580)

    assert response.code == 200
    assert isinstance(response.owner[0], KoreanbotsUser)
    assert isinstance(response.owner[0].bots[0], str)


@pytest.mark.asyncio
async def test_get(client: Koreanbots):
    response = await client.widget("votes", 653534001742741552)
    assert (
        response
        == "https://koreanbots.dev/api/v2/widget/bots/votes/653534001742741552.svg?style=flat&scale=1.0&icon=False"
    )
