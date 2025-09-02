import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Literal

from aiohttp import ClientResponse, ClientSession
from yarl import URL

from koreanbots import __version__
from koreanbots.exception import KoreanbotsException

logger = logging.getLogger(__name__)


@dataclass
class RateLimitInfo:
    """레이트리밋 정보를 담는 데이터클래스"""

    limit: int
    remaining: int
    reset: int
    is_global: bool

    @classmethod
    def from_headers(cls, headers: dict[str, str]) -> "RateLimitInfo":
        return cls(
            limit=int(headers["x-ratelimit-limit"]),
            remaining=int(headers["x-ratelimit-remaining"]),
            reset=int(headers["x-ratelimit-reset"]),
            is_global=headers["x-ratelimit-global"].lower() == "true",
        )

    def get_wait_time(self) -> float:
        current_time = int(time.time())
        if self.reset > current_time:
            return max(0, self.reset - current_time)
        else:
            return max(0, self.reset)


class KoreanbotsRequester:
    BASE = "https://koreanbots.dev/api/"
    VERSION = "v2"

    KOREANBOTS_URL = URL(BASE + VERSION)

    def __init__(
        self,
        api_key: str,
        session: ClientSession | None = None,
    ) -> None:
        self.api_key = api_key
        self.session = session
        # Set the Authorization header if not already set
        if self.session is not None:
            if self.session.headers.get("Authorization") is None:
                self.session.headers["Authorization"] = self.api_key
            self.session.headers["User-Agent"] = f"Koreanbots py-sdk/{__version__}"
            self.session.headers["Content-Type"] = "application/json"

        self._lock = asyncio.Lock()
        self._global_rate_limit_reset: float = 0.0

    async def _handle_rate_limit(
        self,
        response: ClientResponse,
        method: Literal["GET", "POST"],
        path: str,
        params: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """레이트리밋을 처리하는 내부 메서드"""
        rate_limit = RateLimitInfo.from_headers(dict(response.headers))

        if rate_limit.is_global:
            async with self._lock:
                wait_time = rate_limit.get_wait_time()
                self._global_rate_limit_reset = time.time() + wait_time

                logger.warning(
                    f"Waiting {wait_time:.2f} seconds for global rate limit reset"
                )

                await asyncio.sleep(wait_time)
        else:
            wait_time = rate_limit.get_wait_time()

            logger.warning(
                f"Waiting {wait_time:.2f} seconds for route-specific rate limit reset"
            )

            await asyncio.sleep(wait_time)

        return await self.request(method, path, params)

    async def _check_global_rate_limit(self) -> None:
        current_time = time.time()
        if current_time < self._global_rate_limit_reset:
            wait_time = self._global_rate_limit_reset - current_time

            logger.warning(
                f"Preemptively waiting {wait_time:.2f} seconds for global rate limit"
            )

            await asyncio.sleep(wait_time)

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
                    "User-Agent": f"Koreanbots py-sdk/{__version__}",
                }
            )

        await self._check_global_rate_limit()

        url = self.KOREANBOTS_URL.with_path(path)

        # Append query parameters for GET requests
        if method == "GET" and params is not None:
            url = url.with_query(params)
            # Clear the params for the GET request
            params = None

        async with self.session.request(method, url, json=params) as response:
            if response.status == 429:
                return await self._handle_rate_limit(response, method, path, params)

            if response.status != 200:
                raise KoreanbotsException(f"HTTP Error: {response.status}")

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
