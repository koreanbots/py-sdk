import aiohttp
from typing import Any, Literal, Optional

from koreanbots.decorator import required, strict_literal
from koreanbots.errors import HTTPException, error_mapping

BASE = "https://koreanbots.dev/api/"
VERSION = "v2"

KOREANBOTS_URL = BASE + VERSION


class KoreanbotsRequester:
    def __init__(
        self,
        api_key: Optional[str],
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.api_key = api_key
        self.session = session

    async def request(
        self,
        method: Literal["GET", "POST"],
        return_method: Literal["json", "text", "read"],
        endpoint: str,
        **kwargs: Any,
    ):
        if not self.session:
            self.session = aiohttp.ClientSession()

        async with self.session.request(
            method, KOREANBOTS_URL + endpoint, **kwargs
        ) as response:
            if response.status != 200:
                if ERROR_MAPPING.get(response.status):
                    raise ERROR_MAPPING[response.status](
                        response.status, await response.json()
                    )
                else:
                    raise HTTPException(response.status, await response.json())

            return await getattr(response, return_method)()

    @required
    async def get_vote(self, user_id: int):
        await self.request("GET", "json", f"/bots/voted/{user_id}")

    async def get_bot_info(self, bot_id: int):
        await self.request("GET", "json", f"/bots/{bot_id}")

    @required
    async def post_update_bot_info(self, bot_id: int, total_guilds: int):
        await self.request(
            "POST", "json", f"/bots/{bot_id}/stats", json={"servers": total_guilds}
        )

    @strict_literal("widget_type")
    async def get_bot_widget(
        self, widget_type: Literal["votes", "servers", "status"], bot_id: int
    ):
        await self.request("GET", "json", f"/widget/bots/{widget_type}/{bot_id}.svg")

    async def get_user_info(self, user_id: int):
        await self.request("GET", "json", f"/users/{user_id}")
