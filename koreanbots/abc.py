import abc
from typing import Any, Dict


class KoreanbotsABC(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, **response_data: Any) -> None:
        self.response_data = response_data

    @abc.abstractproperty
    def code(self) -> int:
        return self.response_data.get("code", 0)

    @abc.abstractproperty
    def version(self) -> int:
        return self.response_data.get("version", 0)

    @abc.abstractproperty
    def data(self) -> Dict[str, Any]:
        return self.response_data.get("data", {})
