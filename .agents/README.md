# Agent team

This project is built by the agent team in the `agent-team` skill
(`~/.claude/skills/agent-team`). The roles, handoffs and prompts are in its `roles.md`; the team's
general lessons are in its `lessons.md`. This folder holds what is specific to Autonomous:

| File | What it is |
|---|---|
| `project.md` | The founding promise, the never-offer list, speed bars, the test desktop, build commands |
| `lessons.md` | This project's own lessons (the Auditor writes them) |
| `registry.md` | Who is who right now (role → session name) |
| `walk-brief.md` | The walk brief with its fixed fields |
| `releases/` | One release card per release, filled from the RC walk |
| `mutants/` | One mutants manifest per PR, run with the skill's `scripts/mutate.py` |

Check day-1 setup: `python ~/.claude/skills/agent-team/scripts/new_project.py . --check`
