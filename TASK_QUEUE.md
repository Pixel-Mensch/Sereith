# TASK_QUEUE.md

## Priority tasks
1. Decide and document the canonical source layout after the new engine path was added.
Status: In progress
Relevant files: `ARCHITECTURE.md`, `PROJECT_STATE.md`, `src/ai_pnp/`, `src/ai/`, `src/engine/`, `src/ui/`, `src/data/`
Expected outcome: One clearly preferred application path and explicit handling of parallel starter folders.
Notes: Current entry point and runtime now use `src/ai_pnp/engine/`, but parallel folders still exist.

2. Verify the live Ollama path with a running local model.
Status: In progress
Relevant files: `src/ai_pnp/services/llm/narrator_client.py`, `src/ai_pnp/services/llm/ollama_client.py`, `src/ai_pnp/data/config/app_config.json`
Expected outcome: Confirmed real model narration from the local Ollama service without losing the safe fallback path.
Notes: In the latest local validation run, the service was not reachable, so only the fallback path was verified.

3. Deepen the deterministic engine path for campaign memory and quest progression.
Status: Pending
Relevant files: `src/ai_pnp/engine/flow/turn_processor.py`, `src/ai_pnp/engine/state/state_updater.py`, `src/ai_pnp/services/memory/`, `src/ai_pnp/services/content/scene_repository.py`
Expected outcome: Richer state updates, clearer campaign continuity, and stronger engine-owned truth.
Notes: The current scaffold now has scene memory, short-term memory, long-term memory, and summary generation, but only for the first mini-flow.

4. Move persistence toward the documented MVP storage direction.
Status: Pending
Relevant files: `src/ai_pnp/services/storage/save_repository.py`, future `db/sqlite/`
Expected outcome: SQLite-backed game state with clear save/load behavior.
Notes: Current verified state is JSON save/load with slot naming via `save [name]` and `load [name]`.

5. Expand tests around narrator failure modes, memory retrieval quality, and quest branching.
Status: Pending
Relevant files: `tests/`
Expected outcome: Small reliable regression coverage for the prototype path.
Notes: Current verified coverage includes six focused engine tests.

6. Refresh the lightweight module maps after the runtime path change.
Status: Pending
Relevant files: `docs/module-maps/`, `ARCHITECTURE.md`
Expected outcome: Low-cost navigation docs that match the active engine structure.
Notes: Module maps still reflect the earlier scaffold.
