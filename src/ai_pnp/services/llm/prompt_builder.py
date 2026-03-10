import json
from pathlib import Path


class PromptBuilder:
    def __init__(self, npc_repository) -> None:
        self.npc_repository = npc_repository
        prompt_path = Path(__file__).resolve().parents[2] / "content" / "prompts" / "narrator_rules.json"
        with prompt_path.open("r", encoding="utf-8") as handle:
            self.prompt_rules = json.load(handle)

    def build(
        self,
        *,
        state,
        scene: dict,
        action: str,
        interpretation,
        planned_effect: dict,
        target_scene: dict | None,
    ) -> str:
        recent = "\n".join(
            f"- Aktion: {entry['action']} | Intent: {entry['intent']} | Szene: {entry['scene_id']} | Status: {entry['status']}"
            for entry in state.turn_log[-3:]
        ) or "- Keine vorherigen Zuege."
        visible_npcs = self._format_visible_npcs(scene.get("npcs", []))
        quest_lines = "\n".join(
            (
                f"- {quest.title} [{quest.status}] | Ziel: {quest.current_objective or '-'} | "
                f"Fortschritt: {', '.join(quest.progress_flags) or '-'} | Zusammenfassung: {quest.summary}"
            )
            for quest in state.active_quests
        ) or "- Keine aktiven Quests."
        flags = ", ".join(state.world.discovered_flags) or "keine"
        exits = ", ".join(exit_rule["label"] for exit_rule in scene.get("exits", [])) or "keine"
        style_rules = "\n".join(f"- {item}" for item in self.prompt_rules.get("style", []))
        constraints = "\n".join(f"- {item}" for item in self.prompt_rules.get("constraints", []))
        action_hint = planned_effect.get("prompt_hint", "Keine besondere Zusatzlenkung.")
        target_hint = (
            f"Moegliches naechstes Ziel: {target_scene['title']} ({target_scene['description']})"
            if target_scene
            else "Kein Szenenwechsel vorgesehen."
        )

        return (
            f"Rolle:\n{self.prompt_rules['role']}\n\n"
            f"Leitplanken:\n{constraints}\n\n"
            f"Stil:\n{style_rules}\n\n"
            f"Aktuelle Szene:\n"
            f"- ID: {scene['scene_id']}\n"
            f"- Titel: {scene['title']}\n"
            f"- Ort: {state.world.current_location_name}\n"
            f"- Tageszeit: {state.world.time_of_day}\n"
            f"- Beschreibung: {scene['description']}\n"
            f"- Sichtbare NPCs: {visible_npcs}\n"
            f"- Verfuegbare Ausgaenge: {exits}\n\n"
            f"Spielerzustand:\n"
            f"- Name: {state.player.name}\n"
            f"- Abstammung: {state.player.ancestry}\n"
            f"- Rolle: {state.player.role}\n"
            f"- HP: {state.player.hp_current}/{state.player.hp_max}\n"
            f"- Inventar: {', '.join(state.player.inventory) or 'leer'}\n"
            f"- Skills: {', '.join(state.player.skills)}\n\n"
            f"Questrelevanz:\n{quest_lines}\n\n"
            f"Entdeckte Flags: {flags}\n"
            f"Letzte Narration: {state.last_narration or 'noch keine'}\n"
            f"Vorherige Zuege:\n{recent}\n\n"
            f"Interpretation:\n"
            f"- Intent: {interpretation.intent}\n"
            f"- Fokus: {interpretation.subject}\n"
            f"- Zielszene: {interpretation.target_scene_id or '-'}\n"
            f"- Systemhinweis: {action_hint}\n"
            f"- {target_hint}\n\n"
            f"Spieleraktion:\n{action}\n\n"
            "Antworte direkt auf Deutsch, atmosphaerisch, reaktiv, ohne Metakommentare und ohne uebermaessige Wiederholung."
        )

    def _format_visible_npcs(self, npc_ids: list[str]) -> str:
        npcs = self.npc_repository.get_many(npc_ids)
        if not npcs:
            return "keine"
        return "; ".join(
            f"{npc['name']} ({npc['role']}, {npc['summary']})"
            for npc in npcs
        )
