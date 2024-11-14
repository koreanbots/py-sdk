from asyncio.tasks import Task, sleep
from logging import getLogger
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Optional,
    TypeVar,
    Union,
    cast,
)

from aiohttp import ClientSession

from koreanbots.client import Koreanbots

if TYPE_CHECKING:
    import nextcord
    from discord import Client as DiscordpyClient
    from disnake.client import Client as DisnakeClient

T = TypeVar("T")
Coro = Coroutine[Any, Any, T]
CoroT = TypeVar("CoroT", bound=Callable[..., Coro[Any]])

log = getLogger(__name__)


class DiscordpyKoreanbots(Koreanbots):
    """
    Koreanbots를 감싸는 클라이언트 클래스입니다.
    discord.py 및 해당 라이브러리의 포크 전용입니다.

    :param client:
        discord.Client의 클래스입니다. 만약 필요한 경우 이 인수를 지정하세요.
    :type client:
        Optional[DpyABC]

    :param api_key:
        API key를 지정합니다. 만약 필요한 경우 이 키를 지정하세요.
    :type api_key:
        Optional[str]

    :param session:
        aiohttp.ClientSession의 클래스입니다. 만약 필요한 경우 이 인수를 지정하세요. 지정하지 않으면 생성합니다.
    :type session:
        Optional[aiohttp.ClientSession]

    :param run_task:
        봇 정보를 갱신하는 작업을 자동으로 실행합니다. 만약 아니라면 지정하지 않습니다.
    :type run_task:
        bool

    :param include_shard_count:
        샤드 개수를 포함할지 지정합니다. 만약 아니라면 지정하지 않습니다.
    :type include_shard_count:
        bool
    """

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

        if run_task:
            client_ready = getattr(client, "on_ready", None)
            client_event = getattr(client, "event")
            self.guildcount_sender: Optional[Task[None]] = None

            # Set default on_ready handler to start send_guildcount task.
            if client_ready is not None:

                async def on_ready() -> None:
                    self.run_post_guild_count_task()
                    await client_ready()  # call previously registered on_ready handler.

            else:

                async def on_ready() -> None:
                    self.run_post_guild_count_task()

            def event(coro: CoroT, /) -> CoroT:
                if coro.__name__ == "on_ready":

                    async def on_ready() -> None:
                        self.run_post_guild_count_task()
                        await coro()

                    return cast(CoroT, client_event(on_ready))

                return cast(CoroT, client_event(coro))

            client.event(on_ready)
            setattr(client, "event", event)

    @property
    def is_running(self) -> bool:
        return self.guildcount_sender is not None and not self.guildcount_sender.done()

    def run_post_guild_count_task(self) -> None:
        """
        tasks_send_guildcount를 호출하는 함수입니다.
        사용자가 on_ready 이벤트 핸들러를 정의할 때, 이 함수를 호출해 길드 개수를 지속적으로 갱신할 수 있습니다.
        """
        if not self.is_running:
            self.guildcount_sender = self.client.loop.create_task(
                self.tasks_send_guildcount()
            )

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
            log.info("Initiating guild count update...")
            try:
                await self.post_guild_count(int(self.client.user.id), **kwargs)
            except:
                log.exception("Guild count update failed due to an error.")
            else:
                log.info(
                    "Guild count updated successfully. Waiting 30 minutes for the next update."
                )
            await sleep(1800)
