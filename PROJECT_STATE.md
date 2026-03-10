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
- `src/` now contains only the canonical application package `src/ai_pnp/`.
- `main.py` now starts `Application.run()`.
- `Start_AI-PnP.bat` exists in the repository root as a Windows double-click launcher for the current desktop start path.
- The active runtime path is `main.py` -> `Application` -> desktop mode or CLI runner -> `ai_pnp.engine.game_engine.GameEngine`.
- `Application` currently reads `ui_mode` from `src/ai_pnp/data/config/app_config.json`.
- The default local `ui_mode` is `desktop`.
- A first `tkinter` desktop prototype now exists under `src/ai_pnp/ui/desktop/`.
- The desktop prototype now exposes:
  - structured scene and narration display
  - free-text action input with fast re-focus
  - player status with chapter, time, and location
  - active quest overview
  - inventory panel
  - visible NPC/interactions panel
  - recent action log
  - save/load/new-game/refresh controls
- The CLI loop now lives in `src/ai_pnp/ui/cli/runner.py`.
- The CLI still supports `save`, `load`, `state`, and `quit` and remains reachable when `ui_mode` is set to `cli` or via `scripts/run_cli.py`.
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
- `GameEngine` now exposes UI-oriented methods for player status, world status, quests, inventory, visible NPCs, current scene, last narration, recent log, save/load, and turn processing.
- `pyproject.toml` exists with a basic setuptools package definition for Python 3.11+.
- `tests/test_engine_smoke.py` exists and currently covers log capping, quest progress, NPC memory, session summaries, save/load, scene-memory updates, UI-friendly engine API behavior, application boot, CLI-runner startup, and desktop-window smoke checks.
- `docs/module-maps/` exists with initial module notes.
- In the latest local validation run, engine initialization, turn processing, save/load, `tkinter` window creation, `MainWindow` startup, and a desktop action/save/load flow all worked.
- In the latest local validation run, the Ollama fallback path was exercised because the local Ollama service was not reachable from this environment.

## Major areas or modules
- `src/ai_pnp/core/`: application bootstrap plus core models for character, quest, world, and game state.
- `src/ai_pnp/engine/`: active engine flow with game engine, action interpretation, turn processing, and state updates.
- `src/ai_pnp/services/`: scene, quest, and NPC loading; Ollama/fallback narration; memory services; prompt building; and persistence.
- `src/ai_pnp/content/`: JSON world, scenario, NPC, quest, and prompt data for the first mini-flow.
- `src/ai_pnp/ui/`: CLI and desktop UI layers over the same engine core.
- `docs/module-maps/`: lightweight handwritten module summaries.

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
- The redundant parallel source trees under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/` were removed after verifying they had no imports in the active runtime.
- The old compatibility re-export `src/ai_pnp/core/game_engine.py` was removed to keep a single engine path at `src/ai_pnp/engine/game_engine.py`.
- The CLI loop and command parsing were moved out of `GameEngine` into `src/ai_pnp/ui/cli/runner.py`.
- The desktop UI was upgraded from a bare prototype to a more usable play surface with clearer narration hierarchy, inventory, NPC/interactions, and recent-action panels.
- The engine was extended minimally for UI display with `get_world_status()`, `get_inventory()`, and `get_visible_npcs()`.
- Desktop-adjacent smoke coverage was added and the current local suite now passes with `12` tests.
- A root Windows launcher file was added so the project can be started by double-click without typing the Python command manually.

## Known issues
- Persistence is currently JSON based, while the documented MVP target says SQLite.
- The live Ollama path is implemented, but an actual model response was not verifiable in this session because the local Ollama service was not reachable from the execution environment.
- The current desktop UI runs on the main thread; a slow LLM response can block the window until the request returns.
- No linter or dedicated build command was discoverable in the minimal inspected slice.
- Some internal placeholder modules such as `src/ai_pnp/services/content/content_loader.py` and `src/ai_pnp/services/rules/rules_engine.py` still exist locally but are not in the active runtime path.
- The desktop UI is still a single-window prototype; advanced navigation, inventory actions, and richer NPC drill-downs are not implemented yet.

## Current focus
- Verify the live Ollama path on a machine where the local service and model are available.
- Harden the desktop prototype further without leaking game logic into the UI layer.
- Deepen deterministic quest, memory, and campaign progression beyond the first mini-flow.
- Keep documentation aligned with verified local state.

## Risks and uncertainties
- The current implementation does not yet enforce structured AI state proposals versus engine-owned state updates.
- Legal direction is documented, but no content review beyond the inspected starter files was performed.
- No broad secret audit was performed beyond the minimal inspected file set.
- `docs/module-maps/` was not refreshed in this session and may lag behind the new engine path.
