# ARCHITECTURE.md

## Documented target architecture
- Python application layer owns rules, persistence, state transitions, and orchestration.
- The LLM provides narration and optional structured state-update proposals only.
- Persistent game data is intended to move toward SQLite, with JSON files for world definitions, prompt templates, and config.
- UI should remain replaceable. The current local implementation now has desktop and CLI entry modes over the same engine core.

## Current verified local architecture
- Active entry point: `main.py`
- Alternate CLI entry point: `scripts/run_cli.py`
- Runtime path: `main.py` -> `ai_pnp.core.application.Application` -> desktop mode or CLI runner -> `ai_pnp.engine.game_engine.GameEngine`
- Core package: `src/ai_pnp/`
- Current default launch mode: `desktop` via `src/ai_pnp/data/config/app_config.json`
- The top-level `src/` tree now contains only `src/ai_pnp/`.
- Main services currently wired into the application:
  - `services/content/scene_repository.py`
  - `services/content/quest_repository.py`
  - `services/content/npc_repository.py`
  - `services/memory/memory_service.py`
  - `services/memory/session_summary_service.py`
  - `services/storage/save_repository.py`
  - `services/llm/narrator_client.py`
  - `services/llm/ollama_client.py`
  - `services/llm/prompt_builder.py`
- Active engine modules currently wired into the application:
  - `engine/game_engine.py`
  - `engine/parsing/action_interpreter.py`
  - `engine/flow/turn_processor.py`
  - `engine/state/state_updater.py`
- Current UI paths:
  - desktop window in `src/ai_pnp/ui/desktop/main_window.py`
  - desktop launcher in `src/ai_pnp/ui/desktop/app.py`
  - CLI runner in `src/ai_pnp/ui/cli/runner.py`
- Current persistence path: JSON autosave under `src/ai_pnp/data/saves/`

## Verified modules
- `src/ai_pnp/core/`: application bootstrap, config loading, and dataclass-based core models.
- `src/ai_pnp/core/models/`: character, quest, world state, game state, and NPC memory models.
- `src/ai_pnp/engine/`: active engine flow for commands, interpretation, turn processing, and state updates.
- `src/ai_pnp/services/`: scene, quest, and NPC loading; memory and summary services; prompt building; Ollama/fallback narration; and persistence.
- `src/ai_pnp/ui/cli/`: CLI runner wrapper.
- `src/ai_pnp/ui/desktop/`: first `tkinter` desktop prototype over the engine API.
  - `MainWindow` now renders story, character state, quests, inventory, visible NPCs, and recent actions.
- `src/ai_pnp/content/`: JSON-backed world, scenario, NPC, quest, and prompt content.
- `docs/module-maps/`: short handwritten module summaries.

## Important flows
- Current startup flow:
  `main.py` -> `Application` -> config + repositories + engine services -> `Application.run()` -> desktop or CLI mode
- Current CLI flow:
  `scripts/run_cli.py` or `Application.run_cli()` -> `ui/cli/runner.py` -> engine methods (`process_action`, `save_game`, `load_game`, `render_state_summary`)
- Current desktop flow:
  `MainWindow` -> engine UI methods (`get_*`, `process_player_action`, `save_game`, `load_game`) -> engine/services -> UI refresh
  The desktop window currently uses:
  - a dominant story panel with structured scene and narration rendering
  - read-only side panels for character, quests, inventory, NPCs, and recent actions
  - a status bar for feedback and error context
- Current turn flow:
  player text input -> command handling or `TurnProcessor` -> `ActionInterpreter` -> content-backed action lookup -> `PromptBuilder` -> `NarratorClient` -> `StateUpdater` -> `MemoryService` -> `SessionSummaryService` -> autosave
- Current persistence flow:
  `SaveRepository.save()` and `autosave()` write JSON save data under `src/ai_pnp/data/saves/`
- Current narrator flow:
  `NarratorClient` chooses `ollama` or fallback -> `OllamaClient` calls `/api/generate` when enabled -> failures become non-fatal fallback narration
- Current memory flow:
  scene memory lives in `WorldState` -> short-term memory in `turn_log` -> long-term memory in facts/quest progress/NPC memory -> summary snapshots every 10 turns

## Verified ambiguities
- Older local placeholder modules such as `content_loader.py` and `rules_engine.py` remain present inside `src/ai_pnp/services/`, but they are not part of the active runtime path.
- The live Ollama provider path is implemented, but successful model output was not verifiable in this session because the local service was unreachable.
- The desktop UI is currently synchronous and therefore sensitive to slow narrator calls.

## Important files and current role
- `main.py`: root entry point with local `src` path bootstrap and mode dispatch through `Application.run()`.
- `pyproject.toml`: minimal Python packaging metadata for the `src` layout.
- `scripts/run_cli.py`: alternate CLI launcher with the same local import bootstrap.
- `src/ai_pnp/core/application.py`: wires config, repositories, narrator, and engine services into the runtime and launches desktop or CLI mode.
- `src/ai_pnp/core/app_config.py`: loads the local runtime configuration from JSON.
- `src/ai_pnp/core/models/npc_memory.py`: persistent per-NPC memory records.
- `src/ai_pnp/engine/game_engine.py`: owns initial state creation, UI-friendly engine methods, and runtime orchestration without direct CLI I/O.
  The current UI-facing getters include player status, world status, inventory, visible NPCs, current scene, last narration, recent log, and save/load methods.
- `src/ai_pnp/engine/flow/turn_processor.py`: executes the per-turn pipeline.
- `src/ai_pnp/engine/parsing/action_interpreter.py`: classifies raw player actions into coarse intents.
- `src/ai_pnp/engine/state/state_updater.py`: applies deterministic state changes and turn logging.
- `src/ai_pnp/services/content/scene_repository.py`: loads scenes, exits, and action effects from JSON.
- `src/ai_pnp/services/content/quest_repository.py`: loads the initial quest state from JSON.
- `src/ai_pnp/services/content/npc_repository.py`: loads visible NPC context from JSON.
- `src/ai_pnp/services/memory/memory_service.py`: owns short-term and long-term memory updates.
- `src/ai_pnp/services/memory/session_summary_service.py`: creates non-LLM session summaries every 10 turns.
- `src/ai_pnp/services/llm/ollama_client.py`: encapsulates the local Ollama HTTP call.
- `src/ai_pnp/services/llm/narrator_client.py`: narrator facade with provider selection and fallback handling.
- `src/ai_pnp/services/storage/save_repository.py`: current JSON save/load implementation.
- `src/ai_pnp/ui/cli/runner.py`: owns CLI command parsing, the interactive loop, and console I/O.
- `src/ai_pnp/ui/desktop/app.py`: thin launcher for the desktop app.
- `src/ai_pnp/ui/desktop/main_window.py`: current `tkinter` desktop window with structured story presentation, status panels, inventory, NPCs, recent actions, and control buttons.
- `tests/test_engine_smoke.py`: current focused engine, memory, save/load, application-boot, CLI-runner, and desktop-window smoke regression test set.

## Principles
- UI must not own game logic.
- The LLM must not own persistent truth.
- Documented target state and verified local file state must remain clearly separated.
