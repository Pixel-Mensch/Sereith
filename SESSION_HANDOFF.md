# SESSION_HANDOFF.md

## Session summary
- Verified the current structure instead of building on assumptions.
- Removed the redundant top-level placeholder trees under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/` after confirming they were not imported by the active runtime or tests.
- Removed the unused compatibility shim `src/ai_pnp/core/game_engine.py` so the engine has one canonical path at `src/ai_pnp/engine/game_engine.py`.
- Moved the CLI loop and console command parsing out of `GameEngine` into `src/ai_pnp/ui/cli/runner.py`.
- Updated `Application.run_cli()` to delegate to the CLI runner instead of hiding the loop inside the engine.
- Expanded tests to cover application boot and CLI-runner startup on top of the existing engine regressions.

## Current repo state
- `src/` now contains only `src/ai_pnp/` as the canonical application tree.
- `main.py` still launches `Application.run()`, which starts the desktop app by default and can still fall back to CLI mode.
- The CLI interaction path is now `scripts/run_cli.py` or `Application.run_cli()` -> `src/ai_pnp/ui/cli/runner.py` -> `GameEngine`.
- `GameEngine` no longer owns a direct input loop or console output.
- Ten focused tests exist and pass.
- Current persistence is JSON save/load, not SQLite yet.
- `main` is the stable branch and `dev` is the current working branch.

## Validation
- `pytest -q`
- `rg` import check confirming no active imports from the removed top-level `src/` placeholder trees
- scripted boot check for `Application`
- scripted CLI-runner check for `quit`
- No build or linter command was discoverable in the minimal inspected slice.

## Recommended next action
1. Verify the desktop and CLI narrator path with a running local Ollama service and the configured model.
2. Move narrator requests off the desktop UI thread so the window stays responsive during slow responses.
3. Decide whether the inactive internal placeholders inside `src/ai_pnp/services/` should be removed or turned into documented extension points.

## Relevant files
- `AGENTS.md`
- `PROJECT_STATE.md`
- `TASK_QUEUE.md`
- `ARCHITECTURE.md`
- `SESSION_HANDOFF.md`
- `main.py`
- `pyproject.toml`
- `src/ai_pnp/core/application.py`
- `src/ai_pnp/core/app_config.py`
- `src/ai_pnp/core/models/game_state.py`
- `src/ai_pnp/core/models/world_state.py`
- `src/ai_pnp/core/models/quest.py`
- `src/ai_pnp/core/models/npc_memory.py`
- `src/ai_pnp/engine/`
- `src/ai_pnp/ui/cli/runner.py`
- `src/ai_pnp/services/llm/`
- `src/ai_pnp/services/memory/`
- `src/ai_pnp/services/content/scene_repository.py`
- `src/ai_pnp/services/content/quest_repository.py`
- `src/ai_pnp/services/content/npc_repository.py`
- `src/ai_pnp/services/storage/save_repository.py`
- `src/ai_pnp/ui/desktop/app.py`
- `src/ai_pnp/ui/desktop/main_window.py`
- `src/ai_pnp/content/scenarios/prologue.json`
- `src/ai_pnp/content/quests/prologue_quests.json`
- `src/ai_pnp/content/npcs/prologue_npcs.json`
- `src/ai_pnp/content/prompts/narrator_rules.json`
- `src/ai_pnp/content/world/seed_world.json`
- `tests/test_engine_smoke.py`
- `docs/module-maps/`

## Warnings, assumptions, and caveats
- The control files distinguish documented target state from verified local file state; keep that separation intact.
- No broad secret review or full repository scan was performed during this audit.
- `docs/module-maps/` was not refreshed in this session and may lag behind the active engine path.
- The live Ollama integration is implemented, but the latest validation run only verified the fallback path because the local Ollama service was unreachable from this environment.
- The desktop prototype is functional, but narrator calls still run synchronously on the UI thread.
