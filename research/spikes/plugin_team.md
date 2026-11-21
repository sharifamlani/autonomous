# Spike 4.8: can a plugin stand up the team?

**Date:** 2026-11-21 · **Claude Code:** v2.1.330 on native Windows · **ROADMAP row:** 4.8 · **Affects:** D1

## The question

Sharif, 2026-11-21: *"Say we need 4 or 5 Claude sessions: one for Main, one for building, one for
QA, one for testing like a real user, and some others. Is the plugin able to create those
automatically and populate them with the prompts, the information, the registry, and the other
things we'll need? Or do we need some different framework?"*

The deliverable is a Claude Code plugin (D1). If a plugin can't do this, the deliverable changes,
so the answer rests on the official docs plus a hands-on test, not opinion.

## THE ANSWER: plugin + launcher script

**The plugin can stand up the whole team, unattended, from one command. The separate sessions are
started by a launcher script that ships inside the plugin.** D1 holds: the deliverable stays a
plugin. No other framework is needed.

Why this label and not the other two:

- **Not "plugin alone".** A plugin with only agents and skills gives you subagents inside one
  session. That handoff worked (run A), but subagents are not the 4 or 5 independent sessions Sharif
  described: they live and die inside Main's session, report only to it, cap at 20 concurrent, and
  can't keep running on their own. Separate, long-lived role sessions need something to run
  `claude -p` for each role, and the plugin has no declarative "start a session" component. The
  built-in multi-session feature (agent teams) does not work unattended (run D, and the docs).
- **Not "wrong wrapper".** A ~90-line Python script in the plugin's `skills/<name>/scripts/` started
  three separate `claude -p` sessions (builder, then QA and tester in parallel), each with its own
  role prompt, logged their session ids into the registry, and Main collected the results (run B).
  A second script showed a tester session messaging Main directly across sessions (run C). A
  plugin `PermissionRequest` hook removed every permission prompt without any permission flags
  (run F). The Agent SDK would do the same job, but it needs Python/TypeScript and an API key for
  anything distributed to others; `claude -p` from a bundled script already covers it.

**What sits outside the plugin:** only the command that starts the top-level Main session
unattended (for example `claude -p "/autonomous:new-app ..." --plugin-dir <kit>`, or the user typing
the slash command into an interactive session). Permissions no longer have to live there (the hook
covers them); model choice, the budget cap and the background-wait ceiling still do.

**Red flag check:** no part of the founding promise is narrowed. Two expectations change: the
team's sessions talk through files and cross-session messages, not through the experimental
"agent teams" feature; and interactive background sessions (`claude --bg`) can't be started in a
fresh folder without a human accepting the trust prompt once.

## Capability table

| Capability | Result | Evidence |
|---|---|---|
| Plugin ships agents, skills with scripts, hooks, MCP servers, monitors, `bin/` | works | docs (plugins reference, components); `claude plugin validate` passed |
| (a) Create the team folder: registry, project file, lessons, per-role prompts | works | runs A, B, F: `.agents/` with `registry.md`, `project.md`, `lessons.md`, `prompts/{main,builder,qa,tester}.md` |
| (b) 4 agents as plugin subagents in one session (Main = `--agent team-spike:main`) | works | run A: builder 22.6→30.8 s, QA 32.3→41.0 s, tester 32.5→42.1 s (QA and tester overlapped), all `claude-haiku-5-5` |
| (b) 4 agents as separate `claude -p` sessions started by a plugin script | works | run B: 3 child sessions with their own session ids, pair in parallel (builder 10.5 s + max(11.9, 18.1) s = 28.7 s total) |
| (c) Each agent gets its role prompt | works | A: agent body reads `.agents/prompts/<role>.md`; B: `--append-system-prompt-file .agents/prompts/<role>.md` |
| (d) Real handoff: builder writes, QA verdicts, tester runs it, Main collects | works | A, B, F all end `TEAM RESULT: PASS`; QA `VERDICT: APPROVE` with line refs; tester stdout `hello, Ada` |
| Sessions find each other: files (`.agents/handoffs/`) | works | runs A, B, F |
| Sessions find each other: cross-session messaging between `-p` sessions on Windows | works | run C: tester sent `TESTER: WALK PASS, stdout=hello, Ada`; Main wrote it to `inbox.md` with `FROM: team-tester` |
| (e) No permission prompts, via run flags (`--permission-mode`, `--allowedTools`, `--permission-prompts none`) | partly | runs A, B: finished, but compound commands (`cd … && python …`, `echo $?`) were denied; tester could not capture an exit code |
| (e) No permission prompts, via a plugin `PermissionRequest` hook (no permission flags at all) | works | run F: 9 approvals logged across main, builder, QA, tester; 0 denials |
| Plugin agent frontmatter sets its own permissions / hooks / MCP servers | no | docs: `permissionMode`, `hooks`, `mcpServers`, `initialPrompt` ignored for plugin agents |
| Built-in agent teams in headless (`-p`) runs | no | docs + run D: a named teammate request ran as an ordinary subagent; no team or task dir created |
| Plugin script starts interactive background sessions (`claude --bg`) unattended | no (fresh dir) | run E: `Workspace not trusted. Run claude in <dir> once and accept the trust prompt` |
| Agent SDK as the wrapper | not needed | docs: same loop and tools as the CLI, loads plugins; third-party products must use API-key auth |

## Documented facts (official docs, fetched 2026-11-21)

**What a plugin can ship.** Skills (`skills/<name>/SKILL.md`, with supporting files and scripts),
legacy commands, agents, hooks (`hooks/hooks.json`), MCP servers (`.mcp.json`), LSP servers, output
styles, themes, workflows, monitors, and executables in `bin/` that are on the Bash tool's `PATH`.
Path variables `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}` (survives updates) and
`${CLAUDE_PROJECT_DIR}` are substituted in skill, agent and hook content. A `CLAUDE.md` at the
plugin root is not loaded. The manifest field table has no permissions or env key.
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/plugins/components
- https://code.claude.com/docs/en/plugins/create

**Plugin agents.** Supported frontmatter: `name`, `description`, `model`, `effort`, `maxTurns`,
`tools`, `disallowedTools`, `skills`, `memory`, `background`, `omitClaudeMd`, `isolation`, and more.
"Ignored fields: `permissionMode`, `hooks`, `mcpServers`, and `initialPrompt`." Plugin-level hooks
and MCP servers do load, and "Hooks from settings files, managed policy settings, and plugins also
run inside subagents."
- https://code.claude.com/docs/en/plugins/components
- https://code.claude.com/docs/en/hooks

**Hooks.** `SessionStart` fires "when a session begins or resumes" and its stdout is added as
context. `PermissionRequest` fires "when a tool call needs a permission decision" and answers with
`hookSpecificOutput.decision.behavior` (allow/deny). Plugin hooks fire on their events for the
whole session once the plugin loads, not only when one of its skills runs. Monitors "don't start in
non-interactive mode with the `-p` flag".
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/plugins/components

**Subagents.** Background by default when Claude spawns them; parallel; default cap "20 subagents
are running in a session"; nesting allowed "up to three layers below the main conversation"
(`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`); a background subagent's permission prompt surfaces in the
main session; `claude --agent <name>` runs the main thread as an agent. Named subagents can be
messaged with `SendMessage`.
- https://code.claude.com/docs/en/sub-agents

**Headless (`-p`).** Skills and custom commands work in `-p` ("Include `/skill-name` in the prompt
string"). Since v2.1.302 a `-p` run starts in Manual mode; a call that needs approval "is denied
unless something approves it, such as a `PermissionRequest` hook". `--permission-prompts none`
denies anything left unresolved and tells Claude not to retry. Background subagents and workflows
are stopped "after 10 minutes of continuous idle waiting by default"
(`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`, `0` = no cap); a background command the main conversation
started is not cut by that cap. `--output-format json` returns `session_id`, `num_turns`,
`total_cost_usd` and `permission_denials`. `--bare` skips plugins, hooks and CLAUDE.md discovery and
needs an API key.
- https://code.claude.com/docs/en/headless

**Agent teams.** "Experimental and disabled by default" (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).
"In non-interactive mode with the `-p` flag, including Agent SDK sessions, Claude doesn't spawn
teammates." Teammates can use plugin subagent definitions; mailbox files under
`~/.claude/teams/`; limits include "No session resumption with in-process teammates", "One team
per session", "No nested teams", "Lead is fixed", and "You can't set per-teammate permission modes
at spawn time". Split panes need tmux or iTerm2.
- https://code.claude.com/docs/en/agent-teams

**Cross-session messaging.** On by default from v2.1.234 on native Windows; local delivery over a
per-session named pipe; Claude discovers peers with `ListAgents` and sends with `SendMessage`. "Claude
Code binds an inbox socket for a `claude -p` session like an interactive one, so a long-running
`-p` worker can receive messages." To take messages unattended, start the worker with
`crossSessionInbound` set to `accept` in `--settings`. A message "never counts as your consent".
Plain text only; loops are throttled; WSL 2 and native Windows sessions can't reach each other.
- https://code.claude.com/docs/en/cross-session-messaging

**Background sessions (agent view).** `claude --bg "<prompt>"` starts a full session with no
terminal, takes `--agent` and `--name`, and moves into a git worktree before editing. "Claude Code
rejects `--bg` combined with `-p`." Research preview; each session uses quota independently.
- https://code.claude.com/docs/en/agent-view
- https://code.claude.com/docs/en/agents (comparison of subagents, agent view, agent teams,
  workflows, projects)

**Agent SDK.** "A library that runs the Claude Code binary" with the same tools, hooks,
subagents, permissions, sessions and plugin loading. "Unless previously approved, Anthropic does
not allow third party developers to offer claude.ai login or rate limits for their products,
including agents built on the Claude Agent SDK."
- https://code.claude.com/docs/en/agent-sdk/overview

## What we built

A throwaway plugin, `team-spike`, in a scratch folder outside the repo (not committed), loaded with
`--plugin-dir`:

```
plugin_team_spike/plugin/
├── .claude-plugin/plugin.json          # name team-spike, v0.0.1
├── agents/main.md, builder.md, qa.md, tester.md
│                                       # model: haiku, maxTurns 8-20, narrow tools; body = "read .agents/prompts/<role>.md"
├── skills/team-up/                     # mode A: plugin subagents in one session
│   ├── SKILL.md
│   └── scripts/bootstrap_team.py       # writes .agents/: project.md, registry.md, lessons.md, prompts/*.md, handoffs/
├── skills/team-launch/                 # mode B: separate claude -p sessions
│   ├── SKILL.md
│   └── scripts/launch_team.py          # builder, then qa || tester; logs JSON; fills registry with session ids
├── skills/team-message/                # mode C: cross-session message back to Main
│   ├── SKILL.md
│   └── scripts/launch_messenger.py
└── hooks/hooks.json + allow_team.py    # run F: PermissionRequest hook approving Bash|Write|Edit, logging each
```

Toy task: `app/greet.py`; `python app/greet.py Ada` must print exactly `hello, Ada` and exit 0.
Each child session in mode B ran as:

```
claude -p "Do your role now, as your appended system prompt says." --model haiku --max-turns 8 \
  --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Bash(python *),Bash(cd *)" \
  --permission-prompts none --strict-mcp-config --setting-sources project \
  --append-system-prompt-file .agents/prompts/<role>.md --output-format json
```

`--strict-mcp-config --setting-sources project` kept the test sessions from loading the host's
personal MCP servers, plugins and user-level instructions.

## Test runs

All runs from a fresh project folder under the scratch folder. Model `haiku` everywhere. Costs are
the CLI's client-side estimates.

| Run | What | Command (abridged) | Wall clock | Result line |
|---|---|---|---|---|
| validate | manifest + components | `claude plugin validate plugin` (and `--strict`) | <5 s | `✔ Validation passed`; lists 3 skills, 4 agents, 1 hook |
| A | mode A, subagents | `claude -p "/team-spike:team-up" --plugin-dir ../../plugin --agent team-spike:main --model haiku --max-turns 25 --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Bash(python *),Agent" --permission-prompts none --strict-mcp-config --setting-sources project --output-format json --max-budget-usd 1` | 41 s | `success`, 15 turns, $0.0235, `TEAM RESULT: PASS`, 2 Bash denials |
| B | mode B, 3 separate `-p` sessions from a plugin script | `claude -p "/team-spike:team-launch" ...` (same flags + `Bash(cd *)`) | 44 s | `success`, $0.0069 (Main) + $0.0075 + $0.0077 + $0.0094 (children), `LAUNCH DONE in 28.7s, all exit 0: True`, `TEAM RESULT: PASS` |
| C | mode C, cross-session message | `claude -p "/team-spike:team-message" --name team-main ... --settings '{"crossSessionInbound":"accept"}'` | 21 s | Main $0.0080, tester $0.0072, result `TESTER: WALK PASS, stdout=hello, Ada`, 0 denials |
| D | agent teams under `-p` | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude -p "Create an agent team: spawn ONE teammate named qa-mate ..."` | 19 s | $0.0155, "Ran as an ordinary subagent, not a teammate"; 0 team/task dirs for the session |
| E | `claude --bg` from a script | `claude --bg --name team-qa-bg --plugin-dir ../../plugin --agent team-spike:qa ... "Do your role."` | 2 s | `Workspace not trusted. Run claude in <dir> once and accept the trust prompt, then retry.` (no model call) |
| F | mode A, permissions from a plugin hook only | same as A with **no** `--permission-mode` and **no** `--allowedTools`; only `--permission-prompts none` | 41 s | $0.0160, `TEAM RESULT: PASS`, denials `[]`, hook log: 9 `ALLOW` lines across main, builder, qa, tester |

**Totals:** 10 session launches (9 ran a model, E was refused before starting), plus 4
`plugin validate` calls. About 168 s of wall clock across the runs. About $0.10 estimated.

Evidence excerpts:

- Run A registry (written by Main): `| builder | team-spike:builder | 2026-11-21T05:38:16Z | subagent |`
- Run B registry (written by the launcher): `| qa | claude -p session 1cc432bb-… (pid 38532) | 2026-11-21 05:40:13 | separate-session |`
- Run B QA verdict: `VERDICT: APPROVE` … `app/greet.py:6 builds the greeting as f"hello, {name}"`
- Run B tester report: stdout `hello, Ada`, `WALK: PASS`, and "I could not read `$?` … denied for lack
  of an approval surface" (the allowlist gap)
- Run C inbox: `FROM: team-tester` / `TESTER: WALK PASS, stdout=hello, Ada`
- Run F hook log: `team-spike:builder  Write  ALLOW`, `team-spike:tester  Bash  ALLOW`, …

## Risks and limits found

1. **Permission allowlists are brittle.** `Bash(python *)` did not cover `cd <dir> && python …` or
   `echo $?`; the tester honestly reported an exit code it could not observe. A `PermissionRequest`
   hook fixed it, but the spike hook approves everything for Bash/Write/Edit. A public kit must
   scope it (project folder only, a command allowlist, never network or `git push` without a rule)
   or it becomes a blanket bypass for anyone who installs the plugin.
2. **Plugins can't set their own session's permissions, env or model.** Agent frontmatter
   `permissionMode` is ignored and the manifest has no permissions or env key. The hook covers
   permissions; `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`, the model and the budget still come from the
   command that starts Main.
3. **10-minute background cap under `-p`.** Background subagents in a headless Main are stopped
   after 10 idle minutes unless the ceiling is raised. Hours-long runs should keep long work in
   separate `-p` sessions started by a background command (not capped), or raise the ceiling in the
   launch command.
4. **`-p` sessions end when their task ends.** A role that must persist for hours is a series of
   `claude -p --resume <session_id>` calls (the registry holds the id), not one immortal process.
5. **No agent teams headless; no `--bg` without trust.** The two built-in "many sessions" features
   are interactive-first. Experimental agent teams also can't set per-teammate permissions.
6. **Cost accounting is per process.** A parent's `total_cost_usd` excludes child sessions; the
   launcher must sum the children's JSON (it does) or the benchmark will under-report $/task (G2).
7. **Parallel file edits.** QA and tester wrote different files, so no clash. Real builders in
   parallel need worktrees; `isolation: worktree` exists for plugin subagents, separate sessions
   need the launcher to create them.
8. **Windows paths.** A very long working-directory path made Git Bash refuse to start native
   programs ("path longer than allowed for a Win32 working directory"). Keep run folders short.
9. **Not tested here:** an interactive session typing the slash command (the hook should behave
   the same), runs longer than a minute, CUA walks from a child session, and cross-session
   messaging under load.

## What Phase 9 should do

1. **Keep D1.** The kit is a plugin. Its `/autonomous:new-app` skill bootstraps `.agents/`
   (port `agent-team`'s `new_project.py` and templates, copy-don't-rewrite) and runs a bundled
   launcher script that starts each role as its own `claude -p` session with
   `--append-system-prompt-file .agents/prompts/<role>.md`, records `session_id` in
   `registry.md`, and resumes roles with `--resume`.
2. **Use subagents for short side jobs inside a role** (QA's mechanical checks, the builder's
   mutant runs), and separate sessions for the roles themselves.
3. **Ship a scoped `PermissionRequest` hook** instead of relying on `--allowedTools`. Write its
   policy as data (allowed command prefixes, project-only writes), test it with a deny case, and
   log every decision (the log is evidence for the evaluator). This is row 9.3.
4. **Handoffs are files first** (`.agents/handoffs/`, PR bodies), with cross-session messages for
   "wake up, your input is ready". Set `crossSessionInbound: accept` in each worker's `--settings`.
5. **Ship one documented launch command** for fully unattended runs: model, budget cap,
   `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`, `--plugin-dir` or the installed plugin. Keep it a
   one-liner in the README, not a second framework.
6. **The launcher sums child costs and turns** into one run record for the benchmark.
7. **Don't build on agent teams or `claude --bg`** for unattended runs until they work under `-p`
   and in untrusted folders; recheck each Claude Code release.
8. **Before v0.1, re-run this spike at real scale:** an hour-long run with the Tester doing a CUA
   walk from its own session, to prove limits 3, 4 and 7 in practice.
