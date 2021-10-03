from abc import ABCMeta, abstractmethod
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


class DpyABC(metaclass=ABCMeta):
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
    def guilds(self) -> List["DpyGuildABC"]:
        raise NotImplementedError

    @property
    @abstractmethod
    def user(self) -> Optional["DpyUserABC"]:
        raise NotImplementedError

    @property
    @abstractmethod
    def shard_count(self) -> Optional[int]:
        raise NotImplementedError


class DpyUserABC(metaclass=ABCMeta):
    @property
    @abstractmethod
    def id(self) -> int:
        raise NotImplementedError


class DpyGuildABC(metaclass=ABCMeta):
    ...


class DicoABC(metaclass=ABCMeta):
    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def wait_ready(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_closed(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def guild_count(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def shard_count(self) -> Optional[int]:
        raise NotImplementedError

    @property
    @abstractmethod
    def application_id(self) -> Optional[int]:
        raise NotImplementedError
