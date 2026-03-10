import tkinter as tk

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
from ai_pnp.services.memory.memory_service import MemoryService
from ai_pnp.services.memory.session_summary_service import SessionSummaryService
from ai_pnp.services.storage.save_repository import SaveRepository


class Application:
    def __init__(self) -> None:
        self.app_config = AppConfig.from_file()
        self.scene_repository = SceneRepository()
        self.quest_repository = QuestRepository()
        self.npc_repository = NpcRepository()
        self.save_repository = SaveRepository()
        self.prompt_builder = PromptBuilder(self.npc_repository)
        self.narrator_client = NarratorClient(self.app_config)
        self.memory_service = MemoryService()
        self.session_summary_service = SessionSummaryService()
        self.action_interpreter = ActionInterpreter(self.scene_repository)
        self.state_updater = StateUpdater(self.scene_repository, self.memory_service)
        self.turn_processor = TurnProcessor(
            action_interpreter=self.action_interpreter,
            prompt_builder=self.prompt_builder,
            narrator_client=self.narrator_client,
            state_updater=self.state_updater,
            memory_service=self.memory_service,
            session_summary_service=self.session_summary_service,
            scene_repository=self.scene_repository,
            save_repository=self.save_repository,
            autosave_enabled=self.app_config.autosave,
        )
        self.engine = GameEngine(
            scene_repository=self.scene_repository,
            quest_repository=self.quest_repository,
            save_repository=self.save_repository,
            turn_processor=self.turn_processor,
        )

    def run(self) -> None:
        if self.app_config.ui_mode.lower().strip() == "desktop":
            self.run_desktop()
            return
        self.run_cli()

    def run_cli(self) -> None:
        from ai_pnp.ui.cli.runner import run

        run(self.engine)

    def run_desktop(self) -> None:
        from ai_pnp.ui.desktop.app import DesktopApp

        try:
            DesktopApp(self.engine).launch()
        except tk.TclError:
            self.run_cli()
