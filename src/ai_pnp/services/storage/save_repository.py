import json
from pathlib import Path

class SaveRepository:
    def __init__(self) -> None:
        self.save_dir = Path(__file__).resolve().parents[2] / "data" / "saves"
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def autosave(self, state) -> None:
        path = self.save_dir / f"{state.save_name}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(state.to_dict(), handle, ensure_ascii=False, indent=2)
