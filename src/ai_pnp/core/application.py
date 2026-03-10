from ai_pnp.core.game_engine import GameEngine
from ai_pnp.services.content.content_loader import ContentLoader
from ai_pnp.services.llm.narrator_client import NarratorClient
from ai_pnp.services.memory.memory_service import MemoryService
from ai_pnp.services.rules.rules_engine import RulesEngine
from ai_pnp.services.storage.save_repository import SaveRepository

class Application:
    def __init__(self) -> None:
        self.content_loader = ContentLoader()
        self.save_repository = SaveRepository()
        self.rules_engine = RulesEngine()
        self.memory_service = MemoryService()
        self.narrator_client = NarratorClient()

        self.engine = GameEngine(
            content_loader=self.content_loader,
            save_repository=self.save_repository,
            rules_engine=self.rules_engine,
            memory_service=self.memory_service,
            narrator_client=self.narrator_client,
        )

    def run_cli(self) -> None:
        self.engine.run_cli()
