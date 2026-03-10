import json
from pathlib import Path

from ai_pnp.core.models.world_state import WorldState


class SceneRepository:
    def __init__(self) -> None:
        content_root = Path(__file__).resolve().parents[2] / "content"
        self.world_seed_path = content_root / "world" / "seed_world.json"
        self.scenario_path = content_root / "scenarios" / "prologue.json"
        self._world_seed = self._load_json(self.world_seed_path)
        scenario = self._load_json(self.scenario_path)
        self._scenes = {scene["scene_id"]: scene for scene in scenario["scenes"]}

    def _load_json(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def get_scene(self, scene_id: str) -> dict:
        return dict(self._scenes[scene_id])

    def build_initial_world_state(self) -> WorldState:
        start_scene_id = self._world_seed["start_scene_id"]
        scene = self.get_scene(start_scene_id)
        return WorldState(
            chapter=self._world_seed.get("chapter", "Prolog"),
            current_scene_id=start_scene_id,
            current_location_name=scene["location_name"],
            time_of_day=self._world_seed.get("time_of_day", "Abend"),
            discovered_flags=[],
        )

    def resolve_move_target(self, scene_id: str, normalized_action: str) -> str | None:
        scene = self.get_scene(scene_id)
        for keyword, target in scene.get("exits", {}).items():
            if keyword in normalized_action:
                return target
        return None
