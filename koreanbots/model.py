from typing import Any, Dict, List, Optional

from .abc import KoreanbotsABC
from .typing import Category, State, Status


class BaseKoreanbots(KoreanbotsABC):
    def __init__(self, **response_data: Any) -> None:
        self.response_data = response_data

    @property
    def code(self) -> int:
        return self.response_data.pop("code", 0)

    @property
    def version(self) -> int:
        return self.response_data.pop("version", 0)

    @property
    def data(self) -> Dict[str, Any]:
        return self.response_data.pop("data", {})


class KoreanbotsBot(BaseKoreanbots):
    def __init__(self, **response_data: Any) -> None:
        super().__init__(**response_data)

    @property
    def id(self) -> str:
        return self.data.pop("id", "")

    @property
    def name(self) -> str:
        return self.data.pop("name", "")

    @property
    def tag(self) -> str:
        return self.data.pop("tag", "")

    @property
    def avatar(self) -> Optional[str]:
        return self.data.pop("avatar", None)

    @property
    def owners(self) -> List[Dict[str, Any]]:
        return self.data.pop("owners", [])

    @property
    def flags(self) -> int:
        return self.data.pop("flags", 0)

    @property
    def lib(self) -> str:
        return self.data.pop("lib", "")

    @property
    def prefix(self) -> str:
        return self.data.pop("prefix", "")

    @property
    def votes(self) -> int:
        return self.data.pop("votes", 0)

    @property
    def servers(self) -> int:
        return self.data.pop("servers", 0)

    @property
    def intro(self) -> str:
        return self.data.pop("intro", "")

    @property
    def desc(self) -> str:
        return self.data.pop("desc", "")

    @property
    def web(self) -> Optional[str]:
        return self.data.pop("web", None)

    @property
    def git(self) -> Optional[str]:
        return self.data.pop("git", None)

    @property
    def url(self) -> Optional[str]:
        return self.data.pop("url", None)

    @property
    def discord(self) -> Optional[str]:
        return self.data.pop("discord", None)

    @property
    def category(self) -> Category:
        return self.data.pop("category", None)

    @property
    def vanity(self) -> Optional[str]:
        return self.data.pop("vanity", None)

    @property
    def bg(self) -> Optional[str]:
        return self.data.pop("bg", None)

    @property
    def banner(self) -> Optional[str]:
        return self.data.pop("banner", None)

    @property
    def status(self) -> Optional[Status]:
        return self.data.pop("status", None)

    @property
    def state(self) -> Optional[State]:
        return self.data.pop("state", None)


class KoreanbotsUser(BaseKoreanbots):
    def __init__(self, **response_data: Any) -> None:
        super().__init__(**response_data)

    @property
    def id(self) -> int:
        return self.data.pop("id", 0)

    @property
    def username(self) -> str:
        return self.data.pop("username", "")

    @property
    def tag(self) -> str:
        return self.data.pop("tag", "")

    @property
    def github(self) -> Optional[str]:
        return self.data.pop("github", None)

    @property
    def flags(self) -> int:
        return self.data.pop("flags", 0)

    @property
    def bots(self) -> List[Any]:
        return self.data.pop("bots", [])