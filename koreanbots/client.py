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


class Koreanbots(KoreanbotsRequester):
    def __init__(self, api_key: str, session: ClientSession | None = None) -> None:
        super().__init__(api_key, session)

    async def get_bot_info(self, bot_id: int) -> KoreanbotsDataResponse[Bot]:
        res = await self.request_bot_info(bot_id)
        return KoreanbotsDataResponse.from_bot(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def search_bot(
        self, query: str, page: int = 1
    ) -> KoreanbotsDataResponse[list[Bot]]:
        res = await self.request_search_bot(query, page)
        return KoreanbotsDataResponse.from_list_bot(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_heart_ranking_list(
        self, page: int = 1
    ) -> KoreanbotsDataResponse[list[Bot]]:
        res = await self.request_bot_heart_ranking_list(page)
        return KoreanbotsDataResponse.from_list_bot(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_new_bot_list(self) -> KoreanbotsDataResponse[list[Bot]]:
        res = await self.request_new_bot_list()
        return KoreanbotsDataResponse.from_list_bot(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_user_is_voted_bot(
        self, bot_id: int, user_id: int
    ) -> KoreanbotsDataResponse[Vote]:
        res = await self.request_user_is_voted_bot(bot_id, user_id)
        return KoreanbotsDataResponse.from_vote(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def update_bot_info(
        self, bot_id: int, servers: int, shards: int
    ) -> KoreanbotsMessageResponse:
        res = await self.request_update_bot_info(bot_id, servers, shards)
        return KoreanbotsMessageResponse(
            code=res["code"],
            version=res["version"],
            message=res["message"],
        )

    async def get_server_info(self, server_id: int) -> KoreanbotsDataResponse[Server]:
        res = await self.request_server_info(server_id)
        return KoreanbotsDataResponse.from_server(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def search_server(
        self, query: str, page: int = 1
    ) -> KoreanbotsDataResponse[list[Server]]:
        res = await self.request_search_server(query, page)
        return KoreanbotsDataResponse.from_list_server(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_server_administrator(
        self, server_id: int
    ) -> KoreanbotsDataResponse[User]:
        res = await self.request_server_administrator(server_id)
        return KoreanbotsDataResponse.from_user(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_user_is_voted_server(
        self, server_id: int, user_id: int
    ) -> KoreanbotsDataResponse[Vote]:
        res = await self.request_user_is_voted_server(server_id, user_id)
        return KoreanbotsDataResponse.from_vote(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )

    async def get_user_info(self, user_id: int) -> KoreanbotsDataResponse[User]:
        res = await self.request_user_info(user_id)
        return KoreanbotsDataResponse.from_user(
            code=res["code"],
            version=res["version"],
            data=res["data"],
        )
