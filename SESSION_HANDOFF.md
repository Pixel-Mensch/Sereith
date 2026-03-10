# SESSION_HANDOFF.md

## Session summary
- Audited the existing control-file workflow using a minimal repository slice.
- Re-verified Git state, entry points, smoke test, and key architecture files without scanning the full repo.
- Updated the control files so they reflect the currently verified local repo state instead of the earlier bootstrap context.

## Current repo state
- Canonical verified runtime path currently goes through `src/ai_pnp/`.
- A smoke test exists.
- Parallel folders exist under `src/` and still need an explicit structural decision.
- Current persistence is JSON autosave, not SQLite yet.
- `main` is the stable branch and `dev` is the current working branch.

## Validation
- `pytest -q`
- No build or linter command was discoverable in the minimal inspected slice.

## Recommended next action
1. Decide how to handle the parallel `src/` folders and document the result.
2. Replace the placeholder narrator client with a real local-model adapter.
3. Introduce a deterministic state-update path owned by the engine before expanding the UI.

## Relevant files
- `AGENTS.md`
- `PROJECT_STATE.md`
- `TASK_QUEUE.md`
- `ARCHITECTURE.md`
- `SESSION_HANDOFF.md`
- `main.py`
- `pyproject.toml`
- `src/ai_pnp/`
- `tests/test_smoke.py`
- `docs/module-maps/`

## Warnings, assumptions, and caveats
- The control files distinguish documented target state from verified local file state; keep that separation intact.
- The role of `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/` remains unresolved.
- No broad secret review or full repository scan was performed during this audit.
