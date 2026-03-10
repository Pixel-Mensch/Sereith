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
- `main.py` starts the CLI application through `ai_pnp.core.application`.
- The active runtime path is `main.py` -> `Application` -> `ai_pnp.engine.game_engine.GameEngine`.
- A CLI loop exists with `save`, `load`, `state`, and `quit` commands.
- A `TurnProcessor` exists and routes raw actions through action interpretation, prompt building, placeholder narration, state updates, and autosave.
- A `SceneRepository` loads two starter scenes from JSON content files.
- JSON-based save and load support exists through `SaveRepository`.
- `pyproject.toml` exists with a basic setuptools package definition for Python 3.11+.
- `tests/test_engine_smoke.py` exists and verifies that one turn can be processed.
- `docs/module-maps/` exists with initial module notes.
- Additional parallel folders exist under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/`. Their role relative to `src/ai_pnp/` is not yet fully documented.

## Major areas or modules
- `src/ai_pnp/core/`: application bootstrap plus core models for character, quest, world, and game state.
- `src/ai_pnp/engine/`: active engine flow with game engine, action interpretation, turn processing, and state updates.
- `src/ai_pnp/services/`: scene loading, narration adapter boundary, prompt building, and persistence.
- `src/ai_pnp/content/`: JSON world and scenario data for the starter scenes.
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

## Known issues
- The repository contains parallel structure candidates outside `src/ai_pnp/`, which creates ambiguity about the canonical architecture.
- Persistence is currently JSON based, while the documented MVP target says SQLite.
- The narrator client is still a placeholder and not connected to Ollama or another model backend.
- No real desktop or web UI exists yet.
- No linter or dedicated build command was discoverable in the minimal inspected slice.
- Older placeholder modules such as `content_loader.py`, `memory_service.py`, and `rules_engine.py` still exist locally but are not in the active runtime path.

## Current focus
- Stabilize the canonical project structure around the new engine path.
- Replace placeholder narration with a real local-model adapter.
- Deepen deterministic state progression beyond the first scaffold.
- Keep documentation aligned with verified local state.

## Risks and uncertainties
- It is not yet verified whether the non-`ai_pnp` folders under `src/` are legacy, experimental, or intended to remain.
- The current implementation does not yet enforce structured AI state proposals versus engine-owned state updates.
- Legal direction is documented, but no content review beyond the inspected starter files was performed.
- No broad secret audit was performed beyond the minimal inspected file set.
- `docs/module-maps/` was not refreshed in this session and may lag behind the new engine path.
