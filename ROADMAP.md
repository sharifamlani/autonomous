# Autonomous — Step-by-Step Build Plan (LIVING)

> Single source of truth. Update status cells as work lands. A status flip is one cell.

> This document is CANON over every other doc in the repo. Plans are created in §3 Phase order;
> work with no §3 row gets a proposed §3 edit first (CLAUDE.md, top).

> v0.31 · 2026-11-22

---

## §0 You are here

- **Current phase:** Phase 10 (validation ladder); Phase 9 done (design + architecture approved 2026-11-22). Row 8.3 flips when Marketing confirms the review post went live
- **Current step:** benchmark smokes D1–D3 PASS (S1 key 72/72 printed values; S2 inputs leak-free; S3 planted effect recoverable, null clean). Remaining: graders + calibration (D4), bug injection (D5, needs the known-good app), `run.py` and the baseline run (D6)
- **Last update:** 2026-11-22
- **Next action:** the measured S1 baseline run (step 6, in progress), then token caps to Sharif; S2 tolerance (10-B near-zero estimates) also waiting on Sharif.

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
| D17 | Two-scale benchmark: `claude plugin eval` for single-skill behaviour checks; our `benchmark/run.py` for end-to-end tasks (plugin eval caps runs at 1 h / 200 turns, no code graders). Revises D11 | Sharif, 2026-11-22 (decision 9-A) |
| D18 | Every role runs on Claude Code: one `claude -p` session per role step, started by `team.py`; the baseline arm is plain Claude Code without the plugin | Spike 4.8; Sharif, 2026-11-22 |
| D19 | v0.1 runs use Opus 5.5 in both arms; runs execute on native Windows | Sharif, 2026-11-22 (9-C, 9-D) |
| D20 | Kit roles: spec-writer, builder, QA, tester; analyst, replicator. The conductor is code (`team.py`). Marketing runs outside the kit, reading a release card each run writes | Sharif, 2026-11-22 (9-E) |
| D21 | Validation ladder v0.1: S1–S4 (Amlani & Collitt 2021, planted effect + null, LaLonde, leading prompt) and A1–A3 (build, 20 planted bugs, impossible spec); S2 tolerance = same sign, same 5% call, within 10%; budget per D22 | Sharif, 2026-11-22 (10-A to 10-E) |
| D22 | Runs use Sharif's Claude Code subscription: the budget and the efficiency metric are **usage (tokens per task)**, not dollars. Caps are tokens, wall-clock and turns; token ceilings are set from the first measured run. API-equivalent $ is recorded for readers only. Revises 9-B and 10-D | Sharif, 2026-11-22 |
| D23 | Benchmark runs happen in a clean room: workspace at `C:\abench\<run-id>` (outside the user folder, repo and Dropbox) with `--setting-sources project,local --strict-mcp-config`, so the baseline is stock Claude Code (no personal CLAUDE.md, skills or MCP). A run that reaches for the original package or the answer keys is scored FAIL | Spike 2026-11-22; Sharif, 2026-11-22 ("fail it is") |
| D24 | Plan 10 Part 2 approved: runner + steps 1–8; Phase 11 starts after the measured run (step 6) with the remaining tasks built alongside; k = 3 per arm for release checks, k = 1 for dev iterations; token caps set from the measured run | Sharif, 2026-11-22 (10-F to 10-H) |

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
**Status:** ✅ done (288 catalogue entries = 286 distinct papers after two duplicates were found in Phase 7.5 QA; 216 repo candidates; no grading per D16)

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
**Status:** ✅ done (237 repos surveyed after sweep 2, 32 cloned and written up; no grading per D16)

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 6.1 | Merge `public/_candidates/*.tsv`; de-duplicate (was 7.1) | ✅ | — | 2026-11-21 · `19933b9` (216 → 203 unique; `merge_candidates.py --check` PASS) | CLAUDE.md §4 |
| 6.2 | Write `PUBLIC_REPOS.md` (metadata from `gh api`, evidence labels, license notes) (was 7.2) | ✅ | — | 2026-11-21 · `25d42f4` (203 repos, live `gh api` metadata, flags, license notes, findings) | Trading `PUBLIC_REPOS.md` format |
| 6.3 | Shortlist ≤ 20; clone pinned into `public/`; write `manifest.tsv` (was 7.3) | ✅ | — | 2026-11-21 · `a3531b4` (20 pinned; `sync_public_repos.sh --verify` exit 0) | `sync_public_repos.sh` |
| 6.4 | One evaluation section per clone in `public/_README.md` (was 7.4) | ✅ | — | 2026-11-21 · `af194aa` (20 sections in `public/_README.md`) | public/_README.md |
| 6.5 | Per kept repo: its process (how agents are organised, handed work, tested, reviewed) and lessons learned (contributor guides, design docs, postmortems, recurring issues) in `public/_README.md` | ✅ | — | 2026-11-21 · `af194aa` (process, lessons with file/issue cites, take/avoid per repo) | Sharif 2026-11-21 |
| 6.6 | Sweep 2: popularity-led search for automated science and automated development repos the paper-led sweep missed (karpathy/autoresearch, alphaXiv/OpenResearch, ...) | ✅ | — | 2026-11-21 · `58f6ef9` (+34 → 237 repos; `--check` PASS) | Sharif 2026-11-21 |
| 6.7 | Clone the 12 most-starred sweep-2 repos pinned; process-and-lessons write-ups (groups E, F); headline findings | ✅ | — | 2026-11-21 · `1e8d49a`, `d22c29a`, `71e37c1` (32 pinned, `--verify` exit 0; 11 cited issues spot-checked) | Sharif 2026-11-21 |

### Phase 7 — Literature review and CLAUDE.md v1

**Goal:** the synthesis that turns the evidence into the kit's design.
**Entry gate:** Phases 5–6.
**Exit gate:** `LITERATURE_REVIEW.md` with 0 dangling citation IDs; CLAUDE.md v1 committed.
**Status:** ✅ done (review published; CLAUDE.md v1 lessons L1–L11 2026-11-22)
**Plan:** `docs/plans/07_literature_review.md`

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 7.1 | Write `literature/LITERATURE_REVIEW.md`: what the evidence and the repo lessons say per part, and what they imply for the kit's roster, prompts and gates (was 8.1) | ✅ | — | 2026-11-21 · `ff08499` draft → `257dd35` QA'd (16 sections, 162 papers + 28 repos, 35 pp.) | literature/ |
| 7.2 | Citation check script: every ID in the review resolves in `papers.tsv` (was 8.2) | ✅ | — | 2026-11-21 · `de3f956` `check_review.py` (0 dangling; smoke: fake ID caught) + `build_evidence.py` (`c733ac8`) | criterion 9 |
| 7.3 | CLAUDE.md v1: fold in the review's design implications (was 8.3) | ✅ | — | 2026-11-22 · `e55edec` CLAUDE.md §0.5, lessons L1–L11 | this plan |

### Phase 7.5 — QA of the literature review (before the independent grade)

**Goal:** a QA team that did not write the review checks every number, citation and fact before anything is graded or published (Sharif 2026-11-21: "very thorough ... for public release").
**Entry gate:** Phase 7 (full draft, `render_review.py --check` PASS).
**Exit gate:** `literature/qa/LITERATURE_REVIEW_qa.md` shows 0 open blockers and 0 open majors, every fix re-checked.
**Status:** ✅ done (QA PASS 2026-11-21: 135 findings fixed and re-checked)
**Plan:** `docs/plans/07_literature_review.md` § Phase 7.5

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 7.5.1 | Number check: 100% of numbers matched to the PDF or source page | ✅ | — | 2026-11-21 · `257dd35` (753 quotes verified on the PDF page by script; all numbers checked by 5 QA passes) | Sharif 2026-11-21 |
| 7.5.2 | Citation check: every ID resolves; every cited source says what the sentence claims; Literature Cited metadata matches arXiv/Crossref; every repo issue re-checked via `gh api` | ✅ | — | 2026-11-21 · `257dd35` (162 entries' metadata checked; 0 dangling; repo issues re-checked via gh) | Sharif 2026-11-21 |
| 7.5.3 | Fact, fairness and tone check (labs, dates, names; no claims beyond a source; no absolutes without backing) | ✅ | — | 2026-11-21 · `257dd35` (fairness/absolutes pass; 11 blockers found and fixed) | Sharif 2026-11-21 |
| 7.5.4 | Copy, format and privacy pass | ✅ | — | 2026-11-21 · `257dd35` (copy, layout, privacy pass) | CLAUDE.md §9 |
| 7.5.6 | Evidence file `literature/LITERATURE_REVIEW_EVIDENCE.md`: every claim and citation with its verbatim quote, page and location; quotes checked against the PDF by `build_evidence.py`, support checked by QA | ✅ | — | 2026-11-21 · `257dd35` (`LITERATURE_REVIEW_EVIDENCE.md`: 1,043 rows, 753 VERIFIED, 290 checked by hand, 0 failing) | Sharif 2026-11-21 |
| 7.5.5 | Fix round, then QA re-checks every fix | ✅ | — | 2026-11-21 · `257dd35` (re-check confirmed 135/135 fixes; `literature/qa/LITERATURE_REVIEW_qa.md` QA PASS) | global CLAUDE.md |

### Phase 8 — Independent evaluation of the research foundation

**Goal:** an evaluator that did none of the work grades Phases 4–7 against the criteria table.
**Entry gate:** Phase 7.
**Exit gate:** every criterion PASS on the evaluator's scorecard; post for the phase goes out.
**Status:** ⏳ grade PASS; release with Marketing

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 8.1 | Evaluator grades the criteria from a fresh clone (citations and repo metadata re-queried) (was 9.1) | ✅ | — | 2026-11-21 · `12940cd` + `88d47b6` (GRADE PASS 7/7; length criterion raised by Sharif) | D13 |
| 8.2 | Fix rounds until every criterion passes (was 9.2) | ✅ | — | 2026-11-21 · `f05f4a1` (M1 ruflo fairness + 7 minors fixed, re-graded) | global CLAUDE.md |
| 8.3 | Release card from the scorecard; Marketing posts the review to LinkedIn + X with a video about the paper (`make-video` skill) **only on Sharif's express go order** (target 6:00 AM Sun 2026-11-22 EST) (was 9.3) | ⏳ | — | 2026-11-21 · `88d47b6` release card + PDF live; Marketing preparing post + video for Sharif's approval in its session (Sharif: "green light"); video dropped by Sharif (text + page-1 image); Sharif approved in Marketing's session; scheduled 6:00 AM ET Sun 2026-11-22, LinkedIn + X standalone, PDF link held for commenters (Sharif sends replies) | CLAUDE.md §8 |

### Phase 9 — Kit v0.1 design, from the research

**Goal:** the kit's agents, prompts, skills and gates designed from the review, with a plan.
**Entry gate:** Phase 8.
**Exit gate:** plan file with tree, flowchart, derisking and evaluation criteria approved by Sharif.
**Status:** ✅ done (plan + architecture approved by Sharif 2026-11-22: "All that looks good!"; D17–D20)
**Plan:** `docs/plans/09_kit_v01_design.md` + `docs/plans/09_kit_v01_architecture.md`

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 9.1 | Design `/autonomous:new-app` (agent-team roles as plugin agents and skills) (was 10.1) | ✅ | — | 2026-11-22 · `fd1a90c` `a2aae37` `07a013e` approved | D8 |
| 9.2 | Design `/autonomous:new-study` (research protocol as plugin agents and skills) (was 10.2) | ✅ | — | 2026-11-22 · `fd1a90c` `a2aae37` `07a013e` approved | D9 |
| 9.3 | Design unattended run settings (permission flags, background caps, CUA walk) (was 10.3) | ✅ | — | 2026-11-22 · `fd1a90c` `a2aae37` `07a013e` approved | D7, CLAUDE.md §1 |
| 9.4 | Decide which lifted dev skills and agents enter the kit (`research-report`, the three dev agents, scrubbed `scheduled-wakeup-loops` and `agent-spec`) (was 4.3–4.5, O5) | ✅ | — | 2026-11-22 · `fd1a90c` `a2aae37` `07a013e` approved | D6 |

### Phase 10 — Benchmark v0.1: the tests

**Goal:** one app task and one known-answer study, with graders, runnable by `claude plugin eval`.
**Entry gate:** Phase 9.
**Exit gate:** the baseline arm (no plugin) runs end to end and produces a scorecard.
**Status:** ⏳ in progress (ladder approved 2026-11-22, D21; D1–D3 PASS; Part 2, the runner and remaining steps, proposed 2026-11-22)
**Plan:** `docs/plans/10_benchmark_validation.md`

| # | Action | Status | Plan? | Date · Commit / Plan | Source |
|---|---|---|---|---|---|
| 10.1 | App ladder: A1 build, A2 20 planted bugs for QA + tester, A3 impossible spec (was 11.1) | ⏸ | ✅ 10 | `docs/plans/10_benchmark_validation.md` (approved) | D2 |
| 10.2 | Study ladder: S1 reproduce + S2 replicate Amlani & Collitt 2021 (CC0), S3 planted effect + null, S4 traps (LaLonde, leading prompt) (was 11.2) | ~ S1 key, S2 inputs, S3 data done (`3aa257f`); S3 jitter + S4 pending | ✅ 10 | `docs/plans/10_benchmark_validation.md` (approved) | D2 |
| 10.3 | Write graders (deterministic first; LLM judge only with a calibration set) (was 11.3) | ~ study graders calibrated 13/13 (`8f93aad`); app graders with step 7 | ⏸ 10 | gate: 10.1–10.2 | literature 05 |
| 10.4 | Run the no-plugin baseline arm; record the scorecard (was 11.4) | ⏸ | ✅ 10 | gate: 10.3, 10.5 | D17 |
| 10.5 | Runner `benchmark/run.py`: clean room at `C:\abench`, token/minute/turn caps, cheat flags = FAIL, scorecard + TRIAL_LOG + usage log | ✅ | — | 2026-11-22 · `1dee888` (R1–R4 PASS; kit arm comes with Phase 11) | D22, D23 |
| 10.6 | One measured baseline run (S1) → token caps per run (Sharif's call) | ⏸ | ✅ 10 | gate: 10.5 + S1 grader | D22 |

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

- **v0.31 · 2026-11-22** — Steps 4–5 done: S3 jitter (R5) and the study tasks S1–S3 with calibrated graders (R6, 13/13; calibration caught and fixed a double-rounding bug). S2 near-zero tolerance raised to Sharif. Step 6 (measured S1 run) started.
- **v0.30 · 2026-11-22** — Runner built (row 10.5 ✅): clean room R1, hello R2, caps R3 (after a job-object fix for orphaned Git Bash processes), cheat flag R4 all PASS; leak check and regrade moved into `run.py`. Next: S3 jitter and the study graders.
- **v0.29 · 2026-11-22** — Sharif approved plan 10 Part 2 (D24): runner + steps 1–8, overlap with Phase 11 after the measured run, k = 3 release / k = 1 dev. Row 10.5 in progress.
- **v0.28 · 2026-11-22** — Plan 10 Part 2 proposed: the runner (clean room, caps, cheat = FAIL, scorecard) and steps 1–8 to the full baseline. D23: clean room at `C:\abench` (spike: default `claude -p` loads Sharif's CLAUDE.md, skills and ~650k tokens of MCP tools; the flags plus a workspace outside the user folder give stock Claude Code). Rows 10.5–10.6 added; 10.2 partial.
- **v0.27 · 2026-11-22** — Self-serve Claude Code checks: local `.packages/Claude_code/cc.py` reads usage limits, a session's context size and live sessions with 0 model tokens, and compacts stored sessions (85k → 21k proven); running sessions are refused. The measured baseline run no longer needs Sharif to read `/usage`.
- **v0.26 · 2026-11-22** — D22: the kit runs on Sharif's Claude Code subscription, so usage (tokens per task) replaces dollars as the budget and the G2 metric. Dollar caps in 9-B and 10-D removed; token ceilings to be set from the first measured run. CLAUDE.md, plans 09/10 and the research templates updated.
- **v0.25 · 2026-11-22** — Phase 10 smokes D1–D3 PASS: Amlani & Collitt Tables 2–3 reproduced 72/72
  (`53f6891`); the published county FE are coded by county name (1,845 groups vs 3,108 FIPS); with FIPS FE
  the headline rises 2.568 → 2.923. S2 methods-only inputs pass the leak check; S3 planted/null data pass
  the self-test. Inputs and keys stay local.
- **v0.24 · 2026-11-22** — Sharif approved the Phase 9 design and architecture and the Phase 10 ladder ("All
  that looks good!"): decisions D17–D21 recorded (D17 revises D11). Phase 9 done; Phase 10 in progress.
- **v0.23 · 2026-11-22** — Phase 10 validation ladder drafted (Sharif: "compelling ways to validate the
  entire system"; "I love the ladder"). Study tasks from Sharif's own CC0 replication packages (Amlani &
  Collitt 2021 for v0.1; Amlani & Algara 2021 for v0.2), planted effects, traps; app checkers tested
  with planted bugs. Rows 10.1–10.2 redefined.
- **v0.22 · 2026-11-22** — Phase 9 starting architecture drafted (Sharif: "we need a starting architecture
  to iterate on"): deterministic orchestrator + agent roles, file-based run folder, verdict contracts,
  role fences in a hook, caps, `kit.toml` knobs. morluto/rea reviewed (ideas borrowed, not a dependency).
- **v0.21 · 2026-11-22** — Row 7.3 closed: CLAUDE.md §0.5 holds the review's lessons L1–L11 (`e55edec`);
  Phase 7 done. Phase 9 plan drafted (`fd1a90c`). Found: `claude plugin eval` caps a run at 1 h / 200
  turns with no code graders, so the plan proposes revising D11 (decision 9-A).
- **v0.20 · 2026-11-21** — Post #4 (the review) scheduled for 6:00 AM ET Sun 2026-11-22 on LinkedIn
  and X after Sharif's go in Marketing's session. Video dropped by Sharif; text-only with a page-1 image
  of the PDF; link held for commenters, replies drafted by Marketing and sent by Sharif. Row 8.3 flips
  ✅ once the post is confirmed live.
- **v0.19 · 2026-11-21** — Sharif: "length is acceptable and green light". Review PDF published
  (`88d47b6`, GRADE PASS 7/7) with release card; Marketing preparing the post and video, posting only
  on Sharif's approval in its session. Rows 8.1–8.2 closed.
- **v0.18 · 2026-11-21** — Phase 8 grade: 6/7 criteria PASS on independent re-measurement; the one
  major reader finding (ruflo fairness) fixed and re-graded. Only the word-count criterion fails
  (15,043 vs 9-11k); changing it is Sharif's call.
- **v0.17 · 2026-11-21** — Phase 7.5 closed: QA PASS (`257dd35`), 135/135 findings confirmed fixed by a
  re-checker that touched none of the work. Phase 8 (independent evaluator) started.
- **v0.16 · 2026-11-21** — Phase 7.5: five QA passes found 135 issues (11 blockers) and all are fixed,
  e.g. a +0.5-point non-significant result stated as "beat", a quote stitched from figure axis labels, a
  claim cited to an OpenAI post outside the corpus, an unmerged PR called a fix (also corrected in
  PUBLIC_REPOS.md). Corpus corrected to 286 distinct papers (two duplicates). Evidence file published
  (1,043 rows, 753 verified against PDFs, 290 checked by hand, 0 failing). Re-check of every fix running.
- **v0.15 · 2026-11-21** — Full review draft in LaTeX (`ff08499`): 16 sections, 37 pages, 162 papers
  and 27 repos cited, evidence ledger 991 rows (720 verified against PDFs by script). Row 7.2 done.
  Phase 7.5 QA started. Draft is ~13.4k words vs the plan's 9-11k (question to Sharif).
- **v0.14 · 2026-11-21** — Sharif: an evidence file with every claim's verbatim quote, page and
  location (row 7.5.6, `build_evidence.py` checks quotes against the PDFs), and no social post of the
  paper until his express go order.
- **v0.13 · 2026-11-21** — Phase 7 outline approved by Sharif (Annual Review-style article, thesis
  "verification, not capability"). New Phase 7.5: a thorough QA (100% number, citation, fact and tone
  checks) before the independent grade. Release set for 6:00 AM Sun 2026-11-22 with a video.
- **v0.12 · 2026-11-21** — Phase 6 sweep 2 (Sharif): popularity-led search added 34 automated-science
  and automated-development repos the paper-led sweep missed (237 total); the 12 most-starred cloned
  and written up (groups E, F). New findings: autoresearch-style keep/revert loops map onto the study
  protocol but get gamed when the agent can reach the metric (autoresearch #599); hidden failures
  (#152, #302, v3 #5) mean skipped checks never count as passes; safety hooks must fail closed and be
  tested on Windows (#115).
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
