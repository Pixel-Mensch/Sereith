from dataclasses import dataclass

from ai_pnp.core.models.base import BaseModel


@dataclass
class Quest(BaseModel):
    quest_id: str
    title: str
    status: str = "active"
    summary: str = ""

    @classmethod
    def from_dict(cls, payload: dict | None) -> "Quest":
        payload = payload or {}
        return cls(
            quest_id=payload.get("quest_id", "unknown_quest"),
            title=payload.get("title", "Unbenannte Quest"),
            status=payload.get("status", "active"),
            summary=payload.get("summary", ""),
        )
