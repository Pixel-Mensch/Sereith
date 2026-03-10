# SESSION_HANDOFF.md

## Session summary
- Verified the current engine, desktop UI, and tests locally before changing the UX layer.
- Extended `GameEngine` minimally with `get_world_status()`, `get_inventory()`, and `get_visible_npcs()` so the UI can display more state without reading internals directly.
- Rebuilt `src/ai_pnp/ui/desktop/main_window.py` into a more usable single-window desktop surface with clearer narration hierarchy, status, quests, inventory, visible NPCs, and a recent-action log.
- Kept UI callbacks thin: they only trigger engine methods, manage widget state, and refresh the view.
- Added desktop-focused smoke coverage and verified action, save, and load through the window against the local engine.
- Added `Start_AI-PnP.bat` in the repo root as a Windows launcher for the current desktop start path.

## Current repo state
- `src/` now contains only `src/ai_pnp/` as the canonical application tree.
- `main.py` still launches `Application.run()`, which starts the desktop app by default and can still fall back to CLI mode.
- `Start_AI-PnP.bat` now provides a direct Windows launcher for the desktop app.
- The CLI interaction path is now `scripts/run_cli.py` or `Application.run_cli()` -> `src/ai_pnp/ui/cli/runner.py` -> `GameEngine`.
- `GameEngine` no longer owns a direct input loop or console output.
- The desktop window now shows:
  - structured scene and narration text
  - character state
  - quest state
  - inventory
  - visible NPC/interactions
  - recent actions
  - status feedback and save/load/new-game controls
- Twelve focused tests exist and pass.
- Current persistence is JSON save/load, not SQLite yet.
- `main` is the stable branch and `dev` is the current working branch.

## Validation
- `pytest -q`
- scripted desktop check covering `MainWindow` startup, one player action, save, and load
- No build or linter command was discoverable in the minimal inspected slice.

## Recommended next action
1. Verify the desktop and CLI narrator path with a running local Ollama service and the configured model.
2. Move narrator requests off the desktop UI thread so the window stays responsive during slow responses.
3. Decide how much long-term campaign context the desktop UI should expose next, for example session summaries, facts, or richer NPC memory panels.

## Relevant files
- `AGENTS.md`
- `PROJECT_STATE.md`
- `TASK_QUEUE.md`
- `ARCHITECTURE.md`
- `SESSION_HANDOFF.md`
- `main.py`
- `Start_AI-PnP.bat`
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
- The desktop UI is now more usable, but narrator calls still run synchronously on the UI thread.
- Inventory interaction, richer NPC drill-downs, and session-summary panels are still not implemented.
