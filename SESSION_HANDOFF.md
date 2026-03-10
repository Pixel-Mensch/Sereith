# SESSION_HANDOFF.md

## Session summary
- Built the first engine-first runtime scaffold inside `src/ai_pnp/`.
- Added `engine/` modules for command handling, action interpretation, turn processing, and deterministic state updates.
- Added JSON-backed scene content plus a `SceneRepository`.
- Reworked the active runtime so `Application` now wires the new engine path.
- Added JSON save/load support with autosave and a smoke test for one processed turn.

## Current repo state
- Canonical verified runtime path currently goes through `src/ai_pnp/engine/`.
- `main.py` and `scripts/run_cli.py` can start the CLI path.
- A smoke test exists and passes.
- Parallel folders exist under `src/` and still need an explicit structural decision.
- Current persistence is JSON save/load, not SQLite yet.
- `main` is the stable branch and `dev` is the current working branch.

## Validation
- `pytest -q`
- `python main.py`
- No build or linter command was discoverable in the minimal inspected slice.

## Recommended next action
1. Decide how to handle the parallel `src/` folders and older placeholder modules.
2. Replace the placeholder narrator client with a real local-model adapter.
3. Enrich the deterministic engine path with richer scene effects, quest progression, and stronger save/load coverage.

## Relevant files
- `AGENTS.md`
- `PROJECT_STATE.md`
- `TASK_QUEUE.md`
- `ARCHITECTURE.md`
- `SESSION_HANDOFF.md`
- `main.py`
- `pyproject.toml`
- `src/ai_pnp/core/application.py`
- `src/ai_pnp/engine/`
- `src/ai_pnp/services/content/scene_repository.py`
- `src/ai_pnp/services/storage/save_repository.py`
- `src/ai_pnp/content/scenarios/prologue.json`
- `src/ai_pnp/content/world/seed_world.json`
- `tests/test_engine_smoke.py`
- `docs/module-maps/`

## Warnings, assumptions, and caveats
- The control files distinguish documented target state from verified local file state; keep that separation intact.
- The role of `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/` remains unresolved.
- No broad secret review or full repository scan was performed during this audit.
- `docs/module-maps/` was not refreshed in this session and may lag behind the active engine path.
