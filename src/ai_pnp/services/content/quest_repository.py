import json
from pathlib import Path

from ai_pnp.core.models.quest import Quest


class QuestRepository:
    def __init__(self) -> None:
        content_root = Path(__file__).resolve().parents[2] / "content"
        self.quest_path = content_root / "quests" / "prologue_quests.json"
        self._payload = self._load_json(self.quest_path)

    def _load_json(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def build_initial_quests(self) -> list[Quest]:
        return [Quest.from_dict(quest) for quest in self._payload.get("quests", [])]
