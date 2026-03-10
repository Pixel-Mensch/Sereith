# ARCHITECTURE.md

## Documented target architecture
- Python application layer owns rules, persistence, state transitions, and orchestration.
- The LLM provides narration and optional structured state-update proposals only.
- Persistent game data is intended to move toward SQLite, with JSON files for world definitions, prompt templates, and config.
- UI should remain replaceable. CLI exists now; desktop or local web UI can follow later.

## Current verified local architecture
- Active entry point: `main.py`
- Alternate CLI entry point: `scripts/run_cli.py`
- Runtime path: `main.py` -> `ai_pnp.core.application.Application` -> `ai_pnp.engine.game_engine.GameEngine`
- Core package: `src/ai_pnp/`
- Main services currently wired into the application:
  - `services/content/scene_repository.py`
  - `services/storage/save_repository.py`
  - `services/llm/narrator_client.py`
  - `services/llm/prompt_builder.py`
- Active engine modules currently wired into the application:
  - `engine/game_engine.py`
  - `engine/parsing/action_interpreter.py`
  - `engine/flow/turn_processor.py`
  - `engine/state/state_updater.py`
- Current UI path: CLI loop inside `src/ai_pnp/engine/game_engine.py`
- Current persistence path: JSON autosave under `src/ai_pnp/data/saves/`

## Verified modules
- `src/ai_pnp/core/`: application bootstrap and dataclass-based core models.
- `src/ai_pnp/core/models/`: character, quest, world state, and game state models.
- `src/ai_pnp/engine/`: active engine flow for commands, interpretation, turn processing, and state updates.
- `src/ai_pnp/services/`: scene loading, prompt building, narration boundary, and persistence.
- `src/ai_pnp/ui/cli/`: CLI runner wrapper.
- `src/ai_pnp/ui/desktop/`: placeholder desktop app module.
- `src/ai_pnp/content/`: JSON-backed starter world and scenario content.
- `docs/module-maps/`: short handwritten module summaries.

## Important flows
- Current startup flow:
  `main.py` -> `Application` -> repositories and engine services -> `GameEngine.run_cli()`
- Current turn flow:
  player text input -> command handling or `TurnProcessor` -> `ActionInterpreter` -> `PromptBuilder` -> `NarratorClient` -> `StateUpdater` -> autosave
- Current persistence flow:
  `SaveRepository.save()` and `autosave()` write JSON save data under `src/ai_pnp/data/saves/`

## Verified ambiguities
- Parallel top-level folders also exist under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/`.
- The current inspected entry path does not use those folders directly.
- Until documented otherwise, treat `src/ai_pnp/` as the canonical application path and the parallel folders as unresolved structure.
- Older local placeholder modules such as `content_loader.py`, `memory_service.py`, and `rules_engine.py` remain present but are not part of the active runtime path.

## Important files and current role
- `main.py`: root CLI entry point with local `src` path bootstrap.
- `pyproject.toml`: minimal Python packaging metadata for the `src` layout.
- `scripts/run_cli.py`: alternate CLI launcher with the same local import bootstrap.
- `src/ai_pnp/core/application.py`: wires the current repositories and engine services into the runtime.
- `src/ai_pnp/engine/game_engine.py`: owns CLI command handling, initial state creation, and runtime orchestration.
- `src/ai_pnp/engine/flow/turn_processor.py`: executes the per-turn pipeline.
- `src/ai_pnp/engine/parsing/action_interpreter.py`: classifies raw player actions into coarse intents.
- `src/ai_pnp/engine/state/state_updater.py`: applies deterministic state changes and turn logging.
- `src/ai_pnp/services/content/scene_repository.py`: loads the starter world and scenes from JSON.
- `src/ai_pnp/services/storage/save_repository.py`: current JSON save/load implementation.
- `tests/test_engine_smoke.py`: current minimal engine smoke test.

## Principles
- UI must not own game logic.
- The LLM must not own persistent truth.
- Documented target state and verified local file state must remain clearly separated.
