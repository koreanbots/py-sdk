from typing import Any, Dict, List, Optional, Union

from .abc import KoreanbotsABC
from .typing import Category, State, Status


class BaseKoreanbots(KoreanbotsABC):
    def __init__(self, **response_data: Any) -> None:
        self.response_data = response_data

    @property
    def code(self) -> int:
        return self.response_data.get("code", 0)

    @property
    def version(self) -> int:
        return self.response_data.get("version", 0)

    @property
    def data(self) -> Dict[str, Any]:
        return self.response_data.get("data", {})


class KoreanbotsBot(BaseKoreanbots):
    def __init__(
        self,
        call_in_user: bool = False,
        **response_data: Any,
    ) -> None:
        super().__init__(**response_data)
        self.call_in_user = call_in_user

    @property
    def id(self) -> str:
        return self.data.get("id", "")

    @property
    def name(self) -> str:
        return self.data.get("name", "")

    @property
    def tag(self) -> str:
        return self.data.get("tag", "")

    @property
    def avatar(self) -> Optional[str]:
        return self.data.get("avatar", None)

    @property
    def owners(self) -> Union[List["KoreanbotsUser"], List[str]]:
        if self.call_in_user:
            return self.response_data.get("owners", [])

        return list(
            map(
                lambda user: KoreanbotsUser(True, **user),
                self.data.get("owners", []),
            )
        )

    @property
    def flags(self) -> int:
        return self.data.get("flags", 0)

    @property
    def lib(self) -> str:
        return self.data.get("lib", "")

    @property
    def prefix(self) -> str:
        return self.data.get("prefix", "")

    @property
    def votes(self) -> int:
        return self.data.get("votes", 0)

    @property
    def servers(self) -> int:
        return self.data.get("servers", 0)

    @property
    def intro(self) -> str:
        return self.data.get("intro", "")

    @property
    def desc(self) -> str:
        return self.data.get("desc", "")

    @property
    def web(self) -> Optional[str]:
        return self.data.get("web", None)

    @property
    def git(self) -> Optional[str]:
        return self.data.get("git", None)

    @property
    def url(self) -> Optional[str]:
        return self.data.get("url", None)

    @property
    def discord(self) -> Optional[str]:
        return self.data.get("discord", None)

    @property
    def category(self) -> Category:
        return self.data.get("category", None)

    @property
    def vanity(self) -> Optional[str]:
        return self.data.get("vanity", None)

    @property
    def bg(self) -> Optional[str]:
        return self.data.get("bg", None)

    @property
    def banner(self) -> Optional[str]:
        return self.data.get("banner", None)

    @property
    def status(self) -> Optional[Status]:
        return self.data.get("status", None)

    @property
    def state(self) -> State:
        return self.data.get("state", None)


class KoreanbotsUser(BaseKoreanbots):
    def __init__(self, call_in_bots: bool = False, **response_data: Any) -> None:
        super().__init__(**response_data)
        self.call_in_bots = call_in_bots

    @property
    def id(self) -> int:
        return self.data.get("id", 0)

    @property
    def username(self) -> str:
        return self.data.get("username", "")

    @property
    def tag(self) -> str:
        return self.data.get("tag", "")

    @property
    def github(self) -> Optional[str]:
        return self.data.get("github", None)

    @property
    def flags(self) -> int:
        return self.data.get("flags", 0)

    @property
    def bots(
        self,
    ) -> Union[List[KoreanbotsBot], List[str]]:
        if self.call_in_bots:
            return self.response_data.get("bots", [])

        return list(
            map(
                lambda bot: KoreanbotsBot(True, **bot),
                self.data.get("bots", []),
            )
        )