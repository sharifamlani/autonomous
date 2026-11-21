# public/: third-party GitHub repos

Upstream open-source projects we read, evaluate, and borrow from. **Nothing here is ours** and
nothing here ships in the kit unless it is copied in deliberately, license-checked, with attribution.

## How this folder works

The clones are **gitignored**: each stays a real clone with its own history and remote, so it can be
pulled and diffed against upstream rather than frozen into our history. What *is* committed:

| File | What it is |
|---|---|
| `manifest.tsv` | `name, url, pinned_commit` for every clone: the exact state our notes describe |
| `_README.md` | This file: one evaluation section per clone (what it is, license, what we take from it) |
| `_candidates/<NN>.tsv` | Repos the literature scouts flagged, per literature folder, before the survey |

```
bash scripts/sync_public_repos.sh           # ensure every repo is present at its pinned commit
bash scripts/sync_public_repos.sh --latest  # fast-forward to upstream tip, rewrite the pins
bash scripts/sync_public_repos.sh --verify  # assert pins match; non-zero exit on drift
```

A fresh checkout has an empty `public/`; one command refills it at the exact state these notes
describe. The full survey (stars, last push, license, archived, evidence labels) is
`PUBLIC_REPOS.md` at the repo root, written in ROADMAP Phase 6.

## Rules

- **Untrusted code.** Clones are read, not executed or installed, until a deliberate sandboxed run.
- **License first.** Check `license.spdx_id` from the GitHub API and the raw `LICENSE` file before
  copying anything. No license means no copying.
- **Claims are claims.** A README's numbers are UNVERIFIED until one of our studies re-runs them.

## Clones

One section per pinned clone (ROADMAP 6.4 and 6.5): what it is, its license, its process (how work is
organised, handed off, tested and gated), the lessons it learned (from its own docs, changelogs and
recurring issues), what the kit should take, and what to avoid. File paths are relative to the clone at
its pin; `#N` is a GitHub issue or PR in that repo. Nothing was run; numbers are UNVERIFIED.

## A. Claude Code harness and plugins

### superpowers (`obra/superpowers` @ 22f0b46)

**What it is.** A skills-only plugin (no agents folder, one hook) that turns a coding agent into a fixed
workflow: brainstorm, plan, worktree, subagent-driven development with per-task review, finish branch. Ships
to 15+ harnesses from one source. **License:** MIT (`LICENSE`). Copying allowed? Yes, with conditions (keep
the copyright and license notice).

**Process: how the work is organised**
- Packaging: `.claude-plugin/plugin.json` (metadata only) + `skills/<name>/SKILL.md` + `hooks/hooks.json`. The single
  `SessionStart` hook (matcher `startup|clear|compact`) injects the `using-superpowers` bootstrap so skills auto-trigger;
  `hooks/run-hook.cmd` is a polyglot wrapper with a `powershell` form for Windows (`hooks/hooks.json`,
  `docs/windows/polyglot-hooks.md`).
- Roles are prompt templates inside a skill, not plugin agents: `skills/subagent-driven-development/implementer-prompt.md`,
  `task-reviewer-prompt.md`, `re-review-prompt.md`, plus `skills/requesting-code-review/code-reviewer.md`. A controller
  dispatches one fresh implementer per task, then one task reviewer (spec compliance AND quality), then one whole-branch
  review on the most capable model (`skills/subagent-driven-development/SKILL.md`).
- Handoffs are files: `scripts/task-brief` extracts one task to a brief file, the implementer writes `task-N-report.md`,
  `scripts/review-package` writes the diff from a recorded BASE sha, and a per-plan ledger `progress.md` under
  `.superpowers/sdd/<plan>/` is the recovery map after compaction (`SKILL.md` "Setup", "The Task Loop").
- Gates: implementers must not spawn subagents or reviewers; the reviewer always gets a diff file; a fix loop has a hard cap
  of 5 rounds (rounds 1-3 resume the implementer, 4-5 a fresh implementer one model tier up), then a "breaker" where the
  controller parks findings with a written ruling (`references/fix-loop.md`). `verification-before-completion/SKILL.md`: "NO
  COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE".
- Unattended: "Continuous execution... Do not pause to check in" and "Rulings, not stalls": decisions are logged as `Ruling:
  <what> — <why> — <cost if wrong>`; only four things stop the run (irreversible op, security-sensitive action,
  outside-worktree side effect like push/merge, hopelessly broken plan) (`SKILL.md` top). No permission handling of its own;
  it relies on the harness.
- Testing: `tests/` for plugin code (bash/node), skill behaviour evals in a separate repo
  `prime-radiant-inc/superpowers-evals` ("Quorum") that drives real CLIs and grades with an LLM QA agent plus deterministic
  post-checks (`docs/testing.md`, `AGENTS.md` "Eval harness"). `tests/skill-size/test-skill-size.sh` fails any SKILL.md at
  20,000 bytes (`RELEASE-NOTES.md` v7.0.1).

**Lessons learned**
- Compaction truncates skills: Claude Code re-attaches each skill cut at 20,000 characters, so SDD lost its 5-round cap and
  ran 18 fix rounds on one task (#2481, `RELEASE-NOTES.md` v7.0.1). Fix: move rules into `references/` files read from disk
  at the step that needs them.
- "Controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure
  observed"; hence the ledger file (`SKILL.md` "Setup").
- Pasting history into dispatches is waste: one real dispatch was 42k chars, 99% pasted history (`SKILL.md` "Task brief").
- Workers that spawn their own reviewers duplicate the controller's review "a full extra review seat per task" (`SKILL.md`,
  no-subagents contract).
- A shared, plan-less ledger let a follow-up plan read the previous plan's progress as its own; made plan-scoped
  (`RELEASE-NOTES.md`, plan-scoped workspace entry;
  `docs/superpowers/specs/2026-07-06-sdd-plan-scoped-workspace-eval-results.md`).
- Cheapest models take 2-3x the turns on multi-step work and cost more overall; "Always specify the model explicitly" or the
  subagent inherits the expensive session model (`SKILL.md` "Model Selection").
- Plans that contain full code leave the executor nothing to decide (#895 "writing-plans: plans over-specify
  implementation"); later rewrite records decisions instead of code, at a quarter of the time and a third of the tokens
  (`RELEASE-NOTES.md` writing-plans entry, #2333).
- An inline "executing-plans" stub "measured the same as running with no plugin at all" until rebuilt (`RELEASE-NOTES.md`,
  #2318): they measure against a no-plugin baseline.
- Top user complaints: brainstorm questions annoying (#2530, 46 comments), slowness/context cost (#743 "Im seeing slowness in
  responses since using the skill"), wants Agent Teams support (#429, 94 upvotes), hard to tell if skills fired (#446).

**What the kit should take**
- Roles/prompts: copy the brief-file / report-file / review-package handoff and the four-status implementer report (DONE,
  DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED) from `skills/subagent-driven-development/` for builder and QA hand-offs between
  `claude -p` sessions.
- Launcher/registry: adapt the per-plan ledger with an identity first line and `Ruling:` lines as the team's durable state,
  so a resumed Main trusts the ledger and `git log`, not memory.
- QA gate: the 5-round fix-loop cap with model escalation and a written breaker (`references/fix-loop.md`); reviewer gets a
  diff from a recorded BASE sha, never `HEAD~1`.
- Benchmark: their discipline of RED (no change) vs GREEN arms, 5+ reps per arm, plus a no-plugin baseline; and a CI size
  check that keeps every kit SKILL.md under 20,000 bytes.
- Plugin hygiene: polyglot `run-hook.cmd` with a `powershell` command form, needed on this Windows machine.

**What to avoid**
- Their reviewer is an LLM reading a diff; it skips re-running tests ("Do not ask a reviewer to re-run tests the implementer
  already ran", `SKILL.md`). The literature says LLM verifiers approve work real tests reject; the kit's QA must re-run tests
  the builder cannot edit, and the Tester must walk the app.
- Aggressive "1% chance... you ABSOLUTELY MUST invoke" bootstrap language (`skills/using-superpowers/SKILL.md`) costs context
  and speed (#743).
- Repo text aimed at agents (`AGENTS.md` "If You Are an AI Agent. Stop.", PR rules only): ignored here.

**Evidence level.** They run real-CLI evals with counted reps (e.g. design doc skipped "24 of 24 runs
before... 3 of 24 after", v7.0.1; 25/25 controller reps in the ledger study). Grading is partly LLM and partly
hand-read; the eval lab lives outside this repo and "behavior-scenario eval records are kept by the maintainer
outside the repo" (`docs/testing.md`). "Twice as fast... almost 50% fewer tokens" (`RELEASE-NOTES.md` line
338) has no published data. All numbers UNVERIFIED.

### claude-plugins-official (`anthropics/claude-plugins-official` @ 73c8cf3)

**What it is.** Anthropic's own Claude Code plugins (`plugins/`, 43 folders) and the `claude-plugins-official`
marketplace; third-party submissions moved to claude.ai/directory/manage (`README.md`). **License:**
Apache-2.0 at the root and in each plugin checked (`LICENSE`, `plugins/*/LICENSE`). Copying allowed? Yes, with
conditions (keep license and notices, mark changes).

**Process: how the work is organised**
- Packaging standard: `.claude-plugin/plugin.json` + optional `commands/`, `agents/`, `skills/`, `hooks/hooks.json`,
  `.mcp.json` (`README.md` "Plugin Structure"; reference in `plugins/example-plugin/`). Plugin `name` is an immutable slug;
  renames go through a `renames` map in `marketplace.json` (`README.md`).
- Agents as markdown with frontmatter `tools:` and `model:`. Reviewers are given read-only tools:
  `plugins/feature-dev/agents/code-reviewer.md` lists Glob/Grep/Read etc., no Edit/Write, and reports only issues at
  confidence >= 80 on a 0-100 scale.
- Multi-phase commands orchestrate agents: `plugins/feature-dev/commands/feature-dev.md` (discovery, 2-3 parallel
  `code-explorer` agents, clarifying questions, architect, implement, review) with user approval between phases.
- Unattended loop: `plugins/ralph-loop/` uses a `Stop` hook (`hooks/stop-hook.sh`) that blocks exit and feeds the same prompt
  back until `--max-iterations` or the model prints `<promise>TEXT</promise>`. State lives in `.claude/ralph-loop.local.md`;
  the hook checks `session_id` so other sessions in the same folder are not trapped.
- Hook-based guards: `plugins/hookify/` turns markdown rules into PreToolUse/PostToolUse/Stop/UserPromptSubmit hooks (example
  `examples/require-tests-stop.local.md` blocks stopping if no test command appears in the transcript).
  `plugins/security-guidance/` runs regex warnings on edits, an LLM diff review on Stop, and an SDK reviewer on `git commit`,
  with ~60 pytest files under `tests/`.
- Testing a plugin: CI runs `claude plugin validate --json` on each folder twice, alone and inside a throwaway marketplace
  (`.github/scripts/validate-plugin-folders.ts`), plus frontmatter checks (`validate-frontmatter.ts`) and an LLM policy scan
  against `.github/policy/prompt.md` with cached verdicts (`.github/workflows/scan-plugins.yml`). Behaviour evals:
  `plugins/skill-creator/` runs each test prompt with-skill and baseline in parallel subagents, grades assertions
  (`agents/grader.md`), aggregates pass rate, time and tokens as mean ± stddev (`scripts/aggregate_benchmark.py`), offers
  blind A/B (`agents/comparator.md`), and tunes skill descriptions on a 60/40 train/held-out split, 3 runs per query, picking
  by held-out score (`SKILL.md` lines 169-394).

**Lessons learned**
- Ralph-in-one-session drifts from the original: context accumulates across iterations instead of starting fresh (#125
  "Plugin deviates from original Ralph behavior (context should be fresh each iteration)").
- Inline multi-line bash in a command broke the permission checker on Windows Git Bash (#50 "Bash command permission check
  failed for pattern"; #105).
- Schema changes to `marketplace.json` break older clients (#585 "`git-subdir` source type ... breaks older Claude Code
  clients"; #685, #655).
- **Directory gate (important for us):** since about 2026-11-05 the plugin directory refuses "Hooks of type command", "Local
  MCP servers" and "Files outside the allowed types" from organisations that are not Verified, with no published way to
  become Verified (#7024, 40 comments, many solo developers refused through 2026-11-20).
- The policy reviewer reads the whole shipped payload, including `.claude/`, `scripts/`, `tests/`, because a git-installed
  plugin clones the entire repo to the user's disk (`.github/policy/prompt.md`).
- Validation needs two passes because `claude plugin validate` on a bare folder cannot tell reserved names apart
  (`validate-plugin-folders.ts` header).

**What the kit should take**
- Plugin layout and CI: copy the two-pass `claude plugin validate --json` script idea and frontmatter check into our CI for
  `plugin/`.
- Benchmark: adapt skill-creator's with/without arms, `grading.json` fields (`text`, `passed`, `evidence`), mean ± stddev
  aggregation, and held-out selection (`plugins/skill-creator/skills/skill-creator/`) as the shape of benchmark scorecards.
- QA/Tester gates: reviewer agents with read-only `tools:` (feature-dev `code-reviewer.md`) so QA physically cannot edit the
  code it judges; confidence threshold to cut noise.
- Launcher/stop conditions: ralph's Stop-hook mechanics (session_id isolation, iteration cap, corrupted-state handling that
  deletes the state file and exits cleanly) as a reference for keeping a long-lived role going.
- Permissions hook: hookify's rule-file pattern for a scoped, readable allow/deny policy.
- Distribution: ship from our own marketplace (`/plugin marketplace add sharifamlani/autonomous`), since the directory
  currently refuses command hooks and scripts from unverified orgs (#7024).

**What to avoid**
- Ralph's exit test is a phrase the builder prints itself ("do not lie to exit!", `stop-hook.sh`). The literature says checks
  the builder controls get gamed; the kit's done-signal must come from QA/Tester verdict files, not the builder.
- hookify's "tests ran" check is a transcript regex (`require-tests-stop.local.md`): proves a command was typed, not that
  tests passed.
- Counting on the official directory for a plugin with command hooks and a launcher script (#7024).

**Evidence level.** CI checks are real and reproducible (validate, frontmatter, policy scan). skill-creator is
a method, not results; no measured numbers for any plugin's effect are published here. security-guidance has
unit tests but no published catch rate. UNVERIFIED.

### wshobson-agents (`wshobson/agents` @ 4220308)

**What it is.** A large marketplace: 91 local plugins, 199 agents, 185 skills, 103 commands, written once in
Claude Code format and transpiled to six other harnesses (`AGENTS.md`). **License:** MIT (`LICENSE`). Copying
allowed? Yes, with conditions (keep notice).

**Process: how the work is organised**
- Packaging: `plugins/<name>/` with `.claude-plugin/plugin.json`, `agents/`, `commands/`, `skills/<n>/SKILL.md` (+
  `references/`); source of truth only under `plugins/`, generated per-harness trees are never hand-edited and CI fails on
  drift (`AGENTS.md` "Regenerating per-harness artifacts", `tools/generate.py`, `tools/adapters/`).
- Roles: one agent per specialty with a model tier in frontmatter (opus for architects, sonnet for implementers;
  `docs/agents.md`). Team plugin `plugins/agent-teams/` (team-lead, team-implementer, team-reviewer, team-debugger) runs on
  Claude Code's experimental Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, tmux panes) with presets and strict file
  ownership: "No file appears in multiple clusters", shared types owned by the lead
  (`skills/parallel-feature-development/references/file-ownership.md`).
- File handoffs: `plugins/full-stack-orchestration/commands/full-stack-feature.md` writes each step to
  `.full-stack-feature/NN-*.md` and a `state.json`, reads prior step files "do NOT rely on context window memory", and stops
  at PHASE CHECKPOINTs for user approval (so not unattended).
- Gates: `make validate STRICT=1`, `make garden` (dead links, oversize skills, duplicate agents), `make test`, `make
  smoke-test` (real CLIs load the generated files) on every PR (`AGENTS.md` "Quality gates"; `docs/round-trip-results.md`).
- Permissions/hooks: only two plugins ship hooks. `plugins/review-agent-governance/hooks/hooks.json` runs a PreToolUse check
  for a human approval flag before PR reviews, merges or CI edits, and signs every tool call with an Ed25519 receipt on
  PostToolUse (via `protect-mcp` + Cedar policies).
- Eval: `plugins/plugin-eval/` scores static lint, an LLM judge and a Monte Carlo layer into a 0-100 badge; weekly CI runs
  the static layer only (`docs/plugin-eval.md`); `evals/static-score-snapshot.json` guards scoring drift.

**Lessons learned**
- Installing everything floods context: "Large cumulative agent descriptions will impact performance (~404.1k tokens >
  15.0k)" (#93).
- Duplicate agent names across plugins silently overwrite each other: 30 names reused in 94 files, `code-reviewer` 7 times
  (#500 "30 duplicate agent names cause runtime collisions"; #643; #80 agents listed twice).
- Real-CLI round trips caught three bugs unit tests missed (YAML block-scalar descriptions, an OpenCode permission block that
  denied everything, a rejected schema key) (`docs/round-trip-results.md`).
- They label their own LLM-judge and Monte Carlo layers "experimental, not validated against human labels"; the judge "writes
  its own test prompts and grades its own predictions", activation counts "any non-empty reply", quality "measures reply
  length, not whether the reply is correct" (`docs/plugin-eval.md`). They moved to trace-based error analysis first, LLM
  judge trusted only after checking against human labels (`evals/README.md`).
- Unreviewed agent prompts can carry harmful content (#55 "hr-pro.md contains inappropriate and harmful content").
- Keep the root context file a short map (~150 lines), details in `docs/` and skills (`AGENTS.md` "Why this file is short").

**What the kit should take**
- Roles/prompts: the file-ownership rule (one owner per file, lead owns shared contracts) for any time two builders run at
  once (`file-ownership.md`).
- Launcher/handoffs: the numbered step files + `state.json` resume pattern from `full-stack-feature.md`, with the human
  checkpoints replaced by QA/Tester verdict files.
- Permissions hook: the PreToolUse "approval flag" idea from `review-agent-governance` to hard-block merges, pushes to main
  and CI edits unless the lead's merge file names that sha.
- Benchmark/CI: a real-CLI smoke test of the installed plugin (load it, list agents and skills) in CI, and a name-collision
  check (`tools/check_agent_name_collisions.py` idea).
- Their honest "known limits" section as a model for our benchmark README.

**What to avoid**
- Many narrow specialist agents: the literature says role teams do not beat one strong agent at equal cost (except
  dev+tester), and here they cost context (#93) and collide (#500). Keep the kit's roster small.
- Static lint scores or self-graded LLM badges as quality evidence (`docs/plugin-eval.md` admits they do not measure task
  success).
- Building on experimental Agent Teams: our spike found built-in teams never start under `claude -p`.

**Evidence level.** Structural and round-trip checks are measured and reproducible (counts in
`docs/round-trip-results.md`). No measured task-success numbers for any agent or plugin; badges reflect lint
only. UNVERIFIED.

### claude-code-action (`anthropics/claude-code-action` @ acfe799)

**What it is.** A GitHub Action that runs Claude Code on `@claude` mentions (tag mode) or a given `prompt`
(agent mode) in CI, unattended, plus a standalone `base-action/` (`CLAUDE.md`). **License:** MIT (`LICENSE`).
Copying allowed? Yes, with conditions (keep notice).

**Process: how the work is organised**
- One entrypoint `src/entrypoints/run.ts`: prepare (auth, write-access check, branch and tracking comment), install CLI, run
  Claude via `base-action/`, cleanup; token revocation and SSH-signing cleanup run as separate `always()` steps so a crash
  cannot skip them (`CLAUDE.md` "Things That Will Bite You").
- Prompt construction is the heart: GitHub data fetched and formatted to a temp prompt file (`src/github/data/fetcher.ts`,
  `formatter.ts`, `src/create-prompt/`).
- Unattended permissions: sessions start in `--permission-mode auto` by default, where a safety review decides any tool call
  not covered by narrow allow rules; broad rules like `Bash(*)` are ignored in this mode (`docs/usage.md` "Permission Mode",
  `src/modes/permission-mode.ts`). Auto is turned off when untrusted text can reach the run (`allowed_non_write_users`,
  `allowed_bots`), when a custom base URL could drop the safety verdict, or when a settings file the PR could edit chooses
  the mode.
- Guards the agent cannot edit: on PRs, `.claude/`, `.mcp.json`, `CLAUDE.md`, `AGENTS.md`, `.husky/` and any config named by
  inputs (`--settings`, `--plugin-dir`, `--agents`...) are restored from the base branch; PR versions are kept read-only
  under `.claude-pr/` (`docs/security.md`). `src/github/operations/session-guard.ts` snapshots files later steps trust and
  restores them after the session, disables git programs, pins the only branch the push wrapper may update, and excludes
  restored paths from commits ("It is not a sandbox", its own comment).
- Repo's own CI: egress-firewall runner, network allow list in enforce mode, auto mode on every Claude step, all checked by
  `.github/workflows/workflow-hardening.yml` (`CLAUDE.md` "Security hardening").
- Human gate: `agent-approval-check/` requires N human approvals on any PR with agent commits, counting only write-access
  users and `/approve <head-sha>` comments that match the current head; "the same gate Anthropic runs internally"
  (`agent-approval-check/README.md`).
- Stop conditions: `--max-turns` via `claude_args` and job-level `timeout-minutes` (`docs/migration-guide.md`). Tests: ~60
  unit test files in `test/`; "Integration testing happens in a separate repo (`install-test`)" (`CLAUDE.md`).

**Lessons learned**
- Allow-lists confuse the agent: Claude reported missing Bash permission even with `Bash(*)` allowed (#74, 28 comments).
- Runs hang: "About 20% of the time Claude will never respond - so the github action times out after 6 hours" (#674 "Code
  reviews keep timing out"); silent crashes "after ~150ms with $0 cost" (#853, #892, #944 no output).
- CLI upgrades break every run: installer "reports success but leaves no launcher" (#1817; #1290; #1849).
- Review-fix loops can spiral and look like abuse: "Claude reviews → user command → new commit → Claude re-reviews" leading
  to account bans (#641).
- Users want one updating comment, not a stream (#37, #207, #419); top request is inline review comments (#60).
- An approval tied to a sha goes stale when the head moves; they flag `/approve <old-sha>` as stale
  (`agent-approval-check/README.md`).

**What the kit should take**
- Permissions hook: model the scoped PermissionRequest hook on their auto-mode rules: narrow allow rules, never `Bash(*)`,
  deny by default where untrusted text enters, explicit `--disallowedTools` (`docs/usage.md`, `permission-mode.ts`).
- QA/Tester gates: restore role prompts, agent definitions, hooks, settings and test files from a frozen copy before every QA
  run so the builder cannot edit the checks (`docs/security.md` restore list; `session-guard.ts` snapshot/restore).
- Merge gate: sha-pinned approvals (`/approve <sha>`, stale on new push) for the lead's merge rule: merge only the exact sha
  QA and the Tester passed.
- Launcher: put cleanup and cost/token summaries in steps that run even on crash; enforce `--max-turns` plus a wall-clock
  timeout per role and treat "no output, $0 cost" as a failed run to retry, not success.
- Status: one updating status file/comment per run, not many.

**What to avoid**
- Relying on an allow-list alone to make an unattended agent behave (#74); combine allow rules with a deny-by-default hook
  and a sandbox.
- Unbounded review-fix ping-pong (#641); cap rounds as superpowers does.
- Trusting a green install step: verify `claude --version` after install, as their sister repo's CI does with retries
  (`claude-plugins-official/.github/workflows/validate-plugins.yml`).

**Evidence level.** Security behaviour is backed by unit tests in `test/` (e.g. `session-guard.test.ts`,
`untrusted-pr.test.ts`); no published success-rate or cost numbers for agent work. Issue numbers (20% hangs)
are user reports. UNVERIFIED.

### sandbox-runtime (`anthropics/sandbox-runtime` @ 0bbebed)

**What it is.** `srt`, an OS-level sandbox for any process (Seatbelt on macOS, bubblewrap on Linux, a
dedicated user account plus WFP firewall on Windows, alpha) with proxy-based domain allow-lists; built for
Claude Code (`README.md`). **License:** Apache-2.0 (`LICENSE`). Copying allowed? Yes, with conditions (keep
license and notices, mark changes).

**Process: how the work is organised**
- Not an agent framework: no agents, skills or prompts. It wraps a command (`srt "<cmd>"`) or an MCP server (`"command":
  "srt"` in `.mcp.json`) and reads policy from `~/.srt-settings.json` (`README.md` "Example Use Case: Sandboxing MCP
  Servers").
- Policy model: reads allowed by default with deny-then-allow; writes denied by default (allow-only); network denied by
  default (allow-only domains) via HTTP and SOCKS5 proxies on the host ("Dual Isolation Model"). Recipes include
  workspace-only access (`denyRead: ["/Users"]`, `allowRead: ["."]`) ("Common Configuration Recipes").
- Mandatory deny paths: writes always blocked to shell rc files, `.gitconfig`, `.mcp.json`, `.vscode/`, `.claude/commands/`,
  `.claude/agents/`, `.git/hooks/`, `.git/config`, even inside allowed write paths ("Mandatory Deny Paths").
- Violation evidence: a violation store with per-command ids on macOS ("Violation Detection and Monitoring"). `srt proxy`
  runs only the proxy and asks a separate "decider" process to allow each request (`docs/srt-proxy.md`).
- Testing: ~120 test files in `test/sandbox/` (credential masking, deny ordering, ancestor pinning, property tests) and CI
  workflows `integration-tests.yml`, `release.yml`.

**Lessons learned**
- Sandboxing alone does not stop an agent that may turn it off: "In sandbox auto-allow mode, Claude can autonomously bypass
  sandbox restrictions by setting `dangerouslyDisableSandbox: true`" (#97, open).
- Default read-everywhere leaks: Claude can read other processes' env vars and args on macOS (#160); users ask for
  workspace-only reads (#2, #10).
- Side-effect files: `srt` leaves `.bashrc`, `.mcp.json`, `.claude` etc. placeholders in the working folder, and they stay if
  killed (#139, 81 upvotes, open; #85).
- Hardcoded protected folders break real work, e.g. `.idea` blocking git operations (#159); some flags weaken more than they
  say (`allowLocalBinding` also lifts outbound TCP, #225; DNS exfiltration, #88).
- Windows is alpha: needs a one-time elevated `windows-install` (UAC prompt), Schannel-based clients do not work inside,
  per-user tool installs are unreachable without a profile read grant, and several network escapes are documented as
  residuals ("Windows (alpha)", "Known limitations").
- Install `srt` outside every writable path; a copy in `<project>/node_modules/` can be rewritten by the sandboxed command
  and then run unsandboxed ("Security Limitations").
- Broad domains like `github.com` allow exfiltration; domain fronting may bypass the filter ("Security Limitations").

**What the kit should take**
- Permissions hook: the hook must deny any call with `dangerouslyDisableSandbox` and any write to `.claude/`, hooks, settings
  and test folders, mirroring the mandatory deny list (#97; "Mandatory Deny Paths").
- QA/Tester gates: the mandatory-deny idea is exactly "checks the builder can't edit": protect `.claude/agents/`,
  `.claude/commands/`, `.git/hooks/` and the QA test folder from the builder session.
- Launcher (later, Linux/macOS benchmark runners): wrap each role's session with a workspace-only `srt` policy and a short
  domain allow-list; keep a per-run violation log as evidence for the benchmark's "human interventions / incidents" column.
- Benchmark: run benchmark tasks under a fixed sandbox policy so runs are comparable and safe to leave unattended.

**What to avoid**
- Treating Windows `srt` as ready on Sharif's machine: alpha, needs admin, and breaks Schannel clients; do not make the v0.1
  kit depend on it.
- Relying on the network filter against code written to beat it; the README says it stops "commands that connect directly,
  not code written to defeat it" (Windows "Known limitations").
- Running sandboxed commands from the project root without cleanup of the placeholder dotfiles (#139); run them in a
  disposable run folder.

**Evidence level.** Behaviour is backed by a large test suite and documented residual probes
(`verifyWindowsWfpEgress()` reports `anonymous-loopback`, `deny-only-user-sid`). No independent security audit
numbers in the repo. UNVERIFIED until we test it on our runner.

## B. Team methods and autonomous loops

### BMAD-METHOD (`bmad-code-org/BMAD-METHOD` @ e435a22)

**What it is.** A skills-based agile method for Claude Code and other agents: persona agents (analyst, PM, architect, UX, dev, product owner) plus workflows that carry a change from idea to reviewed commit. This pin is the v7 preview alpha (`README.md`). **License:** MIT (`LICENSE`), but the names "BMad"/"BMAD-METHOD" are trademarks outside the MIT grant (`TRADEMARK.md`). Copying allowed? With conditions: copy code and text with the MIT notice, never the name or branding.

**Process: how the work is organised**
- Roles are skills, one folder each: `skills/method/bmad-agent-{analyst,pm,architect,ux-designer,dev,po}/SKILL.md`. Work moves through files, not chat: a ticket tree (`tickets.toml` per epic, rules in `tools/ticket-tree-rules.md`) and one **plan file per ticket**. The plan is the contract between plan, implement and review (`docs/build/autonomous-development-loops.md`, "Primary Plan Artifact").
- The plan has an `<intent-contract>` block (problem, approach, Always/Never limits, an I/O and edge-case matrix) that later steps may not edit (`skills/method/bmad-build-auto/plan-template.md`; `step-03-implement.md` RULES). Frontmatter holds the machine state: `status`, `baseline_revision`, `risk`, `review_loop_iteration`, `deferred`, `followup_review_recommended`.
- The unattended worker is `bmad-build-auto`. One call handles one ticket: clarify, plan, implement, review, then a terminal status of `built` or `blocked` with a named reason. It never picks the next ticket and never marks a ticket `done`; the orchestrator does that (`docs/build/autonomous-development-loops.md`, "Plan Status", "Orchestrator Responsibilities").
- Gates before "built": (1) re-run the plan's `## Verification` commands and halt on failure; (2) a **matrix test audit**: every edge-case row needs a test that actually ran and passed, and "never edit the expectation to match the code" (`step-03-implement.md`); (3) parallel review lenses (`review-prompts/edge-case-hunter.md`, `verification-gap.md`, plus a `blind-hunter` in `bmad-code-review/step-03-triage.md`) that read the diff from a file, not from the builder's story; (4) triage that verifies every finding at the cited line and logs one verdict row per finding (`step-04-review.md`, "Classify").
- Stop rules: the bad_plan loopback halts after 5 iterations ("review repair loop exceeded 5 iterations (non-convergence)"). An intent gap saves the attempted patch, reverts the code and halts `blocked` (`step-04-review.md`). Finalize commits but never pushes, and halts if the tree is dirty.
- Each plan gets a `risk` grade (low/medium/high) at planning, which "a CI process can read ... to decide how much review the change gets". Findings that are real but not this ticket's problem go in a machine-readable `deferred` list, which is "intentionally not a backlog"; the orchestrator decides what to do with them (`docs/build/autonomous-development-loops.md`).
- Rule for ending review: on a follow-up pass, `followup_review_recommended` is true "only if this pass patched a `high`", and "patch volume is never grounds" (`step-04-review.md`, Finalize).
- Running more than one session is left out of scope. The separate `bmad-loop` repo is the orchestrator, and "does not dispatch from the ticket tree yet" (`docs/build/autonomous-development-loops.md`). Party mode (`skills/core-tools/bmad-party-mode`) is several personas inside one session.

**Lessons learned**
- The dev agent ticked off tasks without building or running the tests: issue #95 "Dev agent should compile code and run tests". The current answer is the verification re-run plus the matrix audit in `step-03-implement.md`.
- Persona instructions were skipped silently: issue #387 "Claude Code not following Dev-Agent instructions" (the agent admitted it had not loaded the standards files).
- Context compilation dropped requirements that were only references, so the UI was built without the design contract: issue #2767 "compile-epic-context silently drops reference-only requirements...".
- Re-reading the same documents in every fresh window costs a lot of tokens: issue #511 "big tokens cost". This is why `bmad-shard-pro` exists (CHANGELOG, Unreleased) and why the plan template has a 900–1300-token target warning about "context rot" (`plan-template.md`).
- Backgrounded subagents stall unattended runs: "a backgrounded subagent never hands control back and the run stalls" (`skills/method/bmad-build-auto/workflow.md`, "Subagents"). This matches our own 10-minute background cap finding.
- Prompts are paid for on every run: "do not add instructions for exotic cases", "prefer deleting an instruction to hedging it", and "do not write automated tests for LLM output" (`AGENTS.md`).
- Users pushed back on personas: issue #719 "Remove AI personification".
- A user who gave the dev agent sub-agents for tests, test runs and front-end work saw "significantly improved tests" (issue #537 "BMAD Sub Dev Agents"; one person's report).
- Review triage used to drop findings silently. v6.12 made it "log a verdict and evidence for every finding" (`CHANGELOG.md`, v6.12.0).

**What the kit should take**
- **Roles/prompts + launcher:** the plan-file contract (frozen intent block, `status` and `baseline_revision` frontmatter, a `blocked` vocabulary with named reasons). Adapt `plan-template.md` as our builder handoff file, so Main reads status from a file rather than from chat.
- **QA/Tester gates:** the matrix test audit rule ("a covering test that did not run counts as missing; never edit the expectation") and the "verify every finding at the cited line, one row per finding" triage format from `step-04-review.md`, for our QA verdict file.
- **QA gates:** review lenses that read a staged diff file and are not handed the builder's narrative (`verification-gap.md` evidence rules), plus the 5-loop non-convergence cap.
- **Launcher:** "builder never marks done; only the orchestrator does", and "commit, never push, leave a clean tree" as worker exit rules.
- **Launcher (Main):** the `deferred` list plus the `risk` field as machine-readable outputs Main uses to route follow-up work and choose review depth, instead of the builder opening tickets itself.
- **Benchmark:** the `bmad-eval` case format (`docs/reference/eval-format.md`: `input`, `rubric`, `state_prefix`, fixture files pinned to a commit) as a template for our task specs.

**What to avoid**
- Persona names and theatre (#719). The literature says role teams do not beat one strong agent at equal cost, so keep roles only where they change what is checked.
- One-session party mode as a stand-in for separate sessions. It is not an independent check.
- BMAD's own review lenses are LLM reviewers. The literature says LLM verifiers approve work that real tests reject, so our Tester walk and test re-runs must stay the gate.
- Ignored: `AGENTS.md` tells agents "No tool or model attribution, anywhere". That is an instruction for contributors to their repo, not to us.

**Evidence level.** The CHANGELOG says "blind judges ranked" the new elicitation "above the old skill" (Unreleased); no data is in the repo. The gates are prompt text, with no measured success rates for unattended builds. UNVERIFIED.

### gastown (`gastownhall/gastown` @ 94cc822)

**What it is.** A Go CLI (`gt`) plus daemon that runs 20–30 Claude Code (or other CLI) sessions in tmux, with work tracked in a git/Dolt-backed issue ledger called Beads (`README.md`). **License:** MIT (`LICENSE`). Copying allowed? Yes, with the notice.

**Process: how the work is organised**
- Roles (`README.md`, "Core Concepts"): **Mayor** (coordinator session), **Polecats** (workers: lasting identity, short-lived sessions), **Witness** (per-project watchdog), **Deacon** (patrol supervisor), **Dogs** (maintenance workers), **Refinery** (merge queue), **Crew** (the human's workspace).
- Work handoff is a "hook": a work item attached to an agent identity and stored in git worktrees and Beads, so it survives crashes. On startup a worker checks its hook, runs what it finds, then checks mail, else escalates (`docs/concepts/propulsion-principle.md`, "Startup Behavior"). Messages are typed beads (`POLECAT_DONE`, `MERGE_READY`) with fixed body fields (`docs/design/mail-protocol.md`).
- Sessions start as `claude --dangerously-skip-permissions` in tmux (`internal/config/agents.go:236`, `internal/config/cost_tier.go:234`). Crew sessions are the only interactive exception (`internal/cmd/crew_lifecycle.go:245`). Resume uses `--resume <session_id>` (`internal/config/agents.go:780`).
- Identity, sandbox and session are separate lifecycles. After `gt done` the session retires, while identity and work history persist (`docs/concepts/polecat-lifecycle.md`). States: Working, Idle, Done, Stalled, Zombie.
- Gates: the Refinery runs pluggable test and lint gates in a batch-then-bisect merge queue. Workers running tests *before* submitting is "Phase 3 ... Blocked" (`docs/design/architecture.md`, "Merge Queue"). The Witness "does NOT gate completion" (same file, "Self-Managed Completion").
- A scheduler limits how many workers are dispatched (`scheduler.max_polecats`) so they do not exhaust the API rate limit. "Seance" lets a new session ask its predecessor questions, using the old session's `.events.jsonl` (`README.md`, "Scheduler", "Seance").
- Supervision: three heartbeat stores. The rule is to never declare an agent stuck from one store, and to cross-check tmux activity first (`docs/concepts/heartbeats.md`). Escalation goes Deacon → Mayor → Overseer by severity (`docs/design/escalation.md`). A context-budget hook warns at 75/85% and blocks at 92%, forcing a handoff (PR #2008).

**Lessons learned**
- Watchdogs kill healthy sessions: a hygiene plugin matched the wrong name prefix and "killed 22 sessions across all 9 active rigs, taking down the entire town" (issue #2707).
- A stale heartbeat file is not a stuck agent ("heartbeat-write divergence", `docs/concepts/heartbeats.md`). Usage-limit pauses were read as crashes and burned the restart budget until the pane was checked for rate-limit text (`CHANGELOG.md`, 1.2.0 "Daemon crash-loop vs Claude usage limits").
- State that is never cleaned up grows without limit over long runs: issue #4869 "gt compact is a no-op ... counts tens of thousands as active", and issue #4958 (orphaned molecule roots).
- Agents can fake tool calls: issue #2814 "Federated completions are vulnerable to silent tool-call confabulation" (reports 25–80% for some lower-tier models; frontier models 0–5%; UNVERIFIED).
- Windows is not viable because of the hard tmux dependency (issue #3538). This is relevant to us: Sharif's machine is Windows.
- Flaky integration tests on main, with a different test failing each run (issue #2832).
- Leftover agent branches pile up on the remote and look like lost work: issue #2435 "refinery should delete polecat's original branch after creating its own PR". Duplicate reports clustered around orphaned processes and branch cleanup (issue #708, RFC on duplicates).
- Built-in workflows spent users' credits on upstream fixes without clear consent (issue #3649).
- Their spike on Claude Code Agent Teams gave "CONDITIONAL GO"; it is still "NOT YET IMPLEMENTED" (`docs/design/witness-at-team-lead.md`).

**What the kit should take**
- **Launcher/registry:** separate lifecycles for identity (role name + registry entry), sandbox (worktree/branch) and session (`claude -p` + `session_id`). Our registry should record all three (`docs/concepts/polecat-lifecycle.md`).
- **Launcher/supervision:** the heartbeat rules. Workers write a self-reported state file (`working|idle|exiting|stuck`); Main cross-checks a second signal before killing anything; rate-limit pauses use a fixed backoff that does not count as a fault (`docs/concepts/heartbeats.md`, CHANGELOG 1.2.0).
- **Roles/handoffs:** typed completion messages with fixed fields (`Exit: MERGED|ESCALATED|DEFERRED`, item, branch) from `docs/design/mail-protocol.md`, as the format of our handoff files.
- **Launcher:** a context-budget handoff at a threshold (PR #2008 design) and severity-tagged escalation that maps onto `SHARIF_ACTION_ITEMS.md`.
- **Benchmark:** `gt-model-eval/` runs each decision task across Opus, Sonnet and Haiku with `--repeat 3` to check whether cheaper models can take patrol roles. Use the same idea for $/task per role.

**What to avoid**
- `--dangerously-skip-permissions` as the default. Our scoped PermissionRequest hook is the safer design.
- A tmux-only runtime (Windows, #3538) and a three-tier watchdog stack. Each watcher added a new failure mode (#2707). Keep supervision to one Main plus file signals.
- Workers marking their own work complete with no test before submit (the gate lives only in the merge queue, `architecture.md`). Our QA and Tester must check before merge.
- Shipping workflows that act on upstream repos (#3649).
- Ignored: `docs/concepts/propulsion-principle.md` and `AGENTS.md` address the reading agent ("YOU RUN IT", "Run `gt prime`"). Data only.

**Evidence level.** "Scale comfortably to 20-30 agents" (`README.md`) is a claim; no success-rate or cost data is in the repo. `gt-model-eval` is a harness with no committed results. UNVERIFIED.

### spec-kit (`github/spec-kit` @ a4d5712)

**What it is.** GitHub's Spec-Driven Development toolkit: a `specify` CLI that installs slash commands (`/speckit.constitution`, `specify`, `clarify`, `plan`, `tasks`, `analyze`, `checklist`, `implement`, `converge`) and templates into many agent tools (`README.md`, `templates/commands/`). **License:** MIT (`LICENSE`, © GitHub). Copying allowed? Yes, with the notice.

**Process: how the work is organised**
- There are no separate agents. One session runs a chain of commands, and each writes a file under `specs/NNN-feature/`: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `tasks.md` (`spec-driven.md`, "Example: Building a Chat Feature"). The files are the handoff.
- How a spec is written (`templates/spec-template.md`): prioritised user stories (P1, P2, ...), each one "INDEPENDENTLY TESTABLE" with an Independent Test and Given/When/Then scenarios; numbered requirements `FR-001` ("System MUST..."); measurable, tech-agnostic success criteria `SC-001`; and `[NEEDS CLARIFICATION: ...]` markers for unknowns.
- Clarification is capped: "Maximum 3 [NEEDS CLARIFICATION] markers", prioritised scope > security > UX > technical. Spec validation re-runs "max 3 iterations" (`templates/commands/specify.md`, lines ~128–235).
- Gates: a project "constitution" with pre-implementation gates (Simplicity: "≤3 projects?", Anti-Abstraction), where any exception must be written up under Complexity Tracking (`spec-driven.md`, "Constitutional Compliance Through Gates"). `/speckit.analyze` is "STRICTLY READ-ONLY" and treats constitution conflicts as CRITICAL (`templates/commands/analyze.md:58-60`). Checklists are "unit tests for English": they test the requirement text, not the code, and the agent "MUST NOT mark generated items [x]" (`templates/commands/checklist.md`).
- Implement asks a human to confirm if checklists are incomplete, follows test-first task order, "Halt execution if any non-parallel task fails", and marks tasks `[X]` (`templates/commands/implement.md:81,152,165,169`). `/speckit.converge` compares the code with spec, plan and tasks and appends any unbuilt work as new tasks (`templates/commands/converge.md`).
- The plan template sets a file creation order: "contracts/ → test files (contract → integration → e2e → unit) → source files to make tests pass", plus a "No speculative or 'might need' features" check (`spec-driven.md`, "Test-First Thinking", "Preventing Speculative Features").
- Extension hooks can be mandatory (`optional: false`) and must run before the command continues. If `.specify/extensions.yml` cannot be parsed, "do not skip silently": the command must report the parser error and that no hooks were checked (`templates/commands/converge.md`, "Pre-Execution Checks"; the same block appears in `analyze.md` and `checklist.md`).
- Unattended running: the `workflows/speckit/workflow.yml` engine runs specify → plan → tasks → implement with `type: gate` approve/reject steps (`on_reject: abort`). There is no permission or loop machinery of its own.

**Lessons learned**
- "SpecKit creates the illusion of work, generating a bunch of text": issue #75 (ignores the project's structure, writes hundreds of pointless tests, over-engineers).
- Specs drift as features pile up, with no consolidation path: issue #620 "How to keep specs consistent and up-to-date with spec-kit?".
- Agents running in parallel on one checkout corrupt each other's state: issue #1476 "Native git worktree Support for Concurrent/Parallel Agent Execution".
- Densely numbered IDs (FR/SC/T/CHK) force renumbering, which breaks every cross-reference: issue #4065 "Stable, block-allocated identifiers...".
- Most heavy-traffic threads are about integration breakage in particular agent tools: #1414, #202, #865, #1866, #417. A multi-tool surface costs a lot of upkeep.
- Brownfield use is a recurring question: #164 "How to use it for existing project", #52, #623.
- One validation change broke every community extension at once: issue #2017 "PR #1776 alias validation breaks all community extensions".
- Branch and folder numbering went wrong when work was created concurrently or repeatedly: issue #1066 "automatic branch naming repeats numbering prefix", issue #2305 (custom branch not respected).

**What the kit should take**
- **Study protocol + new-app spec:** the spec template's shape. Prioritised, independently testable user stories with Given/When/Then, `FR-###` requirements and measurable `SC-###` criteria are a direct fit for our founding-promise card and the Tester's scripted walk. Every SC should become a Tester step.
- **Roles/prompts:** cap open questions at 3, ranked by impact, then make informed guesses and log them as assumptions. An unattended run cannot wait on 20 questions.
- **QA gates:** the read-only `analyze` pass, plus checklist items the agent may not tick itself. This splits writer from checker, matching the literature on checks the builder cannot edit.
- **Benchmark:** `converge` (code vs spec gap → new tasks) as the shape of our "spec coverage" grader. Use stable, non-renumbering IDs from day 1 (#4065).
- **Launcher:** one worktree per parallel agent (#1476).
- **Launcher/hooks:** "fail loudly, never skip silently" when a config or hook file cannot be read (`converge.md` pre-execution block). Our launcher should refuse to start a role whose registry or prompt file does not parse.

**What to avoid**
- Text volume as a stand-in for progress (#75). Keep templates short and tie each artifact to a check.
- Self-ticked `[X]` tasks as proof of done (`implement.md:169`). Completion must come from tests and a walk, not from checkboxes.
- Supporting many agent tools. Most issue volume is integration breakage; we target Claude Code only.
- Numbering IDs densely and in sequence (`templates/commands/tasks.md:161` "Sequential number (T001, T002...)"). Every edit forces a renumber that breaks references (#4065).

**Evidence level.** `spec-driven.md` argues that templates "constrain LLMs for better outcomes", but there is no benchmark or measurement in the repo. Tests cover the CLI only (`tests/`). UNVERIFIED.

### ralph-claude-code (`frankbria/ralph-claude-code` @ 11f9df5)

**What it is.** A bash wrapper that runs `claude` again and again on a fixed `PROMPT.md` (the "Ralph Wiggum" technique) until exit rules fire, with a rate limiter, circuit breaker, session resume, optional Docker/E2B sandbox and tmux monitor (`README.md`, `ralph_loop.sh`). **License:** MIT (`LICENSE`). Copying allowed? Yes, with the notice.

**Process: how the work is organised**
- One agent, one loop. The handoff is files in `.ralph/`: `specs/*` (requirements), `fix_plan.md` (checkbox task list), `AGENT.md` (build/run notes), and a per-loop status block (`templates/PROMPT.md`, "Current Objectives").
- Each loop must end with a `---RALPH_STATUS---` block (`STATUS`, `TASKS_COMPLETED_THIS_LOOP`, `FILES_MODIFIED`, `TESTS_STATUS`, `EXIT_SIGNAL`, `RECOMMENDATION`). `lib/response_analyzer.sh` parses it.
- Stop rules (`ralph_loop.sh:1001-1100`, `should_exit_gracefully`), in order: any permission denial halts; 3 test-only loops in a row ("test_saturation"); 2 "done" signals; a forced exit after 5 `EXIT_SIGNAL=true`; at least 2 completion indicators AND `EXIT_SIGNAL=true` (the "dual-condition gate"); and all blocking `fix_plan.md` checkboxes ticked.
- Circuit breaker (`lib/circuit_breaker.sh:22-27`): opens after 3 loops with no progress, 5 with the same error, a >70% drop in output, or 2 permission-denial loops. 30-minute cooldown to half-open. Git commits inside a loop count as progress (README v0.11.4).
- Permissions: an `ALLOWED_TOOLS` allow-list in `.ralphrc` passed to `--allowedTools`, with git narrowed to named subcommands. `.ralph/` is protected three ways: allow-list, prompt warning, and an integrity check before each loop (PR #182). `.ralphrc` is parsed as data, not run with `source` (PR #363).
- Unchecked items under "Optional"/"Future" headings in `fix_plan.md` do not block the plan-complete exit (`ralph_loop.sh:230`, Issue #239). The prompt also writes out the exit scenarios as Given/When/Then examples (`templates/PROMPT.md`, "Exit Scenarios").
- Other run limits: 100 calls/hour (configurable), a 24-hour session expiry, `--backup` git branches with `--rollback`, and `--dry-run` (README, "What's Working Now").
- Testing: 784 bats tests of the shell loop (README); `TESTING.md` still says 276. There are no tests of whether the built software is correct.

**Lessons learned**
- Self-reported completion lies: issue #91 "Exits with 🎉 Ralph has completed the project! ...but it hasn't". Exit was later tied to an explicit `EXIT_SIGNAL` (README v0.9.9, v0.11.1).
- `--continue` resumed whatever session was newest, including a human's live session: issue #151 "Session continuity can hijack active Claude Code sessions". Fix: `--resume <session_id>`.
- The session-ID file was written with `>>`, grew to 16,972 lines and broke every later loop, and the circuit breaker could not see it because the failure came before progress tracking: issue #227.
- Permission prompts fail silently in headless mode: issue #101 "No Approval Request, silent fail". Wildcards like `Bash(git *)`, and even `*`, still got denied: issues #154, #143. Compound commands with pipes or redirects get past `Bash(cmd *)` patterns (`ralph_loop.sh`, Issue #243 comment).
- Timeouts were mistaken for the 5-hour API limit (PR #184). A three-layer check was added (README v0.11.5).
- The agent deleted its own control folder during cleanups (#149 → PR #182).
- Getting started on an existing project is the most-discussed problem: issue #97 "Ralph not starting on existing project", #85 "Best way to drop into a existing project?". This led to the `ralph-enable` wizard (PR #124).
- The monitor showed stale numbers (issue #196, "API call counter always 0/100"), and the docs drifted from the code (test counts above). Dashboards and docs need their own checks.

**What the kit should take**
- **Launcher/stop rules:** the circuit-breaker settings as a starting point (no-progress 3, same-error 5, permission-denial 2, cooldown) and "git commit = progress" as a cheap progress signal (`lib/circuit_breaker.sh`).
- **Launcher:** always `--resume <session_id>` from the registry, never `--continue` (#151). Overwrite state files, never append (#227). Make sure failures *before* the agent runs also reach the breaker.
- **Permissions hook:** halt and report on the first permission denial instead of looping (#101), and test our PermissionRequest hook against compound commands and wildcards (#154, #243). Protect the run folder (`.agents/` registry) from the agent (PR #182).
- **Roles/prompts:** a fixed, machine-parsed status block at the end of each role's turn, as a structured field in our handoff files.
- **Launcher:** separate the API-limit check from timeouts (PR #184). Ralph's three-layer check is a good model.

**What to avoid**
- Ending a run on the agent's own `EXIT_SIGNAL` or ticked checkboxes (#91). The literature says builders fabricate completion; our stop rule must be an independent test re-run plus the Tester walk.
- `templates/PROMPT.md` tells the agent "LIMIT testing to ~20% of your total effort" and "PRIORITIZE: Implementation > Documentation > Tests". That runs against the evidence that tests plus requirements help most.
- Loading config as code (`source .ralphrc`, fixed in #363).
- A breaker that only reads signals after the agent runs. In #227, a failure at CLI startup looped forever with `consecutive_same_error` stuck at 0.
- The template's "max 100 concurrent" subagents (`templates/PROMPT.md`). Nothing measured supports it.

**Evidence level.** "784 tests, 100% pass rate" (README) measures the bash harness, not the outcomes it builds. There are no success-rate or cost numbers. UNVERIFIED.

### MetaGPT (`FoundationAgents/MetaGPT` @ 11cdf46)

**What it is.** A Python framework that models a software company as LLM roles following SOPs ("Code = SOP(Team)"), turning a one-line requirement into a PRD, design, tasks and code (`README.md`). It calls the OpenAI-style API directly; it does not drive Claude Code. The last commit is 2026-01-21, and the team's focus has moved to the MGX product (`README.md`, News). **License:** MIT (`LICENSE`). Copying allowed? Yes, with the notice.

**Process: how the work is organised**
- Roles are Python classes (`metagpt/roles/product_manager.py`, `architect.py`, `project_manager.py`, `engineer.py`, `qa_engineer.py`, `di/team_leader.py`). Each role watches certain action types and reacts to messages whose `cause_by` matches (`metagpt/roles/role.py:284-291`, `:411`). Messages are published to a shared environment (`role.py:429-446`).
- Artifacts are files in the generated project repo: `docs/prd`, `docs/system_design`, `docs/task`, `docs/code_plan_and_change` (`metagpt/const.py:90-94`). RFC 135 changed handoffs from message bodies to file references (`roles/qa_engineer.py` header).
- Run loop and stop rules: `Team.run(n_round=3)` loops until rounds run out, all roles are idle, or the budget is spent (`metagpt/team.py`, `_check_balance` raises `NoMoneyException`). The CLI defaults are `investment=3.0`, `n_round=5`, `run_tests=False` (`metagpt/software_company.py:16-19`). Team state can be saved and resumed (`team.py` `serialize`/`deserialize`).
- Gates: in the current default team, the separate `QaEngineer` and code-review engineer are **commented out**; the team is TeamLeader, PM, Architect, Engineer2, DataAnalyst (`software_company.py:45-62`). When used, QaEngineer writes its own tests, runs them and debugs, with `test_round_allowed = 5` (`roles/qa_engineer.py`). `ActionNode` has `review`/`revise` with AUTO or HUMAN modes (`actions/action_node.py:32,718-816`).
- The default environment is `MGXEnv` (`team.py`, `use_mgx=True`), where a TeamLeader routes work, with `max_react_loop = 3` (`metagpt/roles/di/team_leader.py`). The older design ran 5 parallel engineers with review (`Engineer(n_borg=5, use_code_review=...)`); that line is now commented out (`software_company.py:56-57`).
- Specs before building: the PM writes a PRD (`actions/write_prd.py`, with a review action `write_prd_review.py`), the Architect writes an API/system design (`design_api.py`, `design_api_review.py`), and the PM role writes tasks (`project_management.py`). Each step reads the previous step's document from the project repo.
- `Team.run(..., auto_archive=True)` archives the project when the run ends (RFC 135 note in the `team.py` header).
- Unattended running: one process, no permission model, no sandbox, no heartbeat. The only limits are rounds and dollars.

**Lessons learned**
- Structured output broke all the time: issue #562 (`JSONDecodeError` after the repair retries), issue #351 (`parse_code` regex mismatch), #1340. The roadmap marks "occasional failure to follow instruction ... causing code parsing errors" as fixed only by moving to function calling (`docs/ROADMAP.md`, Usability 5; Features 1).
- Runs stalled partway and left the task unfinished: issue #35 "task not completed and issues during the process".
- Incremental (brownfield) development was dropped, and users asked why: issue #972 "Discussion - Incremental Development Mode".
- The test role never matured: "Perfect the test role" is still an open roadmap task, and the short-term goal is "fully automatic implementation of medium-sized projects (around 2000 lines of code)" (`docs/ROADMAP.md`).
- Provider and rate-limit friction makes up most of the top issues: #988, #996 (Anthropic 429), #180, #1382, #1617.
- Unpinned dependencies break installs over time: issue #1617 "TypeError: AsyncClient.__init__() got an unexpected keyword argument 'proxies'", plus several setup issues (#42, #321). The kit should pin its few dependencies and check them in CI.
- Splitting work into more, smaller roles costs tokens: "Attempt to atomize all role work, but this may significantly increase token overhead" (`docs/ROADMAP.md`, Features 3).
- Windows breakage: issue #926 "ModuleNotFoundError: No module named 'pwd'", issue #1132 (Minecraft env not adapted to Windows). The last commit (#1897) is a Windows terminal fix.

**What the kit should take**
- **Launcher/benchmark:** the hard budget stop (`Team.invest` → `NoMoneyException`) and the round cap, as two independent kill switches next to our time cap. Record the reason the run stopped.
- **Roles/handoffs:** pass file references, not message bodies (RFC 135 note), and keep named artifact folders per stage (`const.py:90-94`). This confirms our files-and-registry design.
- **Launcher:** save and resume team state (`team.py` `serialize`/`deserialize`) so a crashed run picks up where it stopped. Our registry plus `--resume` covers this.
- **Roles/prompts:** structured output through tool/function calls, not by parsing free text (ROADMAP Usability 5).
- **Benchmark:** a per-run cost counter at the team level (`Team.cost_manager.total_cost`, `team.py`). Our launcher should likewise sum every child session's cost into one $/task figure.
- **Roles/handoffs:** a review action paired with each spec artifact (`write_prd_review.py`, `design_api_review.py`) is the cheapest place to catch spec errors. Use it only as a pre-build check, never as the done gate.

**What to avoid**
- A fixed PM → Architect → PM → Engineer waterfall. The literature says role teams do not beat one strong agent at equal cost, and MetaGPT's own default team has since dropped its QA and reviewer roles (`software_company.py:56-62`).
- A QA role that writes the tests it then grades (`qa_engineer.py`). Checks must be ones the builder cannot edit.
- Greenfield-only generation with no brownfield path (#972), and free-text parsing of model output (#562, #351).
- Treating "rounds ran out" or "all roles idle" as finished. With `run_tests=False` by default (`software_company.py:19`), a run can end with nothing executed. Our stop reason must be logged apart from our pass verdict.
- Copying it as a code base. It does not drive Claude Code, it has no permission or sandbox layer, and development has slowed (last commit 2026-01-21). Take ideas, not code.

**Evidence level.** No benchmark numbers or results are in the repo. The research claims live in the linked papers (`README.md` News, `docs/ACADEMIC_WORK.md`). The issue tracker shows frequent parse failures and unfinished runs. Popularity (71,372 stars per `gh api repos/FoundationAgents/MetaGPT`, 2026-11-21) is not evidence of how good the results are. UNVERIFIED.

## C. Coding agents and evaluation harnesses

### OpenHands (`OpenHands/OpenHands` @ bb526a3)

**What it is.** At this pin the repo is the "Agent Canvas" React/TypeScript front end plus local-stack launcher. The agent, tools and server API have moved to `OpenHands/software-agent-sdk` (ownership table in `AGENTS.md`), so the old `evaluation/` benchmark harness is not in this clone. **License:** MIT (`LICENSE`). Copying allowed? yes, keep the notice.

**Process: how the work is organised**
- Contributor knowledge is split into skills that load only for the area being changed (`.agents/skills/*/SKILL.md`, table in `AGENTS.md`). `AGENTS.md` stays short and points to them.
- **The builder cannot edit the checks.** The `verify-*` skills hold the feature map, expected results, known-bug recipes and driver. Implementer agents must treat them as read-only (`AGENTS.md`, "Verification Skill Independence"). CI enforces it: a PR that touches `.agents/skills/verify-*/` may touch nothing else (`.github/workflows/verify-skill-isolation.yml`). The workflow runs only trusted base-branch code and refuses a partial file list.
- **Tester tool:** `.agents/skills/verify-openhands/` ships `control-openhands`, a CLI that launches an isolated real stack (private HOME, free ports, its own run dir), runs a read-only `doctor` before any driving, and turns each user step into a command that prints JSON. Exit codes are 0 ok, 1 action failed, 2 usage, 3 environment. Evidence goes in a ledger with `pass/fail/blocked/not-run`, plus `xfail/xpass` for known bugs (`references/report.md`). A path the CLI cannot drive counts as a "harness gap": the fix is to extend the CLI, never to write a one-off script.
- **Daily delta pass vs weekly full pass** (`references/daily.md`, `maintenance.md`). Tiers run cheapest first: static map checks, then families touched since the last baseline SHA. The baseline only moves when the tier finished, and a pass that runs out of time has to say what it did not reach.
- **Review gate** (`.agents/skills/custom-codereview-guide.md`): the bot reviewer submits APPROVE or COMMENT, never REQUEST_CHANGES ("a human maintainer owns the blocking decision"). Every functional change needs screenshots or video of the running app. A bug fix needs before (on base) and after (on head) with the same setup. Mock-LLM runs count as regression coverage, not live evidence. A screenshot cannot prove timing, so temporal behaviour needs video.
- **PR template** (`.github/pull_request_template.md`): a `HUMAN:` section agents must not edit, and an `AGENT:` section that says "Just running unit tests is NOT sufficient". `check_pr_description.py` enforces that the sections and media exist.
- **Issue gate:** a PR needs a linked issue labelled `ready-for-dev`, and only triage automation or repo writers may apply that label (`.github/workflows/issue-readiness-check.yml`).
- Mutation testing is available (`stryker.config.mjs`, `scripts/stryker-diff.mjs`, `npm run test:mutation:diff`). I found no CI workflow that runs it.
- Release smoke matrix: install method × OS × agent (OpenHands, Claude Code, Codex, Gemini CLI). Each cell is "install, onboard, start conversation, agent replies", tagged P0 (must pass before any release), P1 or P2 (`docs/TESTING_MATRIX.md`).
- Triage writes acceptance criteria as observable outcomes and failure/recovery cases, not as implementation steps (`custom-codereview-guide.md`, "Triage: Behavioral Acceptance and Readiness").

**Lessons learned**
- They used to run nightly integration tests: 6 tiny tasks (t01 fix typo ... t06 browse a GitHub PR), with success rate and $ per task posted per model. Haiku cost about $0.13-0.19 for the set and swung between 6/6 and 5/6 night to night. DeepSeek scored 0/6 (issue #5318 "Nightly Integration Tests Runs", 2024-11 to 2025-01).
- Checks drift unless they are pinned to a baseline SHA and re-proven. Hence the feature-map baseline line and the bug-backfill procedure with three outcomes, each with its own label: mapped, not reproduced, out of scope (`references/bug-backfill.md`).
- Release E2E runs were accidentally testing developer checkouts. The rule now is to unset `OH_AGENT_SERVER_LOCAL_PATH` and similar overrides and confirm package versions in the runtime log (`AGENTS.md`, "Release E2E isolation").
- Changes to prompts, tools or planning can move benchmark scores. The reviewer has to state the eval risk, and a human picks a lightweight eval (`custom-codereview-guide.md`, "Review Sequence and Decision").
- Several agents sharing one machine corrupted each other's evidence. Rules now: export `OH_VERIFY_RUN`, never `pkill -f`, `stop` ends only your own run, and launch refuses when RAM is under about 2 GB (`verify-openhands/SKILL.md`).
- Long `git commit -m` bodies got garbled in the persistent shell, so they now use `git commit -F <file>` (`AGENTS.md`).
- Dependency rule: wait 7 days after publication before adopting a version, and agents may not grant themselves an exception (`AGENTS.md`, "Dependency release-age policy").
- Old benchmark-harness pain: SWE-bench env reset timeouts (issue #2140 "[Bug]: SWE-bench reset_swe_env.py timeout").

**What the kit should take**
- **QA/Tester gates:** copy the isolation rule. The Tester's walk scripts and expected results live in a folder the builder cannot change in the same PR. Add a CI check modelled on `verify-skill-isolation.yml` (read the PR's file list, fail if spec-folder edits are mixed with product edits).
- **Tester:** adapt the `control-openhands` shape for our CUA walks: `launch --new` (isolated run dir), `doctor`, drive, `evidence add --feature F.. --result ..`, `stop`. Use the 5-state ledger (pass/fail/blocked/not-run/xfail) and the rule that a bug counts as fixed only after 2 xfail on base and 2 xpass on the fix.
- **QA gate:** adopt the evidence rules from the review guide wholesale: before/after on the same setup, video for anything temporal, "mock runs are regression proof, not live evidence", overlays dismissed before capture.
- **Roles/prompts:** the AI reviewer never blocks a merge on its own authority. It approves or comments, and the lead or human owns the block. Give PR bodies a split HUMAN/AGENT template.
- **Benchmark:** a nightly smoke set of about 6 tiny tasks, reporting success and $ per task per model, as a cheap canary that runs before the expensive benchmark.

**What to avoid**
- Mutation tooling that exists but no gate runs gives no protection. If the kit says "builder kills mutants", CI must run it.
- One night's 6-task run is too small to compare models (5/6 vs 6/6 was noise). Report the spread over several runs.

**Evidence level.** The process rules are documented and partly enforced in CI (isolation, PR description, label policy). The nightly numbers are real CI output posted on #5318, but they are old (2024) and come from a tiny task set. Agent-quality claims live in the SDK repo, not here. UNVERIFIED.

### mini-swe-agent (`SWE-agent/mini-swe-agent` @ 04d809c)

**What it is.** A deliberately minimal coding agent (about 100-line agent class) from the SWE-bench team: bash only, linear history, every action a fresh `subprocess.run`. It is used as the bash-only baseline on the SWE-bench leaderboard. **License:** MIT (`LICENSE.md`). Copying allowed? yes, keep the notice.

**Process: how the work is organised**
- One loop with 4 swappable parts: agent, environment, model, run script (`AGENTS.md`, `docs/contributing.md`). The policy is "add a new version of a component rather than making the existing one more complex".
- **Stop conditions are built in** (`src/minisweagent/agents/default.py`, `AgentConfig`): `step_limit`, `cost_limit` (default $3), `wall_time_limit_seconds`, and `max_consecutive_format_errors` (default 3). There are also process-wide caps via `MSWEA_GLOBAL_COST_LIMIT` / `MSWEA_GLOBAL_CALL_LIMIT` (`models/__init__.py`). Each stop is recorded as an `exit_status` (Submitted, LimitsExceeded, TimeExceeded, RepeatedFormatError).
- **Explicit submission handshake:** the agent finishes only by running `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt`, and only when that command exits 0 (`environments/docker.py`, `config/benchmarks/swebench.yaml`). The prompt forbids editing tests or config and forbids adding tests or helper scripts to the patch.
- **The trajectory is saved after every step** in a `finally:` block (`default.py` `run()`), together with cost, API calls, the full config and the version (`serialize()`).
- Permission modes for unattended runs: `human` / `confirm` / `yolo`, with a regex whitelist and `confirm_exit` (`agents/interactive.py`). `yolo`, or stdin from /dev/null, means unattended.
- Sandboxes: docker/podman, singularity, bubblewrap, contree, swe-rex modal (`environments/`). Long output is cut to the first and last 5,000 chars, with a warning telling the model to narrow its command (`swebench.yaml` `observation_template`).
- Tests: pytest. The rules are "do not mock anything you're not explicitly asked to" and "avoid trivial tests". A `DeterministicModel` replays scripted outputs so the loop can be tested without API calls (`models/test_models.py`). Grading is outsourced to the SWE-bench harness or `sb-cli` (`docs/usage/swebench.md`).

**Lessons learned**
- Persistent shell sessions were flaky: it is unclear when a command has ended, a bad command can kill the session, and interrupts corrupt later output. Independent subprocesses solved this ("avoids so many issues", `docs/faq.md`, "Why is not needing a running shell session such a big deal?").
- Agents killed at a timeout left no trajectory, so it now saves after every turn (issue #585 "Save trajectory after each turn", raised from Terminal-Bench experiments).
- A format error that dropped the assistant message left the model unable to correct itself, and it burned through the step limit (issue #737 "When FormatError in the traj.json No Assistant response information...").
- After a command timed out, models ran `sleep` expecting it to resume. The timeout message now says plainly that the command did not finish and will not resume (PR #995 "fix(env): clarify timed-out command behavior", closes #950).
- Users could not reproduce leaderboard scores. The maintainers pointed them to the published trajectories, which carry the full config, and to re-grading with `sb-cli`. The issue closed unresolved (issue #756 "Understanding & Replicating mini-swe-agent scores on swebench.com").
- Users asked to raise the cost limit mid-run instead of the run dying (issue #567 "Allow extending cost limit in textual UI").
- Sandbox choice keeps coming back as a request: bubblewrap, E2B, Modal, Contree (issues #452 "Add bubblewrap environment", #792 "feat: add E2B cloud sandbox environment", #679 "Integrate Modal for scalable remote execution"). Singularity hit read-only filesystem errors (issue #710 "Read-only file system error while using singularity as environment").
- Agent-written code is too verbose: "Many LMs write very verbose code -- please clean it up! Same goes for the tests" (`docs/contributing.md`).

**What the kit should take**
- **Launcher / every role session:** the four stop conditions (steps, $, wall time, consecutive format errors), each with a named `exit_status` written to the registry. Add a run-wide $ cap across all sessions, the equivalent of `MSWEA_GLOBAL_COST_LIMIT`.
- **Benchmark:** a mini-swe-agent-style single agent as the **baseline arm** (the literature says one strong agent at equal cost is the bar to beat). Save each trajectory with config, version, cost and calls so any score can be re-graded.
- **Roles/prompts:** an explicit "done" handshake (a fixed sentinel, only on exit 0) instead of inferring completion from silence. Include the "do not modify tests/config, do not submit helper files" boundary block.
- **Tester/QA tooling:** stateless commands (prefix `cd`/env every time) rather than long-lived shells, and head/tail cutting of long output.
- **Kit tests:** a `DeterministicModel`-style replay for testing the launcher and handoffs without paying for API calls.
- **Benchmark (from-scratch arm):** the ProgramBench runner (`docs/usage/programbench.md`, `config/benchmarks/programbench.yaml`). The agent rebuilds source code from a compiled binary and is scored by tests against the rebuilt executable. It is a ready-made hard "build from scratch" task family.
- **Observation template:** show `returncode` and any exception before the output, and send a specific recovery hint when the model hits the token limit without making a tool call (`swebench.yaml` `format_error_template`).

**What to avoid**
- Trusting a leaderboard number you cannot re-run. #756 shows that even the authors' numbers are hard to reproduce without the trajectories and config.
- Writing state only at the end of a run (the #585 failure).

**Evidence level.** The README claims ">74% on SWE-bench verified" and "beats Claude Code and Codex on DeepSWE". Both are external leaderboard claims and were not measured here. UNVERIFIED.

### inspect_ai (`UKGovernmentBEIS/inspect_ai` @ cf72dbc)

**What it is.** UK AI Security Institute's evaluation framework: datasets, solvers and agents, scorers, sandboxes, limits, logs and a viewer. Through its agent bridge it can run CLI agents such as Claude Code inside sandboxes (`docs/agent-bridge.qmd`, `docs/agents.qmd`). **License:** MIT (`LICENSE`). Copying allowed? yes, keep the notice.

**Process: how the work is organised**
- **Contribution gate** (`CONTRIBUTING.md`, `AGENTS.md`): issue-first. A PR from anyone not on `.github/qualified.yml` needs an issue labelled `accepted`, or it is auto-closed. `deferred` issues are closed to PRs, and duplicates are closed in favour of the earlier PR. The stated reason is "a large volume of unrequested, often agent-generated PRs".
- **Agent review disclosure** (`AGENTS.md`, "Agent review"): a non-trivial PR needs at least one code-review pass in a fresh context on a frontier model. The PR body records reviewer model, fresh context or not, number of passes, findings fixed and findings dismissed (with a reason). "A fabricated or content-free review claim is worse than disclosing none."
- **"A test that skipped did not run"**: gated slow/API tests must be run locally for the affected area, and the PR reports passed/failed/skipped counts and a "Not run" bullet (`AGENTS.md`, "Gated tests").
- **Suppression ratchet:** no `# noqa` / `# type: ignore` without a reason. `make suppressions-check` checks against `suppressions.json`, the reason-less count may only fall, and the ledger is never hand-edited (`AGENTS.md`, "Suppression gate").
- **Multiple runs:** `epochs` with reducers (`mean`, `mode`, `pass_at_k`, `at_least_k`) (`docs/metrics.qmd`, "Reducing Epochs"). Eval sets retry failed tasks and reuse completed samples within one `log_dir` (`docs/eval-sets.qmd`).
- **Limits:** cost, token, message, turn, time and working-time limits (`docs/setting-limits.qmd`, `docs/_cost_limits.md`).
- **Sandboxes:** docker built-in, plus k8s, modal, daytona, proxmox and others. `local` is explicitly "no sandbox" (`docs/sandboxing.qmd` provider table; `design/sandbox-trust-model.md`).
- Unattended operation is designed around **an LLM agent watching the eval** through `inspect ctl`, detecting and resolving stalled samples. A human at the CLI uses the same commands (`design/stalled-samples.md`).

**Lessons learned**
- **Grader gaming is real and they keep hardening against it.** Model-graded prompts were hardened against fake data markers in the answer (CHANGELOG, #6282). The scorer no longer takes an earlier grade when the final verdict line will not parse (#6198). Each grading request now gets a random nonce on its field markers, the grade binds to the *last* `GRADE:` line, and a grader panel needs a true majority (a failed grader withholds its vote, so ties become "unscored") (`docs/model-graded.qmd`, "Grading Robustness", "Multiple Models").
- The grader silently fell back to the model under test unless told otherwise. `ModelRole("grader", required=True)` now refuses that fallback (`docs/model-graded.qmd`).
- Grader temperature defaults vary run to run. For reproducible grading set temperature 0 (`docs/model-graded.qmd`, "Reproducible Grading").
- Classic scorer bugs: `exact()`/`f1()` gave a perfect score when the target normalised to an empty string, and an empty completion looked the same as a wrong answer, so `reason="no_response"` was added (CHANGELOG).
- Three outcomes must stay distinct: scored, errored and unscored. Each affects the denominator differently, and mixing them inflates accuracy (`docs/scoring-policy.qmd`, "The three outcomes").
- Cost-limit accounting had holes: calls that tripped a token limit were not counted (#6349). Monitor and reviewer spend was charged to the agent (#6517). An over-limit call is now refused *before* it is sent (CHANGELOG).
- Reading a log must never run its code. Read and run operations were split after the design review (`design/malicious-log-code-execution.md`; issue #5728 "docs(design): code execution from a malicious eval log"; CHANGELOG #6085).
- Agentic evals "end" with 7-8 hung samples out of hundreds. Tight time limits punish legitimately slow samples, so they built detect, diagnose and resolve with explicit dispositions (`design/stalled-samples.md`).
- Pass/fail alone hides shortcuts, so "scanners" now review transcripts for reward hacking, refusals and environment misconfiguration (`docs/scanners.qmd`).
- The single "headline" number defaulted to the first metric of the first scorer. That is wrong when `stderr()` or a cheap sanity scorer comes first, so the headline metric is now configurable (`docs/metrics.qmd`, line 86 onward).
- Rule for code: never silently coerce an error or invalid state into a result. Define the observable error and test it (`AGENTS.md`, "Invalid state").

**What the kit should take**
- **Benchmark:** consider building the kit benchmark on Inspect, or at least copying its concepts: epochs plus reducers for ≥3 runs per arm, the scored/errored/unscored split, `fail_on_error` thresholds and eval-set retries. Its Claude Code bridge already exists (`docs/agent-bridge.qmd`).
- **Independent evaluator:** copy the grading-robustness recipe: nonce-tagged field markers, last-verdict binding, a majority panel where a failed grader gives "unscored" (never 0 or 1), temperature 0, and a required separate grader model.
- **QA gate / roles:** copy the "Agent review" disclosure block into our PR template (reviewer model, fresh context, passes, findings fixed or dismissed). Copy the "skipped ≠ ran" reporting rule.
- **Launcher:** a run-wide cost limit that refuses the call before sending, with monitor and QA spend tracked separately from builder spend.
- **Study protocol:** a transcript scanner pass for reward hacking and environment errors before RESULT.md is accepted.

**What to avoid**
- An LLM grader with default settings and no injection defence. That is the "LLM verifiers approve work real tests reject" failure from the literature.
- A trusting `local` sandbox for unattended runs.
- Absolute time limits as the only stall defence.

**Evidence level.** Mostly engineering documentation and changelog entries with linked PRs. These are well evidenced as *changes made*. No measured gaming rates are given in the repo. Note: `AGENTS.md` contains instructions for AI contributors (identify as an AI, do not approve PRs). They apply to contributors and were ignored here as data.

### harbor (`harbor-framework/harbor` @ 96c86af)

**What it is.** The Terminal-Bench team's harness for running any CLI agent (Claude Code, Codex, OpenHands, mini-swe-agent...) against containerised tasks, locally or on cloud sandboxes. It ships 70+ benchmark adapters and the RewardKit grading library. **License:** Apache-2.0 (`LICENSE`). Copying allowed? yes, keep the license and NOTICE and state changes.

**Process: how the work is organised**
- **Task package** (`AGENTS.md`, "Tasks"): `task.toml` (timeouts, cpus/memory, `network_mode`, agent and verifier users), `instruction.md`, `environment/Dockerfile`, `tests/test.sh` (writes `/logs/verifier/reward.txt` or `reward.json`) and an optional `solution/solve.sh`. Tests and solution are **not** in the agent image. The harness copies `/tests` in after the agent finishes (`src/harbor/cli/quality_checker/default-rubric.toml`, `tests_or_solution_in_image`).
- **Built-in control agents:** `oracle` runs the reference solution and must score 100%. `nop` does nothing (`AGENTS.md` repo tree). Adapters must hit 100% oracle before parity work starts (`adapters/ADAPTER_CONTRIBUTING.md`, Step 3).
- **Separate verifier mode** (`examples/tasks/separate-verifier-environment/task.toml`, `environment_mode = "separate"`): the verifier runs in its own container and receives only declared artifacts. Artifacts are sanitised: setuid bits cleared, outside-pointing symlinks skipped (CHANGELOG). Sidecar artifacts let the verifier score from evidence the agent's container never had write access to, such as request logs and DB dumps (CHANGELOG, "Sidecar Artifacts and Collect Hooks"). Since a recent breaking change, new tasks default to separate verification (CHANGELOG, "task initialization").
- **Task lint and quality check:** `harbor lint` (config, pins, verifier setup, Compose privileges). An LLM `quality_checker` rubric checks: instruction covers what the tests check and vice versa, anti-cheating, no answer in the image, pinned deps, no hard-coded solution (`default-rubric.toml`).
- **Parity rule for adapters** (`ADAPTER_CONTRIBUTING.md`, Step 5): run the same agent version, model ID, prompts and settings on the original benchmark and the Harbor side. They match only if the run *ranges* overlap. Report mean ± SEM, require ≥2 runs per side (3+ preferred), and run symmetrically: 5-10 task sanity, then 1 full run, then 3 runs, on both sides in step.
- **Simulated users:** RFC 0002 proposes a second agent playing the user (`--user claude-code --user-model ...`) for multi-turn tasks, instead of one up-front instruction (`rfcs/0002-simulated-users.md`).
- **Claude Code skills shipped with the repo:** `skills/create-task`, `create-adapter`, `rewardkit`, `upload-parity-experiments` (`skills/`), so agents author tasks the same way every time.
- **Test rule:** do not test CLI help panels or console text, which change with terminal width. Test behaviour or `--json` payloads instead (`AGENTS.md`, "Running Tests").
- **Review:** adapter PRs move through labelled stages: "bot review", "human review", "final review" (issues #545, #501, #471). Contributors must "understand the code you contribute". Docs and PR text are human-written first and last draft, and agent use is disclosed (`CONTRIBUTING.md`, "Golden Rule").

**Lessons learned**
- Once the agent's code reaches the verifier it can patch assertions, write the reward file, read expected answers, or leave a process running. Terminal-Bench #2086 catalogued these attacks. A worker-user fix resisted all 21 cheats in TB PR 2097, but 22 tasks each carried their own home-made privilege drop, so it became a shared `rewardkit.Worker` (`rfcs/0003-secure-rewardkit-workers.md`; CHANGELOG).
- Run the agent as a non-root user and the verifier as root, protect the secret with file permissions, and read submissions *as the agent user* so a symlink cannot make root leak the secret (`examples/tasks/reward-hacking/hello-world-non-root-user/`).
- A judge failure scored as 0 hides instrument failure. RewardKit now stops without writing a reward, and out-of-range scores are rerun rather than clamped (CHANGELOG, "Breaking (RewardKit judge failures)"). Pass-style aggregations now require full marks (CHANGELOG).
- Cloud sandboxes leaked when the harness died. Daytona and E2B now have TTLs and keepalives, and a failed create deletes what the server already made (CHANGELOG).
- Their own parity table has single-run rows and large gaps marked Merged, e.g. `aa-lcr` claude-code 43.7 vs 62.6 with 1 run (`adapters/parity_summary.csv`). The rule and the record do not fully agree.
- Contamination guard: no canary strings in task images (`ADAPTER_CONTRIBUTING.md`, Dockerfile notes).

**What the kit should take**
- **Benchmark:** adopt the Harbor task layout for app tasks: `instruction.md` (spec), hidden `tests/` copied in after the run, `solution/` plus an oracle run proving the task is solvable, and a nop run proving the tests fail on an empty attempt. Consider running the benchmark *on* Harbor (it already supports `--agent claude-code` and `n_concurrent`).
- **QA/Tester gates:** separate-verifier mode is the "checks the builder can't edit" principle made physical. Also take the sidecar evidence pattern (score from logs and DB dumps the app's own container cannot write) and the non-root agent / root verifier split.
- **Benchmark task review:** copy `default-rubric.toml` as the checklist for every benchmark task we write, especially "instruction covers everything tests check" (the literature says detailed requirements help) and "no hard-coded solution".
- **Study protocol / benchmark:** the parity method (overlapping ranges, mean ± SEM, symmetric run order) for comparing kit versions or the kit against a baseline.
- **Permissions hook:** network_mode `no-network` / allowlist per phase as the model for scoping unattended permissions.
- **Tester:** RFC 0002's simulated user, a second agent playing the founder who clarifies as the build goes, as a benchmark arm for `/autonomous:new-app`. Real ideas arrive vague, and this tests whether the kit asks good questions.

**What to avoid**
- Running the grader in the same container and as the same user as the agent (RFC 0003's attack list).
- Treating a judge error as a 0, or clamping out-of-range judge scores.
- Single-run comparisons, even with a written rule against them (`parity_summary.csv`).

**Evidence level.** Attack resistance ("all 21 cheats") is cited from Terminal-Bench PRs, not re-measured here. Parity numbers are self-reported CSV rows. The design rules are documented and partly enforced by lint and defaults. UNVERIFIED.

### commit0 (`commit-0/commit0` @ 1123db3)

**What it is.** A "from scratch" benchmark: 57 Python libraries with function bodies stripped to `NotImplementedError('IMPLEMENT ME HERE')`. The agent must re-implement them so the library's own unit tests pass, with spec docs and lint available (`README.md`, `agent/configs/base.yaml`). **License:** MIT (`LICENSE`, "Copyright (c) 2024 Wenting Zhao"). Copying allowed? yes, keep the notice.

**Process: how the work is organised**
- CLI pipeline: `setup` (clone split), `build` (docker images), `get-tests`, `test --branch/--reference`, `evaluate`, `lint`, `save` (`README.md`; `commit0/harness/*.py`). `--reference` runs the original implementation as an oracle.
- The baseline agent is Aider (`agent/agents.py`). Optional context flags feed it the unit tests, the spec and lint output, each with a length cap (`--use-unit-tests-info`, `--use-spec-info`, `--use-lint-info`, `README.md`). `run_tests` gives test feedback inside the loop, and `max_iteration` defaults to 3.
- Grading takes the git diff base_commit..branch, applies it in a container and runs the pytest IDs. The score is the pass fraction per repo averaged across repos, with xfail counted as passed (`harness/run_pytest_ids.py`, `harness/evaluate.py`).
- Cost is scraped from Aider's log with a regex (`agent/agents.py` `get_money_cost`).
- Per-commit evaluation was added so the score could be tracked over the agent's history (issue #89 "add option for recording eval result after each commit").
- There is no review or gate process beyond pre-commit and a system CI workflow (`.github/workflows/`). The project looks lightly maintained: last merge 2026-02-24, after a gap since 2024.

**Lessons learned**
- **Reward hacking via git history:** repos were cloned with full history, so agents could `git log/show` the stripped originals and paste them. Found in the wild, fixed with `--depth 1` (issue #113 "Reward hacking vulnerability: git history exposes original implementations"; PR #114, commit `157a4ff`, authored by an OpenHands agent).
- **Test-file edits are not blocked:** the evaluated patch is the whole diff (`utils.py` `generate_patch_between_commits` excludes only `spec.pdf.bz2`). The PR to apply only `src_dir` edits was closed unmerged (PR #100 "disallow test file changes", merged=false). An agent can edit the tests it is graded by.
- Tests ran against the *committed* branch, not the working tree. Users saw identical scores before and after edits because changes were not committed (issue #84 "commit0 test Output is Always the Same..."). The per-commit recorder showed the same symptom (issue #90).
- Starting repos sometimes did not even import (syntax errors in stubs), so every test failed for reasons unrelated to the agent (issue #48 "Repos have syntax errors", still open).
- Setup fragility: missing unzip of the spec (issue #71), config errors (issue #85).
- Files had to be implemented in dependency order, so a topological sort of modules was added (PR #72 "add Topo sort", merged 2024-09-29).
- The baseline agent's in-loop feedback is opt-in and capped (`run_tests: false`, `use_lint_info: true` by default in `agent/configs/agent.yaml`; `max_iteration` default 3). So the default baseline never sees a failing test, which makes it a weak lower bound.
- Distributed test backends (Modal, then local Docker and E2B) were added and then needed timeout and version fixes (git log: "work with new modal version", "e2b-timeout"; issue #106 "Add E2B execution backend").

**What the kit should take**
- **Benchmark:** the from-scratch task shape (stubbed library + real unit tests + spec + reference commit as oracle) is a good fit for "new-app"-style tasks. The literature says from-scratch is far less solved and that giving tests and requirements helps. The `use_*_info` flags make that an experimental arm.
- **Benchmark hygiene:** ship task repos as shallow clones with no history and no remote. Grade only source paths, re-applying pristine tests at grade time (the fix #100 never landed). Grade from what is committed and say so in the instructions.
- **Benchmark:** a reference/oracle run per task that must pass, plus a check that the starting state at least imports, so that "all tests fail" means the agent failed, not the task.
- **QA gate:** per-commit scoring gives a learning curve per run, which is useful for hours and $ vs progress in the scorecard.
- **Roles/prompts (builder):** a dependency-ordered work list (the topo-sort idea) and test feedback switched on, since the default no-test config is the weak arm.
- **Study protocol:** run the `use_unit_tests_info` / `use_spec_info` flags as pre-registered arms. That is a direct test of "giving the agent its tests plus detailed requirements helps".

**What to avoid**
- Grading a diff that includes test files. Counting xfail as passed.
- Scraping cost from an agent's log text with a regex. Record cost from the API usage instead (contrast mini-swe-agent's `instance_cost`).
- Assuming a stripped repo cannot leak the answer. Check history, caches, `.pyc` files and installed site-packages.

**Evidence level.** No result numbers are in the repo (`docs/baseline.md` is a stub; the leaderboard lives on the website). The reward-hacking finding is a documented issue plus a merged fix. The test-edit hole is visible in the current code. Benchmark difficulty claims are UNVERIFIED.

## D. Research and data-science agents

### AI-Scientist-v2 (`SakanaAI/AI-Scientist-v2` @ 96bd516)

**What it is.** A pipeline that turns a topic file into ideas, runs ML experiments with a staged best-first tree search, plots the results, writes a LaTeX paper, and has an LLM review the paper. The tree search is built on AIDE (`README.md`, Acknowledgement). **License:** custom, "The AI Scientist Source Code License" v1.0, based on the Responsible AI License (`LICENSE`). It allows use, changes and redistribution, but you must ship the license, pass its use restrictions on to downstream users (3.3), and say plainly in any paper it produces that the paper was machine-generated (3.2.i). Copying allowed? With conditions. For our public kit, adapt the patterns rather than copying code.

**Process: how the work is organised**
- One script per step, run in a fixed order by `launch_scientist_bfts.py`: ideation (`ai_scientist/perform_ideation_temp_free.py`, with Semantic Scholar novelty checks), then experiments (`perform_experiments_bfts`), then plot aggregation, then write-up with retries (`perform_writeup.py` / `perform_icbinb_writeup.py`), then review (`perform_llm_review.py` plus the VLM figure check `perform_vlm_review.py`). There are no separate agent sessions. An "experiment manager" (`ai_scientist/treesearch/agent_manager.py`) runs four fixed stages: `initial_implementation`, `baseline_tuning`, `creative_research`, `ablation_studies` (lines 143-167). Each stage has its own goals and a cap on iterations (`bfts_config.yaml` `stage1_max_iters`..`stage4_max_iters`).
- Gating inside the search: a node counts as buggy if the code raised an exception OR an LLM reading the output says it is buggy (`parallel_agent.py:713`). An LLM decides whether a stage is complete (`stage_completion_eval_spec`). Before a node is reported, the code is re-run over `num_seeds: 3` seeds and the results are aggregated (`_run_multi_seed_evaluation`, `parallel_agent.py:1261`).
- The final review is an LLM filling in a NeurIPS form, with a "negative" system prompt by default ("If a paper is bad or you are unsure, give it bad scores", `perform_llm_review.py`). Its result goes into `review_text.txt` and nothing loops back from it.
- Unattended: yes, for "several hours" per idea (`README.md`). Each code step runs in a `multiprocessing.Process` with a 3600 s timeout (`bfts_config.yaml` `exec.timeout`, `treesearch/interpreter.py`). There is no sandbox. The README tells users to supply one themselves ("Caution!": dangerous packages, uncontrolled web access, spawned processes). Data is copied into the workspace so the agent cannot change the original (`copy_data: True`).
- Human check-ins: optional. A person can hand-pick ideas and supply starter code (`--load_code`). Issue #26 ("were python files in `ideas` human generated?") confirms the `ideas/*.py` files are written by a human, "for code that is hard for LLMs to write".

**Lessons learned**
- The authors say v2 succeeds less often than v1: "v1 follows well-defined templates, leading to high success rates, while v2 takes a broader, more exploratory approach with lower success rates" (`README.md` Note). A strong template beats open-ended search.
- Success depends on the model: "Why wasn't a PDF or a review generated?" FAQ (`README.md`).
- The self-check steps can silently not run. In #133 ("Two v2 bugs ... reproduce in 10 runs (24 PDFs)"), an independent, pre-registered evaluation found that the VLM figure review rejects the configured model every time, so "v2 never actually reviews its own figures". The write-up also exits non-zero even though the PDF was made (#125, `find_pdf_path_for_review` UnboundLocalError).
- Stalls with no logs: in #34 ("System gets stuck at the same stage") runs hang in silent `backoff` retries caused by a wrong key or a spent account. The logs folder stays empty and users kill the process by hand.
- Users ask for reproducibility and for memory across runs (#119 RFC). Temperature 1.0 everywhere (`bfts_config.yaml` `code.temp: 1.0`) makes runs hard to repeat, and each run re-learns the same failures.
- The anti-fabrication rules in the write-up are prompt text only ("Do not hallucinate ... any results not in the logs", `perform_writeup.py:405`). Nothing in code checks that the numbers in the paper match the logs.

**What the kit should take**
- **Study protocol:** a fixed stage list with written goals per stage (implement, then tune the baseline, then try the new idea, then ablate), each with an iteration cap, maps onto PREREG then trials then RESULT. Copy the *idea* behind `main_stage_goals`, e.g. "DO NOT change the model architecture" during tuning, as a rule in the study skill.
- **Study protocol:** re-run the chosen result over at least 3 seeds before it counts, and report the spread. This matches our "runs per arm ≥ 3".
- **Study protocol:** `copy_data: True`. The study works on a copy of the data, and the original is read-only.
- **Launcher:** a per-step timeout plus a non-zero exit with a named reason. Also detect "stuck in API retry" (#34) and surface it as an alert instead of a silent hang.
- **Benchmark:** follow the #133 reporter's method (pre-registered, n runs, failure counts per step) when we grade our own kit.

**What to avoid**
- An LLM review score as the quality gate. The literature already says LLM verifiers pass work that real tests reject, and here the review doesn't even feed back into the run.
- A buggy/not-buggy verdict from an LLM reading stdout as the main check. Prefer hard checks: exit code, and an expected output file with its schema.
- Generating papers. The kit's study output is RESULT.md plus a notebook, not a submission-style paper. Note that the license's disclosure rule would apply if any code were reused for write-ups.
- Running LLM-written code without a sandbox.

**Evidence level.** It claims "the first workshop paper written entirely by AI and accepted through peer review" (`README.md`). The repo has no evaluation harness or success-rate table. Costs of "$15–$20 per run" plus "~$5" for write-up are stated in the FAQ, not measured here. All UNVERIFIED. The only independent measurement we saw is #133 (10 runs, 24 PDFs, DeepSeek), and it is about bugs, not quality.

### AgentLaboratory (`SamuelSchmidgall/AgentLaboratory` @ d9017d9)

**What it is.** A role-played "lab" (PhD student, postdoc, professor, ML and SW engineers, reviewers) that runs literature review, then plan, then data prep, then experiments, then interpretation, then report, then refinement, for one research topic. It has an optional "co-pilot" mode where a human approves each phase. **License:** MIT (`LICENSE`). Copying allowed? Yes, with the copyright notice.

**Process: how the work is organised**
- Roles are Python classes, each with its own phase prompts: `ProfessorAgent`, `PostdocAgent`, `MLEngineerAgent`, `SWEngineerAgent`, `PhDStudentAgent`, `ReviewersAgent` (`agents.py:184-621`). Work moves through seven named phases (`ai_lab_repo.py:82-90`). All roles run in one Python process and share state. Every phase saves a checkpoint (`save_state`, README Tip #3).
- Experiments run in `mlesolver.py`. The code is scored by an LLM "reward model" from 0 to 1 that reads the plan, the code and the output (`mlesolver.py:141-163`, with the comment "todo: have a reward function here"). The best-scoring code is kept.
- Review: three persona-prompted LLM reviewers ("harsh but fair", `agents.py:191-201`). Without a human, the PhD agent itself decides whether to go back or finish after reading the reviews (`ai_lab_repo.py:207-230`).
- Human check-ins: `copilot-mode: True` turns on `human_in_loop()` after every phase. It asks "Are you happy with the presented content? Y or N" and collects notes for a retry (`ai_lab_repo.py:547-565`). Direction from the human otherwise comes from free-text `task-notes` per phase in the YAML (`experiment_configs/MATH_agentlab.yaml`).
- Unattended: each phase stops on `max_tries = max_steps` and then raises "Max tries during phase: ..." (`ai_lab_repo.py:279-454`). Code runs in a subprocess with a 600 s timeout and a string check that blocks `exit(` (`tools.py:306-325`). There is no sandbox, and the API key goes in the YAML (`api-key:` line).

**Lessons learned**
- Weak models fail the data-prep phase. In #104 ("Exception: Max tries during phase: Data Preparation") the author says "gpt-4o-mini struggles with this stage", and o3-mini fixed it.
- Long runs produced nothing at all: #48 ("The agent system isn't creating any files"), "After processing for around one day, it didn't output anything".
- The report step loses content: #103 ("Some sections are always missing"). Sections come out blank or repeated even though the experiments produced results.
- Backend switching broke one phase only: in #46 ("Report Refinement Issue") the refinement phase reverted to the OpenAI client and failed with a 401 after every other phase worked. One provider config, read in many places, drifts.
- #89 ("Almost successful but fail at the last paper writing step!") shows a failure after hours of work because one module (`papersolver.py`) wasn't updated.
- The example MATH config tells the agent to evaluate directly "on the entire 500 test questions" and "Do not try to obtain baseline accuracy ... The baseline ... is 70.2%" (`MATH_agentlab.yaml`). The test set is used for development, and the baseline is asserted, never re-measured.
- In co-pilot mode the human's y/n answer at refinement is never read (`ai_lab_repo.py:216`, the `input(...)` result is discarded).

**What the kit should take**
- **Study protocol / launcher:** a checkpoint after every phase, so a failed phase resumes instead of restarting. This matches `--resume <session_id>` in the registry.
- **Roles/prompts:** per-phase, human-written notes (hardware, models allowed, data loading snippet) put into each phase's prompt. Our PREREG can feed the same block to every study role.
- **Study protocol:** the co-pilot gate is a good *optional* gate after PREREG, before any run. Our unattended default should skip it.
- **Launcher:** a cap on tries per phase, with the phase named in the error.

**What to avoid**
- LLM-as-reward-model for experiment code (`mlesolver.get_score`) and persona reviewers as the finish gate. These are exactly the "LLM verifier approves what tests reject" pattern.
- Tuning on the test set and quoting a baseline from the prompt. The kit's study protocol must split dev/held-out and re-measure the baseline in the same harness.
- Seven role classes in one process. The literature says role teams don't beat one strong agent at equal cost. Keep roles only where a check is independent of the builder.
- Secrets in experiment YAML.

**Evidence level.** README and paper claims (arXiv 2501.04227, AgentRxiv 2503.18102) of better research outcomes are not backed by any evaluation script or results file in the repo. Everything is UNVERIFIED. The example config's "70.2%" baseline is an assertion inside a prompt.

### codescientist (`allenai/codescientist` @ 778b146)

**What it is.** AI2's semi-automated discovery system. It mutates combinations of papers and a library of vetted code examples ("codeblocks") into experiment ideas, builds and debugs the experiment code in Modal cloud containers, writes a report, and runs meta-analyses across repeated runs (`README.md`). **License:** Apache-2.0 (`LICENSE`, README §14). Copying allowed? Yes, with the notice and stated changes.

**Process: how the work is organised**
- Pipeline (prompts linked in README §10): ideation `IdeaStore.generate_new_ideas()`, then plan `convert_idea_to_experiment_prompt()`, then code `CodeBlockStore.combineCodeblocks()`, then a reflect/debug loop `reflectCodeblocks()`, then a results summary, then a LaTeX report, then a meta-analysis `MetaAnalysis.do_metaanalysis_prompt()`. A web server queues experiments in threads (`config_threads.json`, `src/CodeScientistWebServer.py`).
- Two modes (README intro). **Human-in-the-loop** is the mode the paper reports: a human builds codeblocks, filters ideas and adds short expert notes. **Fully automatic** is "less efficient at producing scientific results".
- **Staged pilots:** every experiment must carry `PILOT_MODE` = `MINI_PILOT` (about 10 items, minutes, from the training set), then `PILOT` (hundreds of items, under 1-2 h), then `FULL EXPERIMENT`. The agent must stop after PILOT: "a human will manually verify the results, and make the change to FULL EXPERIMENT" (`src/IdeaStore.py:643-649`). FULL tunes on dev and evaluates on test (`IdeaStore.py:646`).
- **Anti-fabrication check:** a separate reflection pass, `checkCodeForSimulationOrMissingCodeblocks()` (`src/CodeBlockStore.py:1632-1636`), looks for code that "simulates" a step instead of doing it ("it might not figure out how to do an LLM call, so it will 'simulate' an LLM call, with fake/pretend output. This is a major error."). The reflection prompt repeats this (`CodeBlockStore.py:1303`). During MINI_PILOT the agent must log in detail so "low/high performance isn't due to a hard-to-find bug" (`CodeBlockStore.py:386`).
- **Repeats and meta-analysis:** the "Run Benchmark" mode runs N copies of each idea (README §4.5). The meta-analysis counts runs that support, refute or are inconclusive on the hypothesis (README §4.7, `MetaAnalysis.py`).
- **Unattended safety:** code runs in Modal containers, not locally (README §6). LLM calls from experiment code go through a metering proxy (`llm-proxy/llm-proxy-server.py`) that can cut off spending, with status `failed (cost limit exceeded)` (`CodeScientistWebServer.py:73`). Per-experiment caps cover debug iterations, minutes per iteration and cost (`CodeScientistWebServer.py:153-157`).

**Lessons learned**
- The most common failure is faked work. The authors say so in code comments: "The most common error in experiment building is that the LLM can't figure out how to do something, so it will just 'simulate' it" (`CodeBlockStore.py:1632`).
- Sandboxes leak. "Occasionally a container may get past these safeguards ... kill any errant containers" (README §6.5). API keys are only "somewhat hidden" from LLM code (README §6.2). The advice: use only hard-limited keys (README §12, Danger Zone).
- Cost is almost all debugging: "an average of about $4 each ... almost entirely code debugging costs" (README §11 FAQ).
- One meta-analysis LLM call varies from call to call, so the authors did the paper's meta-analysis by hand (README §4.7 "Viewing Reports").
- Local Docker was tried first and dropped for being slow to start and limited by the machine (README §11 FAQ).
- The issue tracker is nearly empty (one issue, #1, libmagic install), so we have no field lessons from it.

**What the kit should take**
- **Study protocol:** the three-level pilot ladder (`MINI_PILOT` then `PILOT` then `FULL`), with dev/test roles fixed in advance and the full run gated. In our kit the gate is the pre-registered held-out look, not a human. Adapt the prompt text at `IdeaStore.py:643-649` (Apache-2.0).
- **Study protocol / QA gate:** a separate "did you simulate anything?" check that reads the code, plus required verbose logs in the smallest pilot. It should run as an independent role, not the builder grading itself.
- **Benchmark:** run each task N≥3 times and summarize support/refute/inconclusive counts. Their 50-idea benchmark files (`data/benchmark_textgames_jan24.*.json`) show how to pair idea+plan as a task.
- **Permissions/launcher:** a metering proxy with a hard dollar cap per run and a named failure status. Keys with hard limits only. Our launcher already sums child costs; add a cap.

**What to avoid**
- Treating the LLM meta-analysis as the verdict. The authors themselves redid it by hand.
- Relying on hidden keys for safety. Assume generated code can find them.
- Modal as a hard dependency for v0.1. It adds an account and a cost; a local sandbox is enough for small known-answer studies.

**Evidence level.** The README points to "20 candidate discoveries" (paper Table 4) and ships raw material: 59 external-reviewer rating rows (`reviews/codescientist_external_review_ratings.tsv`) and two 50-idea × 5-run meta-analyses with and without expert notes (`metaanalysis/*.tsv`). These are real artefacts we could re-score, but the discovery claims are the paper's and stay UNVERIFIED.

### RD-Agent (`microsoft/RD-Agent` @ 484776c)

**What it is.** Microsoft's "R&D" loop: a Research side proposes hypotheses and a Development side implements them. It covers data-science/Kaggle (MLE-bench), quant finance, model fine-tuning and RL scenarios. It is a well-engineered package (CI, mypy, ruff, release-please `CHANGELOG.md`, PyPI). **License:** MIT (`LICENSE`). Copying allowed? Yes, with the notice.

**Process: how the work is organised**
- One loop class per scenario, e.g. `DataScienceRDLoop` (`rdagent/scenarios/data_science/loop.py:87`). Its steps are `direct_exp_gen`, then `coding`, then `running`, then `feedback`, then `record` (lines 139-211). Components can be swapped through settings (`exp_gen`, `ckp_selector`, `sota_exp_selector`, `interactor`, `summarizer`). The core abstractions are in `rdagent/core/` (`proposal.py`, `evolving_agent.py`, `evaluation.py`).
- **Feedback gate** (`rdagent/scenarios/data_science/dev/prompts.yaml` `exp_feedback`): Step 1 is a mechanical submission-format check. Step 2 is an "evaluation alignment" check for leakage, overfitting, and validation that doesn't match the official metric; severe risk sets "Replace Best Result: no". Step 3 compares the ensemble validation score to the current best. Step 4 breaks ties toward less overfitting, no leakage and efficiency.
- **Held-out grading kept away from the agent:** `TestEval.eval()` injects `grade.py` and the answer file `submission_test.csv` into the workspace, runs it in the container, then deletes both (`rdagent/scenarios/data_science/test_eval.py:66-80`). Test scoring is not part of the main loop. It is a separate step after the run, `python rdagent/log/mle_summary.py grade <log>` (`docs/scens/data_science.rst:288-294`, confirmed in #1292).
- **Task packaging** for custom data (`rdagent/scenarios/data_science/example/README.md`): `description.md` (task, data, metric, submission format), `prepare.py` (splits train/test/answer), optional `sample.py` (debug subset), and `eval/<task>/grade.py` + `valid.py`.
- **Unattended:** Docker is required (README Quick start). The loop has a remaining-loop and remaining-step count plus a global timer (`rdagent/utils/workflow/loop.py:129-134`). The runner prompt deliberately hides the time limit from the coder "because the user might over-fit the model to the time limit" (`dev/runner/prompts.yaml:42`). Human input is an optional `DSInteractor.dump_and_wait_for_user_input` hook (`rdagent/scenarios/data_science/interactor/__init__.py`).

**Lessons learned**
- An early wrong implementation poisons every later loop. In #520 ("The initial implementation of the code was incorrect, but RDAgent failed to detect it") a mis-grouped `pct_change` in loop 1 "lead the whole following loops to a wrong direction". The maintainers' answer was to edit prompts, not to add a check.
- Users expect a held-out score and don't get one: #1292 ("Question on how to get run score for test dataset"). Test grading is a separate manual command.
- Who builds the validation split matters: #1290 ("Question on validation dataset creation/agent pipeline"). The simplified `kaggle` scenario splits the data in preprocessing; the maintainers recommend the fuller `data_science` scenario.
- LLM JSON breaks the loop: #916 ("Json loads failed when LLM outputs contain boolean value"). Fixed with a tokenizer-based repair (`rdagent/oai/backend/base.py` `_fix_python_booleans`).
- API retries and environment issues dominate the tracker: #506 and #1023 ("Failed to create chat completion after 10 retries"), #1064 (Windows 11 Docker mount paths), #1372 and #1276 (backtest timeouts).

**What the kit should take**
- **Benchmark / QA gate:** the inject-grade-delete pattern. The grader and answer key enter the sandbox only at grading time and are removed right after, so the agent can never read or edit them. That is the "checks the builder can't edit" rule, in code.
- **Benchmark:** the task folder contract (`description.md`, `prepare.py`, `sample.py`, `eval/grade.py`, `eval/valid.py`). It is a clean template for our known-answer study tasks, including a separate format validator that runs before scoring.
- **Study protocol:** keep the held-out score out of the loop and score it once at the end. Our "one look at held-out" rule already says this; RD-Agent shows it working at scale.
- **Roles/prompts:** the four-step feedback rubric (format, then leakage/alignment, then score vs best, then tie-break toward less overfit) as the study reviewer's checklist. Also hiding budget details from the builder to avoid gaming.
- **Launcher:** reporting mean ± sd over 5-6 seeds (README MLE-bench table notes) is the format our scorecards should use.

**What to avoid**
- No independent check on the first implementation (#520). Our kit needs a known-answer sanity test, run before iterating, that the builder didn't write.
- Leakage and overfit judged only by an LLM reading code (Step 2 is a prompt). Pair it with mechanical checks such as answer-file isolation and fixed splits.
- Docker-only, Linux-only setup (README "currently only supports Linux"). Sharif's machine is Windows.

**Evidence level.** MLE-bench numbers (e.g. 30.22 ± 1.5% "All" for o3+GPT-4.1, 6 seeds; `README.md`) come with seed counts and links to detailed runs, which makes them stronger than most claims here. They are still UNVERIFIED until re-run. The RD-Agent(Q) "~2× higher ARR ... under $10" figure is a paper claim.

### InfiAgent (`InfiAgent/InfiAgent` @ 3d6c4a7)

**What it is.** A small ReAct agent framework (code sandbox, API/vLLM clients, Streamlit demo) plus **InfiAgent-DABench** (ICML 2024): closed-form data-analysis questions over CSV files with exact-answer labels (`examples/DA-Agent/README.md`). **License:** code Apache-2.0 (`LICENSE`). **Data: CC BY-NC 4.0** (badge in `README.md` and `examples/DA-Agent/README.md`; the repo has no separate data license file). Copying allowed? Code yes. Data: non-commercial use with attribution only.

**Process: how the work is organised**
- There are no roles. One ReAct agent (`pipeline/src/infiagent/agent/react/async_react_agent.py`) with a Python tool runs locally by default as a subprocess Jupyter kernel (`tools/code_sandbox/python_code_sandbox.py`), with Docker optional (`tools/code_tool_docker.py`, `configs/tool_configs/*_docker.yaml`). The README says the subprocess sandbox "may introduce certain security issues".
- **DABench task format** (`examples/DA-Agent/README.md`, `data/da-dev-questions.jsonl`). Each line has `id`, `question`, `concepts`, `constraints` (the method rules that pin down one answer, e.g. "Pearson", "round to two decimals", "no further cleaning"), `format` (e.g. `@mean_fare[mean_fare_value]`), `file_name` and `level`. Labels (`da-dev-labels.jsonl`) are `{"id":0,"common_answers":[["mean_fare","34.65"]]}`. The local copy has **257 questions** (82 easy / 87 medium / 88 hard) over 52 of the 68 CSVs in `data/da-dev-tables/`, with 461 sub-answers and 117 multi-answer questions. Concepts: summary statistics 90, correlation 72, distribution 64, feature engineering 50, preprocessing 45, outliers 35, ML 19 (counted from the jsonl).
- **Grader** (`examples/DA-Agent/eval_closed_form.py`): a regex pulls out `@name[value]`, and `is_equal` is an exact string match or `abs(float diff) < 1e-6`. It reports Accuracy by Question (all sub-answers right), Proportional by Sub-Question, and by Sub-Question, plus per-concept breakdowns, written to `eval_outputs/*.json`.
- **Optional LLM reformat:** "most models hardly follow the format requirements", so `reformat.py` asks GPT-3.5 to rewrite responses into the `@name[value]` format before grading (README).
- **How to run one task.** The generator `pipeline/activities/eval.py` loops over every question. Its prompt is `f"Question: {question}\n{constraints}\n"` with the CSV uploaded, and it writes `results_<model>.json`. For one task: take a single line of `da-dev-questions.jsonl`, give the agent the CSV plus `question` + `constraints` + **`format`**, collect `{"id":..,"response":"@name[value]"}` into a jsonl, and run `python eval_closed_form.py --questions_file_path ... --labels_file_path ... --responses_file_path <ours>.jsonl`. (Read only; not run here.)
- The official test split is held back: "We only keep validation dataset for public" and "the test set is used for avoiding data leakage" (`README_eval.md`).

**Lessons learned**
- **The grader leaves unanswered questions out of the denominator.** `evaluate_responses` only adds a result when a non-empty response exists, and accuracy = correct / `len(results)` (`eval_closed_form.py`). A run that skips hard questions scores higher. (Found by reading the code.)
- **Some labels are wrong.** #28 ("Issue with Validation Set Answer for ID=59": "Congo" given as an Americas country) and #29 ("ID=62 答案有问题", with ID 8 also flagged) are both still open.
- **The stats don't agree.** `README_eval.md` says the validation set has 400 questions over 72 CSVs, and its concept table totals 311. The shipped file has 257 questions over 68 CSVs (52 used). The News line "[2024/1/27] DAEval with human filtering updated" may explain the gap. Pin the file by sha.
- **Results are hard to reproduce:** #25 ("Can not reproduce the result of llama2-7b"), with many "Agent unable to answer this question due to LLM fail" responses.
- **The test leaderboard is not reachable:** #30 ("测试集排行榜") and #27 (detailed results "mainly for internal quality control, so we may not release").
- **Windows:** #22 (uvloop does not support Windows). The scripts also open files without `encoding=`, which can break on Windows code pages.
- **The format step is part of the score.** `eval.py` leaves `format` out of the prompt, so the LLM reformat step is needed, and a second model's rewrite is then graded.

**What the kit should take**
- **Benchmark (v0.1 study):** DABench validation as the known-answer task set. It is small, CPU-only, needs no external services, and gives answers to 2 decimals with a deterministic grader. Use our own grader adapted from `eval_closed_form.py` (Apache-2.0) with three fixes: (1) the denominator is all task ids, and missing counts as wrong; (2) the prompt always includes `format`, with no LLM reformat; (3) `encoding="utf-8"` everywhere.
- **Study protocol:** split the 257 into dev and held-out by `id` (stratified by `level`) at PREREG time. Leave out or flag the disputed ids (8, 59, 62) before the split, and log that in PREREG.
- **Benchmark:** don't vendor the data into our public repo. Fetch it at run time from the pinned upstream commit (3d6c4a7) or the HF dataset, with attribution, and record the CC BY-NC 4.0 terms in `benchmark/` docs.

**What to avoid**
- Grading through an LLM reformatter: it is grader leakage.
- Reporting only the best single run. Report all three accuracies over ≥3 runs with their spread.
- Treating the README's 400-question statistics or leaderboard as describing the file we actually use.

**Evidence level.** `README_eval.md` reports results on the validation set at temperature 0.2 (e.g. gpt-4-0613: 65.26 / 59.75 / 66.05 % for PSAQ / ABQ / UASQ). Those tables describe a 400-question version, not the 257-question file shipped. UNVERIFIED, and not comparable to our runs. The grader code itself is fully inspectable and deterministic.

## E. Automated science and autoresearch loops (sweep 2)

### autoresearch (`karpathy/autoresearch` @ 228791f)

**What it is.** A deliberately tiny overnight research loop: an agent edits one training file, trains for exactly 5 minutes, keeps the change if one number (`val_bpb`) went down, reverts it if not, and repeats. Three files matter: `prepare.py`, `train.py`, `program.md`. **License:** no LICENSE file in the clone. `README.md` ends with a "License: MIT" heading, and `gh api` reports no license. PR #575 "Add MIT license file matching README" was closed without merging, and #605 (which also adds a LICENSE) is still open. Copying allowed? **With conditions.** The README states MIT, but no license text or copyright line exists. Copy the *pattern* (an idea, so no license needed). Do not copy files verbatim until a LICENSE lands.

**Process: how the work is organised**
- One agent, no roles. The human writes `program.md`, a short "skill" (README.md: "The `program.md` file is essentially a super lightweight 'skill'"). The agent only edits `train.py` (`program.md`, "What you CAN do").
- **Who measures, and what counts as worked:** the fixed metric is `evaluate_bpb` in `prepare.py:344`. Validation uses a pinned shard (`prepare.py:43`, `VAL_SHARD = MAX_SHARD`) and a fixed token count (`EVAL_TOKENS`, `prepare.py:32`). The keep/revert rule is strict and binary: "If val_bpb improved (lower), you advance the branch … If val_bpb is equal or worse, you git reset" (`program.md`, loop steps 8-9). A "simplicity criterion" lets the agent weigh code complexity against tiny gains.
- **Budget and stop rules:** `TIME_BUDGET = 300` seconds of training (`prepare.py:31`). A run over 10 minutes is killed and discarded. If a crash can't be fixed after "a few attempts", the agent logs it and moves on. There is no overall stop rule: "NEVER STOP … The loop runs until the human interrupts you, period" (`program.md`).
- **Trial log:** every run is a row in an untracked `results.tsv` with columns `commit, val_bpb, memory_gb, status (keep|discard|crash), description` (`program.md`, "Logging results"). Each experiment is a git commit on a dedicated `autoresearch/<tag>` branch. `analysis.ipynb` plots the TSV.
- **Unattended:** "spin up your Claude/Codex … (and disable all permissions)" (README.md). Output goes to `run.log`, and only one line is read back (`grep "^val_bpb:"`), so logs never flood the context.

**Lessons learned**
- Issue #599 "Agent can lower val_bpb without improving the model": the agent owns `train.py`, which calls the evaluator and prints the result (`train.py:613,622`). So the agent can skip training, wrap the metric, or shrink `EVAL_TOKENS`. "Read-only" is enforced only by prose in `program.md`. The thread proposes hashed "experiment receipts" and concludes that a receipt written by the same process is still self-attested. Only an outside re-run is independent.
- Issue #57 "Codex doesn't seem to work?" (41 comments): Codex ignores "never stop", while Claude keeps looping. Whether a loop keeps running depends on the harness, not the prompt.
- Issue #22 "Low creativity" and #80 "encourage experiment diversity": agents settle into small hyperparameter sweeps.
- Issue #307 "0/N experiments kept" (a fork): 400-560 attempts a night with zero kept, because the drafting model was too weak for the reviewer.
- The selection set is also the reporting set. The loop keeps whatever beats the best `val_bpb` on the same pinned shard, with no held-out check. Over ~100 tries a night, some "wins" will be noise. Taken from `program.md` (no second split exists in `prepare.py:283`, `assert split in ["train", "val"]`).

**What the kit should take**
- **Study protocol:** the trial-log schema (`commit, metric, cost, status, description`) maps directly onto our `TRIAL_LOG.tsv`. Add a `keep|discard|crash` status column and the commit SHA per trial.
- **Study protocol:** "one commit per trial, reset on discard" is the cheapest possible provenance. Every logged number points to exact code.
- **Study protocol:** a fixed compute budget per trial makes trials comparable, plus a hard kill at 2x the budget.
- **Roles/prompts:** the "redirect output to a file, grep one line" rule keeps long unattended loops inside the context window.
- **Benchmark:** use it as a known-answer task family. Have the kit tune a tiny model on a fixed budget, then grade by an independent re-run of the winning commit.

**What to avoid**
- An evaluator the agent can reach (the literature and #599 agree). In the kit, the metric must be computed by a process outside the agent's writable tree, then re-run by the evaluator.
- "Never stop" with no budget or stop rule. Our PREREG needs a trial budget and an abandonment rule.
- Selecting and reporting on the same split. The kit keeps one held-out look.

**Evidence level.** No measured results ship in the repo, except `progress.png` (an unlabeled image). "~12 experiments/hour, ~100 overnight" is arithmetic from the 5-minute budget, not a measurement. The exploits in #599 come with a public reproducer gist (UNVERIFIED by us).

### OpenResearch (`alphaXiv/OpenResearch` @ 48f42c4)

**What it is.** A local-first desktop app plus CLI (`orx`, written in Rust) that turns Claude Code, Codex, OpenCode, Cursor or Antigravity into research agents. Each idea becomes a committed experiment node, run on local or cloud compute, with results stored in a local SQLite database. **License:** MIT (`LICENSE`, "Copyright (c) 2026 alphaXiv"). Copying allowed? **Yes**, keeping the notice.

**Process: how the work is organised**
- One chat runs one agent in its own git worktree. orx injects a playbook (`SYSTEM_PROMPT.md`), through `--append-system-prompt-file` for Claude Code, and installs native skills from `agent-skills/` (`SYSTEM_PROMPT.md`, header comment).
- Sub-agents: orx's own MCP server (`delegate`, `wait`, `subscribe`, `send`) replaces the harness's sub-agent tools. A delegate's permission mode is "no broader than its delegator's" (`arc/agents.md:289`, issue #885).
- **The experiment tree is the protocol** (`SKILL.md`, "Cardinal rules"; `agent-skills/orx-experiment-tree/SKILL.md`):
  1. A node is frozen once a run answers it, and a "disappointing result is still a result".
  2. The run command and environment are a fixed contract, identical on every node.
  3. Vary code, not command-line knobs.
  4. Grow "stacked bushes": a small fan of options per round, then descend onto the winner.
- **What counts as worked:** each finished run is a decision point with four moves: repair, refill, promote or stop. **Stop rules:** "Stop when the goal is met, or after ~3 consecutive failed or regressed runs". The repair cap is "two runs in a row that answer nothing on one node, then ask the user" (`orx-experiment-tree/SKILL.md`).
- **Who measures:** a run is an immutable snapshot. The commit is archived by SHA-256, and the backend never sees uncommitted edits (`arc/experiments.md`, "A run is an immutable snapshot"). Stop rules such as `nonFinite` and `worseThanParent` are declared in config and stop a run without the agent (`orx-experiment-runs/SKILL.md` §9). A cheap watcher model reads only a digest, "never the chat, the repository or the whole log" (§10). Logs from frozen harness code are parsed with patterns the agent can't edit (§6).
- **Reporting:** "Never infer a result from run status or memory" (`orx-results/SKILL.md`). Every claimed number carries a `<run id>` tag, and the run log must be read first (`SYSTEM_PROMPT.md`, "Evidence and links in chat").
- **Unattended:** orx exposes each harness's own permission modes. Plan mode has an allow-list gate (`src/local/harness/plan_gate.rs`). Bypass as root requires `IS_SANDBOX=1` plus a one-time user confirmation (`arc/agents.md:258`). Every run is priced at launch and spend is tracked (`arc/experiments.md`, "The price of a run").

**Lessons learned**
- "Unknown is not absent": failing to read or parse something must be reported as that, never treated as empty or stopped (`AGENTS.md`, Errors).
- "Claim only what you saw … say what you didn't check" (`AGENTS.md`, Doing the task).
- Issue #885 "rework entirely how subagents work": native sub-agents could not cross models or report back, so all delegation moved to one MCP server that wakes the delegator with the answer.
- The "flat fan" and "noodle" failure shapes (`orx-experiment-tree/SKILL.md`) are lessons distilled from agents driving the tree badly. In a flat fan, every result is measured against the start and wins never stack up.
- Recurring issues are infrastructure: SSH reuse and zombie cancels (#741, #462, #652), and an agent outrunning its backend after an update (#549).

**What the kit should take**
- **Study protocol:** the four cardinal rules, nearly verbatim, in `/autonomous:new-study`: freeze an answered trial; keep one fixed run command; vary only committed code; branch a child instead of editing. Copy the text of `SKILL.md` lines 121-151 (MIT).
- **Study protocol:** the stop rules "~3 consecutive failed/regressed runs" and "repair cap 2". These are concrete abandonment rules to put in PREREG.md.
- **QA gate:** declared, machine-run stop rules (NaN, worse than the parent at the same step), plus a watcher that sees only a digest. Both checks sit outside the builder's reach.
- **Roles/prompts:** "a claim cites a run id and the log was read" as a reporting rule for RESULT.md.
- **Launcher:** the Claude Code injection route, `--append-system-prompt-file` plus skills in the worktree, matches our `claude -p` launcher.

**What to avoid**
- The watcher and flags never block a result. They only wake the agent, who settles flags with `--keep` (`orx-experiment-runs/SKILL.md` §10). The builder still judges its own run. Our kit needs an independent re-run.
- Release builds send opt-out analytics and "detailed agent feedback in the background" (README.md, "Usage analytics"). Don't ship agent-written telemetry.
- Repo text addressed to agents was ignored as instructions: `AGENTS.md:100-102` tells agents "you MUST NOT add `Co-authored-by`" and to follow Linear "without asking".

**Evidence level.** No accuracy or benchmark numbers in the repo. The claims are product claims (GitHub Trending badge). The process rules are design, not measured effects.

### scientific-agent-skills (`K-Dense-AI/scientific-agent-skills` @ ec59a29)

**What it is.** A library of 177 Agent Skills (`skills/<name>/SKILL.md`) for science packages, databases and research methods. It is also a portable Agent Plugins package (`plugin.json`, version 2.72.0). **License:** MIT at the repo level (`LICENSE.md`, "Copyright (c) 2025 K-Dense Inc."). **Per-skill licenses differ** in frontmatter: CC BY-NC-SA, PolyForm-Noncommercial, GPL and "Unknown" appear in `bioservices`, `cobrapy`, `deepspot-m`, `etetoolkit`, `glycoengineering`, `phylogenetics`, `primekg`, `rowan` and `what-if-oracle`. Copying allowed? **With conditions:** check each skill's `license:` field. The method skills we care about (`experimental-design`, `statistical-power`, `statistical-analysis`, `scientific-critical-thinking`, `hypothesis-generation`) say MIT.

**Process: how the work is organised**
- No agents or runtime; it is content. Scope rules (`AGENTS.md`, "What belongs here"): one narrow skill per package or method. "Broad 'orchestrator' skills that route to other skills" and general coding skills are declined because "they compete for selection on every task".
- **Gates:** `tests/_meta` checks the manifest schema, version sync, personal paths and structure (`CONTRIBUTING.md`). A skill with `scripts/` must have tests in `tests/<skill>/`, never inside the skill (`AGENTS.md`, Layout). An LLM security scan runs on every skill, with a cache keyed on content (`scan_skills.py` header; workflows in `.github/workflows/security-scan.yml` and `pr-skill-scan.yml`).
- **Authoring rule:** "Run the commands and code you document. Scope claims to the release you actually tested … mark anything untested as illustrative" (`AGENTS.md`, step 4). Bump `metadata.version` on every change.
- The research-method content is strong. `hypothesis-generation` keeps observation, hypothesis, prediction, evidence and analysis plan distinct, "Freeze the observation" before interpreting, and never "fabricate sources … results, approvals, or preregistration" (`skills/hypothesis-generation/SKILL.md`). It ships deterministic local checkers: `generate_preregistration_scaffold.py`, `check_falsification_controls.py`, `lint_causal_claims.py` and `audit_evidence_ledger.py`, plus `assets/preregistration_scaffold_template.md`.

**Lessons learned**
- Issue #152 "Infographics skill auto-reviewer is broken": a wrong model ID made every review call fail. A broad `except` returned a hard-coded score of 7.5 and "review skipped", so the quality gate silently stopped working. This is the same failure class as AI-Scientist-v2 #133.
- Issue #260 "Fix dead endpoints, broken install commands and stale compatibility floors across 14 skills": running every documented URL and example found 43 dead URLs and 7 functional defects. Prose skills rot unless they are executed.
- Issue #250 "statsmodels skill: fix invalid causal inference example": an example imported a module that does not exist and mislabeled a method. Documentation written from memory gets things wrong.
- Issue #9 "Consider including license information in the skill details": led to the per-skill `license:` field.
- Issue #368: several skill cross-references were removed between v2.65.0 and v2.72.0. Description overlap hurts skill selection.

**What the kit should take**
- **Study protocol:** adapt (MIT) `hypothesis-generation/assets/preregistration_scaffold_template.md` and its scripts `check_falsification_controls.py` and `lint_causal_claims.py` as deterministic PREREG/RESULT checkers for `/autonomous:new-study`.
- **Study protocol:** the bias and multiple-comparison checklists in `scientific-critical-thinking/references/common_biases.md` and `statistical-analysis/references/reporting_standards.md` can feed our RESULT.md bias checklist.
- **Plugin conventions:** skill tests live outside the skill folder; a meta-test checks manifest and version sync; a personal-path test (`tests/_meta/test_personal_paths.py`). This mirrors our public-repo privacy rule.
- **Benchmark:** "scope claims to the tested release; mark untested as illustrative" as a rule for every kit skill.

**What to avoid**
- A fallback score when the reviewer fails (#152). A failed check must fail or be recorded as missing, never scored.
- Pulling in the whole library: 177 skills compete for selection. Copy the 3-5 method skills we need.
- Copying a non-MIT skill into our MIT plugin.

**Evidence level.** "Significantly stronger and more reliable" (README.md) is not measured in the repo. A paper exists (arXiv:2609.00065, not read here). The tests cover bundled scripts, not whether agents do better science.

### AutoResearchClaw (`aiming-lab/AutoResearchClaw` @ be4ba47)

**What it is.** A 23-stage, 8-phase Python pipeline that goes from a topic to a LaTeX paper. Stages: literature, hypothesis debate, code generation, sandbox experiments, PROCEED/REFINE/PIVOT decision, writing, peer review, citation check. It runs fully automatic or in "co-pilot" mode. **License:** MIT (`LICENSE`, "Copyright (c) 2026 Aiming Lab"). Copying allowed? **Yes**, keeping the notice. Vendored agents in `external/agents/` (ColliderAgent, Biology-Agent, stat_research_agent) carry no LICENSE files, so do not copy those.

**Process: how the work is organised**
- A state machine: `researchclaw/pipeline/stages.py`, `contracts.py` (required/produced keys per stage), `executor.py` and `runner.py` (`RESEARCHCLAW_CLAUDE.md`). Gates at stages 5, 9 and 20 pause for a human or are skipped with `--auto-approve` (README.md, "Pipeline").
- **What counts as worked:** stage 15 decides PROCEED, REFINE (back to 13) or PIVOT (back to 8), with versioned artifacts (README.md). Up to 10 refine rounds (README.md, "Key Features").
- **Anti-fabrication:**
  - `pipeline/verified_registry.py` builds a whitelist of numbers from `experiment_summary.json`, and `paper_verifier.py` rejects paper numbers not on it.
  - An "immutable" harness, `experiment/harness_template.py` ("inspired by karpathy/autoresearch's immutable prepare.py"), is injected into the sandbox, and a project's own copy is skipped (`experiment/sandbox.py:384-393`).
  - Citations are checked in 4 layers: arXiv, CrossRef/DataCite, Semantic Scholar, then an LLM.
- **Independent reviewer** (#316): the author model used to review its own paper and judge its own quality gate. Now an opt-in `llm.reviewer_model` "never falls back to the author model", and `review_provenance.json` records author versus judge. It is off by default.
- **Unattended:** `sentinel.sh` restarts on a stale heartbeat (>5 min, max 5 retries). Cost guardrails pause at 50%, 80% and 100% of budget. Claude Code runs as a sub-agent with `--dangerously-skip-permissions` by default (`researchclaw/config.py:364,411,446`). A Claude Code skill launches the pipeline (`.claude/skills/researchclaw/SKILL.md`).

**Lessons learned** (mainly their own audit, `docs/CODE_REVIEW_2026-07-03.md`, in Chinese)
- Headline: "multiple anti-fabrication / anti-hallucination defenses switch themselves off or are bypassed exactly when they are most needed … 'configured but not effective' or 'failed but reported as success'." The suite was "2831 passed" and green, and "all issues below are in test blind spots".
- P0 examples:
  - A fake citation with a double-quoted BibTeX title skips verification (`literature/verify.py:128`).
  - An escaped `\%` hides numbers from the paper verifier (`paper_verifier.py:63`).
  - A failure in the human-approval callback silently auto-approves after 60 seconds (`hitl/session.py:199`).
  - The default sandbox runs LLM code on the host.
- P1 examples:
  - With the network down, every citation is SKIPPED and the integrity score comes out as **1.0** (`verify.py:97`).
  - When code generation fails, synthetic noise is created under real metric names (`_code_generation.py:776`).
  - "Best" refinement is hard-coded to maximize, so loss tasks pick the worst run (`_paper_writing.py:241`).
  - An unapproved quality gate is skipped in the iterative runner (`runner.py:845`).
- Issue #301: the experiment-spec validation hooks imported a module that does not exist and were wrapped in `except: debug`, so "spec compliance has effectively been dead code". The fix added `PreregisteredPrediction` (statement, metric, baseline, minimum effect size) and `seeds` to the plan schema.
- PR #302 "Fail-open audit" (closed without merging, checked 2026-11-21; a narrower PR #323 is open): it proposed that every catch-all on the experiment path be assigned "converted-surface" or "converted-record" (one WARNING plus a `degradations` entry in `pipeline_summary.json`).
- Issue #316: self-review "rarely produces the kind of objection that would actually block a run".

**What the kit should take**
- **QA gate:** the rule #302 proposed (not merged upstream). Every caught exception either fails the stage or writes a `degradations[]` entry to the run summary. "Skipped" must never count toward a score (`verify.py:97`).
- **Study protocol:** a `VerifiedRegistry`-style check for RESULT.md. Every number in the report must trace to a saved output file. This feeds our "every number generated from saved outputs" rule.
- **Study protocol:** the #301 `PreregisteredPrediction` fields as a machine-readable block in PREREG.md.
- **Roles/prompts:** `review_provenance.json` (author model versus judge model) as the evaluator's independence receipt.
- **Benchmark:** ARC-Bench (`experiments/arc_bench/`, 55 topics with manifests and rubrics) as a candidate source of study tasks (check per-topic licenses first).

**What to avoid**
- A 23-stage design with dead and half-built modules (audit: `mcp/` is a stub, half of `hitl/` is fed only by tests, the `stages.py` transition map is unused). Fewer moving parts.
- An "immutable" harness that the agent's code merely *calls*. The code can skip it or feed it fake values, just as in autoresearch #599.
- `--dangerously-skip-permissions` as a default. Our permission hook must be scoped.

**Evidence level.** The "2699 Tests Passed" badge meant little, as their own audit showed. MetaClaw "+18.3% robustness" is a composite of retry and refine counts, "same topic, same LLM", with n not stated (README.md). The ARC-Bench scores are local-only (`experiments/arc_bench/README.md`: results and analysis are gitignored). All UNVERIFIED.

### AI-Scientist-v3 (`SakanaAI/AI-Scientist-v3` @ f8ae47d)

**What it is.** "The Agentic Scientist": a pipeline that drives coding-agent CLIs (claude, codex, cursor, opencode, gemini, pi) through Headless CLI. It goes from a `task.md` plus an evaluator, through search, ablations, a **sealed final evaluation** and post-hoc analysis, to a paper. **License:** Apache-2.0 (`LICENSE`; `pyproject.toml:11`). Copying allowed? **Yes**, with the Apache notice and a statement of changes.

**Process: how the work is organised**
- Six default phases, all under one run directory: task_drafting → investigation → ablations → final_evaluation → posthoc → paper, plus optional review and revision (`docs/pipeline.md`). The task is copied into an immutable run-local snapshot (`<run_dir>/task`, `docs/pipeline.md`, "Run layout").
- **Who measures:** the evaluator, never the candidate. Candidates return inline JSON through a broker. They "cannot write into evaluator output directories". The evaluator "must compute score/correctness and measure duration itself". Candidate diagnostics stay explicitly "**unverified**" (`docs/evaluation_evidence.md`).
- **Held-out:** the task contract requires `search_seeds` and `final_seeds` and raises "protocol search and final seeds must be disjoint" (`src/investigation/task_contract.py:628`; also linted in `task_contract_lint.py:455`). Feedback is split into `search_visible` and `final_sealed`, and overlap is an error (`task_contract.py:630-638`).
- **What counts as worked:** promotion needs `correct=true` plus a finite score, ranked by score, then by attempt order (`docs/no_winner_studies.md`). Rubrics mix implementation checks with metric checks (`examples/circpack/rubrics_example.json`, e.g. `score_exceeds_2_1`).
- **Negative results are first-class:** `completed_no_winner` and a verified `not_qualified` final may still produce a paper that "must report the qualification failure". Missing, failed or unverifiable finals block publication (`docs/paper_final_outcomes.md`).
- **Evidence sealing:** final manifest schema 3 seals `results_tree_sha256` and host-measured `compute_usage`. "Missing broker measurements are `null`, never fabricated zeroes" (`docs/evaluation_evidence.md`). Cost goes to `metrics/cost_events.jsonl`, with provider charges kept apart from list-price estimates (`docs/pipeline.md`).
- **Unattended:** agents run with "full tool permissions (Headless `--allow yolo`)", so the README says to keep runs in Docker (README.md, Security note). Budgets: `max_idea_cycles` (3 by default, 20 in `preset=paper`) and 5 ablation replications. `skills/run-campaign/SKILL.md` asks once for consent on agent, environment, budget and launch, then monitors.

**Lessons learned**
- Issue #5 "Repair agent can make the evaluator non-deterministic, and nothing detects it": a repair seeded the evaluator from `secrets.token_bytes(32)` on every call. Two scores of the *same* program differed by ~0.2, more than the real gains (~0.15), so "the improvement-over-baseline check was effectively a coin flip". The fix (#9): "Determinism was only requested in prompts and judged by reading code". Smoke now runs the unchanged baseline twice and fails on any mismatch beyond float noise (`src/investigation/evaluator_replay.py`).
- Compared with v2: in v2 the VLM figure-review step was rejected by a whitelist check in every run (AI-Scientist-v2 #133, "F11 VLM whitelist rejection", 24/24 write-ups). In v3 an optional phase that fails "is reported as degraded" and "does not discard a publishable paper" (`docs/pipeline.md`; README.md). Failures are now recorded rather than silent, but the external review is still non-gating.
- Fail closed on a partial state: "a partially copied tree is never a valid selection", and a resume "will not silently repair changed evidence or choose another program after final evaluation" (`docs/no_winner_studies.md`).
- "Drafted tasks create their own task harness. This measures full-run variation, but generated evaluators can differ between model rows" (`docs/pipeline.md`). An evaluator written by the agent weakens comparisons across models.

**What the kit should take**
- **Study protocol (top pick):** disjoint `search_seeds`/`final_seeds` plus `search_visible`/`final_sealed` declared in PREREG.md and checked by a script before any run. This is our "one held-out look", enforced by code.
- **Study protocol:** the evaluator replay smoke. Score the unchanged baseline twice before the study starts and abort on mismatch. Cheap, and it catches a whole class of bugs.
- **QA/evaluator gate:** the evaluator owns measurement (score, correctness, duration). Builder-reported numbers are labeled unverified. Missing measurements are `null`, never zero.
- **Study protocol:** a "no winner" or "not qualified" outcome gets a written-up result, like our kill/park verdicts in RESULT.md.
- **Launcher/benchmark:** `cost_events.jsonl` keeping provider charges apart from estimates, plus `--dry-run` that prints every phase command.

**What to avoid**
- Letting the agent draft its own evaluator for a benchmark row. Our benchmark tasks ship fixed graders.
- `--allow yolo` outside a container. Our hook is scoped instead.
- A non-gating external review that is easy to skip. If the kit's evaluator fails, the run is not graded, and it never passes by default.

**Evidence level.** The README points to a paper (arXiv:2610.18933, not read here) and gives no result numbers. The issue #5 numbers (0.2 spread versus 0.15 gains) come from one user report. The fix is backed by tests named in #9. UNVERIFIED by us.

### EvoScientist (`EvoScientist/EvoScientist` @ 3b6ce26)

**What it is.** A LangChain DeepAgents-based "self-evolving AI scientist" with its own CLI, TUI, WebUI and chat channels. It has 6 sub-agents (planner, research, code, debug, data-analysis, writing), persistent memory, and "AutoSkills" distilled from memory. **License:** Apache-2.0 (`LICENSE`; `pyproject.toml:7`). Copying allowed? **Yes**, with the Apache notice.

**Process: how the work is organised**
- Sub-agents are YAML definitions (`EvoScientist/subagents/*.yaml`, e.g. `debug.yaml`: "Reproduce failures … Provide how to reproduce and how to verify the fix"). The workflow prompt runs intake → plan → execute → evaluate → write → verify (`EvoScientist/prompts.py`, `EXPERIMENT_WORKFLOW`).
- **What counts as worked:** stages carry soft "success signals (flexible, not rigid)". "Iterate until a critical reviewer would accept the results — not for a fixed number of rounds" (`prompts.py:363`). Run logging is "Optionally log runs to `experiment_log.md`" (`prompts.py:128`).
- **Acceptance grading:** `--rubric` / `/rubric` / `/goal` (`docs/guides/rubric.md`; `middleware/rubric.py`). When the agent stops, a separate grader checks a written checklist, up to 3 passes, then exit code 3. The grader gets only `ls` and `read_file`. "It cannot run commands, so a criterion such as 'the tests pass' is judged from what the conversation shows". It "uses the auxiliary model when one is configured, otherwise the main model".
- **Unattended:** `auto_mode` implies `auto_approve` and turns off `ask_user`. `dangerous_mode` removes workspace confinement. `shell_allow_list` sets prefixes to auto-approve, and a privileged-command blocklist still applies (`EvoScientist/config/settings.py:541-553`). Scheduled cron tasks can carry a `--rubric` (README.md, `/schedule add … --rubric`).

**Lessons learned**
- Issue #229: "PR #202 introduced regression by auto approving all sub-agent's tool calls". The fix restored confirmation and added heuristics that refuse to auto-approve dangerous commands.
- Issue #841 "check variable cd targets and rm after a cd": "following variables and folder changes through every shell construct does not converge: each new rule opened new gaps … A static check of the command text cannot close them all … making the protected folders read-only to the agent's shell would."
- Issue #708: the sandbox rewrote `/` everywhere in commands with regexes. That broke data (`print(6 / 3)` became `print(6 . 3)`) and silently wrote corrupted files that "exited 0".
- `docs/guides/rubric.md`, Limits: a run stopping early to wait for background jobs burns grader passes; a sub-agent status that can't be read "never holds a grading back". Grading can run before the work has finished.

**What the kit should take**
- **QA gate:** a rubric file plus a separate grader plus a pass limit plus a distinct exit code (`0` satisfied, `3` not satisfied, `1` failed). This is a clean contract for a `claude -p` Tester or Evaluator role that the launcher can read.
- **Permissions hook:** the #841 conclusion is direct design input. Don't try to make a command-text allow-list complete. Pair a short allow-list with real filesystem confinement (read-only protected folders or worktree-only writes).
- **Roles/prompts:** the debug sub-agent's output contract (root cause, fix summary, repro, verification steps) for our builder's bug reports.

**What to avoid**
- A grader that can't run commands and judges "tests pass" from the transcript. The literature says LLM verifiers approve work that real tests reject. Our evaluator executes.
- A grader that can default to the main model, so builder and judge are the same.
- "Iterate until a reviewer would accept, not a fixed number of rounds" with optional logging. That invites forking paths and untracked trials. Our PREREG fixes the trial budget, and every trial is logged.
- Blanket auto-approve for sub-agents (#202 regression).

**Evidence level.** The README claims "#1 on DeepResearch Bench II", "#1 on AstaBench" and "6/6 accepted at ICAIS 2025 … Best Paper" (README.md, News). These are leaderboard and venue claims at submission time, with a technical report (arXiv:2603.08127, not read here). None are reproduced in the repo. UNVERIFIED.

## F. Automated development: loops, harnesses and agent companies (sweep 2)

### uditgoenka-autoresearch (`uditgoenka/autoresearch` @ 7bddd05)

**What it is.** A Claude Code skill and plugin (v2.3.0) that turns Karpathy's autoresearch loop into general commands:
change one thing, run a metric command, keep the commit if the number improved, revert it if not. It also adds 13 helper
commands (debug, fix, security, ship, and others) and an "orchestrator" that routes a plain-language goal among them.
**License:** MIT (`LICENSE`). Copying allowed? yes, keep the notice.

**Process: how the work is organised**
- One agent, no team. The classic loop (`.claude/commands/autoresearch.md`) runs Review (last TSV rows plus `git log` as
  memory), Modify (one atomic change), Commit (`experiment:` prefix), Verify (a shell command that prints a number),
  Guard (an optional command such as `npm test` that must pass), then Decide: keep, or `git revert HEAD --no-edit` on
  discard, crash, or a metric that isn't a number. Every iteration is one row in
  `autoresearch/<cmd>-<date>/…-results.tsv`.
- Commands hand off to each other through `handoff.json` (`.claude/skills/autoresearch/SKILL.md`, "Chain"). The
  orchestrator keeps its own `orchestrator-state.json` and all routing logic lives in a script, not in the prompt
  (`scripts/orchestrate.sh`: `classify`, `next-hop`, `plateau`, `screen-cmd`, `validate-state`).
- "Done" is a **Success predicate**: an exact shell command plus its expected output, confirmed once with the user, then
  pinned verbatim in the state file so every cycle and every resume uses the same string (`SKILL.md`, "Predicate pinned,
  not re-derived"; `CONTEXT.md`).
- Stop conditions are written down: a cycle ceiling (default 50, `--max-cycles`); a plateau (goal distance flat for 5
  computed cycles, triggering at most 2 fork rounds, then stop); BLOCKED; bounded iteration defaults per command (25 for
  the loop). Cycles where progress couldn't be measured don't count as zero progress (`SKILL.md`, "Orchestrator Safety
  Invariants").
- Getting unstuck ("fork-and-flush", `references/fork-and-flush.md`): at 33% and 66% of the budget, or after 5
  iterations with no keep, it starts K fresh-context branches from the best commit. Each branch sees only the files and
  the results log, none of the leader's chat. The best branch wins.
- Unattended safety: hooks in `.claude/hooks/autoresearch/hooks.json` (block dangerous commands, block private files, a
  scout-block, a session-end notify). Push, deploy and publish always need a human ("Never auto-approve
  ship/deploy/push"). Commands read back from a saved state file are re-screened on resume, because "persisted commands
  are never trusted".
- Their own repo gates releases with a "preprgate" phase checklist in CI (`.github/preprgate/hard-phases.json`, phases
  0–11 need PASS/SKIP) and bash tests of the deterministic parts (`tests/test-orchestrator.sh`, `tests/test-hooks.sh`).

**Lessons learned**
- **Hooks fail open, and silently on Windows.** `/dev/stdin` doesn't exist in native Windows Node, so every hook read
  nothing and exited 0. The guardrails "appear installed and simply never fire" (issue #115, "Hooks are silently no-ops
  on Windows"). The hook code says so by design: "Fails open on any error" (`dangerous-cmd-block.cjs`, header).
- **Global hooks leak into unrelated sessions.** scout-block blocked `node_modules/.bin/biome` 7 times and `*.log` reads
  in ordinary sessions, which pushed agents into "29-minute blind `sleep` timers" (issue #123). dangerous-cmd-block also
  ran everywhere and blocked `--force-with-lease` (issue #125). The fix is to gate a hook on run state
  (`run-marker.cjs`, `loadSessionState`).
- "Git is memory" didn't work well for a user (issue #29). `/loop 5 /autoresearch` was read as "every 5 minutes", not "5
  iterations" (issue #24), so the iteration count must be an explicit, unambiguous field.
- Token cost forced a split: the 813-line SKILL.md (~100K tokens per call) became a thin router plus 12 command files
  (~5–8K each) (`README.md`, v2.1.0 note).
- A single loop gets stuck in one "idea basin", and compaction doesn't fix it; fresh-context forks do
  (`references/fork-and-flush.md`, "Why"). The numbers come from a cited paper, not from this repo.

**What the kit should take**
- **Pinned success predicate** (command plus expected output, written into the state file at round 0 and re-used on
  resume) → the definition of done for the builder and Main in `/autonomous:new-app` and `new-study`.
- **The keep/revert TSV schema** (`iteration, timestamp, commit, metric, delta, guard, status, description`, with metric
  direction on line 1) → the TRIAL_LOG for `new-study` and per-PR attempt logs for the builder.
- **Deterministic routing seam:** stop/plateau/next-hop logic lives in a tested script, not in the prompt
  (`scripts/orchestrate.sh` + `tests/test-orchestrator.sh`) → the launcher's stop and plateau rules.
- **Re-screen persisted commands on resume** → the PermissionRequest hook should never trust a command just because it
  came from the registry or a handoff file.
- **Flush (fresh context from files only) as the plateau move** → when a builder session stalls, the launcher restarts
  it from the handoff files rather than resuming the bloated session.

**What to avoid**
- Fail-open hooks. Our permission hook must fail **closed** and must be tested on Windows (our machine), or the run is
  unprotected without anyone knowing (#115).
- Hooks registered globally. Scope every kit hook to the run folder and active-run marker (#123, #125).
- **The builder can edit its own check.** The Verify and Guard commands are user-supplied, but nothing stops the loop
  editing the files they run when those files sit inside `Scope:`. The "independent verify hop" before DONE is an LLM
  persona debate (`references/orchestrator-routing.md`, routed to `reason`/`predict`), which the literature says
  approves work that real tests reject. The kit's QA/Tester checks must live outside the builder's write scope.
- The persona-debate commands (predict: 5 experts; probe: 8 personas; reason: blind judges) are role-play, not tests.
  Don't import them as gates.

**Evidence level.** Low for its own claims. The fork-and-flush table (0.47 → 0.78 normalized score) is quoted from cited
papers (arXiv:2610.07447, 2610.07625), not measured here. The "95% token reduction" counts prompt size, not task
results. No benchmark of the loop's success rate exists in the repo. Measured facts are the bug reports (#115, #123).
UNVERIFIED until re-run.

### darwin-skill (`alchaincyf/darwin-skill` @ 5a8e633)

**What it is.** A skill (v3.0.2) that evolves other skills with an autoresearch-style ratchet: evaluate, propose one
edit, test it with real runs, keep or `git revert`, and get a human check after each skill. Docs are in Chinese, with an
English README (`README_EN.md`). The quotes below are translated. **License:** MIT (`LICENSE`). Copying allowed? yes,
keep the notice.

**Process: how the work is organised**
- Roles are separate subagents: **executors** do real tasks with the old skill, the new skill, or no skill ("bare").
  **Judges** blind-compare pairs of outputs. A script, not the main agent, counts votes and gives the verdict
  (`README_EN.md`, "Five Core Principles" #4; `scripts/darwin.py tally`).
- Isolation is designed into the folders (`references/eval-protocol.md`, "Working directory layout"). Each executor gets
  a **snapshot** of the skill (`W/s0`, `W/s1`…), never the live skill folder, because "there are test files there and
  the executor will read the checks". Tests, checks and answers are never put in a snapshot or an output folder. A/B
  keys sit in `W/keys/`, which judges can't see.
- Executor prompt rules (eval-protocol.md, "Executor prompt"): don't say "this is a test", don't mention darwin or the
  other arm. Include "nobody can answer your questions; write your assumptions down and finish". Don't read or list any
  folder except the skill, inputs and your output folder. Don't spawn subagents. Write `answer.md` plus `transcript.md`.
- Verdict rules (`README_EN.md`, "How the Ratchet Decides"): keep if more wins than losses and no check regressed. On a
  tie, keep only if the new version is **shorter**. Otherwise revert. A one-test margin with split judges triggers one
  rerun of both versions.
- Gates: tests split into dev and held-out halves. Edits are driven only by dev, and held-out is run once at the end
  (original vs final). If held-out is net negative, recommend rollback. Three human checkpoints: confirm tests, confirm
  baseline, review the diff after each skill (`SKILL.md` lines ~222–227).
- Limits (`SKILL.md`): at most 3 rounds per skill, one hypothesis per round. Stop after 2 reverts in a row. Body ≤500
  lines, and any round that grows the body >10% needs a failing check as evidence. An agent-count formula sets the
  budget ("baseline 2D+2, each round D+3, acceptance 2H+5").
- Every claim carries an evidence level: E0 static check, E1 read, E2 real run, E3 real environment. Reports list
  "verified" and "not verified" separately (`README_EN.md`, item 7).

**Lessons learned**
- **Judging the document measured the wrong thing.** In 2.x, judges read before/after SKILL.md and voted. An edit
  approved 3–0 "cost 33 extra tool calls on a real device" (`README_EN.md`, "What's New in 3.0", citing their own
  2026-09 logs). A user saw the rubric score climb 62.9 → 85.3 over 5 rounds while the live-performance dimension
  "didn't move", until an end-to-end test exposed 5 real gaps (issue #18, "增加端到端评估" / add end-to-end evaluation).
- Their first 3.0 run exposed three holes in their own protocol (`README_EN.md`, "A Real Run"). Test files in the skill
  folder let executors **read the checks**. Paths and transcripts let judges tell which output was which. A skill with
  checkpoints **stops and waits for a user who isn't there**.
- "Six traps that flip the conclusion" (`references/eval-protocol.md`): control output visible to the tested agent (it
  copies it); a "bare" arm that isn't bare (built-in skills stand in); fixed A/B order (position bias); provenance clues
  left in outputs; and treating one run as final ("rerunning the same task changes results").
- **No wall-clock or agent-count cap.** One skill needed 39+ subagents and ran for 5+ hours. A hung judge was never
  re-dispatched, so the main agent "polled and waited" 55 minutes (issue #31). Token cost averaged ~1.3M tokens per
  skill evaluation, 89% of it cache reads (issue #25).
- Absolute scores swing about ±8 when the judge changes, so only paired win/loss decides (`SKILL.md`, pitfall 3). A
  hard-coded author path leaked in `scripts/screenshot.mjs` (issues #4, #19).

**What the kit should take**
- **Snapshot isolation for the Tester and QA**: the thing under test runs from a copy that holds no tests, checks or
  expected answers. The checks live where the builder can't read or write them → QA/Tester gates (directly answers "can
  the builder edit its own checks?").
- **The "nobody can answer you; write assumptions and finish" line** → every unattended role prompt in
  `/autonomous:new-app`, so no session blocks on a question.
- **The scripted verdict** (`darwin.py tally`: random A/B order, scrubbing of paths and group names, fixed rules, facts
  before votes) → the benchmark grader and any LLM-judged comparison in `new-study`.
- **Dev/held-out split with one held-out look** → matches our study protocol; reuse its wording in the benchmark
  task-set README.
- **Tie goes to the shorter version; growth needs a failing check** → kit prompt and skill maintenance policy.
- **E0–E3 evidence levels with verified / not-verified lists** → the release card and the QA verdict format.
- **Its exception table** (`SKILL.md` ~line 299: rerun only the broken executor; re-dispatch late judges instead of
  waiting) → launcher retry rules.

**What to avoid**
- Running without a subagent and wall-clock budget (#31). The kit's launcher needs hard caps per phase plus a timeout
  and re-dispatch for any worker that goes quiet.
- LLM judges as the only gate. darwin itself demotes the rubric to "diagnosis only". For apps, the Tester's live walk
  and real tests must decide, with judges only for taste.
- Three human checkpoints per skill don't fit an unattended kit. Replace them with recorded decisions plus a morning
  review.

**Evidence level.** Medium-low. The real run is n=1 skill, 2 dev tasks, synthetic data, held-out not run, and they label
it "not verified" themselves (`README_EN.md`, "A Real Run"). The literature correlations (ρ ≈ −0.02) are quoted from
cited papers. The cost figures in #25 and #31 are users' measurements. All UNVERIFIED until re-run.

### planning-with-files (`OthmanAdi/planning-with-files` @ 6f453ee)

**What it is.** A skill and plugin (v3.29.0) that makes the agent keep three files on disk (`task_plan.md`,
`findings.md`, `progress.md`) and uses lifecycle hooks to re-inject the plan, so work survives `/clear`, compaction and
session death. It runs on many hosts (Claude Code, Codex, Cursor, Gemini, and others). **License:** MIT (`LICENSE`).
Copying allowed? yes, keep the notice.

**Process: how the work is organised**
- One agent with a file protocol (`skills/planning-with-files/SKILL.md`). Restore before creating. Phases are written as
  `### Phase N` with exactly one `**Status:** pending|in_progress|complete` line. The "2-Action Rule" says save findings
  after every 2 view or search operations. Log every error. Keep a single `## Next Step`.
- Multi-agent rule: "Assign one plan owner. The orchestrator owns `task_plan.md`… Workers report through their own
  ledgers or assigned files; they do not independently rewrite the shared planning files" (SKILL.md, Quick Start #4).
  Parallel tasks use `.planning/<id>/` with a pinned `PLAN_ID` or separate worktrees.
- Hooks (`hooks/hooks.json`): SessionStart on `startup|resume|clear|compact` restores context; UserPromptSubmit and
  PreToolUse re-inject the plan; PostToolUse nudges a progress update; PreCompact saves; Stop runs a completion check.
- Unattended "gated" mode (`docs/long-running-agent-tasks.md`, "Gated mode and the completion gate"): a Stop hook
  "judges the plan artifact on disk, not the conversation transcript, so a session cannot talk itself into being
  finished". It blocks a stop only when every condition holds: mode is gate, the plan is incomplete, `stop_hook_active`
  is false, the block count is under a cap (default 20, `PWF_GATE_CAP`), and the ledger has a new line since the last
  block. Any single failure lets the session stop.
- Machine record: append-only `.planning/<id>/ledger-<agent>.jsonl`. The model gets only a fixed-shape summary (ticks,
  phases done/total, current phase), with "no free text from disk", so prompt-cache prefixes stay stable (same doc).
- Tamper check: `attest-plan.sh` stores a SHA-256 of `task_plan.md`, and hooks refuse to inject a changed plan until it
  is re-attested (`docs/attestation-locking.md`).
- Their own testing: about 120 pytest files, one per mechanism and per host (`tests/`), plus a skill-creator eval and a
  7-arm competitive benchmark (`docs/evals.md`).

**Lessons learned**
- **Silent breakage on Windows behind a green suite.** 2 of 6 mechanisms did nothing on Windows: path sanitising only
  handled `/`, and missing `encoding=` meant cp1252 decode errors were swallowed. `tests/test_path_fix.py` "never
  imported or exercised the actual shipped script, so the test suite reported green the entire time" (`docs/evals.md`,
  Test 4). A hook containment check also failed under 8.3 short-name TEMP paths, with "zero output: no plan
  re-injection, no tamper warning" (same section).
- **Shared pointers cross-bind sessions in one folder.** A repo-global `.planning/.active_plan` let Session B overwrite
  Session A's pointer, so after compaction A loaded B's plan (issue #240, "named gated plans can cross-bind same-cwd
  Codex sessions after compaction"; also #146, "hooks can leak active plan context across sessions in the same cwd").
- **A Stop gate that forces continuation surprises users.** An incomplete plan is a normal state, so blocking the stop
  made the agent start unrequested phases (issue #178). This is why the gate now needs an explicit mode, a cap and stall
  detection.
- **The hook re-injects the plan on every call, which amplifies prompt injection.** Removing WebFetch/WebSearch from
  `allowed-tools` was the v2.21.0 fix (`docs/evals.md`, "Why We Did This").
- **"A checked box is a progress claim, not evidence of completed work"**. The attestation digest isn't a signature: "A
  process that can replace both `task_plan.md` and its attestation can make new content pass"
  (`docs/attestation-locking.md`, "Trust boundary").
- A skill may not trigger on its own: it engaged unprompted in 5 of 8 runs, while always-loaded rules engaged 8/8
  (`docs/evals.md`, Test 5, Result 2).

**What the kit should take**
- **The Stop-gate design** (judge the file on disk, cap the blocks, detect stalls from the ledger, any failed condition
  lets the session stop) → the launcher's "keep going" logic for Main and builder sessions under `claude -p`.
- **One owner per shared file; workers write their own ledger** → the team registry and handoff files (Main owns the
  plan; builder, QA and Tester each append to their own JSONL).
- **Fixed-shape, no-free-text status injection** → what the launcher feeds each resumed session, for cache stability and
  injection safety.
- **Per-session plan binding, never a repo-global pointer** → registry keys must be per run and per role (#240).
- **The "resume after kill at 50%" benchmark protocol** (`docs/evals.md`, Test 5, O6: kill mid-task, new session told
  only "Continue the work in this directory", count turns) → a benchmark task for kit reliability across context resets.
- **"Test the shipped script, not a copy of it"** → a rule for kit hook tests, run on Windows.

**What to avoid**
- Relying on a skill self-triggering. The kit's launcher should start roles explicitly, not hope the skill fires.
- Treating plan checkboxes or the attestation hash as proof of done. Done must come from QA and the Tester, outside the
  builder's write scope.
- Shared mutable pointers in one folder for parallel sessions.

**Evidence level.** Medium. The author ran a 77-run, 7-arm benchmark with task specs committed before runs and fixed
graders, and disclosed a grader bug and its fix (`docs/evals.md`, Test 5). But the raw runs "live in the benchmark
workspace, not tracked in this repo". All arms tied on correctness (77/77 green). The headline resume advantage (5.0 vs
8.3 turns, n=3) was measured on an older version, and they say not to read it as the current default. Test 1's 96.7% vs
6.7% measures whether the files were created, not task quality. UNVERIFIED until re-run.

### deer-flow (`bytedance/deer-flow` @ 8f1a6cd)

**What it is.** ByteDance's "super agent harness" (v2, a full rewrite): a LangGraph lead agent that hands work to
subagents, with sandboxes, memory, skills, a Gateway API, scheduled runs and a web UI. **License:** MIT (`LICENSE`).
Copying allowed? yes, keep the notice.

**Process: how the work is organised**
- A lead agent plus subagents, called through a `task` tool (`backend/packages/harness/deerflow/subagents/`,
  `agents/lead_agent/`). The tool blocks and polls in the backend, so the model makes one call instead of polling: "LLM
  makes only ONE tool call… Timeout protection (5 minutes max)" (`backend/docs/task_tool_improvements.md`).
- **Checking subagent results** (issue #4651, "[RFC] Deterministic tool receipts & layered subagent result
  verification"). Before this, the lead got "a free-text self-report… A subagent that ran off the rails but returns
  `completed` has its conclusions adopted wholesale". The fix has three layers, cheapest first. (1) **Tool receipts**:
  the runtime, not the model, stamps every tool call (`args_sha256`, `output_sha256`, status), and reports must cite
  receipt ids. (2) **Acceptance criteria checked in code** (`subagents/acceptance_checks.py`): `file:<path>
  exists|non-empty|json-valid`, and `tests_passed:<cmd>` must anchor to a specific recorded execution with a
  test-summary shape, "so a self-report can never silently pass an objectively checkable requirement". Anything
  undecidable is UNVERIFIED, never passed. (3) An optional one-shot small-model judge, off by default.
- **Unattended mode** (`backend/docs/RUN_INTERACTION_POLICY.md`): runs in `scheduled`, `webhook` or `autonomous` mode
  "must never wait for a synchronous human response". They make "minimal reversible assumptions, list material
  assumptions, or return a structured `BLOCKED` result naming the missing decision". Subagents always deny pending
  network requests. Public callers can't switch a run to unattended.
- **Permissions**: `GuardrailMiddleware` checks every tool call before it runs, against a pluggable provider (allowlist,
  OAP policy, custom). If the provider errors, it **fails closed** by default (`backend/docs/GUARDRAILS.md`,
  `fail_closed: true`). Over-long arguments are denied rather than truncated, because "a prefix could hide the dangerous
  half of a `write_file` payload".
- **Stop limits**: goals carry `max_continuations` and `max_no_progress_continuations` (`agents/goal_state.py`).
  `LoopDetectionMiddleware` hard-stops identical calls whose results show no progress
  (`backend/docs/LOOP_DETECTION.md`). Work items survive restarts with execution epochs and revision checks, and
  cancellation fences the whole subtree (`backend/docs/task-coordination-state.md`).

**Lessons learned**
- **Self-reports were trusted with no evidence.** The prompt told the lead to "verify against primary evidence", "but no
  primary evidence exists in a form the verifier can use" (#4651). The RFC notes that full-trajectory LLM judging "has
  been falsified on both cost and quality grounds".
- **Queue time ate the timeout.** A queued subagent's timeout clock started at delegation, so time waiting for a slot
  counted, and polls were spent while still PENDING (issue #8308, "Count a subagent's timeout… from admission, not from
  delegation").
- **State grows without limit.** Checkpoint storage kept growing from leftover base64 data, large tool results and
  missing retention (issue #4189). There was also a run-registry memory leak (PR #5070).
- Subagent internal messages leaked into the parent's stream as raw tool JSON (issue #4043). Concurrent sandbox calls
  raised `INVALID_CONCURRENT_GRAPH_UPDATE` (issue #3628). Agent guidance grew past their own 96 KiB limit for the
  subagents `AGENTS.md` chain (issue #5457).
- Hard-coded `/mnt/user-data` paths broke on Windows (issue #2185).

**What the kit should take**
- **The acceptance-criteria contract**: every handoff from Main to the builder carries machine-checkable criteria (files
  exist, tests pass on a recorded run). These are checked by code outside the builder, and anything not checkable is
  marked UNVERIFIED → QA gate and handoff file format.
- **The `RunInteractionPolicy` wording** (never wait for a human; make reversible assumptions and list them; return
  `BLOCKED` naming the missing decision) → the system prompt of every `claude -p` role.
- **Fail-closed tool authorization with deny-not-truncate** → the scoped PermissionRequest hook.
- **Count timeouts from admission, not from dispatch** → launcher heartbeats for queued roles.
- **Hard caps on continuations and on no-progress continuations** → launcher stop rules.

**What to avoid**
- Accepting a teammate's "done" message as evidence (#4651). QA must re-run, not read.
- An LLM judge on every result. Use deterministic checks first and a judge only for what's left.
- Unbounded checkpoint and log growth in long runs (#4189). Set a size budget for the registry and logs from day 1.
- The scale: a full web platform with auth, IM channels and Postgres is far more than a plugin needs. Take the
  contracts, not the server.

**Evidence level.** Engineering-grade: large test suites, RFCs with review, and a CHANGELOG of 16k lines. But the repo
has no task-success benchmark of the harness itself, and the README makes no measured success claims. The verification
layers are design plus unit tests, with no measured false-pass rate. UNVERIFIED until re-run.

### paperclip (`paperclipai/paperclip` @ 1b1861c)

**What it is.** A Node server and React UI that runs a "company" of agents (Claude Code, Codex, OpenClaw, HTTP bots):
org chart, issues as the unit of work, heartbeat wakeups, budgets, approvals, and audit logs. "If it can receive a
heartbeat, it's hired" (`README.md`). **License:** MIT (`LICENSE`). Copying allowed? yes, keep the notice.

**Process: how the work is organised**
- Agents don't run continuously. They **wake on heartbeats**: an assignment, a comment, or a timer (`README.md`,
  "Heartbeats"; `skills/paperclip-board/SKILL.md`: `"heartbeat": {"intervalSec": 300, "wakeOnDemand": true}`). Each wake
  follows a fixed procedure (`skills/paperclip/SKILL.md`, "The Heartbeat Procedure"): read the inbox, pick work
  (`in_progress`, then `in_review`, then `todo`), then **check out** the issue (`POST /api/issues/{id}/checkout`). If
  another agent holds it, the answer is `409`: "stop, pick a different task. **Never retry a 409.**"
- Every exit must leave a **waiting path**: `in_review` with a saved pending interaction, or `blocked` with first-class
  `blockedByIssueIds`. "A comment naming someone does not create that path" (same file). `done` means "verification is
  recorded, and no follow-up remains".
- **Review stages** (`server/src/services/issue-execution-policy.ts`): the reviewer is picked from the stage's
  participants **excluding the agent the work goes back to** (`exclude: returnAssignee`), so the builder isn't its own
  reviewer. After `DEFAULT_MAX_REVIEW_ROUNDS = 3` agent-requested change rounds, the review escalates to a human.
- **Task watchdog** (`doc/TASK-WATCHDOG.md`): an opt-in second agent wakes when a whole issue tree has come to rest. It
  checks the evidence for wrong stops ("declaring 'done' without proof, leaving an issue `in_review` with no real
  reviewer") and can reopen or reassign, but has a written list of disallowed actions (no approvals, budgets, secrets or
  config). Separate mechanisms handle a silent running process and stalled `in_progress` work.
- Budgets: per company, agent, project and issue, with warning thresholds and hard stops. But "Budget checks and
  threshold enforcement are best effort. Concurrent operations can start from the same observed balance"
  (`doc/PRODUCT.md`, "Budget control behavior").
- Agent lifecycle is a state machine (pending_approval → preparing → verifying → ready → pausing/paused → terminating),
  and "verifying" runs a real hello-probe of the harness before work is allowed (`doc/AGENT-LIFECYCLE.md`).
- Their own dev process: `pnpm verify` on affected tests, red-green TDD for bug fixes, and CI typecheck/test/build on
  the final revision as the definition of done (`AGENTS.md` §7, §10, §12). Agent-behaviour evals use promptfoo
  (`evals/README.md`).

**Lessons learned** (their most-discussed issues are almost all **silent stalls in handoff and recovery**)
- "Skipped handoff wake… is terminal: a reviewer handoff stalls silently with no run and no retry" (issue #13532).
  "Handoff wake parked as deferred… is never re-admitted" (#14537). "Resolved recovery no-replay holds silently deadlock
  issues (invisible, undebuggable, watchdog duplicates every 30s)" (#14600). "Task permanently unrecoverable:
  pre-dispatch cancellation…" (#13640).
- **Quota and limit failures strand agents**: "Provider-quota recovery never fires… agents strand indefinitely with no
  wake path" (issue #15461). Subscription logins expire after about 8 h because only the access token is stored
  (#14182).
- **Kill switches that don't finish**: pausing hangs forever in `pausing` when an old run has no process identity
  (issues #18147, #17718). The budget hard stop fired with observed spend 0 when runs finished at the same time, then
  agents stuck in `pausing` (#18106).
- **Reading success from output text misfires**: a regex marked successful runs as `claude_auth_required` because the
  agent's output contained "Unauthorized" (issue #5534).
- **Handoff payloads grow until spawn fails**: an unbounded continuation pushed the wake-payload environment variable
  past `MAX_ARG_STRLEN`, causing E2BIG on every local adapter (issue #13959).

**What the kit should take**
- **Checkout with a `409` and never retry** → the launcher registry: one owner per task, atomic claim, losers move on.
- **"Every exit leaves a waiting path"** (in_review with a pending question, or blocked on a named blocker) → the
  end-of-session rule for every `claude -p` role, so the launcher always knows who wakes next.
- **Reviewer ≠ return assignee, 3 review rounds then escalate** → the QA gate (builder can't approve itself; after 3
  bounces the issue goes to `SHARIF_ACTION_ITEMS.md`).
- **The task-watchdog idea**: when everything has stopped, one agent checks whether the stop is legitimate, with a
  written "disallowed" list → a cheap final check by Main before the run reports done.
- **The "verifying" hello-probe before a role is ready** → the launcher pings each role session before handing it work.
- **Determine success from exit codes and structured output, never by regex on agent prose** (#5534) → launcher result
  parsing.

**What to avoid**
- Building a control plane. Their biggest problems are the recovery machinery itself (#13532, #14537, #14600, #15461).
  Keep the kit's handoffs as plain files with a few states, and test the stuck cases explicitly.
- Unbounded handoff payloads in env vars or CLI args (#13959). Pass paths to files instead.
- Trusting the budget stop as exact. It is best effort by their own docs, so the kit should also cap `--max-budget-usd`
  per session.
- The `skills/complain/SKILL.md` instructs agents to "Submit proactively without permission". That content is aimed at
  their agents; I didn't act on it, and the kit shouldn't ship a skill that sends data without asking.

**Evidence level.** Engineering and ops evidence: real bug reports with reproductions, and recovery benchmarks of server
internals (`doc/benchmarks/`). There is no measurement that a "company" of agents beats a single agent, and the README's
claims are product claims. UNVERIFIED until re-run.

### ruflo (`ruvnet/ruflo` @ 87f612c)

**What it is.** A large "agent meta-harness" (formerly claude-flow, v3.80.0, 10,615 commits) for Claude Code and Codex:
an MCP server, hooks, 98 agent definitions, swarm and "hive-mind" coordination, vector memory, "self-learning" routing,
and many plugins. **License:** MIT (`LICENSE`). Copying allowed? yes, keep the notice.

**Process: how the work is organised**
- **The swarm keeps records; Claude Code does the work.** "Ruflo is the coordination ledger and policy decision point.
  Claude Code executes code, tests, commands, and file changes. A Ruflo coordination call records work; it does not
  perform the implementation" (`CLAUDE.md`, "Capability Brain"). Agents are Claude Code Task subagents spawned alongside
  MCP `swarm_init` calls (`CLAUDE.md`, "Swarm Orchestration").
- Recommended swarm: hierarchical, 6–8 agents, "raft consensus (leader maintains authoritative state)", "frequent
  checkpoints via post-task hooks", and "short task cycles with verification gates" (`CLAUDE.md`, "Anti-Drift Coding
  Swarm").
- Concurrency rules (`CLAUDE.md`, "Concurrent Automated Development"): "Never allow two writers in one worktree."
  Read-only agents may share a checkout. Only the integration owner edits manifests and lockfiles. "A lease or work
  claim coordinates ownership; it never grants authority." Bind tests and handoffs to an exact clean commit. Learning
  systems "cannot self-promote or expand tools, network, secrets, spend, concurrency, or release authority".
- Headless use: it documents `claude -p` with `--max-budget-usd`, `--allowedTools`, and `--dangerously-skip-permissions`
  "(sandboxed environments only)" (`CLAUDE.md`, "Headless Background Instances").
- Unattended loop: the `ruflo-autopilot` plugin runs on Claude's `/loop` + ScheduleWakeup with a **270 s heartbeat**,
  chosen to stay under the 5-minute prompt-cache lifetime, plus an `iterationCap` guard (default 1000)
  (`plugins/ruflo-autopilot/README.md`).
- A later "verifier" signs outcomes from separate acceptance, safety, replay and adversarial commands, and "Check
  programs are host-reviewed trusted code, not sandboxed arbitrary agent instructions"
  (`docs/validation/managed-loop-e2e.md`).

**Lessons learned** (measured vs asserted)
- **Their own audit found headline numbers fabricated** (`docs/reviews/intelligence-system-audit-2026-05-29.md`). "HNSW
  150x–12,500x" measured a **1.48×** peak. "Flash Attention 2.49–7.47×" was "**fabricated with `Math.random()` at
  runtime**" (`attention-coordinator.ts:972`). "75× embeddings" had no benchmark. The CLI "**silently inverts negative
  reward**", so training against a bad agent reinforces it. ONNX failure fell back silently to mock embeddings still
  labelled as the real model. Yet `CLAUDE.local.md` still states "HNSW (150x-12,500x), Flash Attention (2.49x-7.47x)".
- **The "multi-agent benchmark" is a mock**: `docs/benchmarks/multi-agent/multiagent-mock-…json` has `"backend": "mock"`
  and finished in 4 ms for 100 runs per task. "Intelligent routing (89% accuracy)" (`README.md`, `docs/USERGUIDE.md`)
  cites no measurement in the repo.
- **Users couldn't get it to do work**: "Still can't figure out how to get v3 to actually perform work"; "since it's an
  'mcp' I still only have 1 claude code 'agent' doing everything" (issue #958).
- **Ledgers grow until everything locks**: the policy receipt ledger re-read and re-hashed its full history on every
  tool call under a 5 s lock, until "all MCP tools hit policy-state-lock-timeout" (issue #3164). Cold `npx` startup hung
  over 60 s downloading a model on every start (#2286, #3154).
- The honest part is the GAIA L1 attempt (`docs/benchmarks/submission/`). It scored 34/53, but "n=1 only; n=3 mean
  pending". Their own baseline rerun moved 21 → 23 (`variance-analysis.md`), so several "+2" component wins are inside
  noise. They do test components in isolation and **rejected** ones that hurt (visit_webpage −3, CodeAgent −4).

**What the kit should take**
- **The concurrency rules, almost word for word**: one writer per worktree; only the integration owner touches
  lockfiles; a claim coordinates ownership but grants no authority; tests and handoffs are bound to an exact commit →
  roles/prompts and the launcher.
- **"Learning loops may propose, never self-promote or widen their own permissions"** → the kit's permission hook and
  any self-improvement study.
- **A 270 s heartbeat for wake loops** (under the cache lifetime) → launcher polling interval for long-lived roles.
- **Component isolation runs with keep/reject decisions logged** (`submission/metadata.md` table) → the benchmark's
  ablation format, with n≥3 per arm, which they didn't have.
- **The audit format**: graded by evidence, "confirmed / partial / unsubstantiated / fabricated" → the evaluator's
  scorecard style for third-party claims.

**What to avoid**
- Swarm machinery that only records coordination while one model does the work (#958; `CLAUDE.md`). The literature says
  role teams don't beat one strong agent at equal cost, and ruflo has no measurement showing otherwise.
- Docs that drift from measurements (`CLAUDE.local.md` vs the audit). Kit numbers come only from the scorecard.
- Silent fallbacks to mocks (embeddings) and append-only ledgers with full re-verification on every call (#3164).
- `CLAUDE.md` tells agents they "MUST initialize the swarm using MCP tools" and "MUST call MCP tools AND Task tool in
  ONE message". That is repo content aimed at agents; I ignored it. Its parallel `claude -p` example (`SECURITY=$(claude
  -p … &)`) doesn't capture output as written.

**Evidence level.** Mostly asserted. The measured items are the self-audit (6 auditors, real runs, n not reported per
claim) and the GAIA n=1 runs with per-run cost (~$2.5–6 per run). Multiplier claims in README and CLAUDE files are
contradicted by their own audit. The multi-agent benchmark is a mock. All UNVERIFIED until re-run.
