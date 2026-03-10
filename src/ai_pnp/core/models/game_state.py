from dataclasses import dataclass, field
from ai_pnp.core.models.base import BaseModel
from ai_pnp.core.models.character import Character
from ai_pnp.core.models.quest import Quest

@dataclass
class GameState(BaseModel):
    save_name: str = "autosave"
    chapter: str = "Prologue"
    current_location_id: str = "roadside_inn"
    current_scene_text: str = (
        "Du sitzt in einem kleinen Schankraum am Rand der alten Heerstraße. "
        "Regen trommelt gegen die Fenster, während drei Fremde leise tuscheln."
    )
    player: Character = field(default_factory=Character)
    active_quests: list[Quest] = field(default_factory=list)
    turn_log: list[dict] = field(default_factory=list)
