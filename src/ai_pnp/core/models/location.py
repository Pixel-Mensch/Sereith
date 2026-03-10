from dataclasses import dataclass
from ai_pnp.core.models.base import BaseModel

@dataclass
class Location(BaseModel):
    location_id: str
    name: str
    description: str
