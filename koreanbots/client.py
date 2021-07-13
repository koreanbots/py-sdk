import asyncio
from asyncio.events import get_event_loop
from typing import Optional
from logging import getLogger

import aiohttp

from .decorator import strict_literal
from .http import KoreanbotsRequester
from .model import KoreanbotsBot, KoreanbotsUser
from .typing import Client, WidgetStyle, WidgetType

log = getLogger(__name__)


class Koreanbots(KoreanbotsRequester):
    """
    KoreanbotsRequester를 감싸는 클라이언트 클래스 입니다.

    :param client:
        discord.Client의 클래스입니다. 만약 필요한 경우 이 인수를 지정하세요.
    :type client:
        Optional[Client]

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
        샤드 갯수를 포함할지 지정합니다. 만약 아니라면 지정하지 않습니다.
    :type include_shard_count:
        bool
    """

    def __init__(
        self,
        client: Optional[Client] = None,
        api_key: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
        run_task: bool = False,
        include_shard_count: bool = False,
    ) -> None:
        self.client = client

        # Patch discord.py client.close() method to handle session.close()
        if client:
            original_close = client.close

            async def close():
                if self.session is not None and not self.session.closed:
                    await self.session.close()
                await original_close()

            client.close = close

        self.include_shard_count = include_shard_count
        super().__init__(api_key, session)

        if run_task:
            get_event_loop().create_task(self.tasks_send_guildcount())

    async def tasks_send_guildcount(self) -> None:
        """
        길드 갯수를 서버에 전송하는 태스크 입니다.

        :raises RuntimeError:
            클라이언트를 찾을 수 없습니다.
        """

        if not self.client:
            raise RuntimeError("Client Not Found")

        await self.client.wait_until_ready()

        while not self.client.is_closed():
            kwargs = {"servers": len(self.client.guilds)}
            if self.include_shard_count:
                if self.client.shard_count:
                    kwargs.update({"shards": self.client.shard_count})
            log.info("Send")
            await self.guildcount(self.client.user.id, **kwargs)
            log.info("Complete i will sleep")
            await asyncio.sleep(1800)

    async def guildcount(self, bot_id: int, **kwargs: Optional[int]) -> None:
        """
        길드 갯수를 서버에 전송합니다.

        :param bot_id:
            요청할 bot의 ID를 지정합니다.
        :type bot_id:
            int
        """
        await self.post_update_bot_info(bot_id, **kwargs)

    async def userinfo(self, user_id: int) -> KoreanbotsUser:
        """
        유저 정보를 가져옵니다.

        :param user_id:
            요청할 유저의 ID를 지정합니다.
        :type user_id:
            int
        :return:
            유저 정보를 담고 있는 KoreanbotsUser클래스입니다.
        :rtype:
            KoreanbotsUser
        """
        return KoreanbotsUser(**await self.get_user_info(user_id))

    async def botinfo(self, bot_id: int) -> KoreanbotsBot:
        """
        봇 정보를 가져옵니다.

        :param bot_id:
            요청할 봇의 ID를 지정합니다.
        :type bot_id:
            int

        :return:
            봇 정보를 담고 있는 KoreanbotsBot클래스입니다.
        :rtype:
            KoreanbotsBot
        """
        return KoreanbotsBot(**await self.get_bot_info(bot_id))

    @strict_literal(["widget_type", "style"])
    async def widget(
        self,
        widget_type: WidgetType,
        bot_id: int,
        style: WidgetStyle = "flat",
        scale: float = 1.0,
        icon: bool = False,
    ) -> str:
        """
        주어진 bot_id로 widget의 url을 반환합니다.

        :param widget_type:
            요청할 widget의 타입을 지정합니다.
        :type widget_type:
            WidgetType

        :param bot_id:
            요청할 bot의 ID를 지정합니다.
        :type bot_id:
            int

        :param style:
            요청할 widget의 형식을 지정합니다. 기본값은 flat로 설정되어 있습니다.
        :type style:
            WidgetStyle, optional

        :param scale:
            요청할 widget의 크기를 지정합니다. 반드시 0.5이상이어야 합니다. 기본값은 1.0입니다.
        :type scale:
            float, optional

        :param icon:
            요청할 widget의 아이콘을 표시할지를 지정합니다. 기본값은 False입니다.
        :type icon:
            bool, optional

        :return:
            위젯 url을 반환합니다.
        :rtype: str
        """
        return await self.get_bot_widget_url(widget_type, bot_id, style, scale, icon)
