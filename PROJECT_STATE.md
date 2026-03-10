# PROJECT_STATE.md

## Documented project goal
- Build `AI-PnP`, a local PC-based AI Pen and Paper game.
- The LLM is the narrator only. Persistent truth belongs to the engine.
- The target game is a fantasy RPG with persistent world state, characters, quests, NPC relationships, inventory, and session history.
- The MVP storage direction is SQLite plus JSON-based world/config/prompt files.

## Current verified local state
- Git repository is initialized with `main` and `dev`.
- The current working branch is `dev`.
- The working tree was clean before this session started.
- A Python package scaffold exists under `src/ai_pnp/`.
- `main.py` now starts `Application.run()`.
- The active runtime path is `main.py` -> `Application` -> `ai_pnp.engine.game_engine.GameEngine`.
- `Application` currently reads `ui_mode` from `src/ai_pnp/data/config/app_config.json`.
- The default local `ui_mode` is `desktop`.
- A first `tkinter` desktop prototype now exists under `src/ai_pnp/ui/desktop/`.
- The desktop prototype exposes story text, free-text action input, player status, active quests, and save/load/new-game controls.
- The CLI loop still exists with `save`, `load`, `state`, and `quit` commands and remains reachable when `ui_mode` is set to `cli`.
- A `TurnProcessor` exists and routes raw actions through action interpretation, prompt building, narrator selection, state updates, and autosave.
- `SceneRepository`, `QuestRepository`, and `NpcRepository` load the first playable mini-flow from JSON content files.
- The playable scenario currently covers four scenes: `roadside_inn_intro`, `inn_common_room`, `inn_front`, and `roadside_clue`.
- The narrator facade now supports an Ollama-backed path plus a safe local fallback path.
- A multi-layer memory system now exists:
  - scene memory in `WorldState`
  - short-term memory in `turn_log`
  - long-term memory in facts, discovered information, discovered locations, quest progress, and NPC memory
  - generated session summaries after every 10 turns
- JSON-based save and load support exists through `SaveRepository`.
- `GameEngine` now exposes UI-oriented methods for player status, quests, current scene, last narration, recent log, save/load, and turn processing.
- `pyproject.toml` exists with a basic setuptools package definition for Python 3.11+.
- `tests/test_engine_smoke.py` exists and currently covers log capping, quest progress, NPC memory, session summaries, save/load, scene-memory updates, and UI-friendly engine API behavior.
- `docs/module-maps/` exists with initial module notes.
- Additional parallel folders exist under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/`. Their role relative to `src/ai_pnp/` is not yet fully documented.
- In the latest local validation run, engine initialization, turn processing, save/load, `tkinter` window creation, and `MainWindow` startup all worked.
- In the latest local validation run, the Ollama fallback path was exercised because the local Ollama service was not reachable from this environment.

## Major areas or modules
- `src/ai_pnp/core/`: application bootstrap plus core models for character, quest, world, and game state.
- `src/ai_pnp/engine/`: active engine flow with game engine, action interpretation, turn processing, and state updates.
- `src/ai_pnp/services/`: scene, quest, and NPC loading; Ollama/fallback narration; memory services; prompt building; and persistence.
- `src/ai_pnp/content/`: JSON world, scenario, NPC, quest, and prompt data for the first mini-flow.
- `src/ai_pnp/ui/`: CLI wrapper plus placeholder desktop UI module.
- `docs/module-maps/`: lightweight handwritten module summaries.
- Parallel starter areas also exist under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/`.

## Completed work
- Control-file workflow established.
- Initial Python project scaffold added.
- Minimal CLI entry path and smoke test added.
- Import-path bootstrap added so the current `src` layout works for local runs and tests.
- Control-file audit refreshed the documented repo state against the currently verified local files.
- Engine-first runtime scaffold added under `src/ai_pnp/engine/`.
- The starter world now has two JSON-backed scenes, a first turn pipeline, and JSON save/load support.
- The first playable mini-flow now spans the inn, its common room, the front yard, and a first clue site.
- Ollama integration was added behind `NarratorClient`, with safe fallback when the local service or model is unavailable.
- Save/load, discovery flags, and quest progress are now covered by small automated tests.
- Memory layers, NPC memory, session summaries, and stronger quest-state tracking are now wired into the active runtime and save system.
- The engine API was stabilized for UI consumption, including `get_last_narration()`, `get_recent_log()`, and dict-based save/load/action responses.
- The placeholder desktop module was replaced with a functional `tkinter` prototype wired directly to the engine.
- Local verification was expanded to cover engine startup, turn processing, save/load, serializability, and desktop-window startup.

## Known issues
- The repository contains parallel structure candidates outside `src/ai_pnp/`, which creates ambiguity about the canonical architecture.
- Persistence is currently JSON based, while the documented MVP target says SQLite.
- The live Ollama path is implemented, but an actual model response was not verifiable in this session because the local Ollama service was not reachable from the execution environment.
- The current desktop UI runs on the main thread; a slow LLM response can block the window until the request returns.
- No linter or dedicated build command was discoverable in the minimal inspected slice.
- Older placeholder modules such as `content_loader.py`, `memory_service.py`, and `rules_engine.py` still exist locally but are not in the active runtime path.

## Current focus
- Stabilize the canonical project structure around the new engine path.
- Verify the live Ollama path on a machine where the local service and model are available.
- Harden the desktop prototype without leaking game logic into the UI layer.
- Deepen deterministic quest, memory, and campaign progression beyond the first mini-flow.
- Keep documentation aligned with verified local state.

## Risks and uncertainties
- It is not yet verified whether the non-`ai_pnp` folders under `src/` are legacy, experimental, or intended to remain.
- The current implementation does not yet enforce structured AI state proposals versus engine-owned state updates.
- Legal direction is documented, but no content review beyond the inspected starter files was performed.
- No broad secret audit was performed beyond the minimal inspected file set.
- `docs/module-maps/` was not refreshed in this session and may lag behind the new engine path.
