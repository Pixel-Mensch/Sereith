# SESSION_HANDOFF.md

## Session summary
- Built the first actually playable mini-flow around the missing courier.
- Added content-backed scene, quest, NPC, and prompt data for the inn and roadside clue sequence.
- Added an Ollama-backed narrator path behind `NarratorClient` plus a safe fallback path when the local service or model is unavailable.
- Expanded deterministic state progression for discovery flags, quest progress, scene transitions, and turn logging.
- Expanded tests to cover turn processing, save/load, scene changes, and first clue progression.

## Current repo state
- Canonical verified runtime path currently goes through `src/ai_pnp/engine/`.
- `main.py` and `scripts/run_cli.py` can start the CLI path.
- The CLI now supports a first playable inn -> outside -> clue flow.
- Four focused tests exist and pass.
- Parallel folders exist under `src/` and still need an explicit structural decision.
- Current persistence is JSON save/load, not SQLite yet.
- `main` is the stable branch and `dev` is the current working branch.

## Validation
- `pytest -q`
- `python main.py`
- Scripted CLI run covering `state`, asking about the courier, going outside, investigating the clue, saving, and loading
- No build or linter command was discoverable in the minimal inspected slice.

## Recommended next action
1. Decide how to handle the parallel `src/` folders and older placeholder modules.
2. Verify the live Ollama path with a running local service and the configured model.
3. Extend the mini-flow with branching reactions, follow-up consequences, and more quest-state assertions.

## Relevant files
- `AGENTS.md`
- `PROJECT_STATE.md`
- `TASK_QUEUE.md`
- `ARCHITECTURE.md`
- `SESSION_HANDOFF.md`
- `main.py`
- `pyproject.toml`
- `src/ai_pnp/core/application.py`
- `src/ai_pnp/core/app_config.py`
- `src/ai_pnp/engine/`
- `src/ai_pnp/services/llm/`
- `src/ai_pnp/services/content/scene_repository.py`
- `src/ai_pnp/services/content/quest_repository.py`
- `src/ai_pnp/services/content/npc_repository.py`
- `src/ai_pnp/services/storage/save_repository.py`
- `src/ai_pnp/content/scenarios/prologue.json`
- `src/ai_pnp/content/quests/prologue_quests.json`
- `src/ai_pnp/content/npcs/prologue_npcs.json`
- `src/ai_pnp/content/prompts/narrator_rules.json`
- `src/ai_pnp/content/world/seed_world.json`
- `tests/test_engine_smoke.py`
- `docs/module-maps/`

## Warnings, assumptions, and caveats
- The control files distinguish documented target state from verified local file state; keep that separation intact.
- The role of `src/ai/`, `src/engine/`, `src/ui/`, and `src/data/` remains unresolved.
- No broad secret review or full repository scan was performed during this audit.
- `docs/module-maps/` was not refreshed in this session and may lag behind the active engine path.
- The live Ollama integration is implemented, but the latest validation run only verified the fallback path because the local Ollama service was unreachable from this environment.
