# Autonomous — Step-by-Step Build Plan (LIVING)

> Single source of truth. Update status cells as work lands. A status flip is one cell.

> This document is CANON over every other doc in the repo. Plans are created in §3 Phase order;
> work with no §3 row gets a proposed §3 edit first (CLAUDE.md, top).

> v0.2 · 2026-11-20

---

## §0 You are here

- **Current phase:** Phase 3 — Rules, roadmap and scaffolds
- **Current step:** 3.6 README.md + SHARIF_ACTION_ITEMS.md
- **Last update:** 2026-11-20
- **Next action:** Phase 4: copy the lifted dev skills that belong in the kit into `plugin/`, scrub them, and pass `claude plugin validate plugin --strict`.

---

## §1 The North Star

**What it is.** An open-source Claude Code plugin (the kit) that does two kinds of work on its own:
builds apps that actually work, and runs research and data analysis that is actually right. Source:
CLAUDE.md, Goals; Sharif's brief, 2026-11-20 planning session.

**Who it serves.** First Sharif (app builds across his projects, research and data science), then
anyone who installs the plugin from GitHub and wants Claude Code to work unattended with evidence.
Source: CLAUDE.md, North Star.

**What v0.1 delivers.** The plugin installs from this repo; `/autonomous:new-app` takes one benchmark
app spec to a walked, working app, and `/autonomous:new-study` takes one known-answer question to a
pre-registered, reproducible study whose numbers match, both unattended, graded by an independent
evaluator, with a scorecard and a post. Source: Sharif's decision 2026-11-20 ("Both, small").

**What scale feels like.** Each kit version re-runs a growing public benchmark and beats the last
scorecard on success, accuracy, cost and hours; the showcase fills with apps and studies the kit made.
Source: CLAUDE.md §7.

---

## §2 Locked architectural decisions

| ID | Decision | Source |
|---|---|---|
| D1 | The deliverable is the kit (Claude Code plugin) + benchmark + showcase | Sharif, 2026-11-20 |
| D2 | v0.1 proves both halves small: one app task, one known-answer study | Sharif, 2026-11-20 |
| D3 | The repo is public: github.com/sharifamlani/autonomous | Sharif, 2026-11-20 |
| D4 | Paper PDFs are committed in `literature/` | Sharif, 2026-11-20 |
| D5 | `.claude/`, `.agents/`, `.packages/` are local only (gitignored) | Sharif, 2026-11-20 · `9b03690` |
| D6 | Skills built on private material (`sharif-voice`) or holding personal details stay local until scrubbed | `c9b9638` |
| D7 | Unattended browser walks use CUA in an isolated Chrome profile; Claude in Chrome is interactive-only | Spike S3b, 2026-11-20 · `dcc04a0` |
| D8 | App work runs the `agent-team` flywheel (build → QA ‖ walk → merge → RC walk → tag → post) | `agent-team` skill |
| D9 | Research runs Trading's protocol (PREREG first, append-only trial log, one held-out look, Run All notebook) | Trading CLAUDE.md §5 · `fdcc5d5` |
| D10 | Literature first: a question the literature answers gets no new study | Trading CLAUDE.md §5, Sharif 2026-10-24 |
| D11 | The benchmark runs on `claude plugin eval` with a no-plugin baseline arm | Plugin docs check, 2026-11-20 |
| D12 | Evidence decides; only a graded run of the real task counts as proof the kit works | CLAUDE.md §0 |
| D13 | Evaluation criteria are graded by an independent evaluator agent, never the builder | Global CLAUDE.md, 2026-10-28 |

---

## §3 The Checklist

### Phase 0 — Recon, plan and lift

**Goal:** know what is in the repo and in Trading, and agree the plan.
**Entry gate:** Sharif's brief.
**Exit gate:** plan agreed in chat; Trading's research skills and agents copied in.
**Status:** ✅ done

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 0.1 | Inventory this folder, Trading's literature / public repos / research, and the agent-team skill | ✅ | — | 2026-11-20 | planning session |
| 0.2 | Copy Trading's research skills and dev agents into `.claude/` (verbatim) | ✅ | — | 2026-11-20 | Sharif mid-turn ask |
| 0.3 | Plan in chat: tree, flowchart, derisking, evaluation criteria | ✅ | — | 2026-11-20 | planning session |
| 0.4 | Decide the deliverable: kit + benchmark + showcase; v0.1 both halves small | ✅ | — | 2026-11-20 | Sharif |

### Phase 1 — Clean up and publish the repo

**Goal:** a clean, public GitHub repo with no personal data.
**Entry gate:** Phase 0.
**Exit gate:** repo public, CI green, gitleaks clean, working tree clean.
**Status:** ✅ done

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 1.1 | Delete stale Pitwall worktree copies and the Pitwall `.devcontainer` | ✅ | — | 2026-11-20 | `git worktree list` in Pitwall |
| 1.2 | Prune 21 off-topic skills after confirming each exists in its home repo | ✅ | — | 2026-11-20 | planning session |
| 1.3 | Rewrite `.gitignore` for a public repo; add `.gitattributes`, `.env.example` | ✅ | — | 2026-11-20 · `c9b9638` | CLAUDE.md §9 |
| 1.4 | Install gitleaks; scan staged files (0 leaks); keep private skills out | ✅ | — | 2026-11-20 · `c9b9638` | D6 |
| 1.5 | `git init`, create the public repo, push | ✅ | — | 2026-11-20 · `c9b9638` | D3 |
| 1.6 | Keep `.claude/` and `.agents/` local | ✅ | — | 2026-11-20 · `9b03690` | D5 |

### Phase 2 — Day-1 team setup and founding-promise spikes

**Goal:** the agent-team day-1 checklist done, and the founding promise tested on the real platform.
**Entry gate:** Phase 1.
**Exit gate:** `new_project.py --check` prints "day 1 complete"; every promise has a spike result.
**Status:** ✅ done (promise 2's spike is row 4.1)

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 2.1 | Bootstrap `.agents/` and the PR template | ✅ | — | 2026-11-20 · `0d20861` | agent-team `setup.md` §1 |
| 2.2 | Write the founding promise as three user sentences | ✅ | — | 2026-11-20 · `dcc04a0` | setup §2 |
| 2.3 | Spike S2: headless `claude -p` subagent run, no prompts (PASS, 24 s) | ✅ | — | 2026-11-20 · `dcc04a0` | promise 3 |
| 2.4 | Spike S3b: headless CUA walk in an isolated Chrome (PASS, 29 s) | ✅ | — | 2026-11-20 · `dcc04a0` | promise 1, D7 |
| 2.5 | Spike S1: plugin format check against the Claude Code docs (PASS) | ✅ | — | 2026-11-20 · `dcc04a0` | D1, D11 |
| 2.6 | Never-offer list, speed bars, test desktop, failed-gate rule | ✅ | — | 2026-11-20 · `dcc04a0` | setup §3–4 |
| 2.7 | CI: gitleaks over full history; cancel-in-progress for PRs only (green) | ✅ | — | 2026-11-20 · `dcc04a0` | setup §5 |

### Phase 3 — Rules, roadmap and scaffolds

**Goal:** the repo's rules and sequence written down; literature, public and research scaffolds ready.
**Entry gate:** Phase 2.
**Exit gate:** CLAUDE.md has its 7 required sections; `verify_literature.py --links --titles` PASS; `sync_public_repos.sh --verify` exit 0.
**Status:** ⏳ in flight

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 3.1 | Lift `new_study.py`, `verify_literature.py`, `sync_public_repos.sh`, research templates (path/import changes only) | ✅ | — | 2026-11-20 · `4b27ac1` | Trading `scripts/` |
| 3.2 | Adapt PREREG/RESULT to agent-system studies; seed `TRIAL_LOG.tsv` | ✅ | — | 2026-11-20 · `fdcc5d5` | D9 |
| 3.3 | `literature/README.md` index (9 themes), `papers.tsv`; `public/_README.md`, `manifest.tsv` | ✅ | — | 2026-11-20 · `feed376` | Trading `literature/`, `public_repos/` |
| 3.4 | CLAUDE.md v0 | ✅ | — | 2026-11-20 · `7f9ad76` | this plan |
| 3.5 | ROADMAP.md v0.2 | ✅ | — | 2026-11-20 · this commit | `writing-roadmaps` skill |
| 3.6 | README.md (one-page overview) and SHARIF_ACTION_ITEMS.md | ⏳ | — | in flight | CLAUDE.md §2 |
| 3.7 | Marketing post #1 drafted (problem + plan, two hooks, shot list) for Sharif's one approval | ⏸ | — | gate: 3.6 | CLAUDE.md §8 |

### Phase 4 — Kit skeleton: adapt the lifted skills and agents

**Goal:** a valid, installable `plugin/` holding the scrubbed skills and agents the kit needs now.
**Entry gate:** Phase 3.
**Exit gate:** `claude plugin validate plugin --strict` exit 0; headless Run All of the notebook template PASS; 0 references to Trading's package in `plugin/`.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 4.1 | Smoke: headless Run All of `research/_templates/replicate.ipynb` after adapting it (promise 2 mechanism) | ⏸ | — | gate: Phase 3 | `.agents/project.md` |
| 4.2 | Create `plugin/.claude-plugin/plugin.json` and root `.claude-plugin/marketplace.json` | ⏸ | — | gate: 4.1 | CLAUDE.md §7 |
| 4.3 | Copy `research-report` into `plugin/skills/` (path changes only) | ⏸ | — | gate: 4.2 | D9 |
| 4.4 | Copy `bug-hypothesis`, `data-prober`, `demo-verifier` into `plugin/agents/` | ⏸ | — | gate: 4.2 | CLAUDE.md §6 |
| 4.5 | Scrub `scheduled-wakeup-loops` and `agent-spec` of personal details; decide which enter the kit | ⏸ | — | gate: 4.2 | D6 |
| 4.6 | `claude plugin validate plugin --strict` exit 0; install test with `claude --plugin-dir ./plugin` | ⏸ | — | gate: 4.3–4.5 | plugin docs |

### Phase 5 — Pilot research scout (one theme)

**Goal:** prove one scout produces a literature folder and repo candidates that meet the contract.
**Entry gate:** Phase 3 (scaffolds), Phase 4.6 not required.
**Exit gate:** folder 02 passes `verify_literature.py`; ≥ 8 verified papers; candidates TSV has 0 short rows.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 5.1 | Add checks to `verify_literature.py`: README sections, unique IDs, `papers.tsv` rows, PDF integrity | ⏸ | — | gate: Phase 3 | literature/README.md |
| 5.2 | Smoke: arXiv PDF fetch returns `%PDF`; `gh api` returns stars/license/archived | ⏸ | — | gate: 5.1 | derisking smokes 3–4 |
| 5.3 | Write the `research-scout` agent (output contract, no citation without a fetched source) | ⏸ | — | gate: 5.2 | CLAUDE.md §3–4 |
| 5.4 | Run the scout on theme 02 (Claude Code and harness engineering) | ⏸ | — | gate: 5.3 | literature/README.md |
| 5.5 | Verify the pilot; tighten the scout prompt if it fails | ⏸ | — | gate: 5.4 | derisking smoke 6 |

### Phase 6 — Research fan-out (8 scouts)

**Goal:** all nine literature folders filled with verified papers and repo candidates.
**Entry gate:** Phase 5 exit gate.
**Exit gate:** `verify_literature.py --all` PASS; ≥ 90 papers, ≥ 8 per folder.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 6.1 | Dispatch scouts for themes 01, 03, 04, 05 in parallel (compute-budget limits) | ⏸ | — | gate: Phase 5 | parallel-agent-orchestration skill |
| 6.2 | Dispatch scouts for themes 06, 07, 08, 09 in parallel | ⏸ | — | gate: Phase 5 | same |
| 6.3 | Verify each folder; re-dispatch only failing themes | ⏸ | — | gate: 6.1–6.2 | derisking smoke 7 |
| 6.4 | Update the `literature/README.md` scoreboard | ⏸ | — | gate: 6.3 | literature/README.md |

### Phase 7 — Public repos survey and clones

**Goal:** the GitHub survey written and the shortlist cloned and pinned.
**Entry gate:** Phase 6.
**Exit gate:** `PUBLIC_REPOS.md` ≥ 60 repos with full metadata; `sync_public_repos.sh --verify` exit 0.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 7.1 | Merge `public/_candidates/*.tsv`; de-duplicate | ⏸ | — | gate: Phase 6 | CLAUDE.md §4 |
| 7.2 | Write `PUBLIC_REPOS.md` (metadata from `gh api`, evidence labels, license notes) | ⏸ | — | gate: 7.1 | Trading `PUBLIC_REPOS.md` format |
| 7.3 | Shortlist ≤ 20; clone pinned into `public/`; write `manifest.tsv` | ⏸ | — | gate: 7.2 | `sync_public_repos.sh` |
| 7.4 | One evaluation section per clone in `public/_README.md` | ⏸ | — | gate: 7.3 | public/_README.md |

### Phase 8 — Literature review and CLAUDE.md v1

**Goal:** the synthesis that turns the evidence into the kit's design.
**Entry gate:** Phases 6–7.
**Exit gate:** `LITERATURE_REVIEW.md` with 0 dangling citation IDs; CLAUDE.md v1 committed.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 8.1 | Write `literature/LITERATURE_REVIEW.md`: what the evidence says per part, and what it implies for the kit's roster, prompts and gates | ⏸ | — | gate: Phases 6–7 | literature/ |
| 8.2 | Citation check script: every ID in the review resolves in `papers.tsv` | ⏸ | — | gate: 8.1 | criterion 9 |
| 8.3 | CLAUDE.md v1: fold in the review's design implications | ⏸ | — | gate: 8.1 | this plan |

### Phase 9 — Independent evaluation of the research foundation

**Goal:** an evaluator that did none of the work grades Phases 1–8 against the criteria table.
**Entry gate:** Phase 8.
**Exit gate:** every criterion PASS on the evaluator's scorecard; post for the phase goes out.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 9.1 | Evaluator grades criteria 1–11 from a fresh clone (citations and repo metadata re-queried) | ⏸ | — | gate: Phase 8 | D13 |
| 9.2 | Fix rounds until every criterion passes | ⏸ | — | gate: 9.1 | global CLAUDE.md |
| 9.3 | Release card from the scorecard; Marketing posts the update | ⏸ | — | gate: 9.2 | CLAUDE.md §8 |

### Phase 10 — Kit v0.1 design

**Goal:** the kit's agents, prompts, skills and gates designed from the review, with a plan.
**Entry gate:** Phase 9.
**Exit gate:** plan file with tree, flowchart, derisking and evaluation criteria approved by Sharif.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 10.1 | Design `/autonomous:new-app` (agent-team roles as plugin agents and skills) | ⏸ | ⏸ | gate: Phase 9 | D8 |
| 10.2 | Design `/autonomous:new-study` (research protocol as plugin agents and skills) | ⏸ | ⏸ | gate: Phase 9 | D9 |
| 10.3 | Design unattended run settings (permission flags, background caps, CUA walk) | ⏸ | ⏸ | gate: Phase 9 | D7, CLAUDE.md §1 |

### Phase 11 — Benchmark v0.1

**Goal:** one app task and one known-answer study, with graders, runnable by `claude plugin eval`.
**Entry gate:** Phase 10.
**Exit gate:** the baseline arm (no plugin) runs end to end and produces a scorecard.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 11.1 | Pick the app task (spec + scripted user walk + pass checks) | ⏸ | ⏸ | gate: Phase 10 | D2 |
| 11.2 | Pick the known-answer study (a published finding with data we can access) | ⏸ | ⏸ | gate: Phase 10 | D2 |
| 11.3 | Write graders (deterministic first; LLM judge only with a calibration set) | ⏸ | ⏸ | gate: 11.1–11.2 | literature 05 |
| 11.4 | Run the no-plugin baseline arm; record the scorecard | ⏸ | ⏸ | gate: 11.3 | D11 |

### Phase 12 — Kit v0.1 build

**Goal:** the kit built through the agent-team flywheel.
**Entry gate:** Phases 10–11.
**Exit gate:** every PR QA-approved at its sha and walked on staging; plugin validates.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 12.1 | Build `/autonomous:new-app` | ⏸ | ⏸ | gate: Phase 11 | D8 |
| 12.2 | Build `/autonomous:new-study` | ⏸ | ⏸ | gate: Phase 11 | D9 |
| 12.3 | Install test from GitHub on a clean profile | ⏸ | ⏸ | gate: 12.1–12.2 | plugin docs |

### Phase 13 — v0.1 release: unattended benchmark run

**Goal:** the kit runs the v0.1 benchmark unattended and beats the baseline; release ships.
**Entry gate:** Phase 12.
**Exit gate:** evaluator scorecard all PASS; tag `v0.1.0`; post within the hour.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 13.1 | Unattended benchmark run (plugin arm vs baseline), ≥ 3 runs per task | ⏸ | ⏸ | gate: Phase 12 | D11 |
| 13.2 | Independent evaluator scorecard; fix rounds until all PASS | ⏸ | ⏸ | gate: 13.1 | D13 |
| 13.3 | Tag `v0.1.0`; release card; Marketing posts | ⏸ | ⏸ | gate: 13.2 | CLAUDE.md §8 |
| 13.4 | Retro (agent-team Auditor item 8); promote lessons to the skill | ⏸ | ⏸ | gate: 13.3 | agent-team |

### Phase 14 — After v0.1: grow the benchmark, improve the kit

**Goal:** each version adds tasks and beats the last scorecard.
**Entry gate:** Phase 13.
**Exit gate:** ongoing.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 14.1 | Grow the benchmark to about 5 app tasks and 5 known-answer studies | ⏸ | ⏸ | gate: Phase 13 | CLAUDE.md North Star |
| 14.2 | Research studies on kit configurations (prereg, ≥ 3 runs per arm) | ⏸ | ⏸ | gate: Phase 13 | D9 |
| 14.3 | Showcase: the apps and studies the kit made; white paper | ⏸ | ⏸ | gate: Phase 13 | D1 |

---

## §4 Open decisions still to make

| # | Decision | Deadline / Trigger | Phase impact |
|---|---|---|---|
| O1 | Tester desktop: Sharif's machine reserved per walk, or a second Windows user session | before the first app walk | 11, 12 |
| O2 | Models per role (builder, QA, Tester, scouts, evaluator) | Phase 10 | 10–13 |
| O3 | Which published finding is the v0.1 known-answer study | Phase 11 | 11 |
| O4 | Where showcase apps are hosted | Phase 13 | 13, 14 |
| O5 | Whether the scrubbed `scheduled-wakeup-loops` and `agent-spec` enter the kit | Phase 4 | 4 |

---

## §5 Reference index

- `CLAUDE.md` — rules, goals, protocols
- `literature/README.md` — literature index and conventions
- `public/_README.md` — third-party repo rules and evaluations
- `research/_templates/` — PREREG, RESULT, replicate.ipynb
- `~/.claude/skills/agent-team/` — roles, lessons, setup, Pitwall retro
- `../Trading/CLAUDE.md` §5, §10 — the research and literature protocols this repo adapts
- Claude Code plugin docs: https://code.claude.com/docs/en/plugins/manifest-reference.md, https://code.claude.com/docs/en/plugin-evals.md

---

## §6 Changelog

- **v0.2 · 2026-11-20** — First roadmap. Phases 0–2 done (recon and plan; public repo `c9b9638`;
  day-1 setup and spikes `dcc04a0`); Phase 3 in flight (scripts `4b27ac1`, templates `fdcc5d5`,
  scaffolds `feed376`, CLAUDE.md `7f9ad76`). The chat tracker's "Phase 1.5" is Phase 2 here, and
  every later phase number moved up by one, so phases are whole numbers in execution order.
  Phases 4–14 sequence the research foundation, then kit v0.1.
