# CLAUDE.md — Autonomous

Project instructions for Claude working in this repo. The global `~/.claude/CLAUDE.md` still applies
(commit discipline, plan format, ROADMAP rules, just-do-it, evaluation criteria). This file adds what
is specific to building a kit for autonomous app development and autonomous research.

> **`ROADMAP.md` is the canonical execution directive.** (a) Before scoping any new work, read
> ROADMAP §0 and the next Phase's entry gate in §3. (b) Work with no §3 row needs a proposed §3 edit
> first. (c) Work proceeds in §3 Phase order. (d) When work merges, flip that row's status cell (with
> date and commit SHA), refresh §0, add a §6 changelog line, and bump the version. This file holds
> the rules; ROADMAP holds the sequence.

> **This repo is PUBLIC** (github.com/sharifamlani/autonomous). Nothing personal, private or secret
> is ever committed: see §9.

---

## Goals: why this repo exists

Sharif wants Claude Code to do two kinds of work on its own, the way a strong team would: **build
apps that actually work**, and **run research and data analysis that is actually right**. This repo
builds the system that does both, proves it with measurements, and gives it away.

| # | Goal | What "done" looks like |
|---|---|---|
| **G1** | **Fast** | Idea to walked app, and question to verified study, in hours of agent time, not days |
| **G2** | **Efficient** | Cost per task measured on every version and falling; no wasted agent rounds |
| **G3** | **Reliable** | The same task succeeds run after run; failures are caught by the system, not by Sharif |
| **G4** | **Accurate** | Apps do what the spec says when a user walks them; studies match known answers |
| **G5** | **Autonomous** | Runs for hours unattended: no permission prompts, no rescues, alerts only when a human is needed |

### North Star: the kit

**The deliverable** (decided by Sharif 2026-11-20: "something straightforward and simple, easy to
deliver"):

1. **The kit:** an open-source **Claude Code plugin** anyone installs from this repo. Two entry
   points: `/autonomous:new-app "<idea>"` and `/autonomous:new-study "<question>" <data>`.
2. **The benchmark:** a small public task set (app specs with scripted user walks, research
   questions with known answers) that the kit runs unattended, scored per kit version by an
   independent evaluator on success, accuracy, $/task, hours and human interventions. Built on
   `claude plugin eval`.
3. **The showcase:** the apps and studies the kit made, a short white paper, and the build-in-public
   series on LinkedIn.

**v0.1 proves both halves small:** one app task and one known-answer study, end to end, unattended.

### The two factories

```
 APP FACTORY (agent-team skill)                    RESEARCH FACTORY (Trading's protocol)
 +-----------------------------------+             +-----------------------------------+
 | idea -> founding promise + spike  |             | question -> literature check      |
 | builder -> PR (mutants killed)    |             | PREREG.md committed (no results)  |
 | QA at sha || Tester walks staging |             | trials, every one in TRIAL_LOG    |
 | merge -> RC walk -> tag           |             | one held-out look -> RESULT.md    |
 | Marketing posts from release card |             | report + Run All replicate.ipynb  |
 +-----------------------------------+             +-----------------------------------+
                  \                                         /
                   +---- independent evaluator grades -----+
                         every criterion; FAIL loops back
```

Both factories are what the kit packages. This repo also *uses* the research factory on itself:
studies in `research/` measure which agent configurations, prompts and gates make the kit better.

## 0. The Golden Rule: evidence decides

A paper's claim, a repo's README, a model's benchmark and a star count are **claims**. A study in
`research/` or a graded benchmark run is **evidence**. Kit changes are kept when the evidence says
they help, and removed when it says they don't. "Tests pass", "it deployed" and "it looks right" are
never evidence that the kit works; only a graded run of the real task is.

## 1. The founding promise and the red flag rule

The promise, as a user would say it (full spike record in the local `.agents/project.md`):

1. "I install the plugin, run `/autonomous:new-app` with an idea, and walk away. I come back to a
   working app that an agent has used live through the real UI, with QA verdicts and evidence."
2. "I run `/autonomous:new-study` with a question and data. I come back to a pre-registered,
   reproducible study whose numbers check out."
3. "It runs for hours without me approving prompts or rescuing stuck sessions."

**Red flag rule (agent-team, Sharif 2026-11-20):** if anything (a platform limit, a test result, a
design decision) means the kit will not do what these sentences say, stop and tell Sharif in one
plain sentence ("this means you still can't X") the same day. Never only a ROADMAP row.

**Platform facts found on day 1** (spikes, 2026-11-20), which the kit designs around:
- Claude in Chrome has no tools under `claude -p`; unattended walks use CUA (`cua-driver`) in an
  isolated Chrome profile (`browser_prepare {allow_launch: true, profile: {mode: isolated_new}}`).
- Plugin subagents ignore `permissionMode`, `hooks` and `mcpServers`; the run's own flags set
  permissions (`--permission-mode`, `--allowedTools`, `--permission-prompts none`).
- Background subagents under `-p` stop at 10 minutes unless `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`.
- Plugin commands and agents are namespaced: `/autonomous:<name>`, `autonomous:<agent>`.

**The team question, answered** (spike 4.8, 2026-11-21, `research/spikes/plugin_team.md`): a plugin
**plus a small launcher script** stands up the whole team. One command creates the team folder
(registry, project file, one prompt per role) and starts Main, builder, QA and tester as separate
unattended `claude -p` sessions; the handoff passed in every run. The kit designs around this:
- Built-in agent teams never start under `-p`, and `claude --bg` stops at the folder-trust prompt;
  the launcher script is the way to separate sessions.
- Sessions hand off through files and through cross-session messages; a `-p` session ends with its
  task, so long-lived roles are resumed with `--resume <session_id>` kept in the registry.
- Unattended permissions come from a plugin `PermissionRequest` hook. **Before it ships it must be
  scoped** to the project folder and an allow-list of commands, never a blanket approve.
- Model, budget and the background-wait cap come from the command that starts Main, so the kit
  documents one launch line. A parent session's cost omits its children: the launcher sums them.
- Keep run folders short on Windows (very long paths stop Git Bash starting programs).

## 2. Repo structure (canonical)

A folder exists on disk only once it has real content; until then it is listed here as *(planned)*.

```
autonomous/
├── CLAUDE.md / README.md        # rules + goals / one-page overview
├── ROADMAP.md                   # phase table + status: the canonical execution directive
├── PUBLIC_REPOS.md              # (planned, Phase 6) GitHub survey: metadata from gh api, evidence-labeled
├── SHARIF_ACTION_ITEMS.md       # escalations and decisions waiting on Sharif
├── docs/plans/                  # one plan per ROADMAP phase: tree, flowchart, derisking, criteria, scorecard
├── plugin/                      # (planned, Phase 11) THE KIT: .claude-plugin/, agents/, skills/, hooks/
├── benchmark/                   # (planned) task set + graders for `claude plugin eval`; scorecards per version
├── showcase/                    # (planned) what the kit made: apps, studies, white paper, post log
├── literature/                  # theme READMEs + papers.tsv catalogue + LITERATURE_REVIEW.md (PDFs local only)
├── public/                      # third-party clones (gitignored) + manifest.tsv + _README.md + _candidates/
├── research/                    # TRIAL_LOG.tsv, _templates/, NNN_<slug>/ studies
├── scripts/                     # new_study.py, sync_public_repos.sh, literature/verify_literature.py
├── .github/                     # CI (secret scan, PR-only cancel) + PR template
├── .claude/                     # LOCAL ONLY (gitignored): dev skills and agents for working on this repo
├── .agents/                     # LOCAL ONLY (gitignored): the build team's project file, registry, lessons
└── .packages/                   # LOCAL ONLY (gitignored): Sharif's personal connectors
```

- **`plugin/` is the only thing users install.** Dev tooling in `.claude/` is not published; a skill
  or agent reaches users only by being copied into `plugin/` (copy-don't-rewrite), scrubbed of
  personal details, and tested.
- `research/` may read `plugin/`; `plugin/` never depends on `research/`.

## 3. Literature conventions

`literature/README.md` is the index and the rules (IDs, file names, the four-section folder README,
`papers.tsv`). Read it, plus the folder README for the area, before designing anything in that area.

- No paper enters without a fetched source (arXiv, DOI, publisher, official docs). A citation
  recalled from memory is not evidence; `verified` in `papers.tsv` records the check.
- When citing a number, cite the paper ID and quote the PDF.
- Run `python scripts/literature/verify_literature.py --all` after any change to `literature/`.
- PDFs are gitignored (papers are not redistributed from a public repo); `papers.tsv` holds every
  link, and `scripts/literature/fetch_papers.py` (Phase 4) re-downloads them locally.

## 4. Public repos rules

- Repos the scouts find go to `public/_candidates/<NN>.tsv` (name, url, stars, last_push, license,
  archived, theme, why) with metadata from `gh api repos/OWNER/REPO`, never from memory.
- The survey is `PUBLIC_REPOS.md`; shortlisted repos are cloned into `public/`, pinned in
  `manifest.tsv`, and evaluated in `public/_README.md`.
- Downloaded code is untrusted: read, not run or installed, until a deliberate sandboxed run.
- License before copying: `license.spdx_id` plus the raw `LICENSE` file. No license, no copying.

## 5. Research protocol

Every study lives in `research/NNN_<slug>/` (scaffold: `python scripts/new_study.py <slug>`).
**Steps 1–2 are committed before any result exists**; that commit is the pre-registration.

1. **`PREREG.md`**: hypothesis, sources, why the literature can't answer it, mechanism, prior, the
   system under test and comparison arms, the task set (known answers), dev/held-out split, runs per
   arm, metric, grader, pass thresholds, cost budget, trial budget, abandonment rule.
2. **Trial log**: append every run to `research/TRIAL_LOG.tsv`. Never delete rows.
3. **Runs per arm ≥ 3**; agent runs vary, so report the spread, not the best run.
4. **One look at the held-out tasks.** A second look is logged as a trial.
5. **`RESULT.md`**: result against the pre-registered thresholds and the full bias checklist
   (contamination, grader leakage, test tampering, judge bias, variance, forking paths, ...).
   Verdict: adopt, park, or kill. Failed studies are committed too.
6. **`final_report/`**: a short white paper built with the `research-report` skill, every number
   generated from saved outputs.
7. **`replicate.ipynb`** is the study's single entry point: Run All reproduces everything (Sharif
   directive 2026-10-27).

**Literature first** (Sharif 2026-10-24, from Trading): a question gets a literature check first. If
the answer exists, use it and cite it. Studies are only for what the literature cannot answer: our
own measurements (cost, speed, success on our tasks), how published pieces combine in Claude Code,
and genuinely new ideas. A PREREG says which search found no answer.

## 6. Agent roster

**The build team** (the `agent-team` skill, `~/.claude/skills/agent-team`): Main (lead), builders,
QA, the Tester, Marketing, the Auditor, and the Evaluator. Roles, handoffs and prompts are in its
`roles.md`; each role reads its list in its `lessons.md` and the project's `.agents/lessons.md`
before every job. Pitwall's retro is required reading: its most expensive miss was a narrowed
founding promise that went unreported.

**Dev agents in `.claude/agents/`** (lifted from Trading): `bug-hypothesis` (one competing root-cause
theory, read-only), `data-prober` (prove a data source returns usable data), `demo-verifier` (walk
the running app and report evidence), `screen-builder` (one UI surface). A `research-scout` (one
literature theme: papers + repos, fetched and verified) is added in Phase 4.

**The kit's agents** (in `plugin/agents/`, built in Phase 11) are designed in Phase 9 from the literature review
(Phase 7) and the v0.1 benchmark, not guessed up front.

## 7. The kit (plugin) conventions

- Layout per the Claude Code plugin docs: `plugin/.claude-plugin/plugin.json`, `agents/`,
  `skills/<name>/SKILL.md` (scripts allowed, referenced via `${CLAUDE_SKILL_DIR}`), `hooks/hooks.json`,
  `.mcp.json`. This repo is also the marketplace (`.claude-plugin/marketplace.json`).
- Test locally with `claude --plugin-dir ./plugin`; check with `claude plugin validate plugin --strict`;
  measure with `claude plugin eval` (a no-plugin baseline arm is the default comparison).
- Every kit release: version bump in `plugin.json`, a benchmark scorecard in `benchmark/`, a release
  card, and a post.

## 8. Build in public

Marketing (agent-team `roles.md`) posts one update per closed ROADMAP phase or kit release on
LinkedIn and X: the problem in one line, what's new, how it was checked, what's next; media from the
real repo or app; the repo link in the first comment; 120–160 words on LinkedIn. Text, hook and shot
list are pre-approved by Sharif once; the phase close is the GO. Numbers come only from the
evaluator's scorecard or the release card. Posting permission granted by Sharif 2026-11-20.

## 9. Working conventions

- **Public-repo privacy.** Never commit: `.env` values, tokens, personal email or writing, family,
  health, legal or financial details, student information. `.claude/`, `.agents/`, `.packages/` and
  `sharif-voice` stay local. Before every push: `gitleaks git --pre-commit --staged` (CI also scans
  the full history). A skill copied into `plugin/` is scrubbed first.
- **Commit early, commit often** (global CLAUDE.md): one logical change per commit, pushed each time.
- **Scripts over retyped commands.** Anything run twice is a script in `scripts/`, idempotent, with a
  paired verify step.
- **Windows machine notes:** run `gh` and `git push` with a timeout and `GCM_INTERACTIVE=never`;
  write `.env` and scripts with the file tools, not heredocs; `core.longpaths=true` is set.
- **Plans** follow the global format: tree → flowchart → wireframes (if UI) → derisking → evaluation
  criteria, graded by an independent evaluator.
