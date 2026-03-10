from dataclasses import dataclass, field

from ai_pnp.core.models.base import BaseModel


@dataclass
class Character(BaseModel):
    name: str = "Galdahn"
    ancestry: str = "Mensch"
    role: str = "Wanderer"
    level: int = 1
    hp_current: int = 10
    hp_max: int = 10
    inventory: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=lambda: ["Perception", "Diplomacy", "Stealth"])

    @classmethod
    def from_dict(cls, payload: dict | None) -> "Character":
        payload = payload or {}
        return cls(
            name=payload.get("name", "Galdahn"),
            ancestry=payload.get("ancestry", "Mensch"),
            role=payload.get("role", "Wanderer"),
            level=payload.get("level", 1),
            hp_current=payload.get("hp_current", 10),
            hp_max=payload.get("hp_max", 10),
            inventory=list(payload.get("inventory", [])),
            skills=list(payload.get("skills", ["Perception", "Diplomacy", "Stealth"])),
        )
