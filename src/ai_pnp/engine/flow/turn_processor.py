from dataclasses import dataclass


@dataclass
class TurnResult:
    narration: str
    prompt: str
    interpretation: object


class TurnProcessor:
    def __init__(
        self,
        *,
        action_interpreter,
        prompt_builder,
        narrator_client,
        state_updater,
        scene_repository,
        save_repository,
    ) -> None:
        self.action_interpreter = action_interpreter
        self.prompt_builder = prompt_builder
        self.narrator_client = narrator_client
        self.state_updater = state_updater
        self.scene_repository = scene_repository
        self.save_repository = save_repository

    def process_turn(self, state, raw_action: str) -> TurnResult:
        scene = self.scene_repository.get_scene(state.world.current_scene_id)
        interpretation = self.action_interpreter.interpret(raw_action, state.world.current_scene_id)
        prompt = self.prompt_builder.build(state, scene, raw_action, interpretation)
        narration = self.narrator_client.narrate(
            prompt,
            intent=interpretation.intent,
            scene_title=scene["title"],
        )
        self.state_updater.apply(state, raw_action, interpretation, narration)
        self.save_repository.autosave(state)
        return TurnResult(
            narration=state.last_narration,
            prompt=prompt,
            interpretation=interpretation,
        )
