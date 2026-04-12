import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Literal, cast

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
        """HTTP 응답 헤더에서 레이트리밋 정보를 추출하여 인스턴스를 생성합니다."""
        return cls(
            limit=int(headers["x-ratelimit-limit"]),
            remaining=int(headers["x-ratelimit-remaining"]),
            reset=int(headers["x-ratelimit-reset"]),
            is_global=headers["x-ratelimit-global"].lower() == "true",
        )

    def get_wait_time(self) -> float:
        """레이트리밋 리셋까지 대기해야 하는 시간(초)을 반환합니다."""
        current_time = int(time.time())
        if self.reset > current_time:
            return max(0, self.reset - current_time)
        else:
            return max(0, self.reset)


class KoreanbotsRequester:
    BASE = "https://koreanbots.dev"
    API_VERSION = "/api/v2"

    KOREANBOTS_API_URL = URL(BASE + API_VERSION)

    def __init__(
        self,
        api_key: str,
        session: ClientSession | None = None,
    ) -> None:
        """KoreanbotsRequester를 초기화합니다.

        Args:
            api_key: Koreanbots API 인증 키.
            session: 재사용할 aiohttp ClientSession. None이면 요청 시 자동 생성됩니다.
        """
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
        """글로벌 레이트리밋이 활성 상태이면 리셋 시간까지 선제적으로 대기합니다."""
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
        """Koreanbots API에 HTTP 요청을 보냅니다.

        Args:
            method: HTTP 메서드 (GET 또는 POST).
            path: API 엔드포인트 경로.
            params: 요청 파라미터. GET이면 쿼리 파라미터, POST이면 JSON 바디로 전송됩니다.

        Returns:
            API 응답 JSON을 딕셔너리로 반환합니다.

        Raises:
            KoreanbotsException: HTTP 상태 코드가 200이 아닐 때 발생합니다.
        """
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

        url = self.KOREANBOTS_API_URL.with_path(path)

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

            return cast(dict[str, Any], await response.json())

    async def request_bot_info(self, bot_id: int) -> dict[str, Any]:
        """봇 정보를 조회합니다."""
        return await self.request("GET", f"/bots/{bot_id}")

    async def request_search_bot(self, query: str, page: int = 1) -> dict[str, Any]:
        """봇을 검색합니다."""
        return await self.request("GET", "/bots/search", {"query": query, "page": page})

    async def request_bot_heart_ranking_list(self, page: int = 1) -> dict[str, Any]:
        """봇 하트 랭킹 목록을 조회합니다."""
        return await self.request("GET", "/list/bots/votes", {"page": page})

    async def request_new_bot_list(self) -> dict[str, Any]:
        """새로 등록된 봇 목록을 조회합니다."""
        return await self.request("GET", "/list/bots/new")

    async def request_user_is_voted_bot(
        self, bot_id: int, user_id: int
    ) -> dict[str, Any]:
        """특정 유저가 해당 봇에 투표했는지 확인합니다."""
        return await self.request("GET", f"/bots/{bot_id}/vote", {"userID": user_id})

    async def request_update_bot_info(
        self, bot_id: int, servers: int, shards: int
    ) -> dict[str, Any]:
        """봇의 서버 수와 샤드 수를 업데이트합니다."""
        return await self.request(
            "POST", f"/bots/{bot_id}/stats", {"servers": servers, "shards": shards}
        )

    async def request_server_info(self, server_id: int) -> dict[str, Any]:
        """서버 정보를 조회합니다."""
        return await self.request("GET", f"/servers/{server_id}")

    async def request_search_server(self, query: str, page: int = 1) -> dict[str, Any]:
        """서버를 검색합니다."""
        return await self.request(
            "GET", "/servers/search", {"query": query, "page": page}
        )

    async def request_server_administrator(self, server_id: int) -> dict[str, Any]:
        """서버 관리자 정보를 조회합니다."""
        return await self.request("GET", f"/servers/{server_id}/owners")

    async def request_user_is_voted_server(
        self, server_id: int, user_id: int
    ) -> dict[str, Any]:
        """특정 유저가 해당 서버에 투표했는지 확인합니다."""
        return await self.request(
            "GET", f"/servers/{server_id}/vote", {"userID": user_id}
        )

    async def request_user_info(self, user_id: int) -> dict[str, Any]:
        """유저 정보를 조회합니다."""
        return await self.request("GET", f"/users/{user_id}")
