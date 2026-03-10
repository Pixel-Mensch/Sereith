# AGENTS.md

## Purpose
This repository is structured for human and AI-agent collaboration.
The goal is small, reliable changes and clean handoffs.

## Mandatory read order
1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `TASK_QUEUE.md`
4. `ARCHITECTURE.md`
5. `SESSION_HANDOFF.md`
6. `README.md` if present
7. `.github/copilot-instructions.md` when relevant

## Working rules
- Use `dev` as the default working branch. Treat `main` as the stable baseline branch.
- Read only the task-relevant files first. Do not do a full repository scan by default.
- Keep changes small and focused. Do not rewrite unrelated areas.
- Keep commits small and logically scoped to the active task.
- Separate documented target state from verified local file state.
- Mark uncertainty instead of inventing facts.
- Prefer extending the active `src/ai_pnp/` application path over creating new parallel structures.

## Documentation discipline
- After meaningful work, update `PROJECT_STATE.md`, `TASK_QUEUE.md`, and `SESSION_HANDOFF.md`.
- Update `ARCHITECTURE.md` only with facts verified from inspected files.
- Leave the repository handoff ready after every completed step.

## Testing and security
- Run the smallest relevant test, run, or build validation before finishing when a command is known.
- If validation was not run, say so explicitly.
- Never commit secrets, tokens, or machine-local settings.
- If a secret or sensitive artifact risk is found, document the risk without reproducing the value.
