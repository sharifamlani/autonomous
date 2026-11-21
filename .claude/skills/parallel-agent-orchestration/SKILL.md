---
name: parallel-agent-orchestration
description: Use when deciding HOW to split work across Claude agents — subagents, agent teams, background sessions, dynamic workflows, or worktrees. Triggers on "run these in parallel", "spawn agents", "agent team", "fan this out", "split this up", "do these concurrently", "use subagents", "worktree", "we need to move fast", or any plan with 2+ workstreams. Encodes the decision table, the five primitives and their real constraints, and the failure modes that make parallelism slower than serial work. Read BEFORE dispatching anything.
---

# Parallel agent orchestration

## The one rule

**Parallelize the periphery. Serialize the spine.**

The spine is the chain where each piece needs the last one to exist: data call → transform →
render → it works on screen. Every agent you add to the spine waits on another agent, and you
pay coordination cost for zero concurrency.

The periphery is everything that only needs the spine's *interface*, not its code: research,
verification, docs, seed data, deploy config, styling, a second opinion on a bug. That work is
genuinely concurrent and it is where agents win.

A solo builder's instinct under time pressure is to parallelize the thing that feels slowest —
the core build. That is exactly the wrong half.

## Pick a primitive

| Primitive | Use it when | Don't use it when |
|---|---|---|
| **Subagent** (`Agent` tool) | A side task would flood your context with output you'll never reread: probing an API, searching a codebase, verifying a claim. **Default choice.** | You need the result *in* your next edit — just do it inline |
| **Fork** (`/subtask`, or `/fork` pre-2.1.212) | A side task needs everything already in this conversation. Cheaper than a fresh subagent (shares prompt cache) | The task is self-contained — a fresh subagent is cleaner |
| **Agent team** (experimental, off by default) | 3+ workers must *talk to each other*, challenge findings, and share a task list. Research, review, competing-hypotheses debugging | Sequential work, same-file edits, dependency-heavy builds. The docs say so explicitly |
| **Background session** (`claude --bg`, agent view) | Independent tasks you hand off and check later, each in its own worktree | You need to steer it turn by turn |
| **Dynamic workflow** (`Workflow` tool) | Dozens-to-hundreds of agents on one mechanical shape, or findings that must be cross-verified. The *script* holds the plan | Fewer than ~10 units of work. Coordination overhead with no payoff |
| **Worktree** (`--worktree`, `isolation: worktree`) | Two agents would otherwise edit the same files | Agents already own disjoint file sets — isolation costs you a stale checkout |

Worktrees and cross-session messaging are not ways to *run* agents; they are support for the
ones above. Worktrees isolate file edits. Messaging passes findings between sessions you run
yourself.

## Before you dispatch anything: three checks

### 1. Can the work actually be partitioned by file?

Two agents editing one file means one silently overwrites the other. Agent teams **do not**
isolate teammates in worktrees. Either give each agent its own files, or give each a worktree.
Write the file ownership down in the dispatch prompt: *"You own `src/lib/data/*`. Do not touch
anything else."*

### 2. Will permission prompts make you the bottleneck?

Teammate and background-subagent permission prompts surface in the **lead session** — yours.
Four agents each hitting an unapproved `pnpm` invocation turns parallelism into a queue at your
keyboard. **Pre-approve the commands the agents will need before you dispatch**, in
`.claude/settings.local.json`:

```json
{ "permissions": { "allow": ["Bash(pnpm *)", "Bash(git add *)", "Bash(curl -s *)"] } }
```

This is the highest-leverage thing you can do to make parallelism actually parallel.

### 3. What happens to your usage limit?

Every concurrent agent is a separate context window billed independently. The real failure is
not cost, it is **running out of quota mid-build with hours left**. Mitigations, in order:

- Put subagents on a cheaper model: `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` (keep the big model for
  the spine and the decisions, which is where judgment matters).
- Cap concurrency: `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (default 20 — far more than you want).
- Start with 3 agents, not 8. The docs are blunt: *"Three focused teammates often outperform
  five scattered ones."*

## Dispatch mechanics that matter

- **Subagents inherit no conversation history.** A fresh subagent loads CLAUDE.md, project
  context and skills — but nothing you just discussed. Put the task-specific facts *in the
  prompt*. The most common dispatch failure is assuming the agent knows what you know.
- **Send independent calls in one message.** Multiple `Agent` tool calls in a single response
  run concurrently; separate messages run serially.
- **Name the deliverable, not the activity.** "Return a JSON list of the five field names and a
  one-line note on each" beats "look into the schema."
- **Give a stopping condition.** Agents without one keep going. `maxTurns` in a definition, or
  "stop as soon as you can answer the question" in the prompt.
- **Default concurrent subagent limit is 20**; workflows cap at 16 concurrent / 1,000 total per
  run, and `parallel()`/`pipeline()` reject lists over 4,096 items.

## Worktree gotchas that will bite

- **Worktrees branch from the repo's *default branch* by default** (`worktree.baseRef: "fresh"`).
  Mid-build, that means an agent's worktree does **not** contain the work you just committed to
  your feature branch. Set `"baseRef": "head"` to branch from current `HEAD` — essential
  whenever agents must build on in-progress work.
- **A worktree is a fresh checkout, so `.env` is absent** (it's gitignored). Add a
  `.worktreeinclude` listing the gitignored files to copy in, or every worktree agent fails on
  a missing API key.
- **A worktree needs its own dependency install.** `node_modules` does not come along.
- **Isolation is enforced, not advisory.** Edits, command working directories, and git
  redirects that target the main checkout are blocked outright.
- **Windows:** removing a worktree deletes a junction/symlink but not its target.

## Platform constraints to check before promising anything

| Thing | Constraint |
|---|---|
| **Agent teams** | Experimental, **disabled by default**. Needs `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Requires an interactive session — never spawns under `-p` |
| **Split-pane teammates** | Needs tmux or iTerm2. **Not supported in VS Code's integrated terminal, Windows Terminal, or Ghostty.** On Windows/VS Code you get in-process mode only: all teammates in one terminal, navigated with arrow keys |
| **Cross-session messaging** | v2.1.224+ (macOS/Linux), **v2.1.234+ on native Windows**. WSL 2 and native Windows sessions on the same machine cannot reach each other |
| **Dynamic workflows** | v2.1.203+ for `ultracode`; on Pro, must be enabled in `/config` |
| **Agent teams limits** | No session resumption of in-process teammates; task status can lag and block dependents; shutdown is slow; one team per session; **no nested teams** |

**Always verify the installed version supports what you're about to rely on.** `claude --version`
plus `claude --help | grep -- --<flag>` is thirty seconds and prevents planning around a feature
that isn't there.

## Checking on running work

| What | Command |
|---|---|
| Background subagents in this session | `/tasks` |
| Background sessions | `claude agents` (agent view) |
| Dynamic workflow runs | `/workflows` |
| Sessions Claude can message | `/list-agents` (alias `/peers`) |
| Teammates | the agent panel below the prompt; `↑`/`↓` select, `Enter` opens, `x` stops |

## Red flags

| Thought | Reality |
|---|---|
| "More agents will make this faster" | Only for independent work. On the spine it's slower |
| "I'll let the team figure out the split" | Unpartitioned file ownership = overwrites |
| "I'll approve prompts as they come" | You become the serialization point |
| "I'll use agent teams, it's the most powerful" | It's experimental and highest-overhead. Subagents first |
| "The agent knows what we decided" | It has no conversation history. Put it in the prompt |
| "I'll check on them later" | *"Letting a team run unattended for too long increases the risk of wasted effort"* |
