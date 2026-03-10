# TASK_QUEUE.md

## Priority tasks
1. Decide and document the canonical source layout.
Status: In progress
Relevant files: `ARCHITECTURE.md`, `PROJECT_STATE.md`, `src/ai_pnp/`, `src/ai/`, `src/engine/`, `src/ui/`, `src/data/`
Expected outcome: One clearly preferred application path and explicit handling of parallel starter folders.
Notes: Current entry point uses `src/ai_pnp/`, but parallel folders still exist.

2. Replace placeholder narrator client with a local Ollama adapter.
Status: Pending
Relevant files: `src/ai_pnp/services/llm/narrator_client.py`, `src/ai_pnp/services/llm/prompt_builder.py`
Expected outcome: Local model-backed narration with a stable adapter boundary.

3. Move persistence toward the documented MVP storage direction.
Status: Pending
Relevant files: `src/ai_pnp/services/storage/save_repository.py`, future `db/sqlite/`
Expected outcome: SQLite-backed game state with clear save/load behavior.
Notes: Current verified state is JSON autosave only.

4. Implement the first playable scene loop.
Status: Pending
Relevant files: `src/ai_pnp/core/game_engine.py`, `src/ai_pnp/services/*`, `src/ai_pnp/core/models/*`
Expected outcome: Input -> rules -> prompt -> narration -> state update -> save.

5. Expand tests around boot, persistence, and state transitions.
Status: Pending
Relevant files: `tests/`
Expected outcome: Small reliable regression coverage for the prototype path.
