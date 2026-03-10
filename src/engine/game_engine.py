from src.engine.state_manager import StateManager
from src.ai.ai_client import AIClient
from src.ai.prompt_builder import build_prompt

class GameEngine:
    def __init__(self):
        self.state = StateManager()
        self.ai = AIClient()

    def start(self):
        print("AI-PnP Prototype Started")
        print("Type 'quit' to exit.")

        while True:
            action = input("> ")

            if action.lower() == "quit":
                break

            prompt = build_prompt(self.state.get_state(), action)
            response = self.ai.generate(prompt)

            print("\n" + response + "\n")
