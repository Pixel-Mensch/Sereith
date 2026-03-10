# TASK_QUEUE.md

## Priority tasks
1. Verify the live Ollama path with a running local model from the desktop and CLI paths.
Status: In progress
Relevant files: `src/ai_pnp/services/llm/narrator_client.py`, `src/ai_pnp/services/llm/ollama_client.py`, `src/ai_pnp/data/config/app_config.json`, `src/ai_pnp/ui/desktop/`
Expected outcome: Confirmed real model narration from the local Ollama service without losing the safe fallback path.
Notes: In the latest local validation run, the service was not reachable, so only the fallback path was verified.

2. Move narrator calls off the desktop UI thread.
Status: Pending
Relevant files: `src/ai_pnp/ui/desktop/main_window.py`, `src/ai_pnp/services/llm/narrator_client.py`, `src/ai_pnp/engine/game_engine.py`
Expected outcome: The desktop window remains responsive while the narrator request is running.
Notes: The current verified desktop UI now gives clearer feedback during actions, but narrator calls are still synchronous and can block during slow local-model responses.

3. Deepen the deterministic engine path for campaign memory and quest progression.
Status: Pending
Relevant files: `src/ai_pnp/engine/flow/turn_processor.py`, `src/ai_pnp/engine/state/state_updater.py`, `src/ai_pnp/services/memory/`, `src/ai_pnp/services/content/scene_repository.py`
Expected outcome: Richer state updates, clearer campaign continuity, and stronger engine-owned truth.
Notes: The current scaffold now has scene memory, short-term memory, long-term memory, and summary generation, but only for the first mini-flow.

4. Expand tests around narrator failure modes, desktop-engine integration, memory retrieval quality, and quest branching.
Status: Pending
Relevant files: `tests/`
Expected outcome: Small reliable regression coverage for the prototype path.
Notes: Current verified coverage includes twelve focused tests plus manual desktop start/action/save/load verification.

5. Move persistence toward the documented MVP storage direction.
Status: Pending
Relevant files: `src/ai_pnp/services/storage/save_repository.py`, future `db/sqlite/`
Expected outcome: SQLite-backed game state with clear save/load behavior.
Notes: Current verified state is JSON save/load with slot naming via the engine API and CLI commands.

6. Refresh the lightweight module maps after the runtime path change.
Status: Pending
Relevant files: `docs/module-maps/`, `ARCHITECTURE.md`
Expected outcome: Low-cost navigation docs that match the active engine structure.
Notes: Module maps still reflect the earlier scaffold and do not yet cover the cleaned canonical `src/ai_pnp` layout.

7. Decide how far the desktop UI should surface session summaries, facts, and NPC memory without overloading the screen.
Status: Pending
Relevant files: `src/ai_pnp/ui/desktop/main_window.py`, `src/ai_pnp/engine/game_engine.py`
Expected outcome: A clearer plan for the next useful information panels after the current status/quest/inventory/log baseline.
Notes: The current UI already exposes the most important immediate gameplay data, but long-term campaign context is still mostly hidden.

## Recently completed
1. Stabilize the canonical source layout under `src/ai_pnp/`.
Status: Completed
Relevant files: `src/ai_pnp/`, `src/ai/`, `src/engine/`, `src/ui/`, `src/data/`, `src/ai_pnp/ui/cli/runner.py`, `src/ai_pnp/engine/game_engine.py`
Expected outcome: One clearly preferred application path, no redundant top-level `src/` trees, and CLI interaction outside the engine core.
Notes: Completed by removing unreferenced legacy placeholder trees and moving the CLI loop into the UI layer.

2. Upgrade the first desktop UI from prototype to more usable play surface.
Status: Completed
Relevant files: `src/ai_pnp/ui/desktop/main_window.py`, `src/ai_pnp/engine/game_engine.py`, `tests/test_engine_smoke.py`
Expected outcome: Better readability, clearer layout, more visible gameplay data, and light desktop smoke coverage.
Notes: Completed with structured story presentation, character/quest/inventory/NPC/log panels, and UI-focused smoke validation.

3. Add a direct Windows launcher for the current desktop start path.
Status: Completed
Relevant files: `Start_AI-PnP.bat`, `README.md`
Expected outcome: The project can be started on Windows by double-click without manually typing the Python command.
Notes: Completed as a root batch launcher that tries `pyw`, `pythonw`, `py`, and `python` in that order.
