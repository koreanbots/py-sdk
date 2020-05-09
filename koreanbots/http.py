"""
MIT License

Copyright (c) 2020 매리

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from asyncio import get_event_loop
from aiohttp import ClientSession
from json import loads
from logging import getLogger
from .errors import *
from .model import *
log = getLogger(__name__)

async def detectJson(response):
    try:
        return await response.json()
    except ValueError:
        return await response.text()


class HTTPClient:
    r"""KoreanBots의 HTTP 클라이언트를 반환합니다.
    이 클래스는 KoreanBots API와 연결됩니다.

    일부 옵션이 :class:`HTTPClient`에 전달될 수 있습니다.

    파라미터
    -----------
    Token: Optional[:class:`str`]
        KoreanBots의 토큰입니다.
        기본값은 ``None``이며, 토큰이 없을 시 일부 엔드포인트가 제한됩니다.
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        비동기를 사용하기 위한 :class:`asyncio.AbstractEventLoop`입니다.
        기본값은 ``None``이며, 기본 :class:`asyncio.AbstractEventLoop`는 :func:`asyncio.get_event_loop()`를 사용하여 얻습니다.

    속성
    -----------
    loop: :class:`asyncio.AbstractEventLoop`
        HTTP 리퀘스트에 사용되는 :class:`asyncio.AbstractEventLoop` 클래스 입니다.
    http: :class:`.HTTPClient`
        API 호출에 사용되는 :class:`koreanbots.HTTPClient` 클래스 입니다.
    """

    BASE = 'https://api.koreanbots.cf'

    def __init__(self, token=None, loop=None):
        self.loop = loop or get_event_loop()
        self.token = token

    async def request(self, method, url, authorize=True, **kwargs):
        r"""|coro|

        주어진 길드 수를 KoreanBots API로 보냅니다.

        파라미터
        -------------
        method: :class:`str`
            HTTP 리퀘스트 메소드
        url: :class:`str`
            KoreanBots API의 엔드포인트
        authorize: Optional[:class:`bool`]
            API 리퀘스트에 토큰을 함께 전송할지 입니다.
            기본값은 ``True``입니다.

        예외
        --------
        :exc:`.errors.AuthorizeError`
            토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다.
        :exc:`.errors.Unauthrized`
            인증되지 않았습니다, KoreanBots 토큰이 잘못되었을 수 있습니다.
        :exc:`.errors.Forbidden`
            접근 권한이 없습니다.
        :exc:`.errors.NotFound`
            찾을 수 없습니다, 파라미터를 확인하세요.
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        url = self.BASE + url
        kwargs['headers'] = {"content-type":"application/json"}
        if authorize and self.token:
            kwargs['headers']['token'] = self.token
        elif authorize and not self.token:
            raise AuthorizeError('this endpoint required koreanbots token.')
        
        async with ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                log.debug(f'{method} {url} returned {response.status}')
                Data = await detectJson(response)

                if 200 <= response.status < 300:
                    return Data
                
                if response.status == 400:
                    raise HTTPException(response, Data)
                if response.status == 401:
                    raise Unauthorized(response, Data)
                if response.status == 403:
                    raise Forbidden(response, Data)
                if response.status == 404:
                    raise NotFound(response, Data)
                else:
                    raise HTTPException(response, Data)
                
    
    async def postGuildCount(self, guild_count: int):
        r"""|coro|

        주어진 길드 수를 KoreanBots API로 보냅니다.

        파라미터
        -------------
        guild_count: :class:`int`
            전송할 길드의 수

        예외
        --------
        :exc:`.errors.AuthorizeError`
            토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다.
        :exc:`.errors.Unauthrized`
            인증되지 않았습니다, KoreanBots 토큰이 잘못되었을 수 있습니다.
        :exc:`.errors.Forbidden`
            접근 권한이 없습니다.
        :exc:`.errors.NotFound`
            찾을 수 없습니다, 파라미터를 확인하세요.
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        await self.request('POST', '/bots/servers', json={'servers': guild_count})

    async def getVote(self, user_id: int):
        r"""|coro|

        주어진 유저ID의 하트 정보를 가져옵니다.

        파라미터
        -------------
        user_id: :class:`int`
            정보를 가져올 유저의 ID

        예외
        --------
        :exc:`.errors.AuthorizeError`
            토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다.
        :exc:`.errors.Unauthrized`
            인증되지 않았습니다, KoreanBots 토큰이 잘못되었을 수 있습니다.
        :exc:`.errors.Forbidden`
            접근 권한이 없습니다.
        :exc:`.errors.NotFound`
            찾을 수 없습니다, 파라미터를 확인하세요.
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.request('GET', f"/bots/voted/{user_id}")
        return userVoted(Data)

    async def getBot(self, bot_id: int):
        r"""|coro|

        주어진 봇ID의 KoreanBots 정보를 가져옵니다.

        파라미터
        -------------
        bot_id: :class:`int`
            정보를 가져올 봇의 ID

        예외
        --------
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.request('GET', f"/bots/get/{bot_id}", authorize=False)
        return Bot(Data.get('data', {}))

    async def getBots(self, page: int=1):
        r"""|coro|

        KoreanBots의 봇 리스트를 가져옵니다.

        파라미터
        -------------
        page: Optional[:class:`int`]
            봇 리스트의 페이지입니다. 기본값은 ``1``입니다.

        예외
        --------
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.request('GET', '/bots/get', authorize=False, params={'page': page})
        return [Bot(_) for _ in Data.get('data', [])]

    async def searchBots(self, query: str, page: int=1):
        r"""|coro|

        주어진 문자열로 KoreanBots 봇을 검색합니다.

        파라미터
        -------------
        query: :class:`str`
            검색할 봇의 이름
        page: Optional[:class:`int`]
            봇 리스트의 페이지입니다. 기본값은 ``1``입니다.

        예외
        --------
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.request('GET', '/bots/search', authorize=False, params={'q':query,  'page':page})
        return [Bot(_) for _ in Data.get('data', [])]

    async def getBotsByCategory(self, category: Category, page: int=1):
        r"""|coro|

        주어진 카테고리에 해당하는 KoreanBots 정보를 가져옵니다.

        파라미터
        -------------
        category: :class:`.Category`
            KoreanBots의 카테고리
        page: Optional[:class:`int`]
            봇 리스트의 페이지입니다. 기본값은 ``1``입니다.

        예외
        --------
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        if isinstance(category, Category):
            category = category.name
        Data = await self.request('GET', f"/bots/category/{category}", authorize=False, params={'page': page})
        return [Bot(_) for _ in Data.get('data', [])]