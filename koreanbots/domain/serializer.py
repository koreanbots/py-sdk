from dataclasses import asdict, dataclass


@dataclass
class Serializer:
    def to_dict(self):
        return asdict(self)
