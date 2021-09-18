from abc import abstractmethod, ABCMeta
from typing import Any, Dict, List, Optional


class KoreanbotsABC(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, **response_data: Any) -> None:
        self.response_data = response_data

    @property
    @abstractmethod
    def code(self) -> int:
        return self.response_data.get("code", 0)

    @property
    @abstractmethod
    def version(self) -> int:
        return self.response_data.get("version", 0)

    @property
    @abstractmethod
    def data(self) -> Dict[str, Any]:
        return self.response_data.get("data", {})


class DiscordABC(metaclass=ABCMeta):
    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def wait_until_ready(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_closed(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def guilds(self) -> List["DiscordGuildABC"]:
        raise NotImplementedError

    @property
    @abstractmethod
    def user(self) -> Optional["DiscordUserABC"]:
        raise NotImplementedError

    @property
    @abstractmethod
    def shard_count(self) -> Optional[int]:
        raise NotImplementedError


class DiscordUserABC(metaclass=ABCMeta):
    @property
    @abstractmethod
    def id(self) -> int:
        raise NotImplementedError


class DiscordGuildABC(metaclass=ABCMeta):
    ...
