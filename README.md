# AI-PnP

Desktop-first AI Pen and Paper project with a persistent game state.
The LLM is only the narrator.
The actual rules, state, memory, and persistence live in the application core.

## Current local runtime

- `main.py` starts the CLI application.
- The active runtime path is `Application -> GameEngine -> TurnProcessor`.
- Commands currently supported in the CLI:
  - `state`
  - `save [name]`
  - `load [name]`
  - `quit`
- The current scaffold contains:
  - initial character and quest
  - two scenes
  - action interpretation
  - prompt building
  - placeholder narration
  - JSON save/load and autosave

## Current direction

The project is designed to stay legally publishable by using a Pathfinder-compatible rules approach
while avoiding direct use of protected setting IP.

## Run

```python
python main.py
```

## Test

```python
pytest -q
```

## Planned UI

The architecture is UI-agnostic.
It can start with CLI, move to desktop later, and still support a web UI in the future.

## Notes

- Current verified persistence is JSON save/load under `src/ai_pnp/data/saves/`.
- SQLite remains the documented MVP target, not the current local implementation.
