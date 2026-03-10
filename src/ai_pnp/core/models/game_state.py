from dataclasses import dataclass, field

from ai_pnp.core.models.base import BaseModel
from ai_pnp.core.models.character import Character
from ai_pnp.core.models.npc_memory import NpcMemory
from ai_pnp.core.models.quest import Quest
from ai_pnp.core.models.world_state import WorldState


@dataclass
class GameState(BaseModel):
    save_name: str = "autosave"
    player: Character = field(default_factory=Character)
    world: WorldState = field(default_factory=WorldState)
    active_quests: list[Quest] = field(default_factory=list)
    turn_log: list[dict[str, object]] = field(default_factory=list)
    facts: list[str] = field(default_factory=list)
    discovered_locations: list[str] = field(default_factory=list)
    discovered_information: list[str] = field(default_factory=list)
    quest_progress: list[str] = field(default_factory=list)
    npc_relationships: list[dict[str, object]] = field(default_factory=list)
    npc_memory: list[NpcMemory] = field(default_factory=list)
    session_summaries: list[dict[str, object]] = field(default_factory=list)
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
            facts=list(payload.get("facts", [])),
            discovered_locations=list(payload.get("discovered_locations", [])),
            discovered_information=list(payload.get("discovered_information", [])),
            quest_progress=list(payload.get("quest_progress", [])),
            npc_relationships=list(payload.get("npc_relationships", [])),
            npc_memory=[NpcMemory.from_dict(item) for item in payload.get("npc_memory", [])],
            session_summaries=list(payload.get("session_summaries", [])),
            last_narration=payload.get("last_narration", ""),
            status_message=payload.get("status_message", ""),
        )
