from asyncio import sleep
from asyncio.events import AbstractEventLoop, get_event_loop
from asyncio.locks import Event
from datetime import datetime
from typing import Any, Dict, Literal, Optional
from logging import getLogger

import aiohttp

from .decorator import required, strict_literal
from .errors import ERROR_MAPPING, HTTPException
from .typing import WidgetStyle, WidgetType

BASE = "https://koreanbots.dev/api/"
VERSION = "v2"

KOREANBOTS_URL = BASE + VERSION

log = getLogger(__name__)


class KoreanbotsRequester:
    def __init__(
        self,
        api_key: Optional[str] = None,
        loop: Optional[AbstractEventLoop] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.session = session
        self.api_key = api_key
        self.loop = loop or get_event_loop()
        self._global_limit = Event()
        self._global_limit.set()

    def __del__(self):
        try:
            loop = get_event_loop()
            if loop.is_running():
                loop.create_task(self.session.close()) # type: ignore
            else:
                loop.run_until_complete(self.session.close()) # type: ignore
        except Exception:
            pass

    async def request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        response = None

        if not self.session:
            self.session = aiohttp.ClientSession(loop=self.loop)

        if not self._global_limit.is_set():
            await self._global_limit.wait()

        for _ in range(5):
            async with self.session.request(
                method, KOREANBOTS_URL + endpoint, **kwargs
            ) as response:
                remain_limit = response.headers["x-ratelimit-remaining"]
                if remain_limit == 0 or response.status == 429:
                    reset_limit_timestamp = int(response.headers["x-ratelimit-reset"])
                    reset_limit = datetime.fromtimestamp(reset_limit_timestamp)
                    retry_after = reset_limit - datetime.now()
                    self._global_limit.clear()
                    await sleep(retry_after.total_seconds())
                    self._global_limit.set()
                    continue

                if response.status != 200:
                    if ERROR_MAPPING.get(response.status):
                        raise ERROR_MAPPING[response.status](
                            response.status, await response.json()
                        )
                    else:
                        raise HTTPException(response.status, await response.json())
                return await response.json()

        assert None

    async def get_bot_info(self, bot_id: int) -> Dict[str, Any]:
        return await self.request("GET", f"/bots/{bot_id}")

    @required
    async def post_update_bot_info(
        self, bot_id: int, total_guilds: int
    ) -> Dict[str, Any]:
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
    ) -> str:
        return (
            KOREANBOTS_URL
            + f"/widget/bots/{widget_type}/{bot_id}.svg?style={style}&scale={scale}&icon={icon}"
        )

    async def get_user_info(self, user_id: int):
        return await self.request("GET", f"/users/{user_id}")
