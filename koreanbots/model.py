from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Optional, TypeVar

from .typing import Category, State, Status


class KoreanbotsResponseABC(ABC): ...


T = TypeVar("T", bound=KoreanbotsResponseABC)


@dataclass(frozen=True)
class KoreanbotsResponse(Generic[T]):
    code: int
    """상태 코드"""
    version: int
    """버전"""
    data: T


@dataclass(eq=True, frozen=True)
class KoreanbotsBot(KoreanbotsResponseABC):
    """
    봇의 정보를 가져왔을때 반환되는 인스턴스입니다.
    """

    id: Optional[str] = field(repr=True, compare=True, default=None)
    """아이디"""
    name: Optional[str] = field(repr=True, compare=False, default=None)
    """이름"""
    tag: Optional[str] = field(repr=False, compare=False, default=None)
    """태그"""
    avatar: Optional[str] = field(repr=False, compare=False, default=None)
    """아바타"""
    flags: int = field(repr=False, compare=False, default=0)
    """플래그"""
    lib: Optional[str] = field(repr=False, compare=False, default=None)
    """라이브러리"""
    prefix: Optional[str] = field(repr=False, compare=False, default=None)
    """프리픽스"""
    votes: int = field(repr=False, compare=False, default=0)
    """투표 수"""
    servers: int = field(repr=False, compare=False, default=0)
    """서버 수"""
    shards: int = field(repr=False, compare=False, default=0)
    """샤드 수"""
    intro: Optional[str] = field(repr=False, compare=False, default=None)
    """소개 문구"""
    desc: Optional[str] = field(repr=False, compare=False, default=None)
    """설명 문구"""
    web: Optional[str] = field(repr=False, compare=False, default=None)
    """웹사이트 주소"""
    git: Optional[str] = field(repr=False, compare=False, default=None)
    """깃 주소"""
    url: Optional[str] = field(repr=False, compare=False, default=None)
    """주소"""
    discord: Optional[str] = field(repr=False, compare=False, default=None)
    """디스코드 주소"""
    category: Optional[Category] = field(repr=False, compare=False, default=None)
    """카테고리"""
    vanity: Optional[str] = field(repr=False, compare=False, default=None)
    """가상 주소"""
    bg: Optional[str] = field(repr=False, compare=False, default=None)
    """배경 이미지 주소"""
    banner: Optional[str] = field(repr=False, compare=False, default=None)
    """배너 이미지 주소"""
    status: Optional[Status] = field(repr=False, compare=False, default=None)
    """상태"""
    state: Optional[State] = field(repr=False, compare=False, default=None)
    """Koreanbots에서의 상태"""


@dataclass(eq=True, frozen=True)
class KoreanbotsUser(KoreanbotsResponseABC):
    """
    유저 정보를 가져왔을때 반환되는 클래스입니다.
    """

    id: int = field(repr=True, compare=True, default=0)
    """아이디"""
    username: str = field(repr=True, compare=False, default="")
    """유저 이름"""
    globalName: str = field(repr=True, compare=False, default="")
    """유저 글로벌 이름"""
    tag: str = field(repr=False, compare=False, default="")
    """태그"""
    github: Optional[str] = field(repr=False, compare=False, default=None)
    """Github 주소"""
    flags: int = field(repr=False, compare=False, default=0)
    """플래그"""


@dataclass(eq=True, frozen=True)
class KoreanbotsServer(KoreanbotsResponseABC):
    """
    서버 정보를 가져왔을때 반환되는 클래스입니다.
    """

    id: int = field(repr=True, compare=True, default=0)
    """ID"""
    name: str = field(repr=True, compare=False, default="")
    """서버 이름"""
    flags: int = field(repr=False, compare=False, default=0)
    """플래그"""
    intro: Optional[str] = field(repr=False, compare=False, default=None)
    """소개문구"""
    desc: Optional[str] = field(repr=False, compare=False, default=None)
    """설명문구"""
    votes: int = field(repr=True, compare=False, default=0)
    """투표수"""
    category: Optional[Category] = field(repr=False, compare=False, default=None)
    """카테고리"""
    invite: str = field(repr=False, compare=False, default="")
    """초대링크"""
    state: Optional[State] = field(repr=False, compare=False, default=None)
    """Koreanbots에서의 상태"""
    vanity: Optional[str] = field(repr=False, compare=False, default=None)
    """서버의 가상 주소"""
    bg: Optional[str] = field(repr=False, compare=False, default=None)
    """배경 이미지 주소"""
    banner: Optional[str] = field(repr=False, compare=False, default=None)
    """배너 이미지 주소"""
    icon: Optional[str] = field(repr=False, compare=False, default=None)
    """아이콘"""
    members: int = field(repr=False, compare=False, default=0)
    """멤버 수"""
    emojis: List["Emoji"] = field(repr=False, compare=False, default_factory=list)
    """Emoji 인스턴스를 담고 있는 리스트"""
    boostTier: int = field(repr=False, compare=False, default=0)
    """부스트 레벨"""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KoreanbotsServer":
        return cls(
            id=data["id"],
            name=data["name"],
            flags=data["flags"],
            intro=data.get("intro"),
            desc=data.get("desc"),
            votes=data["votes"],
            category=data.get("category"),
            invite=data["invite"],
            state=data.get("state"),
            vanity=data.get("vanity"),
            bg=data.get("bg"),
            banner=data.get("banner"),
            icon=data.get("icon"),
            members=data["members"],
            emojis=[
                Emoji(id=e["id"], name=e["name"], url=e["url"]) for e in data["emojis"]
            ],
            boostTier=data["boostTier"],
        )


@dataclass(eq=True, frozen=True)
class CircularKoreanbotsBot(KoreanbotsBot):
    owners: List[str] = field(repr=False, compare=False, default_factory=list)


@dataclass(eq=True, frozen=True)
class CircularKoreanbotsUser(KoreanbotsUser):
    bots: List[str] = field(repr=False, compare=False, default_factory=list)
    servers: List[str] = field(repr=False, compare=False, default_factory=list)


@dataclass(eq=True, frozen=True)
class CircularKoreanbotsServer(KoreanbotsServer):
    owner: str = field(repr=False, compare=False, default="")


@dataclass(eq=True, frozen=True)
class KoreanbotsUserResponse(KoreanbotsUser):
    bots: List["CircularKoreanbotsBot"] = field(
        repr=False, compare=False, default_factory=list
    )
    servers: List[CircularKoreanbotsServer] = field(
        repr=False, compare=False, default_factory=list
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KoreanbotsUserResponse":
        return cls(
            id=data["id"],
            username=data["username"],
            globalName=data["globalName"],
            tag=data["tag"],
            github=data.get("github"),
            flags=data["flags"],
            servers=[
                CircularKoreanbotsServer(
                    id=s["id"],
                    name=s["name"],
                    flags=s["flags"],
                    intro=s.get("intro"),
                    desc=s.get("desc"),
                    votes=s["votes"],
                    category=s.get("category"),
                    invite=s["invite"],
                    state=s.get("state"),
                    vanity=s.get("vanity"),
                    bg=s.get("bg"),
                    banner=s.get("banner"),
                    icon=s.get("icon"),
                    members=s["members"],
                    emojis=[
                        Emoji(id=e["id"], name=e["name"], url=e["url"])
                        for e in s["emojis"]
                    ],
                    boostTier=s["boostTier"],
                    owner=s["owner"],
                )
                for s in data["servers"]
            ],
            bots=[
                CircularKoreanbotsBot(
                    id=b["id"],
                    name=b["name"],
                    tag=b["tag"],
                    avatar=b["avatar"],
                    flags=b["flags"],
                    lib=b["lib"],
                    prefix=b["prefix"],
                    votes=b["votes"],
                    servers=b["servers"],
                    shards=b["shards"],
                    intro=b.get("intro"),
                    desc=b.get("desc"),
                    web=b.get("web"),
                    git=b.get("git"),
                    url=b.get("url"),
                    discord=b.get("discord"),
                    category=b.get("category"),
                    vanity=b.get("vanity"),
                    bg=b.get("bg"),
                    banner=b.get("banner"),
                    status=b.get("status"),
                    state=b.get("state"),
                    owners=b["owners"],
                )
                for b in data["bots"]
            ],
        )


@dataclass(eq=True, frozen=True)
class KoreanbotsBotResponse(KoreanbotsBot):
    owners: List["CircularKoreanbotsUser"] = field(
        repr=False, compare=False, default_factory=list
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KoreanbotsBotResponse":
        return cls(
            id=data["id"],
            name=data["name"],
            tag=data["tag"],
            avatar=data["avatar"],
            flags=data["flags"],
            lib=data["lib"],
            prefix=data["prefix"],
            votes=data["votes"],
            servers=data["servers"],
            shards=data["shards"],
            intro=data.get("intro"),
            desc=data.get("desc"),
            web=data.get("web"),
            git=data.get("git"),
            url=data.get("url"),
            discord=data.get("discord"),
            category=data.get("category"),
            vanity=data.get("vanity"),
            bg=data.get("bg"),
            banner=data.get("banner"),
            status=data.get("status"),
            state=data.get("state"),
            owners=[
                CircularKoreanbotsUser(
                    id=o["id"],
                    username=o["username"],
                    globalName=o["globalName"],
                    tag=o["tag"],
                    github=o.get("github"),
                    flags=o["flags"],
                    bots=o["bots"],
                )
                for o in data["owners"]
            ],
        )


@dataclass(eq=True, frozen=True)
class KoreanbotsServerResponse(KoreanbotsServer):
    owner: "CircularKoreanbotsUser" = field(
        repr=False, compare=False, default=CircularKoreanbotsUser()
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KoreanbotsServerResponse":
        return cls(
            id=data["id"],
            name=data["name"],
            flags=data["flags"],
            intro=data.get("intro"),
            desc=data.get("desc"),
            votes=data["votes"],
            category=data.get("category"),
            invite=data["invite"],
            state=data.get("state"),
            vanity=data.get("vanity"),
            bg=data.get("bg"),
            banner=data.get("banner"),
            icon=data.get("icon"),
            members=data["members"],
            emojis=[
                Emoji(id=e["id"], name=e["name"], url=e["url"]) for e in data["emojis"]
            ],
            boostTier=data["boostTier"],
            owner=CircularKoreanbotsUser(
                id=data["owner"]["id"],
                username=data["owner"]["username"],
                globalName=data["owner"]["globalName"],
                tag=data["owner"]["tag"],
                github=data["owner"].get("github"),
                flags=data["owner"]["flags"],
                bots=data["owner"]["bots"],
                servers=data["owner"]["servers"],
            ),
        )


@dataclass(eq=True, frozen=True)
class Emoji:
    """
    이모지 정보를 가져왔을때 반환되는 클래스입니다.
    """

    id: int = field(repr=True, compare=True, default=0)
    """ID"""
    name: str = field(repr=True, compare=False, default="")
    """이모지 이름"""
    url: str = field(repr=False, compare=False, default="")
    """이모지 url"""


@dataclass(eq=True, frozen=True)
class KoreanbotsVoteResponse(KoreanbotsResponseABC):
    voted: bool = field(repr=True, compare=True, default=False)
    """투표 여부"""
    last_vote: int = field(repr=True, compare=True, default=0)
    """마지막으로 투표한 일자"""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KoreanbotsVoteResponse":
        return cls(voted=data["voted"], last_vote=data["lastVote"])
