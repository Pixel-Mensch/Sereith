class PromptBuilder:
    def build(self, state, action: str, rule_result: dict, memory: list[dict]) -> str:
        recent = "\n".join(
            f"Aktion: {entry['action']} | Ergebnis: {entry['result'][:80]}"
            for entry in memory[-3:]
        ) or "Keine vorherigen Züge."
        return (
            f"Kapitel: {state.chapter}\n"
            f"Ort: {state.current_location_id}\n"
            f"Spieler: {state.player.name}\n"
            f"HP: {state.player.hp_current}/{state.player.hp_max}\n"
            f"Aktueller Szenentext: {state.current_scene_text}\n"
            f"Regelauswertung: {rule_result}\n"
            f"Vorherige Züge:\n{recent}\n"
            f"Neue Aktion: {action}\n"
            "Antworte als atmosphärischer Erzähler in deutscher Sprache."
        )
