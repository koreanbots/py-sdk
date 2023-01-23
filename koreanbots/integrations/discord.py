from asyncio.tasks import sleep, Task
from logging import getLogger
from typing import TYPE_CHECKING, Optional, Union

from aiohttp import ClientSession

from koreanbots.client import Koreanbots

if TYPE_CHECKING:
    import nextcord
    from discord import Client as DiscordpyClient
    from disnake.client import Client as DisnakeClient

log = getLogger(__name__)


class DiscordpyKoreanbots(Koreanbots):
    def __init__(
        self,
        client: Union["DiscordpyClient", "nextcord.Client", "DisnakeClient"],
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

        client_ready = getattr(client, "on_ready", None)
        self.guildcount_sender: Optional[Task] = None

        # Set default on_ready handler to start send_guildcount task.
        if client_ready is not None:
            async def on_ready():
                self.run_post_guild_count_task()
                await client_ready()    # call previously registered on_ready handler.
        else:
            async def on_ready():
                self.run_post_guild_count_task()

        client.event(on_ready)

    @property
    def is_running(self) -> bool:
        return self.guildcount_sender is not None and not self.guildcount_sender.done()

    def run_post_guild_count_task(self):
        if not self.is_running:
            self.guildcount_sender = self.client.loop.create_task(self.tasks_send_guildcount())

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
