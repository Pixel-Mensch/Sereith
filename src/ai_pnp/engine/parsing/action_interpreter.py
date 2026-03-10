from dataclasses import dataclass, field


@dataclass
class ActionInterpretation:
    intent: str
    raw_action: str
    normalized_action: str
    target_scene_id: str | None = None
    matched_keywords: list[str] = field(default_factory=list)


class ActionInterpreter:
    def __init__(self, scene_repository) -> None:
        self.scene_repository = scene_repository

    def interpret(self, raw_action: str, current_scene_id: str) -> ActionInterpretation:
        normalized = raw_action.strip().lower()
        intent = "freeform"
        matched_keywords: list[str] = []
        target_scene_id: str | None = None

        keyword_groups = {
            "observe": ["observe", "untersuche", "beobachte", "schaue", "mustere", "betrachte"],
            "talk": ["rede", "sprich", "frage", "unterhalte", "sage"],
            "stealth": ["schleiche", "verstecke", "ducke", "verberge"],
            "move": ["gehe", "geh", "verlasse", "trete", "raus", "hinaus", "hinein", "betrete"],
        }

        for candidate_intent, keywords in keyword_groups.items():
            hits = [keyword for keyword in keywords if keyword in normalized]
            if hits:
                intent = candidate_intent
                matched_keywords = hits
                break

        if intent == "move":
            target_scene_id = self.scene_repository.resolve_move_target(current_scene_id, normalized)

        return ActionInterpretation(
            intent=intent,
            raw_action=raw_action,
            normalized_action=normalized,
            target_scene_id=target_scene_id,
            matched_keywords=matched_keywords,
        )
