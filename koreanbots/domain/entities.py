from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from koreanbots.domain.abc import SerializableEntity
from koreanbots.domain.bot import AbstractBot, BotWithOwnerID
from koreanbots.domain.server import AbstractServer, ServerWithOwnerID
from koreanbots.domain.user import AbstractUser

T = TypeVar("T")


@dataclass
class User(AbstractUser):
    bots: list[BotWithOwnerID]
    servers: list[ServerWithOwnerID]


@dataclass
class Server(AbstractServer):
    owner: User


@dataclass
class Bot(AbstractBot):
    owners: list[User]


@dataclass
class Vote(SerializableEntity):
    voted: bool
    lastVote: int


@dataclass
class KoreanbotsResponse:
    code: int
    version: int


@dataclass
class KoreanbotsMessageResponse(KoreanbotsResponse):
    message: str


@dataclass
class KoreanbotsDataResponse(KoreanbotsResponse, Generic[T]):
    data: T

    @classmethod
    def from_bot(
        cls, code: int, version: int, data: dict[str, Any]
    ) -> "KoreanbotsDataResponse[Bot]":
        return KoreanbotsDataResponse(
            code=code,
            version=version,
            data=Bot.from_dict(data),
        )

    @classmethod
    def from_list_bot(
        cls, code: int, version: int, data: list[dict[str, Any]]
    ) -> "KoreanbotsDataResponse[list[Bot]]":
        return KoreanbotsDataResponse(
            code=code,
            version=version,
            data=[Bot.from_dict(item) for item in data],
        )

    @classmethod
    def from_user(
        cls, code: int, version: int, data: dict[str, Any]
    ) -> "KoreanbotsDataResponse[User]":
        return KoreanbotsDataResponse(
            code=code,
            version=version,
            data=User.from_dict(data),
        )

    @classmethod
    def from_list_user(
        cls, code: int, version: int, data: list[dict[str, Any]]
    ) -> "KoreanbotsDataResponse[list[User]]":
        return KoreanbotsDataResponse(
            code=code,
            version=version,
            data=[User.from_dict(item) for item in data],
        )

    @classmethod
    def from_server(
        cls, code: int, version: int, data: dict[str, Any]
    ) -> "KoreanbotsDataResponse[Server]":
        return KoreanbotsDataResponse(
            code=code,
            version=version,
            data=Server.from_dict(data),
        )

    @classmethod
    def from_list_server(
        cls, code: int, version: int, data: list[dict[str, Any]]
    ) -> "KoreanbotsDataResponse[list[Server]]":
        return KoreanbotsDataResponse(
            code=code,
            version=version,
            data=[Server.from_dict(item) for item in data],
        )

    @classmethod
    def from_vote(
        cls, code: int, version: int, data: dict[str, Any]
    ) -> "KoreanbotsDataResponse[Vote]":
        return KoreanbotsDataResponse(
            code=code,
            version=version,
            data=Vote.from_dict(data),
        )
