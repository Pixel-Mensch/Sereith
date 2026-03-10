from dataclasses import dataclass

from ai_pnp.core.models.character import Character
from ai_pnp.core.models.game_state import GameState


@dataclass
class EngineResponse:
    message: str
    should_quit: bool = False


class GameEngine:
    def __init__(self, scene_repository, quest_repository, save_repository, turn_processor) -> None:
        self.scene_repository = scene_repository
        self.quest_repository = quest_repository
        self.save_repository = save_repository
        self.turn_processor = turn_processor
        self.state = self._create_initial_state()

    def _create_initial_state(self, save_name: str = "autosave") -> GameState:
        world = self.scene_repository.build_initial_world_state()
        opening_scene = self.scene_repository.get_scene(world.current_scene_id)
        state = GameState(
            save_name=save_name,
            player=Character(),
            world=world,
            active_quests=self.quest_repository.build_initial_quests(),
            turn_log=[],
            facts=[],
            discovered_locations=[world.current_location_name],
            discovered_information=[],
            quest_progress=[],
            npc_relationships=[],
            npc_memory=[],
            session_summaries=[],
            last_narration=opening_scene["description"],
            status_message="Neue Sitzung gestartet. Die Geruechte um den verschwundenen Kurier liegen in der Luft.",
        )
        return state

    def get_player_status(self) -> dict:
        return {
            "name": self.state.player.name,
            "ancestry": self.state.player.ancestry,
            "role": self.state.player.role,
            "level": self.state.player.level,
            "hp_current": self.state.player.hp_current,
            "hp_max": self.state.player.hp_max,
            "inventory": list(self.state.player.inventory),
            "skills": list(self.state.player.skills),
        }

    def get_active_quests(self) -> list[dict]:
        return [quest.to_dict() for quest in self.state.active_quests]

    def get_current_scene(self) -> dict:
        scene = self.scene_repository.get_scene(self.state.world.current_scene_id)
        return {
            "scene_id": scene["scene_id"],
            "title": scene["title"],
            "location_name": scene["location_name"],
            "description": scene["description"],
            "scene_objects": list(self.state.world.scene_objects),
            "npc_present": list(self.state.world.npc_present),
            "temporary_scene_flags": list(self.state.world.temporary_scene_flags),
        }

    def describe_current_scene(self) -> str:
        scene = self.get_current_scene()
        return f"{scene['title']}\n{scene['description']}"

    def render_state_summary(self) -> str:
        quests = []
        for quest in self.state.active_quests:
            progress = ", ".join(quest.progress_flags) or "-"
            objectives = ", ".join(quest.objectives) or "-"
            quests.append(
                f"{quest.title} [{quest.status}] | Ziele: {objectives} | Fortschritt: {progress}"
            )
        quest_summary = "\n".join(quests) or "-"
        flags = ", ".join(self.state.world.discovered_flags) or "-"
        facts = ", ".join(self.state.facts[-5:]) or "-"
        summary = self.state.session_summaries[-1]["summary_text"] if self.state.session_summaries else "-"
        return (
            f"Save: {self.state.save_name}\n"
            f"Kapitel: {self.state.world.chapter}\n"
            f"Szene: {self.state.world.current_scene_id}\n"
            f"Ort: {self.state.world.current_location_name}\n"
            f"Zeit: {self.state.world.time_of_day}\n"
            f"Flags: {flags}\n"
            f"Facts: {facts}\n"
            f"Quests:\n{quest_summary}\n"
            f"Letzte Summary: {summary}\n"
            f"Status: {self.state.status_message or '-'}"
        )

    def save_game(self, save_name: str | None = None) -> EngineResponse:
        self.save_repository.save(self.state, save_name=save_name)
        self.state.status_message = f"Spielstand gespeichert: {self.state.save_name}"
        return EngineResponse(self.state.status_message)

    def load_game(self, save_name: str | None = None) -> EngineResponse:
        target = save_name or self.state.save_name
        if not self.save_repository.exists(target):
            return EngineResponse(f"Kein Spielstand gefunden: {target}")
        self.state = self.save_repository.load(target)
        self.state.status_message = f"Spielstand geladen: {target}"
        return EngineResponse(f"{self.state.status_message}\n\n{self.describe_current_scene()}")

    def process_player_action(self, action: str):
        return self.turn_processor.process_turn(self.state, action)

    def process_action(self, action: str):
        return self.process_player_action(action)

    def handle_input(self, raw_input: str) -> EngineResponse:
        action = raw_input.strip()
        if not action:
            return EngineResponse("Leere Eingabe ignoriert.")

        lowered = action.lower()
        if lowered == "quit":
            return EngineResponse("Spiel beendet.", should_quit=True)
        if lowered.startswith("save"):
            parts = action.split(maxsplit=1)
            return self.save_game(parts[1].strip() if len(parts) > 1 else None)
        if lowered.startswith("load"):
            parts = action.split(maxsplit=1)
            return self.load_game(parts[1].strip() if len(parts) > 1 else None)
        if lowered == "state":
            return EngineResponse(self.render_state_summary())

        result = self.process_player_action(action)
        message = result.narration
        if result.system_note:
            message = f"{message}\n\n[System: {result.system_note}]"
        return EngineResponse(message)

    def run_cli(self) -> None:
        print("AI-PnP gestartet")
        print("Befehle: save [name], load [name], state, quit\n")
        print(self.describe_current_scene())
        while True:
            response = self.handle_input(input("\n> "))
            print(f"\n{response.message}")
            if response.should_quit:
                break
