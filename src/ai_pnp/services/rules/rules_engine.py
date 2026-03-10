class RulesEngine:
    def evaluate(self, state, action: str) -> dict:
        lowered = action.lower()
        if "untersuche" in lowered or "schaue" in lowered:
            return {"type": "skill_check", "skill": "Perception", "difficulty": 12}
        if "überrede" in lowered or "frage" in lowered:
            return {"type": "social_check", "skill": "Diplomacy", "difficulty": 11}
        return {"type": "freeform", "skill": None, "difficulty": None}
