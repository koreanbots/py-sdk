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

from asyncio import get_event_loop, Event, sleep
from aiohttp import ClientSession
from datetime import datetime
from json import loads
from logging import getLogger
from io import BytesIO
from .errors import *
from .model import *
log = getLogger(__name__)

async def detectJson(response):
    try:
        return await response.json()
    except ValueError:
        return await response.text()

try:
    from cairosvg import svg2png
except:
    svg2png = None
    
class HTTPClient:
    r"""KoreanBots의 HTTP 클라이언트를 반환합니다.
    이 클래스는 KoreanBots API와 연결됩니다.

    일부 옵션이 HTTPClient에 전달될 수 있습니다.

    파라미터
    -----------
    Token: str
        KoreanBots의 토큰입니다.
    loop: 선택[asyncio.AbstractEventLoop]
        비동기를 사용하기 위한 asyncio.AbstractEventLoop입니다.
        기본값은 None이며, 기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.

    속성
    -----------
    loop: asyncio.AbstractEventLoop
        HTTP 리퀘스트에 사용되는 asyncio.AbstractEventLoop 클래스 입니다.
    """

    BASE = 'https://koreanbots.dev/api/v2'

    def __init__(self, bot_id: int, token=None, loop=None):
        self.loop = loop or get_event_loop()
        self.token = token
        self.id = bot_id

        self._globalLimit = Event()
        self._globalLimit.set()

    async def request(self, method, endpoint, authorize=True, **kwargs):
        r"""주어진 길드 수를 KoreanBots API로 보냅니다.

        파라미터
        -------------
        method: str
            HTTP 리퀘스트 메소드
        url: str
            KoreanBots API의 엔드포인트
        authorize: 선택[bool]
            API 리퀘스트에 토큰을 함께 전송할지 입니다.
            기본값은 True입니다.

        예외
        --------
        .errors.AuthorizeError
            토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다.
        .errors.Unauthrized
            인증되지 않았습니다, KoreanBots 토큰이 잘못되었을 수 있습니다.
        .errors.Forbidden
            접근 권한이 없습니다.
        .errors.NotFound
            찾을 수 없습니다, 파라미터를 확인하세요.
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        url = self.BASE + endpoint
        kwargs['headers'] = {"content-type":"application/json"}
        if authorize and self.token:
            kwargs['headers']['token'] = self.token
        elif authorize and not self.token:
            raise AuthorizeError('this endpoint required koreanbots token.')
        
        if not self._globalLimit.is_set():
            await self._globalLimit.wait()

        for tries in range(5):
            async with ClientSession() as session:
                async with session.request(method, url, **kwargs) as response:
                    log.debug(f'{method} {url} returned {response.status}')
                    Data = await detectJson(response)
                    
                    remainLimit = response.headers.get('x-ratelimit-remaining')
                    if remainLimit == 0 or response.status == 429:
                        resetLimitTimestamp = int(response.headers.get('x-ratelimit-reset'))
                        resetLimit = datetime.fromtimestamp(resetLimitTimestamp)

                        retryAfter = resetLimit - datetime.now()

                        log.warning(r"we're now rate limited. retrying after %.2f seconds", retryAfter.total_seconds())
                        if not endpoint == '/bot/servers':
                            self._globalLimit.clear()

                        await sleep(retryAfter.total_seconds())
                        if not endpoint == '/bot/servers':
                            self._globalLimit.set()

                        continue

                    if 200 <= response.status < 300:
                        return Data
                    
                    if response.status == 401:
                        raise Unauthorized(response, Data)
                    elif response.status == 403:
                        raise Forbidden(response, Data)
                    elif response.status == 404:
                        raise NotFound(response, Data)
                    else:
                        raise HTTPException(response, Data)
        raise HTTPException(response, Data)
                
    
    async def postGuildCount(self, guild_count: int):
        r"""주어진 길드 수를 KoreanBots API로 보냅니다.

        파라미터
        -------------
        guild_count: int
            전송할 길드의 수

        예외
        --------
        .errors.AuthorizeError
            토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다.
        .errors.Unauthrized
            인증되지 않았습니다, KoreanBots 토큰이 잘못되었을 수 있습니다.
        .errors.Forbidden
            접근 권한이 없습니다.
        .errors.NotFound
            찾을 수 없습니다, 파라미터를 확인하세요.
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        await self.request('POST', f'/bots/{self.id}/stats', json={'servers': guild_count})

    async def getVote(self, user_id: int):
        r"""주어진 유저ID의 하트 정보를 가져옵니다.

        파라미터
        -------------
        user_id: int
            정보를 가져올 유저의 ID

        예외
        --------
        .errors.AuthorizeError
            토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다.
        .errors.Unauthrized
            인증되지 않았습니다, KoreanBots 토큰이 잘못되었을 수 있습니다.
        .errors.Forbidden
            접근 권한이 없습니다.
        .errors.NotFound
            찾을 수 없습니다, 파라미터를 확인하세요.
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.request('GET', f"/bots/{self.id}/vote?userID={user_id}")
        return userVoted(Data)

    async def getBot(self, bot_id: int):
        r"""주어진 봇ID의 KoreanBots 정보를 가져옵니다.

        파라미터
        -------------
        bot_id: int
            정보를 가져올 봇의 ID

        예외
        --------
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.request('GET', f"/bots/{bot_id}", authorize=False)
        return Bot(Data.get('data', {}))

    async def getUser(self, user_id: int):
        r"""주어진 유저ID의 KoreanBots 정보를 가져옵니다.

        파라미터
        -------------
        user_id: int
            정보를 가져올 유저의 ID

        예외
        --------
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.request('GET', f"/users/{user_id}", authorize=False)
        return User(Data.get('data', {}))

    async def getBots(self, page: int=1):
        r"""KoreanBots의 봇 리스트를 가져옵니다.

        파라미터
        -------------
        page: 선택[int]
            봇 리스트의 페이지입니다. 기본값은 1입니다.

        예외
        --------
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.request('GET', '/list/bots/vote', authorize=False, params={'page': page})
        return [Bot(_) for _ in Data.get('data', [])]

    async def searchBots(self, query: str, page: int=1):
        r"""주어진 문자열로 KoreanBots 봇을 검색합니다.

        파라미터
        -------------
        query: str
            검색할 봇의 이름
        page: 선택[int]
            봇 리스트의 페이지입니다. 기본값은 1입니다.

        예외
        --------
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.request('GET', '/search/bots', authorize=False, params={'query':query,  'page':page})
        return [Bot(_) for _ in Data.get('data', [])]

    async def getBotsByCategory(self, category: Category, page: int=1):
        r"""주어진 카테고리에 해당하는 KoreanBots 정보를 가져옵니다.

        파라미터
        -------------
        category: .Category
            KoreanBots의 카테고리
        page: 선택[int]
            봇 리스트의 페이지입니다. 기본값은 1입니다.

        예외
        --------
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        if isinstance(category, Category):
            category = category.name
        Data = await self.request('GET', f"/bots/category/{category}", authorize=False, params={'page': page})
        return [Bot(_) for _ in Data.get('data', [])]
    
    async def getVoteWidget(self, bot_id: int):
        r"""주어진 봇ID의 투표 수 위젯(png)을 가져옵니다.

        파라미터
        -------------
        bot_id: int
            정보를 가져올 봇의 ID

        예외
        --------
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        if not svg2png:
            raise NotImplementedError
            
        URL = await self.getVoteWidgetURL(bot_id)

        async with ClientSession() as session:
            async with session.get(URL) as response:
                SVG = await response.read()
        
        fp = BytesIO()
        svg2png(bytestring=SVG, write_to=fp)
        fp.seek(0)

        return fp
    
    async def getVoteWidgetURL(self, bot_id: int):
        r"""주어진 봇ID의 투표 수 위젯 주소를 가져옵니다.

        파라미터
        -------------
        bot_id: int
            정보를 가져올 봇의 ID

        예외
        --------
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.getBot(bot_id)
        if not Data: return

        return f"{self.BASE}/widget/bots/votes/{bot_id}.svg"
    
    async def getServerWidgetURL(self, bot_id: int):
        r"""주어진 봇ID의 서버 수 위젯 주소를 가져옵니다.

        파라미터
        -------------
        bot_id: int
            정보를 가져올 봇의 ID

        예외
        --------
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        Data = await self.getBot(bot_id)
        if not Data: return

        return f"{self.BASE}/widget/bots/servers/{bot_id}.svg"
    
    async def getServerWidget(self, bot_id: int):
        r"""주어진 봇ID의 서버 수 위젯(png)을 가져옵니다.

        파라미터
        -------------
        bot_id: int
            정보를 가져올 봇의 ID

        예외
        --------
        .errors.HTTPException
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        if not svg2png:
            raise NotImplementedError
        
        URL = await self.getServerWidgetURL(bot_id)

        async with ClientSession() as session:
            async with session.get(URL) as response:
                SVG = await response.read()
        
        fp = BytesIO()
        svg2png(bytestring=SVG, write_to=fp)
        fp.seek(0)

        return fp
