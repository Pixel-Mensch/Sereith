import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    project_name: str = "AI-PnP"
    language: str = "de"
    ui_mode: str = "cli"
    llm_provider: str = "ollama"
    ollama_model: str = "qwen2.5:7b"
    ollama_host: str = "http://localhost:11434"
    ollama_timeout_seconds: int = 30
    autosave: bool = True

    @classmethod
    def default_path(cls) -> Path:
        return Path(__file__).resolve().parents[1] / "data" / "config" / "app_config.json"

    @classmethod
    def from_file(cls, path: Path | None = None) -> "AppConfig":
        config_path = path or cls.default_path()
        with config_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return cls(
            project_name=payload.get("project_name", "AI-PnP"),
            language=payload.get("language", "de"),
            ui_mode=payload.get("ui_mode", "cli"),
            llm_provider=payload.get("llm_provider", "ollama"),
            ollama_model=payload.get("ollama_model", "qwen2.5:7b"),
            ollama_host=payload.get("ollama_host", "http://localhost:11434"),
            ollama_timeout_seconds=payload.get("ollama_timeout_seconds", 30),
            autosave=payload.get("autosave", True),
        )
