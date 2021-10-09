from asyncio.events import get_event_loop
from asyncio.tasks import sleep
from logging import getLogger
from typing import Optional, Union

from aiohttp import ClientSession

from koreanbots.client import Koreanbots

try:
    import discord  # type: ignore
except ImportError:
    pass

try:
    import disnake.client.Client as DisnakeClient
except ImportError:
    pass

try:
    import nextcord  # type: ignore
except ImportError:
    pass

log = getLogger(__name__)


class DiscordpyKoreanbots(Koreanbots):
    def __init__(
        self,
        client: Union["discord.Client", "nextcord.Client", "DisnakeClient"],
        api_key: str,
        session: Optional[ClientSession] = None,
        run_task: bool = False,
        include_shard_count: bool = False,
    ):
        self.client = client

        # Patch discord.py client.close() method to handle session.close()
        original_close = getattr(client, "close")

        async def close() -> None:
            if self.session is not None and not self.session.closed:
                await self.session.close()
            await original_close()

        setattr(client, "close", close)

        self.include_shard_count = include_shard_count
        super().__init__(api_key, session)

        if run_task:
            get_event_loop().create_task(self.tasks_send_guildcount())

    async def tasks_send_guildcount(self) -> None:
        """
        길드 개수를 서버에 전송하는 태스크 입니다.

        :raises RuntimeError:
            클라이언트를 찾을 수 없습니다.
        """

        if not self.client:
            raise RuntimeError("Client Not Found")

        await self.client.wait_until_ready()

        while not self.client.is_closed():
            if not self.client.user:
                continue

            kwargs = {"servers": len(self.client.guilds)}
            if self.include_shard_count:
                if self.client.shard_count:
                    kwargs.update({"shards": self.client.shard_count})
            log.info("Send")
            await self.guildcount(self.client.user.id, **kwargs)
            log.info("Complete i will sleep")
            await sleep(1800)
