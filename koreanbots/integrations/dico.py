from asyncio.events import get_event_loop
import logging
from asyncio.tasks import sleep
from typing import Optional

from aiohttp import ClientSession
from dico import Client  # type: ignore

from koreanbots.http import KoreanbotsRequester

log = logging.getLogger(__name__)


class DicoKoreanbotsHelper(KoreanbotsRequester):
    """
    KoreanbotsRequester를 감싸는 클라이언트 클래스입니다.
    dico 전용입니다.

    :param client:
        dico.Client의 클래스입니다.
    :type client:
        dico.Client

    :param api_key:
        API key를 지정합니다.
    :type api_key:
        str

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
        client: Client,
        api_key: str,
        session: Optional[ClientSession] = None,
        run_task: bool = False,
        include_shard_count: bool = False,
    ):
        self.client = client

        if client:
            original_close = client.close

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

        await self.client.wait_ready()

        while not self.client.websocket_closed:
            if not self.client.application_id:
                continue

            kwargs = {"servers": self.client.guild_count}
            if self.include_shard_count:
                if self.client.shard_count:
                    kwargs.update({"shards": self.client.shard_count})
            log.info("Send")
            await self.post_update_bot_info(int(self.client.application_id), **kwargs)
            log.info("Complete i will sleep")
            await sleep(1800)
