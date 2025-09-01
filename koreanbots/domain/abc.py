from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T", bound="KoreanbotsEntity")


@dataclass(frozen=True)
class KoreanbotsEntity(ABC):
    pass


@dataclass(frozen=True)
class KoreanbotsResponse(KoreanbotsEntity, Generic[T]):
    code: int
    version: str
    data: T
