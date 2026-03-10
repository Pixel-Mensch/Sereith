from dataclasses import dataclass
from ai_pnp.core.models.base import BaseModel

@dataclass
class NPC(BaseModel):
    npc_id: str
    name: str
    role: str
    location_id: str
    attitude: str = "neutral"
