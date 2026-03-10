# Agent Workflow

## Mandatory Read Order
Before touching code or docs, read in this order:
1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `TASK_QUEUE.md`
4. `ARCHITECTURE.md`
5. `SESSION_HANDOFF.md`
6. `README.md` if present
7. `.github/copilot-instructions.md` when using Copilot or similar inline assistants

## Working Rules
- Use `dev` as the default working branch. Treat `main` as the stable branch.
- Do not do a full repository scan by default. Start with the root file list, the control files above, `README.md` if present, obvious config files, and obvious entry points.
- Keep changes small, focused, and directly related to the active task.
- Do not rewrite or refactor unrelated areas.
- If information is unknown, document the uncertainty instead of inventing details.

## Documentation Discipline
- After any meaningful change, update the relevant control files before stopping.
- At minimum, keep `PROJECT_STATE.md`, `TASK_QUEUE.md`, and `SESSION_HANDOFF.md` current.
- Update `ARCHITECTURE.md` only with facts verified from inspected files.
- Leave the repository handoff ready after every completed step.

## Git Discipline
- Prefer direct work on `dev` unless there is a clear reason for a separate feature branch.
- Make small, logically separated commits.
- Do not merge to `main` until the work is stable, documented, and verified.
- Stage only files related to the active task.

## Testing Expectations
- Run the smallest relevant test, build, or lint command before finishing when a command is known.
- If no validation command is known, say so explicitly in `SESSION_HANDOFF.md` and `PROJECT_STATE.md`.
- Do not claim verification that was not performed.

## Security Expectations
- Never commit secrets, tokens, credentials, or machine-local settings.
- Do not print sensitive values into docs or commit messages.
- If a secret risk is discovered, note the file and the risk without reproducing the value.

## Empty or Incomplete Areas
- If the repository lacks source files, README, tests, or build config, record that as a gap and use clearly marked placeholders.
- Add only the minimum structure needed for the current task.
