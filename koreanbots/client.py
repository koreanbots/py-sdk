import asyncio
from typing import Optional
from logging import getLogger

import aiohttp

from .decorator import strict_literal
from .http import KoreanbotsRequester
from .model import KoreanbotsBot, KoreanbotsUser
from .typing import Client, WidgetStyle, WidgetType

log = getLogger(__name__)


class Koreanbots(KoreanbotsRequester):
    def __init__(
        self,
        client: Optional[Client] = None,
        api_key: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        task: bool = False,
    ) -> None:
        self.client = client
        super().__init__(api_key, session=session, loop=loop)

        if task and client:
            self.loop = loop or client.loop
            self.loop.create_task(self.tasks_send_guildcount())

    async def tasks_send_guildcount(self) -> None:
        if not self.client:
            raise RuntimeError("Client Not Found")

        await self.client.wait_until_ready()

        while not self.client.is_closed():
            log.info("Send")
            await self.guildcount(self.client.user.id, len(self.client.guilds))
            log.info("Complete i will sleep")
            await asyncio.sleep(1800)

    async def guildcount(self, bot_id: int, total_guilds: int) -> None:
        await self.post_update_bot_info(bot_id, total_guilds)

    async def userinfo(self, user_id: int) -> KoreanbotsUser:
        return KoreanbotsUser(**await self.get_user_info(user_id))

    async def botinfo(self, bot_id: int) -> KoreanbotsBot:
        return KoreanbotsBot(**await self.get_bot_info(bot_id))

    @strict_literal("widget_type")
    @strict_literal("style")
    async def widget(
        self,
        widget_type: WidgetType,
        bot_id: int,
        style: WidgetStyle = "flat",
        scale: float = 1.0,
        icon: bool = False,
    ) -> str:
        return await self.get_bot_widget_url(widget_type, bot_id, style, scale, icon)
