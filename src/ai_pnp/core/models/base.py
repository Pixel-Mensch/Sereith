from dataclasses import asdict, dataclass

@dataclass
class BaseModel:
    def to_dict(self) -> dict:
        return asdict(self)
