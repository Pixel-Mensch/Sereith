# AI-PnP

Desktop-first AI Pen and Paper project with a persistent game state.
The LLM is only the narrator.
The actual rules, state, memory, and persistence live in the application core.
The first verified content basis is now the Sereith starter region around Eidenkehr on the Valedorn-Seufzerforst border.

## Current local runtime

- `main.py` starts the desktop application by default.
- The active runtime path is `Application -> GameEngine -> TurnProcessor`.
- `Application` reads `src/ai_pnp/data/config/app_config.json` and launches either:
  - desktop mode via `tkinter`
  - CLI mode when `ui_mode` is set to `cli`
- The desktop prototype currently provides:
  - structured story view with scene header and latest narration
  - free-text player input with direct resend focus
  - character, chapter, time, and location status
  - active quest overview
  - inventory panel
  - visible NPC/interactions panel
  - recent action log
  - `Neues Spiel`, `Speichern`, `Laden`, and `Aktualisieren`
- Commands currently supported in the CLI:
  - `state`
  - `save [name]`
  - `load [name]`
  - `quit`
- The current scaffold contains:
  - initial character and quest
  - a Sereith-backed starter region with six scenes for the first mini-campaign
  - action interpretation with simple subject detection
  - prompt building with scene, NPC, quest, short-term memory, long-term facts, and session summary context
  - Ollama-backed narration with safe fallback
  - JSON save/load and autosave
  - scene memory, short-term memory, long-term memory, and session summaries
  - UI-friendly engine methods for scene, narration, player status, quests, save/load, and recent log access

## Current direction

The project is designed to stay legally publishable by using a Pathfinder-compatible rules approach
while avoiding direct use of protected setting IP.

## Run desktop

```python
python main.py
```

Oder unter Windows per Doppelklick:

```text
Start_AI-PnP.bat
```

## Run CLI

Set `"ui_mode": "cli"` in `src/ai_pnp/data/config/app_config.json`, then run:

```python
python main.py
```

## Ollama

- Default config lives in `src/ai_pnp/data/config/app_config.json`
- Current local narrator config:
  - `llm_provider = "ollama"`
  - `ollama_model = "qwen2.5:7b"`
  - `ollama_host = "http://localhost:11434"`
- If Ollama is not running or the model is missing, the CLI falls back to a local placeholder narrator and keeps the game running.
- The same fallback path is used in the desktop prototype, so the app remains playable without a live Ollama service.

## Test

```python
pytest -q
```

## Verified in the latest local session

- Engine initialization works.
- Turn processing works.
- JSON save/load works.
- `GameState` remains serializable.
- `tkinter` window creation works locally.
- `MainWindow` can be instantiated, refreshed, and driven through an action plus save/load.
- `13` focused tests currently pass.
- A root Windows launcher file exists and points at the current desktop start path.

## Notes

- Current verified persistence is JSON save/load under `src/ai_pnp/data/saves/`.
- SQLite remains the documented MVP target, not the current local implementation.
- In the latest local validation run, the fallback narrator path was exercised because Ollama was not reachable from the environment.
- The desktop UI is intentionally thin: game logic stays in `GameEngine`, `TurnProcessor`, and related services.
- The desktop UI still calls the narrator synchronously on the main thread; slow model responses can still block the window for now.
- The verified starter questline is `Die stillen Register von Eidenkehr`, built around a missing courier, unstable registers, suspiciously smooth healing, and the first quiet signs of the White Ebb.
