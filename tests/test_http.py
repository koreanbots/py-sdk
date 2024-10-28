import pytest

from koreanbots.client import Koreanbots


@pytest.mark.asyncio
async def test_get_bot_info(session: Koreanbots):
    response = await session._http.get_bot_info(653534001742741552)
    assert response["code"] == 200


@pytest.mark.asyncio
async def test_get_user_info(session: Koreanbots):
    response = await session._http.get_user_info(285185716240252929)
    assert response["code"] == 200


@pytest.mark.asyncio
async def test_get_server_info(session: Koreanbots):
    response = await session._http.get_server_info(653083797763522580)
    assert response["code"] == 200


@pytest.mark.asyncio
async def test_get(session: Koreanbots):
    response = await session._http.get_bot_widget_url("votes", 653534001742741552)
    assert (
        response
        == "https://koreanbots.dev/api/v2/widget/bots/votes/653534001742741552.svg?style=flat&scale=1.0&icon=False"
    )
