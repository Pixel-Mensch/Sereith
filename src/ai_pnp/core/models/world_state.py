from dataclasses import dataclass, field

from ai_pnp.core.models.base import BaseModel


@dataclass
class WorldState(BaseModel):
    chapter: str = "Prolog"
    current_scene_id: str = "roadside_inn_intro"
    current_location_name: str = "Schankstube an der Heerstrasse"
    time_of_day: str = "Abend"
    discovered_flags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict | None) -> "WorldState":
        payload = payload or {}
        return cls(
            chapter=payload.get("chapter", "Prolog"),
            current_scene_id=payload.get("current_scene_id", "roadside_inn_intro"),
            current_location_name=payload.get(
                "current_location_name",
                "Schankstube an der Heerstrasse",
            ),
            time_of_day=payload.get("time_of_day", "Abend"),
            discovered_flags=list(payload.get("discovered_flags", [])),
        )
