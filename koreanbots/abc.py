from abc import ABCMeta, abstractmethod
from typing import Any, Dict


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
