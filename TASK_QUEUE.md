# Task Queue

| Priority | Task | Status | Relevant Files | Expected Outcome | Blockers / Notes |
| --- | --- | --- | --- | --- | --- |
| P0 | Maintain control-file workflow | Done | `AGENTS.md`, `PROJECT_STATE.md`, `TASK_QUEUE.md`, `ARCHITECTURE.md`, `SESSION_HANDOFF.md`, `.github/copilot-instructions.md` | Repo stays handoff ready for future agents | Completed in this setup pass |
| P1 | Define project purpose and scope | Pending | `README.md`, `PROJECT_STATE.md`, `ARCHITECTURE.md` | Clear statement of what this repo is for | Purpose not present in inspected files |
| P1 | Add initial README | Pending | `README.md` | Human-readable project overview and setup guidance | README currently missing |
| P1 | Add first code/config scaffold | Pending | Unknown until stack is chosen | Establish actual entry points and working structure | Language/framework not yet defined |
| P2 | Discover or define validation commands | Pending | Future build/test config, `PROJECT_STATE.md`, `SESSION_HANDOFF.md` | Repeatable test/lint/build expectations | No tests or tooling are present yet |
| P1 | Seed ignore rules for local/secrets files | Done | `.gitignore` | Prevent accidental commit of local settings or secrets | Minimal rules added during setup |
| P2 | Refine ignore rules once the stack is known | Pending | `.gitignore` | Ignore only the right generated files for the chosen stack | Current ignore rules are intentionally generic |
