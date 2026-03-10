from dataclasses import dataclass, field

from ai_pnp.core.models.base import BaseModel


@dataclass
class NpcMemory(BaseModel):
    npc_id: str
    attitude: str = "neutral"
    last_topic: str = ""
    known_player_actions: list[str] = field(default_factory=list)
    relationship_score: int = 0

    @classmethod
    def from_dict(cls, payload: dict | None) -> "NpcMemory":
        payload = payload or {}
        return cls(
            npc_id=payload.get("npc_id", "unknown_npc"),
            attitude=payload.get("attitude", "neutral"),
            last_topic=payload.get("last_topic", ""),
            known_player_actions=list(payload.get("known_player_actions", [])),
            relationship_score=payload.get("relationship_score", 0),
        )
