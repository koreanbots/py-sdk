import pytest

from koreanbots.client import Koreanbots
from koreanbots.domain.entities import User
from koreanbots.domain.bot import BotWithOwnerID


@pytest.mark.asyncio
async def test_bot_info(session: Koreanbots):
    response = await session.get_bot_info(653534001742741552)
    assert response.code == 200
    assert response.data.name == "KODL"
    assert isinstance(response.data.owners[0], User)
    assert isinstance(response.data.owners[0].bots[0], str)


@pytest.mark.asyncio
async def test_get_user_info(session: Koreanbots):
    response = await session.get_user_info(285185716240252929)

    assert response.code == 200
    assert isinstance(response.data.bots[0], BotWithOwnerID)


@pytest.mark.asyncio
async def test_get_server_info(session: Koreanbots):
    response = await session.get_server_info(653083797763522580)

    assert response.code == 200
    assert isinstance(response.data.owner, User)


@pytest.mark.asyncio
async def test_get(session: Koreanbots):
    response = str(session.widget(653534001742741552, "votes"))
    assert (
        response
        == "https://koreanbots.dev/widget/bots/votes/653534001742741552.svg?style=flat&scale=1.0&icon=False"
    )
