import json
from pathlib import Path


class NpcRepository:
    def __init__(self) -> None:
        content_root = Path(__file__).resolve().parents[2] / "content"
        self.npc_path = content_root / "npcs" / "starter_npcs.json"
        payload = self._load_json(self.npc_path)
        self._npcs = {npc["npc_id"]: npc for npc in payload.get("npcs", [])}

    def _load_json(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def get_npc(self, npc_id: str) -> dict:
        return dict(self._npcs[npc_id])

    def get_many(self, npc_ids: list[str]) -> list[dict]:
        return [self.get_npc(npc_id) for npc_id in npc_ids if npc_id in self._npcs]
