# ARCHITECTURE.md

## Documented target architecture
- Python application layer owns rules, persistence, state transitions, and orchestration.
- The LLM provides narration and optional structured state-update proposals only.
- Persistent game data is intended to move toward SQLite, with JSON files for world definitions, prompt templates, and config.
- UI should remain replaceable. CLI exists now; desktop or local web UI can follow later.

## Current verified local architecture
- Active entry point: `main.py`
- Runtime path: `main.py` -> `ai_pnp.core.application.Application` -> `ai_pnp.core.game_engine.GameEngine`
- Core package: `src/ai_pnp/`
- Main services currently wired into the application:
  - `services/content/content_loader.py`
  - `services/storage/save_repository.py`
  - `services/rules/rules_engine.py`
  - `services/memory/memory_service.py`
  - `services/llm/narrator_client.py`
  - `services/llm/prompt_builder.py`
- Current UI path: CLI loop inside `src/ai_pnp/core/game_engine.py`
- Current persistence path: JSON autosave under `src/ai_pnp/data/saves/`

## Verified modules
- `src/ai_pnp/core/`: application bootstrap and game loop.
- `src/ai_pnp/core/models/`: dataclass-based models for character, quest, location, NPC, and game state.
- `src/ai_pnp/services/`: placeholder service layer for content, storage, rules, memory, and narration.
- `src/ai_pnp/ui/cli/`: CLI runner wrapper.
- `src/ai_pnp/ui/desktop/`: placeholder desktop app module.
- `src/ai_pnp/content/`: authored content placeholders.
- `docs/module-maps/`: short handwritten module summaries.

## Important flows
- Current startup flow:
  `main.py` -> `ai_pnp.core.application.Application` -> `GameEngine.run_cli()`
- Current turn flow:
  player text input -> rules evaluation -> prompt build -> narrator response -> memory record -> autosave
- Current persistence flow:
  `SaveRepository.autosave()` writes JSON save data under `src/ai_pnp/data/saves/`

## Verified ambiguities
- Parallel top-level folders also exist under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/`.
- The current inspected entry path does not use those folders directly.
- Until documented otherwise, treat `src/ai_pnp/` as the canonical application path and the parallel folders as unresolved structure.

## Important files and current role
- `main.py`: root CLI entry point with local `src` path bootstrap.
- `pyproject.toml`: minimal Python packaging metadata for the `src` layout.
- `scripts/run_cli.py`: alternate CLI launcher with the same local import bootstrap.
- `src/ai_pnp/core/application.py`: wires the current service set into the engine.
- `src/ai_pnp/core/game_engine.py`: owns the current CLI loop and turn orchestration.
- `src/ai_pnp/services/storage/save_repository.py`: current JSON autosave implementation.
- `tests/test_smoke.py`: current minimal boot test.

## Principles
- UI must not own game logic.
- The LLM must not own persistent truth.
- Documented target state and verified local file state must remain clearly separated.
