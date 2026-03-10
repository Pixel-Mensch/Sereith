from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class TurnResult:
    narration: str
    prompt: str
    interpretation: object
    narrator_provider: str
    system_note: str | None = None


class TurnProcessor:
    def __init__(
        self,
        *,
        action_interpreter,
        prompt_builder,
        narrator_client,
        state_updater,
        memory_service,
        session_summary_service,
        scene_repository,
        save_repository,
        autosave_enabled: bool = True,
    ) -> None:
        self.action_interpreter = action_interpreter
        self.prompt_builder = prompt_builder
        self.narrator_client = narrator_client
        self.state_updater = state_updater
        self.memory_service = memory_service
        self.session_summary_service = session_summary_service
        self.scene_repository = scene_repository
        self.save_repository = save_repository
        self.autosave_enabled = autosave_enabled

    def process_turn(self, state, raw_action: str) -> TurnResult:
        scene = self.scene_repository.get_scene(state.world.current_scene_id)
        interpretation = self.action_interpreter.interpret(raw_action, state.world.current_scene_id)
        planned_effect = self.scene_repository.get_action_effect(
            state.world.current_scene_id,
            interpretation.intent,
            interpretation.subject,
        )
        target_scene = None
        if interpretation.target_scene_id:
            target_scene = self.scene_repository.get_scene(interpretation.target_scene_id)

        prompt = self.prompt_builder.build(
            state=state,
            scene=scene,
            action=raw_action,
            interpretation=interpretation,
            planned_effect=planned_effect,
            target_scene=target_scene,
        )
        narration_result = self.narrator_client.narrate(
            prompt,
            intent=interpretation.intent,
            subject=interpretation.subject,
            scene_title=scene["title"],
            fallback_hint=planned_effect.get("fallback_narration", ""),
        )
        self.state_updater.apply(
            state=state,
            raw_action=raw_action,
            interpretation=interpretation,
            narration_result=narration_result,
            planned_effect=planned_effect,
        )
        self.memory_service.record_turn(
            state,
            player_action=raw_action,
            interpretation=interpretation,
            narration=state.last_narration,
            timestamp=datetime.now(UTC).isoformat(),
        )
        summary = self.session_summary_service.maybe_create_summary(state)
        if summary and not narration_result.note:
            narration_result.note = "Neue Sitzungssummary erstellt."
        elif summary and narration_result.note:
            narration_result.note = f"{narration_result.note} | Neue Sitzungssummary erstellt."

        if self.autosave_enabled:
            self.save_repository.autosave(state)

        return TurnResult(
            narration=state.last_narration,
            prompt=prompt,
            interpretation=interpretation,
            narrator_provider=narration_result.provider,
            system_note=narration_result.note,
        )
