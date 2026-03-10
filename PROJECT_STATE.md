# PROJECT_STATE.md

## Documented project goal
- Build `AI-PnP`, a local PC-based AI Pen and Paper game.
- The LLM is the narrator only. Persistent truth belongs to the engine.
- The target game is a fantasy RPG with persistent world state, characters, quests, NPC relationships, inventory, and session history.
- The MVP storage direction is SQLite plus JSON-based world/config/prompt files.

## Current verified local state
- Git repository is initialized with `main` and `dev`.
- The current working branch is `dev`.
- The working tree was clean at audit time.
- A Python package scaffold exists under `src/ai_pnp/`.
- `main.py` starts the CLI application through `ai_pnp.core.application`.
- A minimal CLI loop, placeholder narrator client, prompt builder, rules engine, memory service, content loader, and JSON autosave repository are present.
- `pyproject.toml` exists with a basic setuptools package definition for Python 3.11+.
- `tests/test_smoke.py` exists.
- `docs/module-maps/` exists with initial module notes.
- Additional parallel folders exist under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/`. Their role relative to `src/ai_pnp/` is not yet fully documented.

## Major areas or modules
- `src/ai_pnp/core/`: application bootstrap and current game loop.
- `src/ai_pnp/core/models/`: current game-state model layer.
- `src/ai_pnp/services/`: content loading, narration, rules, memory, and persistence services.
- `src/ai_pnp/ui/`: CLI wrapper plus placeholder desktop UI module.
- `docs/module-maps/`: lightweight handwritten module summaries.
- Parallel starter areas also exist under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/`.

## Completed work
- Control-file workflow established.
- Initial Python project scaffold added.
- Minimal CLI entry path and smoke test added.
- Import-path bootstrap added so the current `src` layout works for local runs and tests.
- Control-file audit refreshed the documented repo state against the currently verified local files.

## Known issues
- The repository contains parallel structure candidates outside `src/ai_pnp/`, which creates ambiguity about the canonical architecture.
- Persistence is currently JSON autosave based, while the documented MVP target says SQLite.
- The narrator client is still a placeholder and not connected to Ollama or another model backend.
- No real desktop or web UI exists yet.
- No linter or dedicated build command was discoverable in the minimal inspected slice.

## Current focus
- Stabilize the canonical project structure.
- Replace placeholder systems with the first playable vertical slice.
- Keep documentation aligned with verified local state.

## Risks and uncertainties
- It is not yet verified whether the non-`ai_pnp` folders under `src/` are legacy, experimental, or intended to remain.
- The current implementation does not yet enforce structured AI state proposals versus engine-owned state updates.
- Legal direction is documented, but no content review beyond the inspected starter files was performed.
- No broad secret audit was performed beyond the minimal inspected file set.
