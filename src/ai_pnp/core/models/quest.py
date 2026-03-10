from dataclasses import dataclass, field

from ai_pnp.core.models.base import BaseModel


@dataclass
class Quest(BaseModel):
    quest_id: str
    title: str
    status: str = "active"
    summary: str = ""
    objectives: list[str] = field(default_factory=list)
    progress_flags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict | None) -> "Quest":
        payload = payload or {}
        return cls(
            quest_id=payload.get("quest_id", "unknown_quest"),
            title=payload.get("title", "Unbenannte Quest"),
            status=payload.get("status", "active"),
            summary=payload.get("summary", ""),
            objectives=list(payload.get("objectives", [])),
            progress_flags=list(payload.get("progress_flags", [])),
        )
