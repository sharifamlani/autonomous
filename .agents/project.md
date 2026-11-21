# Autonomous: team specifics

Read with the `agent-team` skill's `roles.md`. Product: **Autonomous** · Owner: **Sharif**. These
fill the placeholders in the skill's role prompts. Main fills this in on day 1, before any feature.

## The founding promise

The 1–3 sentences a user would say if the product works, taken from the original design artifact
(<link to the founding idea / spec>). Each is proven on the real platform by a spike before any
feature, and re-checked at every decision, ADR and gate.

1. "I can …"
   - Spike: <what was run, on which platform> · Result: <PASS / FAIL, date, evidence>

A FAIL here is a red flag for Sharif the same day.

## Never offer

Options Sharif has ruled out. Main checks every options list against this before sending.

- …

## Speed bars

| Bar | Our share (what the product controls) | Platform share | Threshold | Measured by |
|---|---|---|---|---|
| | | | | |

## The test desktop

- Where walks run: <second machine / VM / second Windows user session / Sharif's machine, reserved>
- Tester state file (its first line is the walk line): `<path>`
- Test profile or install location (never Sharif's own): `<path>`
- Guarded launch and stop scripts: `<path>`
- Release cards: `.agents/releases/<version>.md`

## Build and verify

- Build: `<command>` · Tests: `<command>` · Verify before every push: `<command>`
- Mutation runner: `python ~/.claude/skills/agent-team/scripts/mutate.py .agents/mutants/pr-<n>.json`
- CI cancels in-progress runs for pull requests only: <yes / to do>

## Marketing

- Channels: LinkedIn, X · Voice skill and draft checker: <names>
- Posting permission confirmed with one approved post: <date>
- Repo link for the first comment: <url> · Series name: <name>

## Failed-gate rule

A check that fails because of the PR blocks the merge. A check that fails the same way on current
main may merge only when main's own run shows the same failure, the failure has a named owner, and
the release tag stays blocked until it is fixed.
