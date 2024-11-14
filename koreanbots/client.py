from logging import getLogger
from typing import Optional
from warnings import warn

import aiohttp

from koreanbots.decorator import strict_literal
from koreanbots.errors import KoreanbotsException
from koreanbots.http import KoreanbotsRequester
from koreanbots.model import (
    KoreanbotsBotResponse,
    KoreanbotsResponse,
    KoreanbotsServerResponse,
    KoreanbotsUserResponse,
    KoreanbotsVoteResponse,
)
from koreanbots.typing import VoteType, WidgetStyle, WidgetType

log = getLogger(__name__)


class Koreanbots(KoreanbotsRequester):
    """
    KoreanbotsRequester를 감싸는 클라이언트 클래스입니다.

    :param api_key:
        API key를 지정합니다. 만약 필요한 경우 이 키를 지정하세요.
    :type api_key:
        Optional[str]

    :param session:
        aiohttp.ClientSession의 클래스입니다. 만약 필요한 경우 이 인수를 지정하세요. 지정하지 않으면 생성합니다.
    :type session:
        Optional[aiohttp.ClientSession]
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        super().__init__(api_key, session)

    async def post_guild_count(self, bot_id: int, **kwargs: Optional[int]) -> None:
        """
        길드 개수를 서버에 전송합니다.

        :param bot_id:
            요청할 bot의 ID를 지정합니다.
        :type bot_id:
            int
        """
        await super().post_update_bot_info(bot_id, **kwargs)

    async def get_user_info(
        self, user_id: int
    ) -> KoreanbotsResponse[KoreanbotsUserResponse]:
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
        data = await super().get_user_info(user_id)

        code = data["code"]
        version = data["version"]
        data = data["data"]

        return KoreanbotsResponse(
            code=code, version=version, data=KoreanbotsUserResponse.from_dict(data)
        )

    async def get_bot_info(
        self, bot_id: int
    ) -> KoreanbotsResponse[KoreanbotsBotResponse]:
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
        data = await super().get_bot_info(bot_id)

        code = data["code"]
        version = data["version"]
        data = data["data"]

        return KoreanbotsResponse(
            code=code, version=version, data=KoreanbotsBotResponse.from_dict(data)
        )

    async def get_server_info(
        self, server_id: int
    ) -> KoreanbotsResponse[KoreanbotsServerResponse]:
        """
        서버 정보를 가져옵니다.

        :param server_id:
            요청할 서버의 ID를 지정합니다.
        :type server_id:
            int

        :return:
            봇 정보를 담고 있는 KoreanbotsServer클래스입니다.
        :rtype:
            KoreanbotsServer
        """

        data = await super().get_server_info(server_id)

        code = data["code"]
        version = data["version"]
        data = data["data"]

        return KoreanbotsResponse(
            code=code, version=version, data=KoreanbotsServerResponse.from_dict(data)
        )

    @strict_literal(["widget_type", "style"])
    async def get_widget(
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

    async def get_bot_vote(
        self, user_id: int, bot_id: int
    ) -> KoreanbotsResponse[KoreanbotsVoteResponse]:
        """
        user_id를 통해 주어진 bot_id에 대한 투표 여부를 반환합니다.

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
        data = await super().get_bot_vote(user_id, bot_id)

        code = data["code"]
        version = data["version"]
        data = data["data"]

        return KoreanbotsResponse(
            code=code, version=version, data=KoreanbotsVoteResponse.from_dict(data)
        )

    async def get_server_vote(
        self, user_id: int, server_id: int
    ) -> KoreanbotsResponse[KoreanbotsVoteResponse]:
        """
        user_id를 통해 주어진 server_id에 대한 투표 여부를 반환합니다.

        :param user_id:
            요청할 user의 ID를 지정합니다.
        :type user_id:
            int

        :param server_id:
            요청할 봇의 ID를 지정합니다.
        :type server_id:
            int

        :return:
            투표여부를 담고 있는 KoreanbotsVote클래스입니다.
        :rtype:
            KoreanbotsVote
        """
        data = await super().get_server_vote(user_id, server_id)

        code = data["code"]
        version = data["version"]
        data = data["data"]

        return KoreanbotsResponse(
            code=code, version=version, data=KoreanbotsVoteResponse.from_dict(data)
        )

    # deprecated since 3.0.0

    async def guildcount(self, bot_id: int, **kwargs: Optional[int]) -> None:
        warn(
            "guildcount 메서드는 post_guild_count로 변경되었습니다.", DeprecationWarning
        )

        return await self.post_guild_count(bot_id, **kwargs)

    async def userinfo(
        self, user_id: int
    ) -> KoreanbotsResponse[KoreanbotsUserResponse]:
        warn("userinfo 메서드는 get_user_info로 변경되었습니다.", DeprecationWarning)

        return await self.get_user_info(user_id)

    async def botinfo(self, bot_id: int) -> KoreanbotsResponse[KoreanbotsBotResponse]:
        warn("botinfo 메서드는 get_bot_info로 변경되었습니다.", DeprecationWarning)

        return await self.get_bot_info(bot_id)

    async def serverinfo(
        self, server_id: int
    ) -> KoreanbotsResponse[KoreanbotsServerResponse]:
        warn(
            "serverinfo 메서드는 get_server_info로 변경되었습니다.", DeprecationWarning
        )

        return await self.get_server_info(server_id)

    @strict_literal(["widget_type", "style"])
    async def widget(
        self,
        widget_type: WidgetType,
        bot_id: int,
        style: WidgetStyle = "flat",
        scale: float = 1.0,
        icon: bool = False,
    ) -> str:
        warn("widget 메서드는 get_widget으로 변경되었습니다.", DeprecationWarning)

        return await self.get_widget(widget_type, bot_id, style, scale, icon)

    async def is_voted_bot(
        self, user_id: int, bot_id: int
    ) -> KoreanbotsResponse[KoreanbotsVoteResponse]:
        warn("is_voted_bot 메서드는 get_bot_vote로 변경되었습니다.", DeprecationWarning)

        return await self.get_bot_vote(user_id, bot_id)

    async def is_voted_server(
        self, user_id: int, server_id: int
    ) -> KoreanbotsResponse[KoreanbotsVoteResponse]:
        warn(
            "is_voted_server 메서드는 get_server_vote로 변경되었습니다.",
            DeprecationWarning,
        )

        return await self.get_server_vote(user_id, server_id)
