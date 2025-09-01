from dataclasses import dataclass
from typing import Literal

from koreanbots.domain.abc import SerializableEntity

Category = Literal[
    "커뮤니티",
    "IT & 과학",
    "봇",
    "친목",
    "음악",
    "교육",
    "연애",
    "게임",
    "오버워치",
    "리그 오브 레전드",
    "배틀그라운드",
    "마인크래프트",
]

State = Literal["ok", "reported", "blocked", "unreachable"]


@dataclass
class Emoji(SerializableEntity):
    id: str
    name: str
    url: str


@dataclass
class AbstractServer(SerializableEntity):
    id: str
    name: str
    icon: str | None
    flags: int
    votes: int
    members: int
    boostTier: int
    intro: str
    desc: str
    category: list[Category]
    invite: str
    emojis: list[Emoji]
    state: State
    vanity: str | None
    bg: str | None
    banner: str | None


@dataclass
class ServerWithOwnerID(AbstractServer):
    owner: str
