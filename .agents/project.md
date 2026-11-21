# Autonomous: team specifics

Read with the `agent-team` skill's `roles.md`. Product: **Autonomous** · Owner: **Sharif**. These
fill the placeholders in the skill's role prompts. Main fills this in on day 1, before any feature.

## The deliverable

An open-source **Claude Code plugin** (the kit) that anyone installs from this GitHub repo, proven by
a small public **benchmark** that runs unattended and is scored for every kit version, plus a
**showcase** (the apps and studies the kit made, a short white paper, the LinkedIn series).
Decided by Sharif 2026-11-20: "something straightforward and simple, easy to deliver."
v0.1 proves both halves small: one app task and one known-answer study, end to end.

## The founding promise

The sentences a user would say if the product works (source: Sharif's brief in the 2026-11-20
planning session: fast, efficient, reliable, accurate, autonomous app development and research).
Each is proven on the real platform by a spike before any feature, and re-checked at every
decision, ADR and gate.

1. "I install the plugin, run `/autonomous:new-app` with an idea, and walk away. I come back to a
   working app that an agent has used live through the real UI, with QA verdicts and evidence."
   - Spike S3b (2026-11-20, this Windows machine): headless `claude -p` drove a CUA-launched
     isolated Chrome (`browser_prepare {allow_launch: true, profile: {mode: isolated_new}}`),
     navigated to example.com and read "Example Domain", then closed it. Result: **PASS** (29 s).
   - Finding: Claude in Chrome exposes 0 tools under `claude -p` (interactive sessions only), and
     CUA refuses Sharif's own Chrome profile without a consent grant. Unattended walks therefore use
     CUA in an isolated profile, which is also what the team lessons require.
2. "I run `/autonomous:new-study` with a question and data. I come back to a pre-registered,
   reproducible study (a Run All notebook and a short report) whose numbers check out."
   - Spike: not yet run in this repo. The mechanism exists in Trading (protocol, `research-report`
     with `check_report.py` and headless nbclient execution, Study 053's committed executed
     notebook). Result: **PENDING**: a headless Run All of a template notebook here is the first
     smoke of Phase 3; the end-to-end proof is a v0.1 evaluation criterion.
3. "It runs for hours without me approving prompts or rescuing stuck sessions."
   - Spike S2 (2026-11-20): headless `claude -p --permission-mode bypassPermissions` spawned a
     subagent that wrote and verified a file, 24 s, no prompts. Result: **PASS for the mechanism**;
     the multi-hour run is a v0.1 evaluation criterion.
   - Platform limits to design around (Claude Code docs, 2026-11-20): plugin subagents ignore
     `permissionMode`, `hooks` and `mcpServers`, so the run's own flags set permissions
     (`--permission-mode auto|dontAsk`, `--allowedTools`, `--permission-prompts none`); background
     subagents under `-p` stop at 10 minutes unless `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`;
     monitors don't start under `-p`; commands are namespaced (`/autonomous:new-app`).

A FAIL here is a red flag for Sharif the same day.

## Never offer

Options Sharif has ruled out. Main checks every options list against this before sending.

- Mermaid diagrams (ASCII only, unless Sharif asks in that message).
- Walks in Sharif's own browser profile or editor windows.
- A stand-in reviewer when QA is unavailable.
- Loosening an evaluation criterion to make work pass.

## Speed bars

Set from the v0.1 baseline run; every later kit version must beat its predecessor's scorecard.

| Bar | Our share (what the product controls) | Platform share | Threshold | Measured by |
|---|---|---|---|---|
| App task, idea to walked app | agent turns, retries, idle waits between stages | model latency, tool start-up | v0.1 baseline | `claude plugin eval` run log |
| Study task, question to verified report | same | same | v0.1 baseline | `claude plugin eval` run log |
| Cost per task | tokens our prompts and agents spend | model price | v0.1 baseline | eval `--json` cost |
| Human interventions per task | everything | permission prompts the platform forces | 0 | run log |

## The test desktop

- Where walks run: Sharif's machine, reserved per walk (walk line OPEN, Sharif away); every browser
  walk runs in a CUA-launched isolated Chrome profile, never Sharif's own windows. A second Windows
  user session is the upgrade if walks collide with his work.
- Tester state file (its first line is the walk line): `~/.autonomous/tester_state.md` (outside the repo)
- Test profile or install location (never Sharif's own): CUA `isolated_new` Chrome profile
- Guarded launch and stop scripts: to do with the first app task (`scripts/walk/`)
- Release cards: `.agents/releases/<version>.md`

## Build and verify

- Build: none yet · Tests: `claude plugin validate plugin/ --strict` and `claude plugin eval` (from
  the kit's first release) · Verify before every push: `gitleaks git --pre-commit --staged`
- Mutation runner: `python ~/.claude/skills/agent-team/scripts/mutate.py .agents/mutants/pr-<n>.json`
- CI cancels in-progress runs for pull requests only: yes (`.github/workflows/ci.yml`, 2026-11-20)

## Marketing

- Channels: LinkedIn, X · Voice skill and draft checker: `sharif-voice` (local only, private corpus)
- Posting permission confirmed with one approved post: granted by Sharif 2026-11-20; confirmed
  in practice by the first approved post (post #1, when the repo goes public)
- What counts as a release: each closed ROADMAP phase or kit version; its release card is filled
  from the independent evaluator's scorecard (plus the walk, for app work)
- Repo link for the first comment: https://github.com/sharifamlani/autonomous · Series name: Building an autonomous factory in public

## Failed-gate rule

A check that fails because of the PR blocks the merge. A check that fails the same way on current
main may merge only when main's own run shows the same failure, the failure has a named owner, and
the release tag stays blocked until it is fixed.
