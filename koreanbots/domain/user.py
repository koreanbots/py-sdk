from dataclasses import dataclass

from koreanbots.domain.abc import SerializableEntity


@dataclass
class AbstractUser(SerializableEntity):
    id: str
    username: str
    tag: str
    github: str | None
    flags: int
