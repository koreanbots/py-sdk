import abc
from typing import Any, Dict, List, Optional


class KoreanbotsABC(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, **response_data: Any) -> None:
        self.response_data = response_data

    @abc.abstractproperty
    def code(self) -> int:
        return self.response_data.get("code", 0)

    @abc.abstractproperty
    def version(self) -> int:
        return self.response_data.get("version", 0)

    @abc.abstractproperty
    def data(self) -> Dict[str, Any]:
        return self.response_data.get("data", {})


class DiscordABC(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def wait_until_ready(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def is_closed(self) -> bool:
        raise NotImplementedError

    @abc.abstractproperty
    def guilds(self) -> List["DiscordGuildABC"]:
        raise NotImplementedError

    @abc.abstractproperty
    def user(self) -> Optional["DiscordUserABC"]:
        raise NotImplementedError

    @abc.abstractproperty
    def shard_count(self) -> Optional[int]:
        raise NotImplementedError


class DiscordUserABC(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def id(self) -> int:
        raise NotImplementedError


class DiscordGuildABC(metaclass=abc.ABCMeta):
    ...
