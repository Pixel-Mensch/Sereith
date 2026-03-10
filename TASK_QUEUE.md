# TASK_QUEUE.md

## Priority tasks
1. Decide and document the canonical source layout after the new engine path was added.
Status: In progress
Relevant files: `ARCHITECTURE.md`, `PROJECT_STATE.md`, `src/ai_pnp/`, `src/ai/`, `src/engine/`, `src/ui/`, `src/data/`
Expected outcome: One clearly preferred application path and explicit handling of parallel starter folders.
Notes: Current entry point and runtime now use `src/ai_pnp/engine/`, but parallel folders still exist.

2. Replace the placeholder narrator client with a local model adapter.
Status: Pending
Relevant files: `src/ai_pnp/services/llm/narrator_client.py`, `src/ai_pnp/services/llm/prompt_builder.py`
Expected outcome: Local model-backed narration with a stable adapter boundary.
Notes: Ollama is the documented primary candidate, but the adapter boundary should remain model-agnostic.

3. Deepen the deterministic engine path for actions and state progression.
Status: Pending
Relevant files: `src/ai_pnp/engine/flow/turn_processor.py`, `src/ai_pnp/engine/state/state_updater.py`, `src/ai_pnp/services/content/scene_repository.py`
Expected outcome: Richer state updates, clearer scene transitions, and stronger engine-owned truth.
Notes: The current scaffold covers observe, talk, stealth, move, and freeform at a first-pass level.

4. Move persistence toward the documented MVP storage direction.
Status: Pending
Relevant files: `src/ai_pnp/services/storage/save_repository.py`, future `db/sqlite/`
Expected outcome: SQLite-backed game state with clear save/load behavior.
Notes: Current verified state is JSON autosave only.

5. Expand tests around commands, persistence, and scene transitions.
Status: Pending
Relevant files: `tests/`
Expected outcome: Small reliable regression coverage for the prototype path.
Notes: Current verified coverage is one engine smoke test.

6. Refresh the lightweight module maps after the runtime path change.
Status: Pending
Relevant files: `docs/module-maps/`, `ARCHITECTURE.md`
Expected outcome: Low-cost navigation docs that match the active engine structure.
Notes: Module maps still reflect the earlier scaffold.
