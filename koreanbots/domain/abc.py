from abc import ABC
from dataclasses import dataclass


from koreanbots.domain.deserializer import Deserializer
from koreanbots.domain.serializer import Serializer



@dataclass
class KoreanbotsEntity(ABC):
    pass


@dataclass
class SerializableEntity(KoreanbotsEntity, Serializer, Deserializer):
    pass
