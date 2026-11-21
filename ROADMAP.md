# Autonomous — Step-by-Step Build Plan (LIVING)

> Single source of truth. Update status cells as work lands. A status flip is one cell.

> This document is CANON over every other doc in the repo. Plans are created in §3 Phase order;
> work with no §3 row gets a proposed §3 edit first (CLAUDE.md, top).

> v0.11 · 2026-11-21

---

## §0 You are here

- **Current phase:** Phase 6 done (203 repos surveyed, 20 cloned with process and lessons); Phase 7 next
- **Current step:** waiting on Sharif for Phase 7 (literature review: what the 288 papers and 20 repos imply for the kit)
- **Last update:** 2026-11-21
- **Next action:** Phase 7 on Sharif's go.

---

## §0.5 Phase renumbering map (v0.5, 2026-11-21)

Sharif, 2026-11-21: research and testing come before any kit building. The old Phase 4 (kit
skeleton) is split: its notebook spike stays first; its plugin rows move to the design and build phases.

| Old | New | Phase |
|---|---|---|
| 4.1 | 4.1 | Notebook spike (promise 2) |
| 4.2–4.6 | 11.1, 11.2, 11.5, 9.4 | Plugin files, copied skills, validate → build; which skills enter the kit → design |
| 5 | 4 | Pilot research scout (5.1→4.2, 5.1b→4.3, 5.2→4.4, 5.3→4.5, 5.4→4.6, 5.5→4.7) |
| 6 | 5 | Research fan-out |
| 7 | 6 | Public repos survey |
| 8 | 7 | Literature review |
| 9 | 8 | Independent evaluation |
| 10 | 9 | Kit design |
| 11 | 10 | Benchmark v0.1 |
| 12 | 11 | Kit build (absorbs old 4.2–4.6) |
| 13 | 12 | v0.1 release |
| 14 | 13 | Grow |

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
| D4 | Paper PDFs stay local (gitignored); `literature/` READMEs and `papers.tsv` are public; `fetch_papers.py` re-downloads PDFs | Sharif, 2026-11-20 (revised same day) |
| D5 | `.claude/`, `.agents/`, `.packages/` are local only (gitignored) | Sharif, 2026-11-20 · `9b03690` |
| D6 | Skills built on private material (`sharif-voice`) or holding personal details stay local until scrubbed | `c9b9638` |
| D7 | Unattended browser walks use CUA in an isolated Chrome profile; Claude in Chrome is interactive-only | Spike S3b, 2026-11-20 · `dcc04a0` |
| D8 | App work runs the `agent-team` flywheel (build → QA ‖ walk → merge → RC walk → tag → post) | `agent-team` skill |
| D9 | Research runs Trading's protocol (PREREG first, append-only trial log, one held-out look, Run All notebook) | Trading CLAUDE.md §5 · `fdcc5d5` |
| D10 | Literature first: a question the literature answers gets no new study | Trading CLAUDE.md §5, Sharif 2026-10-24 |
| D11 | The benchmark runs on `claude plugin eval` with a no-plugin baseline arm | Plugin docs check, 2026-11-20 |
| D12 | Evidence decides; only a graded run of the real task counts as proof the kit works | CLAUDE.md §0 |
| D13 | Evaluation criteria are graded by an independent evaluator agent, never the builder | Global CLAUDE.md, 2026-10-28 |
| D14 | License: MIT (repo and plugin) | Sharif, 2026-11-20 |
| D15 | The kit is a plugin plus a launcher script that starts each role as its own `claude -p` session (not built-in agent teams, not a separate framework); its permission hook is scoped to the project folder and an allow-list | Spike 4.8, 2026-11-21 · `4261c62` |
| D16 | Literature collection is not independently graded: scouts self-check with `verify_literature.py`, nothing more ("just get as much literature as we possibly can. We don't need to grade that.") | Sharif, 2026-11-21 |

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
**Status:** ✅ done

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 3.1 | Lift `new_study.py`, `verify_literature.py`, `sync_public_repos.sh`, research templates (path/import changes only) | ✅ | — | 2026-11-20 · `4b27ac1` | Trading `scripts/` |
| 3.2 | Adapt PREREG/RESULT to agent-system studies; seed `TRIAL_LOG.tsv` | ✅ | — | 2026-11-20 · `fdcc5d5` | D9 |
| 3.3 | `literature/README.md` index (9 themes), `papers.tsv`; `public/_README.md`, `manifest.tsv` | ✅ | — | 2026-11-20 · `feed376` | Trading `literature/`, `public_repos/` |
| 3.4 | CLAUDE.md v0 | ✅ | — | 2026-11-20 · `7f9ad76` | this plan |
| 3.5 | ROADMAP.md v0.2 | ✅ | — | 2026-11-20 · this commit | `writing-roadmaps` skill |
| 3.6 | README.md (one-page overview) and SHARIF_ACTION_ITEMS.md | ✅ | — | 2026-11-20 · this commit | CLAUDE.md §2 |
| 3.7 | Marketing post #1 drafted (problem + plan, two hooks, shot list) for Sharif's one approval | ✅ | — | 2026-11-21 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7529775542837882880/) · [X](https://x.com/SharifAmlani/status/2124034377281577170) | CLAUDE.md §8 |

### Phase 4 — Research tooling, notebook spike and pilot scout

**Goal:** prove research can run unattended: the notebook template runs headless, the literature tools work, and one scout fills one theme to the contract.
**Entry gate:** Phase 3.
**Exit gate:** headless Run All of the notebook template PASS; folder 02 passes `verify_literature.py --all`; ≥ 8 verified papers; candidates TSV has 0 short rows; independent evaluator scorecard all PASS.
**Status:** ✅ done (C1–C8 PASS, independent evaluator); waiting on Sharif before Phase 5
**Plan:** `docs/plans/04_research_tooling_and_pilot.md` · setup C1–C7 PASS (independent evaluator, 2026-11-21) · research: `docs/plans/research_plan.md`

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 4.1 | Spike: adapt `research/_templates/replicate.ipynb` and Run All headless (promise 2 mechanism) (was 4.1) | ✅ | ✅ 04 | 2026-11-21 · `d366253` | `.agents/project.md` |
| 4.2 | Add checks to `verify_literature.py`: README sections, unique IDs, `papers.tsv` rows, PDF integrity; fix `--all` (was 5.1) | ✅ | ✅ 04 | 2026-11-21 · `b8693bf` | literature/README.md |
| 4.3 | Write `scripts/literature/fetch_papers.py`: download every `papers.tsv` row's PDF locally, verify `%PDF` (was 5.1b) | ✅ | ✅ 04 | 2026-11-21 · `b8693bf` | D4 |
| 4.4 | Smoke: arXiv PDF fetch returns `%PDF`; `gh api` returns stars/license/archived (was 5.2) | ✅ | ✅ 04 | 2026-11-21 · `b8693bf` | plan smokes |
| 4.5 | Write the `research-scout` agent (output contract, no citation without a fetched source) (was 5.3) | ✅ | ✅ 04 | 2026-11-21 · local (`.claude/`, gitignored) | CLAUDE.md §3–4 |
| 4.6 | Run the scout on theme 02 (Claude Code and harness engineering) (was 5.4) | ✅ | ✅ 04 | 2026-11-21 · `be1834a` (15 sources, 23 repos) | literature/README.md |
| 4.7 | Independent evaluator grades the pilot; tighten the scout prompt if it fails (was 5.5) | ✅ | ✅ 04 | 2026-11-21 · `be1834a` (C8 PASS 8/8, independent evaluator) | D13 |
| 4.8 | Spike: can a plugin stand up the team (Main, builder, QA, tester + registry and prompts) from one command, unattended? Docs + hands-on test plugin; answer: plugin alone / plugin + launcher / other framework | ✅ | ✅ research | 2026-11-21 · `4261c62` (answer: plugin + launcher script) | Sharif 2026-11-21; D1 |
| 4.9 | Inventory our own skills (agent-team, shipping/development flywheel incl. hackathon mode, pm-lead-session, parallel-agent-orchestration, ...): purpose, kit part, lessons (local `.agents/playbook_inventory.md`) | ✅ | ✅ research | 2026-11-21 · local (`.agents/playbook_inventory.md`, 29/29) | Sharif 2026-11-21 |

### Phase 5 — Research fan-out (8 scouts)

**Goal:** all nine literature folders filled with verified papers and repo candidates.
**Entry gate:** Phase 4 exit gate.
**Exit gate:** `verify_literature.py --all` PASS; ≥ 90 papers, ≥ 8 per folder.
**Status:** ✅ done (288 papers, 216 repo candidates after round 2 and the lab sweep; no grading per D16)

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 5.1 | Dispatch scouts for themes 01, 03, 04, 05 in parallel (compute-budget limits) (was 6.1) | ✅ | — | 2026-11-21 · `25a77ca` (themes 01, 03, 04, 05: 64 sources) | parallel-agent-orchestration skill |
| 5.2 | Dispatch scouts for themes 06, 07, 08, 09 in parallel (was 6.2) | ✅ | — | 2026-11-21 · `501df84` (themes 06–09: 62 sources) | same |
| 5.3 | Verify each folder; re-dispatch only failing themes (was 6.3) | ✅ | — | 2026-11-21 · `b711e02` (checker PASS, 9 folders, 141 papers, 137 repos) | `verify_literature.py` |
| 5.4 | Update the `literature/README.md` scoreboard (was 6.4) | ~ | — | parked: scoreboard rows 01, 03–09 not filled (Sharif: no extra work on literature) | literature/README.md |
| 5.5 | Round 2: 9 scouts add 10–15 papers per theme, lab-first (Sharif: leading labs and funded startups only) | ✅ | — | 2026-11-21 · `1fff37e` (+115, 12 cross-theme duplicates removed) | Sharif 2026-11-21 |
| 5.6 | Lab sweep: fill gaps lab by lab (OpenAI, Anthropic, Google DeepMind, Meta, Microsoft, Cognition, Cursor, Sakana, Ai2, METR, Epoch, Mistral, Cohere, Replit) | ✅ | — | 2026-11-21 · `60dc6aa` (+32) | Sharif 2026-11-21 |

### Phase 6 — Public repos survey and clones

**Goal:** the GitHub survey written, the shortlist cloned and pinned, and each kept repo's process and lessons learned written down.
**Entry gate:** Phase 5.
**Exit gate:** `PUBLIC_REPOS.md` ≥ 60 repos with full metadata; `sync_public_repos.sh --verify` exit 0.
**Status:** ✅ done (203 repos surveyed, 20 cloned and written up; no grading per D16)

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 6.1 | Merge `public/_candidates/*.tsv`; de-duplicate (was 7.1) | ✅ | — | 2026-11-21 · `19933b9` (216 → 203 unique; `merge_candidates.py --check` PASS) | CLAUDE.md §4 |
| 6.2 | Write `PUBLIC_REPOS.md` (metadata from `gh api`, evidence labels, license notes) (was 7.2) | ✅ | — | 2026-11-21 · `25d42f4` (203 repos, live `gh api` metadata, flags, license notes, findings) | Trading `PUBLIC_REPOS.md` format |
| 6.3 | Shortlist ≤ 20; clone pinned into `public/`; write `manifest.tsv` (was 7.3) | ✅ | — | 2026-11-21 · `a3531b4` (20 pinned; `sync_public_repos.sh --verify` exit 0) | `sync_public_repos.sh` |
| 6.4 | One evaluation section per clone in `public/_README.md` (was 7.4) | ✅ | — | 2026-11-21 · `af194aa` (20 sections in `public/_README.md`) | public/_README.md |
| 6.5 | Per kept repo: its process (how agents are organised, handed work, tested, reviewed) and lessons learned (contributor guides, design docs, postmortems, recurring issues) in `public/_README.md` | ✅ | — | 2026-11-21 · `af194aa` (process, lessons with file/issue cites, take/avoid per repo) | Sharif 2026-11-21 |

### Phase 7 — Literature review and CLAUDE.md v1

**Goal:** the synthesis that turns the evidence into the kit's design.
**Entry gate:** Phases 5–6.
**Exit gate:** `LITERATURE_REVIEW.md` with 0 dangling citation IDs; CLAUDE.md v1 committed.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 7.1 | Write `literature/LITERATURE_REVIEW.md`: what the evidence and the repo lessons say per part, and what they imply for the kit's roster, prompts and gates (was 8.1) | ⏸ | — | gate: Phases 5–6 | literature/ |
| 7.2 | Citation check script: every ID in the review resolves in `papers.tsv` (was 8.2) | ⏸ | — | gate: 7.1 | criterion 9 |
| 7.3 | CLAUDE.md v1: fold in the review's design implications (was 8.3) | ⏸ | — | gate: 7.1 | this plan |

### Phase 8 — Independent evaluation of the research foundation

**Goal:** an evaluator that did none of the work grades Phases 4–7 against the criteria table.
**Entry gate:** Phase 7.
**Exit gate:** every criterion PASS on the evaluator's scorecard; post for the phase goes out.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 8.1 | Evaluator grades the criteria from a fresh clone (citations and repo metadata re-queried) (was 9.1) | ⏸ | — | gate: Phase 7 | D13 |
| 8.2 | Fix rounds until every criterion passes (was 9.2) | ⏸ | — | gate: 8.1 | global CLAUDE.md |
| 8.3 | Release card from the scorecard; Marketing posts the update (was 9.3) | ⏸ | — | gate: 8.2 | CLAUDE.md §8 |

### Phase 9 — Kit v0.1 design, from the research

**Goal:** the kit's agents, prompts, skills and gates designed from the review, with a plan.
**Entry gate:** Phase 8.
**Exit gate:** plan file with tree, flowchart, derisking and evaluation criteria approved by Sharif.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 9.1 | Design `/autonomous:new-app` (agent-team roles as plugin agents and skills) (was 10.1) | ⏸ | ⏸ 09 | gate: Phase 8 | D8 |
| 9.2 | Design `/autonomous:new-study` (research protocol as plugin agents and skills) (was 10.2) | ⏸ | ⏸ 09 | gate: Phase 8 | D9 |
| 9.3 | Design unattended run settings (permission flags, background caps, CUA walk) (was 10.3) | ⏸ | ⏸ 09 | gate: Phase 8 | D7, CLAUDE.md §1 |
| 9.4 | Decide which lifted dev skills and agents enter the kit (`research-report`, the three dev agents, scrubbed `scheduled-wakeup-loops` and `agent-spec`) (was 4.3–4.5, O5) | ⏸ | ⏸ 09 | gate: Phase 8 | D6 |

### Phase 10 — Benchmark v0.1: the tests

**Goal:** one app task and one known-answer study, with graders, runnable by `claude plugin eval`.
**Entry gate:** Phase 9.
**Exit gate:** the baseline arm (no plugin) runs end to end and produces a scorecard.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 10.1 | Pick the app task (spec + scripted user walk + pass checks) (was 11.1) | ⏸ | ⏸ 10 | gate: Phase 9 | D2 |
| 10.2 | Pick the known-answer study (a published finding with data we can access) (was 11.2) | ⏸ | ⏸ 10 | gate: Phase 9 | D2 |
| 10.3 | Write graders (deterministic first; LLM judge only with a calibration set) (was 11.3) | ⏸ | ⏸ 10 | gate: 10.1–10.2 | literature 05 |
| 10.4 | Run the no-plugin baseline arm; record the scorecard (was 11.4) | ⏸ | ⏸ 10 | gate: 10.3 | D11 |

### Phase 11 — Kit v0.1 build

**Goal:** the kit built through the agent-team flywheel, starting from an empty `plugin/`.
**Entry gate:** Phases 9–10.
**Exit gate:** every PR QA-approved at its sha and walked on staging; `claude plugin validate plugin --strict` exit 0; 0 references to Trading's package in `plugin/`.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 11.1 | Create `plugin/.claude-plugin/plugin.json` and root `.claude-plugin/marketplace.json` (was 4.2) | ⏸ | ⏸ 11 | gate: Phase 10 | CLAUDE.md §7 |
| 11.2 | Copy in the skills and agents chosen in 9.4 (copy-don't-rewrite, scrubbed) (was 4.3–4.5) | ⏸ | ⏸ 11 | gate: 11.1 | D6, D9 |
| 11.3 | Build `/autonomous:new-app` (was 12.1) | ⏸ | ⏸ 11 | gate: 11.2 | D8 |
| 11.4 | Build `/autonomous:new-study` (was 12.2) | ⏸ | ⏸ 11 | gate: 11.2 | D9 |
| 11.5 | `claude plugin validate plugin --strict` exit 0; install test with `claude --plugin-dir ./plugin` (was 4.6) | ⏸ | ⏸ 11 | gate: 11.3–11.4 | plugin docs |
| 11.6 | Install test from GitHub on a clean profile (was 12.3) | ⏸ | ⏸ 11 | gate: 11.5 | plugin docs |

### Phase 12 — v0.1 release: unattended benchmark run

**Goal:** the kit runs the v0.1 benchmark unattended and beats the baseline; release ships.
**Entry gate:** Phase 11.
**Exit gate:** evaluator scorecard all PASS; tag `v0.1.0`; post within the hour.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 12.1 | Unattended benchmark run (plugin arm vs baseline), ≥ 3 runs per task (was 13.1) | ⏸ | ⏸ 12 | gate: Phase 11 | D11 |
| 12.2 | Independent evaluator scorecard; fix rounds until all PASS (was 13.2) | ⏸ | ⏸ 12 | gate: 12.1 | D13 |
| 12.3 | Tag `v0.1.0`; release card; Marketing posts (was 13.3) | ⏸ | ⏸ 12 | gate: 12.2 | CLAUDE.md §8 |
| 12.4 | Retro (agent-team Auditor item 8); promote lessons to the skill (was 13.4) | ⏸ | ⏸ 12 | gate: 12.3 | agent-team |

### Phase 13 — After v0.1: grow the benchmark, improve the kit

**Goal:** each version adds tasks and beats the last scorecard.
**Entry gate:** Phase 12.
**Exit gate:** ongoing.
**Status:** ⏸ planned

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 13.1 | Grow the benchmark to about 5 app tasks and 5 known-answer studies (was 14.1) | ⏸ | ⏸ | gate: Phase 12 | CLAUDE.md North Star |
| 13.2 | Research studies on kit configurations (prereg, ≥ 3 runs per arm) (was 14.2) | ⏸ | ⏸ | gate: Phase 12 | D9 |
| 13.3 | Showcase: the apps and studies the kit made; white paper (was 14.3) | ⏸ | ⏸ | gate: Phase 12 | D1 |

---

## §4 Open decisions still to make

| # | Decision | Deadline / Trigger | Phase impact |
|---|---|---|---|
| O1 | Tester desktop: Sharif's machine reserved per walk, or a second Windows user session | before the first app walk | 10, 11 |
| O2 | Models per role (builder, QA, Tester, scouts, evaluator) | Phase 9 | 9–12 |
| O3 | Which published finding is the v0.1 known-answer study | Phase 10 | 10 |
| O4 | Where showcase apps are hosted | Phase 12 | 12, 13 |
| O5 | Whether the scrubbed `scheduled-wakeup-loops` and `agent-spec` enter the kit | Phase 9 (row 9.4) | 9, 11 |

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

- **v0.11 · 2026-11-21** — Phase 6 closed: 216 candidates merged to 203 repos with live GitHub
  metadata (`PUBLIC_REPOS.md`, `public/candidates.tsv`); 20 shortlisted, cloned pinned, and written up
  for process and lessons (`public/_README.md`). Found: Anthropic's plugin directory refuses command
  hooks from non-Verified organisations (claude-plugins-official #7024), so the kit ships from this
  repo's own marketplace; InfiAgent-DABench's scorer drops unanswered questions and needs fixing
  before the v0.1 study. Phase 7 unblocked.
- **v0.10 · 2026-11-21** — Literature round 2 (`1fff37e`, +115, lab-first per Sharif) and a lab-by-lab
  sweep (`60dc6aa`, +32): 288 papers, 216 repo candidates. 12 cross-theme duplicates removed; ERA and
  REPRO-Bench re-added (S31, S32) after both scouts dropped them. "When not to use an evaluator" rule
  written to global and project CLAUDE.md.
- **v0.9 · 2026-11-21** — Phase 5 closed: all 9 literature folders filled (141 papers, 137 repo
  candidates), checker PASS. D16: Sharif dropped independent grading of literature collection; the
  partly applied batch-2 wording fixes were committed as they stood. Plugin answer locked as D15.
- **v0.8 · 2026-11-21** — Phase 4 closed. Pilot scout filled theme 02 (15 sources, 23 repos; C8 PASS
  8/8, `be1834a`). Plugin-team spike (4.8, `4261c62`): a plugin plus a small launcher script stands up
  Main, builder, QA and tester as separate unattended sessions with a working handoff; D1 holds, no
  red flag. Agent teams and `claude --bg` do not work unattended. Skills inventory 29/29 (local);
  7 empty skill copies re-copied.
- **v0.7 · 2026-11-21** — Sharif approved the research plan (`docs/plans/research_plan.md`) and added
  three things: row 4.9, an inventory of our own skills as the starting point; row 4.8, a spike on whether a plugin can stand up the whole agent team (changes D1 if
  not), and row 6.5, each kept repo's process and lessons learned. 4.6 pilot scout started.
- **v0.6 · 2026-11-21** — Phase 3 closed: post #1 live on LinkedIn (3.7; A2 closed). Phase 4 setup
  done: notebook template runs headless (4.1, `d366253`; promise 2's mechanism proven), literature
  checker, fetcher and smokes (4.2–4.4, `b8693bf`), `research-scout` agent (4.5, local). Independent
  evaluator: C1–C7 PASS. Research (4.6) waits on Sharif's go.
- **v0.5 · 2026-11-21** — Phases reordered at Sharif's direction: research and testing before any
  kit building (§0.5 map). Old Phase 4 split: 4.1 notebook spike stays; plugin rows 4.2–4.6 move to
  Phase 11 (build) and 9.4 (design decision). Old Phases 5–14 become 4–13. Row 4.6 (first scout run)
  waits on Sharif's go. Marketing takes posting approval relayed through Main (`.agents/project.md`).
- **v0.4 · 2026-11-20** — D4 revised by Sharif: paper PDFs are gitignored; the literature index and catalogue stay public; row 5.1b adds `fetch_papers.py`. `.github/` stays tracked (CI secret scan).
- **v0.3 · 2026-11-20** — MIT license added (D14; action item A3 closed). Post #1 hooks revised at Sharif's request; still waiting on his pick (A2).
- **v0.2 · 2026-11-20** — First roadmap. Phases 0–2 done (recon and plan; public repo `c9b9638`;
  day-1 setup and spikes `dcc04a0`); Phase 3 in flight (scripts `4b27ac1`, templates `fdcc5d5`,
  scaffolds `feed376`, CLAUDE.md `7f9ad76`). The chat tracker's "Phase 1.5" is Phase 2 here, and
  every later phase number moved up by one, so phases are whole numbers in execution order.
  Phases 4–14 sequence the research foundation, then kit v0.1.
