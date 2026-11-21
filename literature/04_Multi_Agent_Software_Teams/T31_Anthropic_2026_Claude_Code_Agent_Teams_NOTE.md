# T31 Anthropic (2026): Orchestrate teams of Claude Code sessions (agent teams)

- **Citation:** Anthropic. (2026). *Orchestrate teams of Claude Code sessions.* Claude Code docs.
- **Link:** https://code.claude.com/docs/en/agent-teams
- **Fetched:** 2026-11-21 (full page read; the page is a living doc with no date, so the fetch date is
  the version).
- **Why no PDF:** official product documentation; there is no PDF version.

## What it says (quoted from the page)

- "Agent teams are experimental and disabled by default" (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).
  One session is the lead; teammates "share a task list, claim work, and communicate directly".
  Task claiming "uses file locking to prevent race conditions".
- When not to: "Agent teams add coordination overhead and use significantly more tokens than a single
  session ... For sequential tasks, same-file edits, or work with many dependencies, a single session
  or subagents are more effective."
- Best uses are research and review, separately owned modules, competing-hypothesis debugging and
  cross-layer work; "Avoid file conflicts: Two teammates editing the same file leads to overwrites."
- Sizing: "Start with 3-5 teammates"; "Three focused teammates often outperform five scattered ones"
  (no data given).
- Quality gates: `TeammateIdle`, `TaskCreated` and `TaskCompleted` hooks "exit with code 2 to prevent
  completion and send feedback".
- Unattended use: "In non-interactive mode with the `-p` flag, including Agent SDK sessions, Claude
  doesn't spawn teammates" (a named subagent runs as an ordinary subagent). Teammates do not inherit
  the lead's conversation history, and the page lists "Task status can lag" and "No session
  resumption with in-process teammates" among known limitations.

## Limits

- Vendor documentation, not evidence of effectiveness: it gives no success-rate or cost numbers, and
  its advice ("3-5 teammates") is untested here. Its value to the kit is the platform facts: teams
  are interactive-only, so an unattended `claude -p` run can use subagents but not agent teams.
