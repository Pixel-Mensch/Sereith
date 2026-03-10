from dataclasses import dataclass, field


@dataclass
class ActionInterpretation:
    intent: str
    raw_action: str
    normalized_action: str
    subject: str = "default"
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
            "observe": ["untersuche", "beobachte", "schaue", "mustere", "betrachte", "sieh", "pruefe"],
            "talk": ["rede", "sprich", "frage", "unterhalte", "sage", "erkundige"],
            "stealth": ["schleiche", "verstecke", "ducke", "verberge"],
            "move": ["gehe", "geh", "verlasse", "trete", "raus", "hinaus", "hinein", "betrete", "folge"],
        }

        subject_groups = {
            "innkeeper": ["wirtin", "wirt", "theke"],
            "strangers": ["fremde", "reisende", "gaeste", "reisender"],
            "courier": ["kurier", "bote"],
            "clue": ["spur", "spuren", "hinweis", "abdruck", "schlamm", "faden"],
        }

        for candidate_intent, keywords in keyword_groups.items():
            hits = [keyword for keyword in keywords if keyword in normalized]
            if hits:
                intent = candidate_intent
                matched_keywords = hits
                break

        subject = "default"
        for candidate_subject, keywords in subject_groups.items():
            if any(keyword in normalized for keyword in keywords):
                subject = candidate_subject
                break

        if subject == "clue" and intent == "observe":
            target_scene_id = self.scene_repository.resolve_action_target(
                current_scene_id,
                intent,
                subject,
            )

        if intent == "move":
            target_scene_id = self.scene_repository.resolve_move_target(current_scene_id, normalized)

        return ActionInterpretation(
            intent=intent,
            raw_action=raw_action,
            normalized_action=normalized,
            subject=subject,
            target_scene_id=target_scene_id,
            matched_keywords=matched_keywords,
        )
