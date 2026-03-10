import json
from pathlib import Path

from ai_pnp.core.models.game_state import GameState


class SaveRepository:
    def __init__(self, save_dir: Path | None = None) -> None:
        self.save_dir = save_dir or Path(__file__).resolve().parents[2] / "data" / "saves"
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, save_name: str) -> Path:
        return self.save_dir / f"{save_name}.json"

    def save(self, state: GameState, save_name: str | None = None) -> Path:
        if save_name:
            state.save_name = save_name
        path = self._get_path(state.save_name)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(state.to_dict(), handle, ensure_ascii=False, indent=2)
        return path

    def autosave(self, state: GameState) -> Path:
        return self.save(state)

    def load(self, save_name: str) -> GameState:
        path = self._get_path(save_name)
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        state = GameState.from_dict(payload)
        state.save_name = save_name
        return state

    def exists(self, save_name: str) -> bool:
        return self._get_path(save_name).exists()
