import asyncio
from koreanbots.decorator import strict_literal
from typing import Literal, Optional, Type

import aiohttp
from koreanbots.http import KoreanbotsRequester
from koreanbots.errors import HTTPException
import discord
import contextlib


class Koreanbots(KoreanbotsRequester):
    def __init__(
        self,
        client: Type[discord.Client],
        api_key: str,
        session: Optional[aiohttp.ClientSession],
    ) -> None:
        self.client = client
        super().__init__(api_key, session=session)

    async def send_guildcount_tasks(self):
        await self.client.wait_until_ready()  # type: ignore
        while not self.client.is_closed():  # type: ignore

            with contextlib.suppress(HTTPException):
                await self.guildcount()

            await asyncio.sleep(1800)

    async def guildcount(self):
        total_guilds = len(self.client.guilds)  # type: ignore
        bot_id = (await self.client.application_info()).id  # type:ignore
        return await self.post_update_bot_info(bot_id, total_guilds)

    async def userinfo(self, user_id: int):
        return await self.get_user_info(user_id)

    async def botinfo(self, bot_id: int):
        return await self.get_bot_info(bot_id)

    @strict_literal("widget_type")
    async def widget(
        self, widget_type: Literal["votes", "servers", "status"], bot_id: int
    ):
        return await self.get_bot_widget(widget_type, bot_id)