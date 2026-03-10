class NarratorClient:
    def narrate(self, prompt: str, *, intent: str, scene_title: str) -> str:
        del prompt
        intros = {
            "observe": "Du laesst den Blick langsam durch die Szene wandern.",
            "talk": "Deine Worte schneiden durch das leise Murmeln der Umgebung.",
            "stealth": "Mit bedachten Schritten versuchst du, moeglichst wenig Aufmerksamkeit zu erregen.",
            "move": "Du verlaesst deinen bisherigen Platz und setzt die Szene in Bewegung.",
            "freeform": "Die Welt reagiert auf dein Vorhaben mit gespannter Aufmerksamkeit.",
        }
        intro = intros.get(intent, intros["freeform"])
        return (
            f"{intro} In {scene_title} nimmt die Situation eine neue Wendung.\n\n"
            "[Platzhalter-Narration fuer spaeteren lokalen Modelladapter.]"
        )
