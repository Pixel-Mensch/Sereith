from ai_pnp.core.models.game_state import GameState
from ai_pnp.services.llm.prompt_builder import PromptBuilder

class GameEngine:
    def __init__(self, content_loader, save_repository, rules_engine, memory_service, narrator_client) -> None:
        self.content_loader = content_loader
        self.save_repository = save_repository
        self.rules_engine = rules_engine
        self.memory_service = memory_service
        self.narrator_client = narrator_client
        self.prompt_builder = PromptBuilder()
        self.state = self.content_loader.create_initial_state()

    def process_action(self, action: str) -> str:
        rule_result = self.rules_engine.evaluate(self.state, action)
        memory = self.memory_service.get_recent_context(self.state)
        prompt = self.prompt_builder.build(self.state, action, rule_result, memory)
        narration = self.narrator_client.narrate(prompt)
        self.memory_service.record_turn(self.state, action, narration)
        self.save_repository.autosave(self.state)
        return narration

    def run_cli(self) -> None:
        print("AI-PnP gestartet")
        print("Zum Beenden 'quit' eingeben.\n")
        print(self.state.current_scene_text)
        while True:
            action = input("\n> ").strip()
            if action.lower() == "quit":
                print("Spiel beendet.")
                break
            if not action:
                continue
            result = self.process_action(action)
            print(f"\n{result}")
