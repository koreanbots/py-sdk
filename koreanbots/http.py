from asyncio import sleep
from asyncio.events import get_event_loop
from asyncio.locks import Event
from datetime import datetime
from functools import wraps
from typing import Any, Dict, Literal, Optional
from logging import getLogger

import aiohttp

from .decorator import strict_literal
from .errors import ERROR_MAPPING, HTTPException, AuthorizeError
from .typing import WidgetStyle, WidgetType

BASE = "https://koreanbots.dev/api/"
VERSION = "v2"

KOREANBOTS_URL = BASE + VERSION

log = getLogger(__name__)


def required(f: Any):
    @wraps(f)
    async def decorator_function(
        self: "KoreanbotsRequester", *args: Any, **kwargs: Any
    ):
        if not self.api_key:
            raise AuthorizeError("This endpoint required koreanbots token.")

        return await f(self, *args, **kwargs)

    return decorator_function


class KoreanbotsRequester:
    """
    Koreanbots의 API를 요청하는 클래스입니다.

    :param api_key:
        KoreanBots의 토큰입니다. 기본값은 None 입니다.
    :type api_key:
        Optional[str], optional

    :param session:
        aiohttp.ClientSession의 클래스입니다. 전달되지 않으면 생성합니다. 기본값은 None 입니다.
    :type session:
        Optional[aiohttp.ClientSession], optional
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.session = session
        self.api_key = api_key
        self._global_limit = Event()
        self._global_limit.set()

    # How to close the session if discord.Client is not specified.
    def __del__(self):
        if self.session:
            if not self.session.closed:
                loop = get_event_loop()
                if loop.is_running():
                    loop.create_task(self.session.close())
                else:
                    loop.run_until_complete(self.session.close())

    async def request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Koreanbots의 url을 기반으로 요청합니다.
        레이트리밋을 핸들합니다.

        :param method:
            HTTP 메소드입니다. GET, POST만 사용할 수 있습니다.
        :type method:
            Literal["GET", "POST"]
        :param endpoint:
            요청을 실행할 API 페이지의 주소입니다.
        :type endpoint:
            str

        :raises NotFound:
            요청할 수 없는 페이지입니다.
        :raises BadRequest:
            잘못된 요청입니다.
        :raises Forbidden:
            요청을 할 권한이 없습니다.

        :raises HTTPException:
            응답에 오류가 있습니다.

        :return:
            요청 결과를 반환합니다.
        :rtype:
            Dict[str, Any]
        """

        if not self.session:
            self.session = aiohttp.ClientSession()

        if not self._global_limit.is_set():
            await self._global_limit.wait()

        for _ in range(5):
            async with self.session.request(
                method, KOREANBOTS_URL + endpoint, **kwargs
            ) as response:
                remain_limit = response.headers["x-ratelimit-remaining"]
                if remain_limit == 0 or response.status == 429:
                    reset_limit_timestamp = int(response.headers["x-ratelimit-reset"])
                    reset_limit = datetime.fromtimestamp(reset_limit_timestamp)
                    retry_after = reset_limit - datetime.now()
                    self._global_limit.clear()
                    await sleep(retry_after.total_seconds())
                    self._global_limit.set()
                    continue

                if response.status != 200:
                    if ERROR_MAPPING.get(response.status):
                        raise ERROR_MAPPING[response.status](
                            response.status, await response.json()
                        )
                    else:
                        raise HTTPException(response.status, await response.json())
                return await response.json()

        assert None

    async def get_bot_info(self, bot_id: int) -> Dict[str, Any]:
        """
        주어진 bot_id로 bot의 정보를 반환합니다.

        :param bot_id:
            요청할 bot의 ID를 지정합니다.
        :type bot_id:
            int

        :return:
            요청 결과를 반환합니다.
        :rtype:
            Dict[str, Any]
        """
        return await self.request("GET", f"/bots/{bot_id}")

    @required
    async def post_update_bot_info(self, bot_id: int, **kwargs: int) -> Dict[str, Any]:
        """
        주어진 bot_id로 bot의 정보를 갱신합니다.

        :param bot_id:
            요청할 bot의 ID를 지정합니다.
        :type bot_id:
            int

        :param kwargs:
            갱신할 정보를 지정합니다.
            'servers' 인자와 'shards' 인자 이외의 값이 들어갈경우 무시합니다.
        :type kwargs:
            int

        :raises AuthorizeError:
            api_key가 없거나 유효하지 않은 경우。

        :return:
            요청 결과를 반환합니다.
        :rtype:
            Dict[str, Any]
        """

        return await self.request(
            "POST",
            f"/bots/{bot_id}/stats",
            json={x: kwargs[x] for x in kwargs if x not in ["servers", "shards"]},
            headers={"Authorization": self.api_key},
        )

    @strict_literal("widget_type")
    @strict_literal("style")
    async def get_bot_widget_url(
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
        if scale < 0.5:
            raise ValueError(f"scale must be greater than to 0.5, not {scale}")

        return (
            KOREANBOTS_URL
            + f"/widget/bots/{widget_type}/{bot_id}.svg?style={style}&scale={scale}&icon={icon}"
        )

    async def get_user_info(self, user_id: int):
        """
        주어진 user_id로 user의 정보를 반환합니다.

        :param user_id:
            요청할 user의 ID를 지정합니다.
        :type user_id:
            int
        """
        return await self.request("GET", f"/users/{user_id}")
