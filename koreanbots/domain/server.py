from dataclasses import dataclass
from typing import Literal

from koreanbots.domain.abc import KoreanbotsEntity

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


@dataclass(frozen=True)
class Emoji(KoreanbotsEntity):
    id: str
    name: str
    url: str


@dataclass(frozen=True)
class AbstractServer(KoreanbotsEntity):
    """
    FIELD	TYPE	DESCRIPTION
    id	string	서버의 ID
    name	string	서버의 디스코드 유저네임
    icon	?string	서버의 아바타 해시
    owner	User	서버의 소유자
    flags	integer	서버의 플래그
    votes	integer	서버의 하트 수
    members	integer	서버의 유저 수
    boostTier	integer	서버의 부스트 티어 (0~3)
    intro	string	서버의 짧은 설명
    desc	string	서버의 긴 설명
    category	Category[]	서버의 카테고리
    invite	string	서버의 초대코드
    emojis	Emoji[]	서버의 이모지
    vanity	?string	서버의 VANITY URL
    bg	?string	서버의 배경 이미지 주소
    banner	?string	서버의 배너 이미지 주소
    state	State	한국 디스코드 리스트에서의 서버의 상태
    """

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
    vanity: str | None
    bg: str | None
    banner: str | None
    state: State


@dataclass(frozen=True)
class ServerWithOwnerID(AbstractServer):
    owner: str
