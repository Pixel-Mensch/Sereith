class PromptBuilder:
    def build(self, state, scene: dict, action: str, interpretation) -> str:
        recent = "\n".join(
            f"- Aktion: {entry['action']} | Intent: {entry['intent']} | Szene: {entry['scene_id']}"
            for entry in state.turn_log[-3:]
        ) or "- Keine vorherigen Zuege."
        exits = ", ".join(scene.get("exits", {}).keys()) or "keine offensichtlichen Ausgaenge"
        flags = ", ".join(state.world.discovered_flags) or "keine"
        quests = ", ".join(quest.title for quest in state.active_quests) or "keine aktive Quest"
        return (
            "Du bist ein atmosphaerischer Erzaehler fuer ein lokales Fantasy Pen-and-Paper-Spiel.\n"
            "Der Game State gehoert dem System. Erzaehle nur narrativ und fuehre keine unkontrollierten Regel- oder State-Aenderungen aus.\n\n"
            f"Kapitel: {state.world.chapter}\n"
            f"Szene: {scene['scene_id']} ({scene['title']})\n"
            f"Ort: {state.world.current_location_name}\n"
            f"Tageszeit: {state.world.time_of_day}\n"
            f"Spieler: {state.player.name}\n"
            f"HP: {state.player.hp_current}/{state.player.hp_max}\n"
            f"Skills: {', '.join(state.player.skills)}\n"
            f"Aktive Quests: {quests}\n"
            f"Entdeckte Flags: {flags}\n"
            f"Verfuegbare Ausgaenge: {exits}\n"
            f"Szenenbeschreibung: {scene['description']}\n"
            f"Letzte Narration: {state.last_narration or 'noch keine'}\n"
            f"Interpretation: intent={interpretation.intent}, ziel={interpretation.target_scene_id or '-'}\n"
            f"Vorherige Zuege:\n{recent}\n"
            f"Neue Aktion: {action}\n"
            "Antworte auf Deutsch in 2 bis 4 Saetzen und bleibe in der Szene."
        )
