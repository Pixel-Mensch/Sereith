class SessionSummaryService:
    def maybe_create_summary(self, state) -> dict | None:
        if not state.turn_log:
            return None

        if len(state.turn_log) % 10 != 0:
            return None

        current_turn_count = len(state.turn_log)
        if state.session_summaries and state.session_summaries[-1]["turn_count"] == current_turn_count:
            return None

        recent_actions = ", ".join(
            entry["player_action"]
            for entry in state.turn_log[-3:]
        ) or "keine Aktionen"
        flags = ", ".join(state.world.discovered_flags[-5:]) or "keine"
        quest_bits = []
        for quest in state.active_quests:
            quest_bits.append(
                f"{quest.title}: {', '.join(quest.progress_flags[-3:]) or quest.status}"
            )
        quest_text = "; ".join(quest_bits) or "keine aktiven Quests"

        summary = {
            "turn_count": current_turn_count,
            "summary_text": (
                f"Bis Zug {current_turn_count} fuehrte der Spieler zuletzt folgende Schritte aus: {recent_actions}. "
                f"Wichtige Flags: {flags}. Queststatus: {quest_text}."
            ),
        }
        state.session_summaries.append(summary)
        return summary
