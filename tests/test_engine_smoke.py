from pathlib import Path

from ai_pnp.engine.flow.turn_processor import TurnProcessor
from ai_pnp.engine.game_engine import GameEngine
from ai_pnp.engine.parsing.action_interpreter import ActionInterpreter
from ai_pnp.engine.state.state_updater import StateUpdater
from ai_pnp.services.content.scene_repository import SceneRepository
from ai_pnp.services.llm.narrator_client import NarratorClient
from ai_pnp.services.llm.prompt_builder import PromptBuilder
from ai_pnp.services.storage.save_repository import SaveRepository


def test_engine_processes_one_turn_and_autosaves(tmp_path: Path) -> None:
    scene_repository = SceneRepository()
    save_repository = SaveRepository(save_dir=tmp_path)
    turn_processor = TurnProcessor(
        action_interpreter=ActionInterpreter(scene_repository),
        prompt_builder=PromptBuilder(),
        narrator_client=NarratorClient(),
        state_updater=StateUpdater(scene_repository),
        scene_repository=scene_repository,
        save_repository=save_repository,
    )
    engine = GameEngine(
        scene_repository=scene_repository,
        save_repository=save_repository,
        turn_processor=turn_processor,
    )

    narration = engine.process_action("untersuche die schankstube")

    assert "Platzhalter-Narration" in narration
    assert engine.state.turn_log
    assert "inn_room_observed" in engine.state.world.discovered_flags
    assert (tmp_path / "autosave.json").exists()
