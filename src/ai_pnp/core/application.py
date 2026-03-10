from ai_pnp.engine.flow.turn_processor import TurnProcessor
from ai_pnp.engine.game_engine import GameEngine
from ai_pnp.engine.parsing.action_interpreter import ActionInterpreter
from ai_pnp.engine.state.state_updater import StateUpdater
from ai_pnp.services.content.scene_repository import SceneRepository
from ai_pnp.services.llm.narrator_client import NarratorClient
from ai_pnp.services.llm.prompt_builder import PromptBuilder
from ai_pnp.services.storage.save_repository import SaveRepository


class Application:
    def __init__(self) -> None:
        self.scene_repository = SceneRepository()
        self.save_repository = SaveRepository()
        self.prompt_builder = PromptBuilder()
        self.narrator_client = NarratorClient()
        self.action_interpreter = ActionInterpreter(self.scene_repository)
        self.state_updater = StateUpdater(self.scene_repository)
        self.turn_processor = TurnProcessor(
            action_interpreter=self.action_interpreter,
            prompt_builder=self.prompt_builder,
            narrator_client=self.narrator_client,
            state_updater=self.state_updater,
            scene_repository=self.scene_repository,
            save_repository=self.save_repository,
        )
        self.engine = GameEngine(
            scene_repository=self.scene_repository,
            save_repository=self.save_repository,
            turn_processor=self.turn_processor,
        )

    def run_cli(self) -> None:
        self.engine.run_cli()
