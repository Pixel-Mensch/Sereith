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

## Verified ambiguities
- Parallel top-level folders also exist under `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/`.
- The current inspected entry path does not use those folders directly.
- Until documented otherwise, treat `src/ai_pnp/` as the canonical application path and the parallel folders as unresolved structure.

## Principles
- UI must not own game logic.
- The LLM must not own persistent truth.
- Documented target state and verified local file state must remain clearly separated.
