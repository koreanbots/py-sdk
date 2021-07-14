from typing import Any, Callable, Coroutine, Literal, TypeVar

CORO = TypeVar("CORO", bound=Callable[..., Coroutine[Any, Any, Any]])

WidgetType = Literal["votes", "servers", "status"]

WidgetStyle = Literal["classic", "flat"]

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

Status = Literal[
    "online",
    "idle",
    "dnd",
    "streaming",
    "offline",
]

State = Literal[
    "ok",
    "reported",
    "blocked",
    "private",
    "archived",
]
