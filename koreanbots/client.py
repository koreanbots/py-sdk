from typing import Literal

from aiohttp import ClientSession

from koreanbots.domain.entities import (
    Bot,
    KoreanbotsDataResponse,
    KoreanbotsMessageResponse,
    Server,
    User,
    Vote,
)
from koreanbots.request import KoreanbotsRequester

WidgetType = Literal["votes", "servers", "status"]
WidgetStyle = Literal["classic", "flat"]


class BotWidgetURLBuilder:
    """봇 위젯 URL을 단계적으로 구성하는 빌더 클래스."""

    def __init__(self, bot_id: int, widget_type: WidgetType) -> None:
        """빌더를 초기화합니다.

        Args:
            bot_id: 위젯을 생성할 봇의 ID.
            widget_type: 위젯 타입 (votes, servers, status 중 하나).
        """
        self._bot_id = bot_id
        self._widget_type = widget_type
        self._style: WidgetStyle = "flat"
        self._scale: float = 1.0
        self._icon: bool = False

    def style(self, style: WidgetStyle) -> "BotWidgetURLBuilder":
        """위젯 스타일을 설정합니다.

        Args:
            style: 위젯 스타일 (classic 또는 flat).
        """
        self._style = style
        return self

    def scale(self, scale: float) -> "BotWidgetURLBuilder":
        """위젯 크기 배율을 설정합니다.

        Args:
            scale: 위젯 배율. 0.5 이상이어야 합니다.

        Raises:
            ValueError: scale이 0.5 미만일 때 발생합니다.
        """
        if scale < 0.5:
            raise ValueError(f"scale must be greater than or equal to 0.5, not {scale}")
        self._scale = scale
        return self

    def icon(self, icon: bool = True) -> "BotWidgetURLBuilder":
        """위젯에 아이콘 표시 여부를 설정합니다.

        Args:
            icon: True면 아이콘을 표시합니다.
        """
        self._icon = icon
        return self

    def _build(self) -> str:
        return (
            KoreanbotsRequester.BASE
            + f"/widget/bots/{self._widget_type}/{self._bot_id}.svg"
            + f"?style={self._style}&scale={self._scale}&icon={self._icon}"
        )

    def __str__(self) -> str:
        return self._build()

    def __repr__(self) -> str:
        return self._build()


class Koreanbots(KoreanbotsRequester):
    def __init__(self, api_key: str, session: ClientSession | None = None) -> None:
        """Koreanbots 클라이언트를 초기화합니다.

        Args:
            api_key: Koreanbots API 인증 키.
            session: 재사용할 aiohttp ClientSession. None이면 요청 시 자동 생성됩니다.
        """
        super().__init__(api_key, session)

    async def get_bot_info(self, bot_id: int) -> KoreanbotsDataResponse[Bot]:
        """봇 정보를 조회합니다."""
        res = await self.request_bot_info(bot_id)
        return KoreanbotsDataResponse.from_bot(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def search_bot(
        self, query: str, page: int = 1
    ) -> KoreanbotsDataResponse[list[Bot]]:
        """봇을 검색합니다."""
        res = await self.request_search_bot(query, page)
        return KoreanbotsDataResponse.from_list_bot(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_heart_ranking_list(
        self, page: int = 1
    ) -> KoreanbotsDataResponse[list[Bot]]:
        """봇 하트 랭킹 목록을 조회합니다."""
        res = await self.request_bot_heart_ranking_list(page)
        return KoreanbotsDataResponse.from_list_bot(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_new_bot_list(self) -> KoreanbotsDataResponse[list[Bot]]:
        """새로 등록된 봇 목록을 조회합니다."""
        res = await self.request_new_bot_list()
        return KoreanbotsDataResponse.from_list_bot(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_user_is_voted_bot(
        self, bot_id: int, user_id: int
    ) -> KoreanbotsDataResponse[Vote]:
        """특정 유저가 해당 봇에 투표했는지 확인합니다."""
        res = await self.request_user_is_voted_bot(bot_id, user_id)
        return KoreanbotsDataResponse.from_vote(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def update_bot_info(
        self, bot_id: int, servers: int, shards: int
    ) -> KoreanbotsMessageResponse:
        """봇의 서버 수와 샤드 수를 업데이트합니다."""
        res = await self.request_update_bot_info(bot_id, servers, shards)
        return KoreanbotsMessageResponse(
            code=res["code"],
            version=res["version"],
            message=res["message"],
        )

    async def get_server_info(self, server_id: int) -> KoreanbotsDataResponse[Server]:
        """서버 정보를 조회합니다."""
        res = await self.request_server_info(server_id)
        return KoreanbotsDataResponse.from_server(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def search_server(
        self, query: str, page: int = 1
    ) -> KoreanbotsDataResponse[list[Server]]:
        """서버를 검색합니다."""
        res = await self.request_search_server(query, page)
        return KoreanbotsDataResponse.from_list_server(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_server_administrator(
        self, server_id: int
    ) -> KoreanbotsDataResponse[User]:
        """서버 관리자 정보를 조회합니다."""
        res = await self.request_server_administrator(server_id)
        return KoreanbotsDataResponse.from_user(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_user_is_voted_server(
        self, server_id: int, user_id: int
    ) -> KoreanbotsDataResponse[Vote]:
        """특정 유저가 해당 서버에 투표했는지 확인합니다."""
        res = await self.request_user_is_voted_server(server_id, user_id)
        return KoreanbotsDataResponse.from_vote(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_user_info(self, user_id: int) -> KoreanbotsDataResponse[User]:
        """유저 정보를 조회합니다."""
        res = await self.request_user_info(user_id)
        return KoreanbotsDataResponse.from_user(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    def widget(self, bot_id: int, widget_type: WidgetType) -> BotWidgetURLBuilder:
        """봇 위젯 URL 빌더를 반환합니다.

        Args:
            bot_id: 위젯을 생성할 봇의 ID.
            widget_type: 위젯 타입 (votes, servers, status 중 하나).

        Example:
            >>> url = str(client.widget(123456789, "servers").style("classic").scale(1.5).icon())
        """
        return BotWidgetURLBuilder(bot_id, widget_type)
