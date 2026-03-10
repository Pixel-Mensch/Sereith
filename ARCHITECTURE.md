# Architecture

## High-Level Structure
- Root documentation for AI-agent workflow and project tracking.
- `.github/` for assistant-specific guidance.
- No application source tree exists yet.

## Main Modules and Responsibilities
- `AGENTS.md`: required workflow and repository handling rules for future agents.
- `PROJECT_STATE.md`: current known project state, gaps, and risks.
- `TASK_QUEUE.md`: prioritized next work items.
- `ARCHITECTURE.md`: verified structural notes only.
- `SESSION_HANDOFF.md`: latest session summary and next-step guidance.
- `.github/copilot-instructions.md`: condensed assistant instructions.

## Entry Points
- No runtime, build, or CLI entry points are present yet.

## Important Flows
- Agent workflow:
  Read control files -> inspect only the minimal needed project files -> make small focused changes -> run the smallest relevant validation -> update control files -> leave a clear handoff.
- Git workflow:
  Keep `main` stable -> do active work on `dev` -> avoid unrelated branch sprawl -> commit focused changes only.

## Important Files
- `AGENTS.md`: primary operating instructions.
- `PROJECT_STATE.md`: project status snapshot.
- `TASK_QUEUE.md`: prioritized work backlog.
- `ARCHITECTURE.md`: current verified structure.
- `SESSION_HANDOFF.md`: next-session launch point.
- `.github/copilot-instructions.md`: short inline assistant rules.
- `.gitignore`: minimal protection against committing local-only files.

## Notes
- This file intentionally avoids stack-specific claims because no code or config was available in the inspected set.
