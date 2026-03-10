# SESSION_HANDOFF.md

## Session summary
- Verified the current local scaffold after recent user changes.
- Fixed the immediate `src`-layout startup issue so `main.py`, `scripts/run_cli.py`, and tests can import `ai_pnp`.
- Updated the control files to separate documented target architecture from verified local file state.
- Prepared the repository for a clean baseline commit on `main`.

## Current repo state
- Canonical verified runtime path currently goes through `src/ai_pnp/`.
- A smoke test exists.
- Parallel folders exist under `src/` and still need an explicit structural decision.
- Current persistence is JSON autosave, not SQLite yet.

## Validation
- `pytest -q`
- `python main.py`

## Recommended next action
1. Decide how to handle the parallel `src/` folders and document the result.
2. Replace the placeholder narrator client with a real Ollama-backed adapter.
3. Introduce a deterministic state-update path owned by the engine before expanding the UI.

## Relevant files
- `main.py`
- `pyproject.toml`
- `src/ai_pnp/`
- `tests/test_smoke.py`
- `tests/conftest.py`
- `docs/module-maps/`
