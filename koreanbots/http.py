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
    BASE = 'https://api.koreanbots.cf'

    def __init__(self, token=None, loop=None):
        self.loop = loop or get_event_loop()
        self.token = token

    async def request(self, method, url, authorize=True, **kwargs):
        url = BASE + url
        kwargs['headers'] = {"content-type":"application/json"}
        if authorize:
            kwargs['headers']['token'] = self.token
        
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
        await self.request('POST', '/bots/servers', json={'servers': guild_count})

    async def getVote(self, user_id: int):
        Data = await self.request('GET', f"/bots/voted/{user_id}")
        return userVoted(Data)

    async def getBot(self, bot_id: int):
        Data = await self.request('GET', f"/bots/get/{bot_id}", authorize=False)
        return Bot(Data.get('data', {}))

    async def getBots(self, page: int=1):
        Data = await self.request('GET', '/bots/get', authorize=False, params={'page': page})
        return [Bot(_) for _ in Data.get('data', [])]

    async def searchBots(self, query: str, page: int=1):
        Data = await self.request('GET', '/bots/search', authorize=False, params={'q':query,  'page':page})
        return [Bot(_) for _ in Data.get('data', [])]

    async def getBotsByCategory(self, category: Category, page: int=1):
        if isinstance(category, Category):
            category = category.name
        Data = await self.request('GET', f"/bots/category/{category}", authorize=False, params={'page': page})
        return [Bot(_) for _ in Data.get('data', [])]