from pathlib import Path

from ai_pnp.core.app_config import AppConfig
from ai_pnp.engine.flow.turn_processor import TurnProcessor
from ai_pnp.engine.game_engine import GameEngine
from ai_pnp.engine.parsing.action_interpreter import ActionInterpreter
from ai_pnp.engine.state.state_updater import StateUpdater
from ai_pnp.services.content.npc_repository import NpcRepository
from ai_pnp.services.content.quest_repository import QuestRepository
from ai_pnp.services.content.scene_repository import SceneRepository
from ai_pnp.services.llm.narrator_client import NarratorClient
from ai_pnp.services.llm.prompt_builder import PromptBuilder
from ai_pnp.services.storage.save_repository import SaveRepository


def build_engine(tmp_path: Path) -> GameEngine:
    scene_repository = SceneRepository()
    quest_repository = QuestRepository()
    npc_repository = NpcRepository()
    save_repository = SaveRepository(save_dir=tmp_path)
    config = AppConfig(llm_provider="placeholder", autosave=True)
    turn_processor = TurnProcessor(
        action_interpreter=ActionInterpreter(scene_repository),
        prompt_builder=PromptBuilder(npc_repository),
        narrator_client=NarratorClient(config),
        state_updater=StateUpdater(scene_repository),
        scene_repository=scene_repository,
        save_repository=save_repository,
        autosave_enabled=True,
    )
    return GameEngine(
        scene_repository=scene_repository,
        quest_repository=quest_repository,
        save_repository=save_repository,
        turn_processor=turn_processor,
    )


def test_engine_processes_one_turn_and_sets_discovery(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)

    result = engine.process_action("mustere die fremden")

    assert "Fremden" in result.narration or "Fremder" in result.narration
    assert "observed_strangers" in engine.state.world.discovered_flags
    assert engine.state.turn_log
    assert (tmp_path / "autosave.json").exists()


def test_save_and_load_preserve_core_state(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)
    engine.process_action("frage die wirtin nach dem kurier")
    engine.handle_input("save slot1")

    reloaded = build_engine(tmp_path)
    response = reloaded.handle_input("load slot1")

    assert "Spielstand geladen" in response.message
    assert "heard_about_courier" in reloaded.state.world.discovered_flags
    quest = reloaded.state.active_quests[0]
    assert "heard_about_courier" in quest.progress_flags


def test_scene_change_works_for_move_actions(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)

    response = engine.handle_input("gehe hinaus")

    assert engine.state.world.current_scene_id == "inn_front"
    assert "Vor dem Gasthaus" in response.message
    assert "went_outside" in engine.state.world.discovered_flags


def test_quest_progress_advances_to_first_clue(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)

    engine.process_action("frage die wirtin nach dem kurier")
    engine.handle_input("gehe hinaus")
    engine.process_action("untersuche die spuren")

    quest = engine.state.active_quests[0]
    assert engine.state.world.current_scene_id == "roadside_clue"
    assert "found_first_clue" in engine.state.world.discovered_flags
    assert "found_first_clue" in quest.progress_flags
