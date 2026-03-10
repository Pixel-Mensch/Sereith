class NarratorClient:
    def narrate(self, prompt: str) -> str:
        return (
            "Der Erzähler verarbeitet deine Aktion und beschreibt die Szene weiter.\n\n"
            f"[Platzhalter-Narration]\n{prompt}"
        )
