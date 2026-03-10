class StateUpdater:
    def __init__(self, scene_repository, memory_service) -> None:
        self.scene_repository = scene_repository
        self.memory_service = memory_service

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
            status_message = self._apply_effect(
                state,
                planned_effect,
                fallback_status=status_message,
                interpretation=interpretation,
                raw_action=raw_action,
            )
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
        state.world.scene_objects = list(scene.get("scene_objects", []))
        state.world.npc_present = list(scene.get("npcs", []))
        state.world.temporary_scene_flags = []
        self.memory_service.add_discovered_location(state, scene["location_name"])
        enter_effect = self.scene_repository.get_enter_effect(target_scene_id)
        status_message = self._apply_effect(
            state,
            enter_effect,
            fallback_status=fallback_status,
            interpretation=None,
            raw_action="scene_enter",
        )
        final_narration = f"{narration}\n\n{scene['description']}"
        return status_message, final_narration

    def _apply_effect(self, state, effect: dict, fallback_status: str, interpretation, raw_action: str) -> str:
        if not effect:
            return fallback_status

        for flag in effect.get("discovered_flags", []):
            if flag not in state.world.discovered_flags:
                state.world.discovered_flags.append(flag)
            self.memory_service.add_discovered_information(state, flag)
            if flag.endswith("_at_inn") or flag.endswith("_outside") or flag.endswith("_clue"):
                self.memory_service.add_fact(state, flag)

        for flag in effect.get("temporary_scene_flags", []):
            if flag not in state.world.temporary_scene_flags:
                state.world.temporary_scene_flags.append(flag)

        for fact in effect.get("facts", []):
            self.memory_service.add_fact(state, fact)

        for info in effect.get("discovered_information", []):
            self.memory_service.add_discovered_information(state, info)

        for quest_update in effect.get("quest_updates", []):
            self._apply_quest_update(state, quest_update)

        npc_memory = effect.get("npc_memory")
        if npc_memory:
            topic = npc_memory.get("last_topic", interpretation.subject if interpretation else "")
            self.memory_service.update_npc_memory(
                state,
                npc_id=npc_memory["npc_id"],
                topic=topic,
                player_action=raw_action,
                delta=npc_memory.get("relationship_delta", 0),
            )

        return effect.get("status_message", fallback_status)

    def _apply_quest_update(self, state, quest_update: dict) -> None:
        quest = next(
            (item for item in state.active_quests if item.quest_id == quest_update["quest_id"]),
            None,
        )
        if quest is None:
            return

        for flag in quest_update.get("progress_flags", []):
            if flag not in quest.progress_flags:
                quest.progress_flags.append(flag)
            self.memory_service.add_quest_progress(state, flag)

        if quest_update.get("status"):
            quest.status = quest_update["status"]

        objectives = quest_update.get("objectives")
        if objectives:
            quest.objectives = list(objectives)

        if quest_update.get("summary_append"):
            summary_append = quest_update["summary_append"].strip()
            if summary_append and summary_append not in quest.summary:
                if quest.summary:
                    quest.summary = f"{quest.summary} {summary_append}"
                else:
                    quest.summary = summary_append
