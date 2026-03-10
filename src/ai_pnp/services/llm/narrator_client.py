from dataclasses import dataclass

from ai_pnp.services.llm.ollama_client import OllamaClient, OllamaClientError


@dataclass
class NarrationResult:
    text: str
    provider: str
    note: str | None = None


class NarratorClient:
    def __init__(self, app_config, ollama_client: OllamaClient | None = None) -> None:
        self.app_config = app_config
        self.ollama_client = ollama_client or OllamaClient(
            host=app_config.ollama_host,
            timeout_seconds=app_config.ollama_timeout_seconds,
        )

    def narrate(
        self,
        prompt: str,
        *,
        intent: str,
        subject: str,
        scene_title: str,
        fallback_hint: str = "",
    ) -> NarrationResult:
        provider = self.app_config.llm_provider.lower().strip()
        if provider == "ollama":
            try:
                text = self.ollama_client.generate(
                    model=self.app_config.ollama_model,
                    prompt=prompt,
                )
                return NarrationResult(text=text, provider="ollama")
            except OllamaClientError as exc:
                return NarrationResult(
                    text=self._fallback_narration(intent, subject, scene_title, fallback_hint),
                    provider="fallback",
                    note=str(exc),
                )

        return NarrationResult(
            text=self._fallback_narration(intent, subject, scene_title, fallback_hint),
            provider="placeholder",
            note="Lokaler Platzhalter-Erzaehler aktiv.",
        )

    def _fallback_narration(
        self,
        intent: str,
        subject: str,
        scene_title: str,
        fallback_hint: str,
    ) -> str:
        intros = {
            "observe": "Du laesst den Blick aufmerksam durch die Umgebung wandern.",
            "talk": "Deine Frage durchschneidet das gedempfte Murmeln der Szene.",
            "stealth": "Mit angehaltenem Atem suchst du den leisen Weg.",
            "move": "Du setzt dich in Bewegung und ziehst die Szene mit dir weiter.",
            "freeform": "Die Welt reagiert auf dein Vorhaben mit gespannter Aufmerksamkeit.",
        }
        subject_hint = {
            "innkeeper": "Die Wirtin mustert dich mit sichtbarer Nervositaet.",
            "strangers": "Die drei Fremden beobachten dich ueber ihre Becherrander hinweg.",
            "courier": "Beim Wort 'Kurier' stockt fuer einen Augenblick jedes andere Geraeusch.",
            "clue": "Im Schmutz liegt etwas, das nicht zu einem gewoehnlichen Abend passt.",
            "default": "",
        }
        intro = intros.get(intent, intros["freeform"])
        focus = subject_hint.get(subject, "")
        parts = [intro, f"In {scene_title} verdichtet sich der Augenblick."]
        if focus:
            parts.append(focus)
        if fallback_hint:
            parts.append(fallback_hint)
        return " ".join(part.strip() for part in parts if part.strip())
