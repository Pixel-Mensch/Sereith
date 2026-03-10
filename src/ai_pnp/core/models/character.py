from dataclasses import dataclass, field
from ai_pnp.core.models.base import BaseModel

@dataclass
class Character(BaseModel):
    name: str = "Galdahn"
    ancestry: str = "Human"
    role: str = "Wanderer"
    level: int = 1
    hp_current: int = 10
    hp_max: int = 10
    inventory: list[str] = field(default_factory=list)
    known_skills: list[str] = field(default_factory=lambda: ["Perception", "Diplomacy"])
