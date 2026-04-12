from dataclasses import dataclass
from typing import Literal

from koreanbots.domain.abc import SerializableEntity

Category = Literal[
    "관리",
    "뮤직",
    "전적",
    "게임",
    "도박",
    "로깅",
    "빗금 명령어",
    "웹 대시보드",
    "밈",
    "레벨링",
    "유틸리티",
    "대화",
    "NSFW",
    "검색",
    "학교",
    "코로나19",
    "번역",
    "오버워치",
    "리그 오브 레전드",
    "배틀그라운드",
    "마인크래프트",
]

Status = Literal["online", "idle", "dnd", "streaming", "offline"]

State = Literal["ok", "reported", "blocked", "private", "archived"]


@dataclass
class AbstractBot(SerializableEntity):
    id: str
    name: str
    tag: str
    avatar: str | None
    flags: int
    lib: str
    prefix: str
    votes: int
    servers: int | None
    shards: int | None
    intro: str
    desc: str
    web: str | None
    git: str | None
    url: str | None
    discord: str | None
    category: list[Category]
    vanity: str | None
    bg: str | None
    banner: str | None
    status: Status | None
    state: State
    enforcements: list[str]


@dataclass
class BotWithOwnerID(AbstractBot):
    owners: list[str]
