from dataclasses import dataclass
from ai_pnp.core.models.base import BaseModel

@dataclass
class Quest(BaseModel):
    quest_id: str
    title: str
    status: str = "active"
    summary: str = ""
