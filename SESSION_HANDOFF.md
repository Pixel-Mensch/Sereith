# SESSION_HANDOFF.md

## Session summary
- Ran a targeted lore audit against the locally inspected starter content, prompt rules, quest data, and NPC data before changing live content.
- Replaced the generic starter tavern content with Sereith-grounded content for Eidenkehr on the Valedorn-Seufzerforst border.
- Added Sereith content files for world principles, metaphysics, magic, major threats, themes, regions, factions, ancestries, locations, starter NPCs, starter questline, and lore prompt rules.
- Reworked the active starter scenario in `src/ai_pnp/content/scenarios/prologue.json` into a six-scene mini-campaign route covering the inn, back room, namesquare, register house, healing house, and the Weisssaum waystone.
- Pointed `QuestRepository` and `NpcRepository` at the new starter files and extended `PromptBuilder` to merge narrator rules with Sereith lore rules.
- Added a regression test for the starter route across innkeeper, register house, healing house, and the first White Ebb clue.

## Current repo state
- `src/` now contains only `src/ai_pnp/` as the canonical application tree.
- `main.py` still launches `Application.run()`, which starts the desktop app by default and can still fall back to CLI mode.
- `Start_AI-PnP.bat` now provides a direct Windows launcher for the desktop app.
- The CLI interaction path is now `scripts/run_cli.py` or `Application.run_cli()` -> `src/ai_pnp/ui/cli/runner.py` -> `GameEngine`.
- `GameEngine` no longer owns a direct input loop or console output.
- The desktop window now shows:
  - structured scene and narration text
  - character state
  - quest state
  - inventory
  - visible NPC/interactions
  - recent actions
  - status feedback and save/load/new-game controls
- The active content basis is now Sereith rather than the earlier generic fantasy placeholder content.
- The locally verified starter region is Eidenkehr, a small border settlement with:
  - the inn `Der Hinterlegte Krug`
  - the namesquare
  - the register house `Haus der Zweiten Schrift`
  - the healing house `Haus der Ruhigen Naht`
  - the Weisssaum waystone on the Seufzerforst path
- The locally verified starter questline is `Die stillen Register von Eidenkehr`.
- Thirteen focused tests exist and pass.
- Current persistence is JSON save/load, not SQLite yet.
- `main` is the stable branch and `dev` is the current working branch.

## Validation
- `pytest -q`
- scripted engine flow covering innkeeper -> register house -> healing house -> Weisssaum clue route
- No build or linter command was discoverable in the minimal inspected slice.

## Recommended next action
1. Verify the desktop and CLI narrator path with a running local Ollama service and the configured model against the new Sereith prompt rules.
2. Extend the Eidenkehr questline beyond the first hard clue, especially the return path from Weisssaum into register, healing, and faction consequences.
3. Move narrator requests off the desktop UI thread so the window stays responsive during slow responses.

## Relevant files
- `AGENTS.md`
- `PROJECT_STATE.md`
- `TASK_QUEUE.md`
- `ARCHITECTURE.md`
- `SESSION_HANDOFF.md`
- `main.py`
- `Start_AI-PnP.bat`
- `pyproject.toml`
- `src/ai_pnp/core/application.py`
- `src/ai_pnp/core/app_config.py`
- `src/ai_pnp/core/models/game_state.py`
- `src/ai_pnp/core/models/world_state.py`
- `src/ai_pnp/core/models/quest.py`
- `src/ai_pnp/core/models/npc_memory.py`
- `src/ai_pnp/engine/`
- `src/ai_pnp/ui/cli/runner.py`
- `src/ai_pnp/services/llm/`
- `src/ai_pnp/services/memory/`
- `src/ai_pnp/services/content/scene_repository.py`
- `src/ai_pnp/services/content/quest_repository.py`
- `src/ai_pnp/services/content/npc_repository.py`
- `src/ai_pnp/services/storage/save_repository.py`
- `src/ai_pnp/ui/desktop/app.py`
- `src/ai_pnp/ui/desktop/main_window.py`
- `src/ai_pnp/content/scenarios/prologue.json`
- `src/ai_pnp/content/quests/starter_questline.json`
- `src/ai_pnp/content/npcs/starter_npcs.json`
- `src/ai_pnp/content/prompts/narrator_rules.json`
- `src/ai_pnp/content/prompts/lore_rules.json`
- `src/ai_pnp/content/world/seed_world.json`
- `src/ai_pnp/content/world/world_overview.json`
- `src/ai_pnp/content/world/metaphysics.json`
- `src/ai_pnp/content/world/magic_system.json`
- `src/ai_pnp/content/world/major_threats.json`
- `src/ai_pnp/content/world/themes.json`
- `src/ai_pnp/content/regions/`
- `src/ai_pnp/content/factions/major_factions.json`
- `src/ai_pnp/content/peoples/ancestries.json`
- `src/ai_pnp/content/locations/starter_region_locations.json`
- `tests/test_engine_smoke.py`
- `docs/module-maps/`

## Warnings, assumptions, and caveats
- The control files distinguish documented target state from verified local file state; keep that separation intact.
- No broad secret review or full repository scan was performed during this audit.
- `docs/module-maps/` was not refreshed in this session and may lag behind the active engine path.
- The live Ollama integration is implemented, but the latest validation run only verified the fallback path because the local Ollama service was unreachable from this environment.
- The desktop UI is now more usable, but narrator calls still run synchronously on the UI thread.
- Inventory interaction, richer NPC drill-downs, and session-summary panels are still not implemented.
- The Sereith lore integration in this session focused on the starter region and the first mini-campaign only; broader regional and faction content is still background data, not active gameplay.
