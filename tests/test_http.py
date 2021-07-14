import pytest

from koreanbots.client import Koreanbots


@pytest.mark.asyncio
async def test_get_bot_info(client: Koreanbots):
    response = await client.get_bot_info(653534001742741552)
    assert response["code"] == 200


@pytest.mark.asyncio
async def test_get_user_info(client: Koreanbots):
    response = await client.get_user_info(285185716240252929)
    assert response["code"] == 200


@pytest.mark.asyncio
async def test_get(client: Koreanbots):
    response = await client.get_bot_widget_url("votes", 653534001742741552)
    assert (
        response
        == "https://koreanbots.dev/api/v2/widget/bots/votes/653534001742741552.svg?style=flat&scale=1.0&icon=False"
    )
