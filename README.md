# AI-PnP

Desktop-first AI Pen and Paper project with a persistent game state.
The LLM is only the narrator.
The actual rules, state, memory, and persistence live in the application core.

## Current direction

The project is designed to stay legally publishable by using a Pathfinder-compatible rules approach
while avoiding direct use of protected setting IP.

## Run

```python
python main.py
```

## Planned UI

The architecture is UI-agnostic.
It can start with CLI, move to desktop later, and still support a web UI in the future.
