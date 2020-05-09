from asyncio import sleep
from logging import getLogger
from .http import HTTPClient
from .errors import HTTPException
from .model import Category as CategoryModel
log = getLogger(__name__)

class Client:
    def __init__(self, Bot, Token, loop=None, postCount=True):
        self.Bot = Bot
        self.loop = loop or Bot.loop
        self.http = HTTPClient(Token, loop=loop)
        if postCount:
            self.loop.create_task(self.postCount())
    
    async def postCount(self):
        await self.Bot.wait_until_ready()
        while not self.Bot.is_closed():
            log.info('Autoposting guild count to koreanbots.')
            
            try:
                await self.postGuildCount()
            except HTTPException:
                pass
            await sleep(1800)
    
    async def postGuildCount(self):
        GuildCounts = len(self.Bot.guilds)
        await self.http.postGuildCount(GuildCounts)

    async def getVote(self, user_id: int):
        return await self.http.getVote(user_id)

    async def getBot(self, bot_id: int):
        return await self.http.getBot(bot_id)

    async def getBots(self, page: int=1):
        return await self.http.getBots(page)

    async def searchBots(self, query: str, page: int=1):
        return await self.http.searchBots(query, page)

    async def getBotsByCategory(self, category: CategoryModel, page: int=1):
        return await self.http.getBotsByCategory(category, page)