import asyncio
from datetime import datetime
from typing import Any, Dict, Literal, Optional

import aiohttp

from .decorator import required, strict_literal
from .errors import ERROR_MAPPING, HTTPException
from .typing import WidgetStyle, WidgetType

BASE = "https://beta.koreanbots.dev/api/"
VERSION = "v2"

KOREANBOTS_URL = BASE + VERSION


class KoreanbotsRequester:
    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self.api_key = api_key
        self.session = session
        self.loop = loop or asyncio.get_event_loop()
        self.queue = asyncio.Queue()

    def __del__(self) -> None:
        if self.session:
            if self.loop.is_running():
                self.loop.create_task(self.session.close())
            else:
                self.loop.run_until_complete(self.session.close())

    async def handle_ratelimit(
        self, session: aiohttp.ClientSession, *args, **kwargs
    ) -> Dict[str, Any]:
        async with session.request(*args, **kwargs) as response:
            remain_limit = response.headers["x-ratelimit-remaining"]
            if remain_limit == 0 or response.status == 429:
                await self.queue.put(session.request(*args, **kwargs))
                reset_limit_timestamp = int(response.headers["x-ratelimit-reset"])
                resetLimit = datetime.fromtimestamp(reset_limit_timestamp)
                retryAfter = resetLimit - datetime.now()
                print(
                    "we're now rate limited. retrying after %.2f seconds",
                    retryAfter.total_seconds(),
                )
                await asyncio.sleep(retryAfter.total_seconds())

                blocked_session_request: aiohttp.client._RequestContextManager = (
                    await self.queue.get()
                )
                async with blocked_session_request as response:
                    return await response.json()

            elif response.status != 200:
                if ERROR_MAPPING.get(response.status):
                    raise ERROR_MAPPING[response.status](
                        response.status, await response.json()
                    )
                else:
                    raise HTTPException(response.status, await response.json())

            return await response.json()

    async def request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if not self.session:
            self.session = aiohttp.ClientSession()

        response = await self.handle_ratelimit(
            self.session, method, KOREANBOTS_URL + endpoint, **kwargs
        )

        return response

    async def get_bot_info(self, bot_id: int):
        return await self.request("GET", f"/bots/{bot_id}")

    @required
    async def post_update_bot_info(self, bot_id: int, total_guilds: int):
        return await self.request(
            "POST",
            f"/bots/{bot_id}/stats",
            json={"servers": total_guilds},
            headers={"Authorization": self.api_key},
        )

    @strict_literal("widget_type")
    @strict_literal("style")
    async def get_bot_widget_url(
        self,
        widget_type: WidgetType,
        bot_id: int,
        style: WidgetStyle = "flat",
        scale: float = 1.0,
        icon: bool = False,
    ):
        return (
            KOREANBOTS_URL
            + f"/widget/bots/{widget_type}/{bot_id}.svg?style={style}&scale={scale}&icon={icon}"
        )

    async def get_user_info(self, user_id: int):
        return await self.request("GET", f"/users/{user_id}")
