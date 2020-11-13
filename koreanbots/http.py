import aiohttp
import asyncio
from .errors import *
import logging
import datetime

log = logging.getLogger(__name__)


class HTTPClient:
    BASE: str = "https://beta.koreanbots.dev/api/v2"

    def __init__(
        self, token: str = None, loop: asyncio.AbstractEventLoop = None
    ) -> None:
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.token: token = token

        self.globalLimit: asyncio.Event = asyncio.Event()
        self.globalLimit.set()

    async def request(
        self, method: str, endpoint: str, authorize: bool = True, **kwargs
    ) -> dict:
        url: str = self.BASE + endpoint

        if "headers" not in kwargs:
            kwargs["headers"] = {}

        kwargs["headers"]["content-type"] = "application/json"

        if authorize:
            if self.token:
                kwargs["headers"]["token"] = self.token
            else:
                raise AuthorizeError("This endpoint required koreanbots token.")

        if not self.globalLimit.is_set():
            await self.globalLimit.wait()

        for _ in range(5):
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as resp:
                    log.debug(f"{method} {url} returned {resp.status}")

                    try:
                        Data: dict = await resp.json()
                    except ValueError:
                        Data: str = await resp.text()

                    limitRemain: int = resp.headers.get("x-ratelimit-remaining")
                    if limitRemain == 0 or resp.status == 429:
                        limitResetTimestamp: int = int(
                            resp.headers.get("x-ratelimit-reset")
                        )
                        limitReset: datetime.datetime = datetime.datetime.fromtimestamp(
                            limitResetTimestamp
                        )

                        retryAfter: datetime.timedelta = limitReset - datetime.now()

                        log.warning(
                            r"we're now rate limited. retrying after %.2f seconds",
                            retryAfter.total_seconds(),
                        )

                        self.globalLimit.clear()
                        await asyncio.sleep(retryAfter.total_seconds())
                        self.globalLimit.set()

                        continue
                    elif resp.status == 500:
                        continue

                    if 200 <= resp.status < 300:
                        return Data

                    if resp.status == 401:
                        raise Unauthorized(resp, Data)
                    elif resp.status == 403:
                        raise Forbidden(resp, Data)
                    elif resp.status == 404:
                        raise NotFound(resp, Data)
                    else:
                        raise HTTPException(resp, Data)

        raise RequestFailedError

    async def graphql(self, Query: str) -> dict:
        Data: dict = await self.request("POST", "/graphql", json={"query": Query})

        if "errors" in Data:
            Error: dict = Data["errors"][0]

            raise GraphQLError(f"{Error['err_type']}: {Error['message']}")

        return Data["data"]

    async def postGuildCount(self, guildCount: int) -> dict:
        payload: str = f"""
            mutation{{
                bot(servers: {guildCount}) {{
                    id
                    servers
                }}
            }}
        """

        return await self.graphql(payload)

    async def getVote(self, userId: int) -> dict:
        raise NotImplementedError

    async def getBot(self, botId: int) -> dict:
        payload: str = f"""
            query{{
                bot(id: "{botId}") {{
                    id
                    lib
                    prefix
                    name
                    servers
                    votes
                    intro
                    desc
                    avatar
                    url
                    web
                    git
                    category
                    tag
                    discord
                    state
                    verified
                    trusted
                    boosted
                    partnered
                    vanity
                    banner
                    status
                    bg
                    owners {{
                        id
                        avatar
                        tag
                        username
                        perm
                        github
                        bots {{
                            id
                        }}
                    }}
                }}
            }}
        """

        return await self.graphql(payload)

    async def list(self, type: str, query: str = None, page: int = 1) -> dict:
        type: str = type.upper()

        if type not in ["VOTE", "NEW", "TRUSTED", "PARTNERED", "SEARCH", "CATEGORY"]:
            raise ValueError("Unexpected type.")

        if type == "SEARCH" and not query:
            raise TypeError("`SEARCH` type needs `query`.")

        if not query:
            query: str = ""

        payload: str = f"""
            query{{
                list(type: {type}, page: {page}, query: "{query}") {{
                    data {{
                        id
                        lib
                        prefix
                        name
                        servers
                        votes
                        intro
                        desc
                        avatar
                        url
                        web
                        git
                        category
                        tag
                        discord
                        state
                        verified
                        trusted
                        boosted
                        partnered
                        vanity
                        banner
                        status
                        bg
                        owners {{
                            id
                            avatar
                            tag
                            username
                            perm
                            github
                            bots {{
                                id
                            }}
                        }}
                    }}
                    currentPage
                    totalPage
                }}
            }}
        """

        return await self.graphql(payload)