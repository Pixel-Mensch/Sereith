class StateUpdater:
    def __init__(self, scene_repository) -> None:
        self.scene_repository = scene_repository

    def apply(self, state, raw_action: str, interpretation, narration: str) -> None:
        final_narration = narration
        status_message = "Aktion verarbeitet."

        if interpretation.intent == "move":
            status_message = self._apply_move(state, interpretation)
            if interpretation.target_scene_id:
                scene = self.scene_repository.get_scene(state.world.current_scene_id)
                final_narration = f"{narration}\n\n{scene['description']}"
        elif interpretation.intent == "observe":
            status_message = self._apply_observation(state)
        elif interpretation.intent == "talk":
            status_message = "Du suchst das Gespraech."
        elif interpretation.intent == "stealth":
            status_message = "Du bewegst dich vorsichtig und unauffaellig."
        else:
            status_message = "Die Szene nimmt deine Handlung auf."

        state.last_narration = final_narration
        state.status_message = status_message
        state.turn_log.append(
            {
                "action": raw_action,
                "intent": interpretation.intent,
                "scene_id": state.world.current_scene_id,
                "status": status_message,
                "narration": final_narration,
            }
        )
        if len(state.turn_log) > 25:
            state.turn_log[:] = state.turn_log[-25:]

    def _apply_move(self, state, interpretation) -> str:
        if not interpretation.target_scene_id:
            return "Du findest von hier aus keinen passenden Weg."

        scene = self.scene_repository.get_scene(interpretation.target_scene_id)
        state.world.current_scene_id = scene["scene_id"]
        state.world.current_location_name = scene["location_name"]
        return f"Szene gewechselt: {scene['location_name']}"

    def _apply_observation(self, state) -> str:
        scene = self.scene_repository.get_scene(state.world.current_scene_id)
        new_flags = 0
        for flag in scene.get("discover_flags", []):
            if flag not in state.world.discovered_flags:
                state.world.discovered_flags.append(flag)
                new_flags += 1
        if new_flags:
            return f"Du bemerkst {new_flags} neue Details."
        return "Du nimmst keine weiteren neuen Hinweise wahr."
