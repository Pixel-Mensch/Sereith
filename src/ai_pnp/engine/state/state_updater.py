class StateUpdater:
    def __init__(self, scene_repository) -> None:
        self.scene_repository = scene_repository

    def apply(self, state, raw_action: str, interpretation, narration_result, planned_effect: dict) -> None:
        final_narration = narration_result.text
        status_message = self._default_status(interpretation.intent)
        if interpretation.intent == "move":
            status_message, final_narration = self._apply_move(
                state,
                interpretation,
                narration_result.text,
            )
        else:
            status_message = self._apply_effect(state, planned_effect, status_message)
            target_scene_id = planned_effect.get("target_scene_id")
            if target_scene_id:
                transition_status, final_narration = self._transition_to_scene(
                    state,
                    target_scene_id,
                    narration_result.text,
                    fallback_status=status_message,
                )
                status_message = transition_status

        state.last_narration = final_narration
        state.status_message = status_message
        state.turn_log.append(
            {
                "action": raw_action,
                "intent": interpretation.intent,
                "subject": interpretation.subject,
                "scene_id": state.world.current_scene_id,
                "status": status_message,
                "narration": final_narration,
                "narration_provider": narration_result.provider,
                "system_note": narration_result.note,
            }
        )
        if len(state.turn_log) > 25:
            state.turn_log[:] = state.turn_log[-25:]

    def _default_status(self, intent: str) -> str:
        messages = {
            "observe": "Du nimmst die Szene genauer in den Blick.",
            "talk": "Du suchst das Gespraech.",
            "stealth": "Du bewegst dich vorsichtig und unauffaellig.",
            "move": "Du setzt dich in Bewegung.",
        }
        return messages.get(intent, "Die Szene nimmt deine Handlung auf.")

    def _apply_move(self, state, interpretation, narration: str) -> tuple[str, str]:
        if not interpretation.target_scene_id:
            return "Du findest von hier aus keinen passenden Weg.", narration
        return self._transition_to_scene(
            state,
            interpretation.target_scene_id,
            narration,
            fallback_status="Du wechselst den Ort.",
        )

    def _transition_to_scene(
        self,
        state,
        target_scene_id: str,
        narration: str,
        *,
        fallback_status: str,
    ) -> tuple[str, str]:
        scene = self.scene_repository.get_scene(target_scene_id)
        state.world.current_scene_id = scene["scene_id"]
        state.world.current_location_name = scene["location_name"]
        enter_effect = self.scene_repository.get_enter_effect(target_scene_id)
        status_message = self._apply_effect(state, enter_effect, fallback_status)
        final_narration = f"{narration}\n\n{scene['description']}"
        return status_message, final_narration

    def _apply_effect(self, state, effect: dict, fallback_status: str) -> str:
        if not effect:
            return fallback_status

        for flag in effect.get("discovered_flags", []):
            if flag not in state.world.discovered_flags:
                state.world.discovered_flags.append(flag)

        for quest_update in effect.get("quest_updates", []):
            self._apply_quest_update(state, quest_update)

        return effect.get("status_message", fallback_status)

    def _apply_quest_update(self, state, quest_update: dict) -> None:
        quest = next(
            (item for item in state.active_quests if item.quest_id == quest_update["quest_id"]),
            None,
        )
        if quest is None:
            return

        newly_added = False
        for flag in quest_update.get("progress_flags", []):
            if flag not in quest.progress_flags:
                quest.progress_flags.append(flag)
                newly_added = True

        if quest_update.get("status"):
            quest.status = quest_update["status"]
        if quest_update.get("current_objective"):
            quest.current_objective = quest_update["current_objective"]
        if quest_update.get("summary_append") and newly_added:
            summary_append = quest_update["summary_append"].strip()
            if summary_append and summary_append not in quest.summary:
                if quest.summary:
                    quest.summary = f"{quest.summary} {summary_append}"
                else:
                    quest.summary = summary_append
