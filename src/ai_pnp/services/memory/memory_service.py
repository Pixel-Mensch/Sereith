class MemoryService:
    def __init__(self, max_turn_log_entries: int = 20) -> None:
        self.max_turn_log_entries = max_turn_log_entries

    def record_turn(self, state, *, player_action: str, interpretation, narration: str, timestamp: str) -> None:
        state.turn_log.append(
            {
                "player_action": player_action,
                "interpretation": {
                    "intent": interpretation.intent,
                    "subject": interpretation.subject,
                    "target_scene_id": interpretation.target_scene_id,
                },
                "narration": narration,
                "timestamp": timestamp,
                "scene_id": state.world.current_scene_id,
            }
        )
        if len(state.turn_log) > self.max_turn_log_entries:
            state.turn_log[:] = state.turn_log[-self.max_turn_log_entries:]

    def add_fact(self, state, fact: str) -> None:
        if fact and fact not in state.facts:
            state.facts.append(fact)

    def add_discovered_information(self, state, info: str) -> None:
        if info and info not in state.discovered_information:
            state.discovered_information.append(info)

    def add_discovered_location(self, state, location_name: str) -> None:
        if location_name and location_name not in state.discovered_locations:
            state.discovered_locations.append(location_name)

    def add_quest_progress(self, state, progress_flag: str) -> None:
        if progress_flag and progress_flag not in state.quest_progress:
            state.quest_progress.append(progress_flag)

    def update_npc_memory(self, state, *, npc_id: str, topic: str, player_action: str, delta: int = 0) -> None:
        if not npc_id:
            return

        npc_memory = next((entry for entry in state.npc_memory if entry.npc_id == npc_id), None)
        if npc_memory is None:
            from ai_pnp.core.models.npc_memory import NpcMemory

            npc_memory = NpcMemory(npc_id=npc_id)
            state.npc_memory.append(npc_memory)

        npc_memory.last_topic = topic
        if player_action not in npc_memory.known_player_actions:
            npc_memory.known_player_actions.append(player_action)
        npc_memory.relationship_score += delta
        npc_memory.relationship_score = max(-10, min(10, npc_memory.relationship_score))
        if npc_memory.relationship_score >= 2:
            npc_memory.attitude = "positive"
        elif npc_memory.relationship_score <= -2:
            npc_memory.attitude = "negative"
        else:
            npc_memory.attitude = "neutral"

        relationship_entry = next(
            (item for item in state.npc_relationships if item["npc_id"] == npc_id),
            None,
        )
        if relationship_entry is None:
            relationship_entry = {
                "npc_id": npc_id,
                "attitude": npc_memory.attitude,
                "last_interaction": player_action,
                "known_information": [topic] if topic else [],
            }
            state.npc_relationships.append(relationship_entry)
        else:
            relationship_entry["attitude"] = npc_memory.attitude
            relationship_entry["last_interaction"] = player_action
            if topic and topic not in relationship_entry["known_information"]:
                relationship_entry["known_information"].append(topic)
