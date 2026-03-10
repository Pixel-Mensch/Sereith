from dataclasses import dataclass, field

from ai_pnp.core.models.base import BaseModel
from ai_pnp.core.models.character import Character
from ai_pnp.core.models.quest import Quest
from ai_pnp.core.models.world_state import WorldState


@dataclass
class GameState(BaseModel):
    save_name: str = "autosave"
    player: Character = field(default_factory=Character)
    world: WorldState = field(default_factory=WorldState)
    active_quests: list[Quest] = field(default_factory=list)
    turn_log: list[dict[str, str]] = field(default_factory=list)
    last_narration: str = ""
    status_message: str = ""

    @classmethod
    def from_dict(cls, payload: dict | None) -> "GameState":
        payload = payload or {}
        return cls(
            save_name=payload.get("save_name", "autosave"),
            player=Character.from_dict(payload.get("player")),
            world=WorldState.from_dict(payload.get("world")),
            active_quests=[Quest.from_dict(item) for item in payload.get("active_quests", [])],
            turn_log=list(payload.get("turn_log", [])),
            last_narration=payload.get("last_narration", ""),
            status_message=payload.get("status_message", ""),
        )
