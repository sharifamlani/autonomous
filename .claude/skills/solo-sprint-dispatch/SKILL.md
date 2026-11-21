---
name: solo-sprint-dispatch
description: Use during a fixed-deadline solo build sprint (hackathon, demo day, timeboxed spike) when one human plus Claude must ship a working demo in hours. Triggers on "hackathon", "we have N hours", "build day", "sprint", "ship by", "demo at", "maximize my time", or executing a timeboxed build plan. Gives the concrete three-track partition, the hour-by-hour dispatch pattern, the pre-flight permission setup, and the quota guardrail. Pairs with parallel-agent-orchestration (read that for primitive choice).
---

# Solo sprint dispatch

For one human + Claude against a hard deadline. Assumes you've read
`parallel-agent-orchestration` for *which* primitive; this is *what to dispatch, when*.

## The budget is attention, not tokens

With one builder, the scarce resource is **your** serial attention. You can only read one
transcript, make one decision, approve one prompt at a time. So the goal of dispatching agents
is not "more code per minute" — it is **keeping your attention on the spine while the periphery
gets done anyway.**

That reframes everything. An agent that needs three check-ins costs more attention than it
saves. An agent that returns one artifact you glance at and accept is pure gain.

**Dispatch rule: if it will need steering, you do it. If it returns a deliverable, an agent does it.**

## The three-track partition

Almost every demo build decomposes into three tracks that touch disjoint files:

| Track | Owns | Who | Why |
|---|---|---|---|
| **Spine** | the end-to-end path: input → data → model → output on screen | **You + main session, serially** | Every step depends on the last. Unparallelizable by nature |
| **Periphery** | styling, the one screen that must look finished, seed/fixture data, deploy config | Subagent, own files | Needs the spine's *interface*, not its internals |
| **Record** | README, demo script, data-source citations, model disclosure | Subagent, docs only | Depends on nothing. Pure deadline insurance |

The Record track is the one people skip and then scramble for in the last fifteen minutes,
badly, while the demo is unrehearsed. **Dispatch it early and it is simply done.**

## Hour-by-hour pattern for a ~5-hour build

| Phase | You (spine, serial) | Dispatched concurrently |
|---|---|---|
| **Pre-flight** (before the clock) | Permissions, keys, version, worktree config — see below | — |
| **Hour 0** | Lock the idea. Write the demo script *first*. Scaffold + deploy an empty app immediately | — (nothing to parallelize yet; don't force it) |
| **Hour 1** | Thinnest real slice: one real input → one real data call → something on screen | 1 subagent: **probe & document** the exact shape of every external data source you'll touch |
| **Hour 2** | Make the model call load-bearing. Keep the slice working | 1 subagent: **the one screen** that must look finished (owns `components/`, `styles/`) |
| **Hour 3** | Harden the single path. Handle the empty/error state the demo will hit | 1 subagent: **README + citations + model disclosure**, read from the actual code |
| **Hour 4** | **Rehearse against the deployed URL, timed, twice** | 1 subagent: **verifier** — run the live URL, check DOM/console/network, report evidence |
| **Last 20 min** | Submit. Stop building | — |

Three concurrent agents, never more. Each returns an artifact. None needs steering.

## Pre-flight: do these before the clock starts

Each one removes a serialization point later.

1. **Update the toolchain.** `claude update`. A version that lacks `--bg`, `/subtask`, or
   cross-session messaging silently removes options you were counting on. Verify after:
   `claude --help | grep -- --bg`.
2. **Pre-approve the commands agents will need.** Permission prompts from background agents and
   teammates land in *your* session and block everything. Add to `.claude/settings.local.json`
   an allow list covering your package manager, git, curl, and test runner.
3. **Point subagents at a cheaper model.** `CLAUDE_CODE_SUBAGENT_MODEL=sonnet`. Keeps the strong
   model for the spine and the judgment calls, and materially delays quota exhaustion.
4. **Set `worktree.baseRef: "head"`** if any agent will run in a worktree. The default branches
   from the repo's default branch, so the agent would not see the work you just committed.
5. **Write `.worktreeinclude`** listing `.env` and friends, or worktree agents fail on a missing
   key.
6. **Make one real API call with the real key.** A key that authenticates but 402s on the third
   call is worse than no key, because you won't suspect it.

## The quota guardrail

Running out of model quota at hour three with the demo unbuilt is the worst outcome available to
you, and parallelism is what causes it. Treat quota as a fuel gauge:

- **Cap at 3 concurrent agents.** Not a cost rule — an attention rule that happens to also
  protect quota.
- **Subagents on the cheaper model**, main session on the strong one.
- **Never run `ultracode` / automatic workflow orchestration during a timeboxed build.** It turns
  every substantive request into a multi-agent run. Excellent for a Tuesday audit, ruinous when
  you have four hours and one shot.
- **If you hit a limit, stop dispatching entirely** and finish the spine by hand. The spine is
  what gets scored.

## Dispatch prompt template

A dispatched agent has **no conversation history**. Every dispatch needs all five:

```
CONTEXT:   <the 3 facts the agent cannot discover on its own>
OWNS:      <exact file paths. "Do not modify anything else.">
TASK:      <the deliverable, as a noun>
DONE WHEN: <a condition the agent can check itself>
RETURN:    <the exact shape you want back>
```

Missing `OWNS` causes overwrites. Missing `DONE WHEN` causes an agent that never stops.

## What never gets dispatched

- **The idea decision.** Yours. An agent will happily justify any option.
- **The demo narration.** You're performing it; you have to believe it.
- **The last integration step.** When pieces must meet, one mind holds both sides.
- **Anything you haven't verified once by hand.** Delegating an unverified assumption
  parallelizes the error.

## Post-sprint

Stale worktrees and orphan branches survive the sprint. `git worktree list`, then
`git worktree remove --force` for each agent worktree. Confirm everything is pushed:
`git cherry -v @{upstream}` should be empty.
