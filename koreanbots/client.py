from logging import getLogger
from typing import Optional

import aiohttp

from koreanbots.decorator import strict_literal
from koreanbots.http import KoreanbotsRequester
from koreanbots.model import KoreanbotsBot, KoreanbotsUser, KoreanbotsVote
from koreanbots.typing import WidgetStyle, WidgetType

log = getLogger(__name__)


class Koreanbots(KoreanbotsRequester):
    """
    KoreanbotsRequester를 감싸는 클라이언트 클래스입니다.

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
        api_key: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        super().__init__(api_key, session)

    async def guildcount(self, bot_id: int, **kwargs: Optional[int]) -> None:
        """
        길드 개수를 서버에 전송합니다.

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

    async def is_voted(self, user_id: int, bot_id: int) -> KoreanbotsVote:
        """
        주어진 bot_id로 user_id를 통해 해당 user의 투표 여부를 반환합니다.

        :param user_id:
            요청할 user의 ID를 지정합니다.
        :type user_id:
            int

        :param bot_id:
            요청할 봇의 ID를 지정합니다.
        :type bot_id:
            int

        :return:
            투표여부를 담고 있는 KoreanbotsVote클래스입니다.
        :rtype:
            KoreanbotsVote
        """
        return KoreanbotsVote(**await self.get_user_vote(user_id, bot_id))
