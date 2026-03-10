from pathlib import Path
import json

from ai_pnp.core.app_config import AppConfig
from ai_pnp.core.application import Application
from ai_pnp.engine.flow.turn_processor import TurnProcessor
from ai_pnp.engine.game_engine import GameEngine
from ai_pnp.engine.parsing.action_interpreter import ActionInterpreter
from ai_pnp.engine.state.state_updater import StateUpdater
from ai_pnp.services.content.npc_repository import NpcRepository
from ai_pnp.services.content.quest_repository import QuestRepository
from ai_pnp.services.content.scene_repository import SceneRepository
from ai_pnp.services.llm.narrator_client import NarratorClient
from ai_pnp.services.llm.prompt_builder import PromptBuilder
from ai_pnp.services.memory.memory_service import MemoryService
from ai_pnp.services.memory.session_summary_service import SessionSummaryService
from ai_pnp.services.storage.save_repository import SaveRepository
from ai_pnp.ui.cli.runner import handle_cli_input, run


def build_engine(tmp_path: Path) -> GameEngine:
    scene_repository = SceneRepository()
    quest_repository = QuestRepository()
    npc_repository = NpcRepository()
    memory_service = MemoryService()
    save_repository = SaveRepository(save_dir=tmp_path)
    config = AppConfig(llm_provider="placeholder", autosave=True)
    turn_processor = TurnProcessor(
        action_interpreter=ActionInterpreter(scene_repository),
        prompt_builder=PromptBuilder(npc_repository),
        narrator_client=NarratorClient(config),
        state_updater=StateUpdater(scene_repository, memory_service),
        memory_service=memory_service,
        session_summary_service=SessionSummaryService(),
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


def test_turn_log_is_limited_to_twenty_entries(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)

    for index in range(25):
        engine.process_player_action(f"mustere die fremden {index}")

    assert len(engine.state.turn_log) == 20
    assert engine.state.turn_log[0]["player_action"] == "mustere die fremden 5"


def test_quest_progress_is_set_for_innkeeper_conversation(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)

    engine.process_player_action("frage die wirtin nach dem kurier")

    quest = engine.state.active_quests[0]
    assert "heard_about_courier" in quest.progress_flags
    assert "asked_innkeeper" in quest.progress_flags
    assert "heard_about_courier" in engine.state.quest_progress
    assert "courier_last_seen_at_inn" in engine.state.facts


def test_npc_memory_is_created_for_innkeeper(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)

    engine.process_player_action("frage die wirtin nach dem kurier")

    npc_memory = next(item for item in engine.state.npc_memory if item.npc_id == "innkeeper")
    assert npc_memory.last_topic == "courier"
    assert npc_memory.known_player_actions
    assert npc_memory.relationship_score == 1


def test_session_summary_is_generated_after_ten_turns(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)

    for index in range(10):
        engine.process_player_action(f"mustere die fremden {index}")

    assert len(engine.state.session_summaries) == 1
    assert engine.state.session_summaries[0]["turn_count"] == 10


def test_save_and_load_preserve_extended_memory_state(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)
    engine.process_player_action("frage die wirtin nach dem kurier")
    engine.process_action("gehe hinaus")
    engine.process_player_action("untersuche die spuren")
    handle_cli_input(engine, "save campaign1")

    reloaded = build_engine(tmp_path)
    response = handle_cli_input(reloaded, "load campaign1")

    assert "Spielstand geladen" in response.message
    assert "courier_last_seen_at_inn" in reloaded.state.facts
    assert "Vor dem Gasthaus" in reloaded.state.discovered_locations
    assert "found_road_clue" in reloaded.state.quest_progress
    assert reloaded.state.npc_memory


def test_scene_change_updates_scene_memory(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)

    engine.process_action("gehe hinaus")

    current_scene = engine.get_current_scene()
    assert current_scene["scene_id"] == "inn_front"
    assert "laterne" in current_scene["scene_objects"]
    assert current_scene["npc_present"] == []


def test_engine_ui_methods_return_simple_data(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)

    result = engine.process_player_action("frage die wirtin nach dem kurier")

    assert result["ok"] is True
    assert result["narration"]
    assert isinstance(engine.get_player_status(), dict)
    assert isinstance(engine.get_current_scene(), dict)
    assert isinstance(engine.get_active_quests(), list)
    assert isinstance(engine.get_last_narration(), str)
    assert isinstance(engine.get_recent_log(), list)


def test_save_and_load_api_are_ui_friendly_and_serializable(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)
    engine.process_player_action("frage die wirtin nach dem kurier")

    saved = engine.save_game("ui_slot")
    reloaded = build_engine(tmp_path)
    loaded = reloaded.load_game("ui_slot")

    assert saved["ok"] is True
    assert loaded["ok"] is True
    assert loaded["scene"]["scene_id"] == reloaded.state.world.current_scene_id
    json.dumps(reloaded.state.to_dict())


def test_application_boots_with_engine() -> None:
    app = Application()

    assert app.engine.get_current_scene()["scene_id"] == "roadside_inn_intro"


def test_cli_runner_is_importable_and_owns_the_loop(tmp_path: Path) -> None:
    engine = build_engine(tmp_path)
    outputs: list[str] = []
    commands = iter(["quit"])

    run(
        engine=engine,
        input_func=lambda _prompt="": next(commands),
        output_func=outputs.append,
    )

    assert outputs[0] == "AI-PnP gestartet"
    assert any("Spiel beendet." in line for line in outputs)
