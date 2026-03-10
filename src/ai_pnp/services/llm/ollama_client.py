import json
from dataclasses import dataclass
from urllib import error, request


class OllamaClientError(Exception):
    pass


@dataclass
class OllamaClient:
    host: str
    timeout_seconds: int = 30

    def generate(self, *, model: str, prompt: str) -> str:
        if not model:
            raise OllamaClientError("Kein Ollama-Modell konfiguriert.")

        payload = json.dumps(
            {
                "model": model,
                "prompt": prompt,
                "stream": False,
            }
        ).encode("utf-8")
        http_request = request.Request(
            self._build_endpoint(),
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            raise OllamaClientError(self._extract_error_message(exc)) from exc
        except error.URLError as exc:
            raise OllamaClientError(
                "Ollama ist nicht erreichbar. Pruefe, ob der lokale Dienst laeuft."
            ) from exc
        except TimeoutError as exc:
            raise OllamaClientError("Ollama hat nicht rechtzeitig geantwortet.") from exc

        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise OllamaClientError("Ollama hat eine ungueltige Antwort geliefert.") from exc

        response_text = payload.get("response", "").strip()
        if not response_text:
            raise OllamaClientError("Ollama hat eine leere Antwort geliefert.")
        return response_text

    def _build_endpoint(self) -> str:
        base = self.host.rstrip("/")
        if base.endswith("/api"):
            return f"{base}/generate"
        return f"{base}/api/generate"

    def _extract_error_message(self, exc: error.HTTPError) -> str:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
        except Exception:
            payload = {}
        message = payload.get("error") or exc.reason
        return f"Ollama-Fehler: {message}"
