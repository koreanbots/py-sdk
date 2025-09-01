from typing import Any, Literal

from aiohttp import ClientSession
from yarl import URL


class KoreanbotsRequester:
    BASE = "https://koreanbots.dev/api/"
    VERSION = "v2"

    KOREANBOTS_URL = URL(BASE + VERSION)

    def __init__(self, api_key: str, session: ClientSession | None = None) -> None:
        self.api_key = api_key
        self.session = session
        # Set the Authorization header if not already set
        if self.session is not None:
            if self.session.headers.get("Authorization") is None:
                self.session.headers["Authorization"] = self.api_key

    async def request(
        self,
        method: Literal["GET", "POST"],
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        # Create a new session if one doesn't exist
        if self.session is None:
            self.session = ClientSession(
                headers={
                    "Authorization": self.api_key,
                    "Content-Type": "application/json",
                }
            )

        url = self.KOREANBOTS_URL.with_path(path)

        # Append query parameters for GET requests
        if method == "GET" and params is not None:
            url = url.with_query(params)
            # Clear the params for the GET request
            params = None

        async with self.session.request(method, url, json=params) as response:
            if response.status == 429:
                ...

            if response.status != 200:
                ...

            return await response.json()

    async def request_bot_info(self, bot_id: int) -> dict[str, Any]:
        return await self.request("GET", f"/bots/{bot_id}")

    async def request_search_bot(self, query: str, page: int = 1) -> dict[str, Any]:
        return await self.request("GET", "/bots/search", {"query": query, "page": page})

    async def request_bot_heart_ranking_list(self, page: int = 1) -> dict[str, Any]:
        return await self.request("GET", "/list/bots/votes", {"page": page})

    async def request_new_bot_list(self) -> dict[str, Any]:
        return await self.request("GET", "/list/bots/new")

    async def request_user_is_voted_bot(
        self, bot_id: int, user_id: int
    ) -> dict[str, Any]:
        return await self.request("GET", f"/bots/{bot_id}/vote", {"userID": user_id})

    async def request_update_bot_info(
        self, bot_id: int, servers: int, shards: int
    ) -> dict[str, Any]:
        return await self.request(
            "POST", f"/bots/{bot_id}/stats", {"servers": servers, "shards": shards}
        )

    async def request_server_info(self, server_id: int) -> dict[str, Any]:
        return await self.request("GET", f"/servers/{server_id}")

    async def request_search_server(self, query: str, page: int = 1) -> dict[str, Any]:
        return await self.request(
            "GET", "/servers/search", {"query": query, "page": page}
        )

    async def request_server_administrator(self, server_id: int) -> dict[str, Any]:
        return await self.request("GET", f"/servers/{server_id}/owners")

    async def request_user_is_voted_server(
        self, server_id: int, user_id: int
    ) -> dict[str, Any]:
        return await self.request(
            "GET", f"/servers/{server_id}/vote", {"userID": user_id}
        )

    async def request_user_info(self, user_id: int) -> dict[str, Any]:
        return await self.request("GET", f"/users/{user_id}")
