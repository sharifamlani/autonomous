# Phase 9 plan: kit v0.1 design, built to test and iterate

**ROADMAP rows:** 9.1–9.4 · **Status:** approved by Sharif 2026-11-22 (D17–D20) · **Date:** 2026-11-22
**Inputs:** the literature review (`literature/LITERATURE_REVIEW.pdf`, Table 3, Summary Points, §13),
the lessons table in `CLAUDE.md` §0.5 (L1–L11), spike 4.8 (`research/spikes/plugin_team.md`, D15),
and the `claude plugin eval` docs (https://code.claude.com/docs/en/plugin-evals.md, read 2026-11-22).
**Architecture:** `docs/plans/09_kit_v01_architecture.md` (components, run folder, state machines,
file contracts, role fences, caps, the `kit.toml` knobs).

```
AUTONOMOUS — phase plan
─────────────────────────────────
Phase 7-8  : Review, QA, grade, post      [████████████████████] ✅
Phase 9    : Kit v0.1 design (this plan)  [██████████⏸.........] waiting on you
Phase 10   : Benchmark v0.1 (the tests)
Phase 11   : Kit v0.1 build
Phase 12   : v0.1 release (unattended run)
```

## The idea in one paragraph

v0.1 is the smallest kit that can be **measured and improved**, not the most complete one. Think
of it as a test kitchen, not a restaurant: one dish of each kind (one app, one study), a scale that
weighs every plate the same way (the benchmark runner), and a notebook where every change to the
recipe is logged and kept only if the plates get better (the trial log). The review says what goes
in the recipe: the builder never grades its own work; something it cannot edit decides "done".

## What the review tells us to build (and not build)

| Build | Because (review) | Don't build | Because |
|---|---|---|---|
| Hidden acceptance checks written from the spec **before** the build | L1, L3 (strong/moderate) | A big role roster (marketing, auditor, PM) inside the kit; marketing runs as a separate session that reads the kit's release card | L5: roles without an independent check have no accuracy evidence |
| A Tester that uses the running app and records what it saw | L1, L2; Future Issue 1 | An LLM reviewer that reads the builder's summary | L4: 49.4% false approvals in T18 |
| A study path that commits PREREG before data, then one held-out look | L9 | Auto-generated context files, many skills | L7: lean harness |
| Caps on $, time, turns, repeated errors + an honest `STUCK` exit | L8 | "Retry until green" loops with no cap | L8, P5: compounding failures |
| A benchmark with a budget-matched baseline arm and k = 3 runs | L10, L11 | Judging v0.1 by one good run | L10: single runs can't rank |

## Found while planning: the benchmark tool can't run the full tasks

`claude plugin eval` (D11) caps each run at **1 hour and 200 turns**, has **no custom-code graders**
(no pytest, no browser walk after the run), and shell commands need the OS sandbox (**WSL2** on
Windows). Like a bathroom scale that tops out at 50 kg: fine for weighing parts, useless for the
whole truck. So v0.1 uses two scales:

1. **`claude plugin eval`** for fast behaviour checks of single skills (< 1 h, regex/file graders):
   e.g. "new-study commits PREREG before touching held-out data", "builder never says DONE without a
   test-output file".
2. **`benchmark/run.py`** (ours) for the end-to-end tasks: it starts each arm as a `claude -p` run
   with caps, then grades from **outside** the run's folder (pytest, the browser walk, the answer
   key) and writes a scorecard with the same fields as plugin eval (score, delta, cost, duration,
   per-run results).

This changes D11 (decision **9-A** below). It does not narrow the founding promise.

## Folder / file structure

```
autonomous/
├── docs/plans/09_kit_v01_design.md        # THIS plan (Phase 9 exit = Sharif approves it)
├── CLAUDE.md                              # §0.5 lessons L1–L11 (row 7.3, done with this plan)
├── ROADMAP.md                             # D11 revised; rows 9.1–9.4 flipped; Phase 10–12 rows adjusted
├── plugin/                                # THE KIT (built in Phase 11)
│   ├── .claude-plugin/plugin.json         # name "autonomous", version 0.1.0
│   ├── skills/
│   │   ├── new-app/SKILL.md               # Main's playbook: spec -> checks -> build -> QA || walk -> report
│   │   ├── new-app/scripts/team.py        # launcher: one `claude -p` per role, caps, registry (spike 4.8 code)
│   │   ├── new-app/templates/             # spec.md, rubric.md, RUN_REPORT.md
│   │   ├── new-study/SKILL.md             # Main's playbook: scaffold -> PREREG -> dev trials -> 1 look -> replicate
│   │   ├── new-study/scripts/seal.py      # splits data; seals held-out outside the analyst's folder
│   │   ├── new-study/templates/           # PREREG.md, RESULT.md, replicate.ipynb skeleton, TRIAL_LOG.tsv
│   │   └── done-means-evidence/SKILL.md   # L2 rule every role loads: no DONE without artifacts; STUCK exit
│   ├── agents/
│   │   ├── spec-writer.md                 # idea -> spec + hidden acceptance checks (before any code)
│   │   ├── builder.md                     # builds in app/, runs its own app, cannot read checks/
│   │   ├── qa.md                          # runs tests, checks diff against rubric.md (not the builder's story)
│   │   ├── tester.md                      # walks the running app (CUA, isolated profile), screenshots per check
│   │   ├── analyst.md                     # study: PREREG, dev-split trials, notebook
│   │   └── replicator.md                  # study: fresh Run All of replicate.ipynb, checks every number
│   ├── hooks/hooks.json                   # PermissionRequest + PreToolUse hooks
│   ├── hooks/gate.py                      # allow-list; per-role folder fences (builder can't read checks/)
│   └── evals/                             # plugin-eval behaviour cases (< 1 h each)
├── benchmark/                             # THE SCALE (built in Phase 10)
│   ├── _README.md                         # how to run, what each field means
│   ├── run.py                             # arms x tasks x runs; caps; grades from outside; scorecard
│   ├── tasks/app_001/                     # idea prompt, grader (API tests + walk script), calibration pair
│   ├── tasks/study_001/                   # question, data fetch script, grader; answer key kept local only
│   └── results/<kit-version>/<ts>/        # scorecard.json + scorecard.md per benchmark run
├── research/001_kit_v01_vs_baseline/      # the kit evaluated as a study: PREREG before the first scored run
└── research/TRIAL_LOG.tsv                 # one row per benchmark run, never deleted
```

## Flowchart: one benchmark run, and the iteration loop around it

```
 +----------------------+     +--------------------------------------------------------------+
 | benchmark/run.py     |     | RUN FOLDER  runs/<id>/  (temp, short path on Windows)         |
 | --arm kit|baseline   |---->|                                                              |
 | --task app_001|...   |     |  baseline arm: one `claude -p` with the same prompt, model,  |
 | --runs 3             |     |  $ cap and time cap, no plugin                               |
 +----------------------+     |                                                              |
            ^                 |  kit arm: `claude -p "/autonomous:new-app <idea>"`           |
            |                 |    Main -> spec-writer --> spec.md + checks/ (hidden)        |
            |                 |         -> builder (cwd app/, gate.py fences checks/)        |
            |                 |         -> QA (runs tests, rubric) || tester (walks app)     |
            |                 |         -> FAIL? back to builder (max 3 rounds) ---+         |
            |                 |         -> RUN_REPORT.md: DONE | STUCK | CAP <-----+         |
            |                 +------------------------------+-------------------------------+
            |                                                | run ends (or cap kills it)
            |                                                v
            |                 +--------------------------------------------------------------+
            |                 | GRADER (outside the run, never visible to it)                |
            |                 |  app: start app -> API tests + scripted browser walk         |
            |                 |  study: estimate vs answer key; PREREG commit before 1st     |
            |                 |         held-out read (git log + gate.py log)                |
            |                 |  + false-DONE check: report says DONE but grader fails?      |
            |                 +------------------------------+-------------------------------+
            |                                                v
            |                 +------------------------------+-------------------------------+
            |                 | scorecard.json/.md  +  TRIAL_LOG.tsv row (append-only)       |
            |                 +------------------------------+-------------------------------+
            |                                                v
            |                 +--------------------------------------------------------------+
            +-- keep/revert --| ITERATE: one kit change per trial; keep it only if the       |
                              | scorecard improves at equal or lower cost (dev runs, k = 1)   |
                              | release check: k = 3, both arms, independent evaluator        |
                              +--------------------------------------------------------------+

 new-study inside the kit arm:
   seal.py splits data (held-out outside analyst cwd) -> analyst writes PREREG.md -> git commit
   -> dev-split trials (every one logged) -> run.py's held-out script makes the ONE look
   -> replicator (fresh session) Run All replicate.ipynb, checks every number -> RESULT.md
```

**No UI wireframes:** the kit has no screen. What the user sees is `RUN_REPORT.md`; its template
(status, checks passed with screenshot links, cost, hours, interventions) is fixed in Phase 11.

## Derisking (in dependency order; Phase 10–11 execute against these)

| # | What it proves | Command | Expected | If it fails → |
|---|---|---|---|---|
| S1 | A launcher-started `claude -p` session runs under caps and is killed cleanly at the cap | `python benchmark/run.py --arm baseline --task smoke_hello --runs 1 --max-tokens 200000 --max-min 2` | `status=CAP` or `status=DONE`, scorecard written, no orphan `claude` process (`tasklist | grep -c claude` unchanged) | Fix the kill/timeout path in run.py before anything else |
| S2 | The fence works: the builder cannot read `checks/` | `python plugin/hooks/gate.py --selftest` | `8/8 fence cases PASS` (read/glob/grep/bash cat into checks/ all denied for builder; allowed for tester) | Fence is the core of L1; redesign the gate before building roles |
| S3 | Graders are trustworthy instruments (L11) | `python benchmark/run.py --calibrate --task all` | Each grader: known-good scores ≥ threshold, known-bad scores < threshold | Fix the grader; no scored run until it passes |
| S4 | The Tester can walk a running app unattended in an isolated profile (D7) | `python benchmark/run.py --arm kit --task smoke_walk --runs 1` | `tester: 3/3 checks PASS`, 3 screenshots in `runs/<id>/evidence/`, 0 permission prompts | Re-run spike S3b; fall back to Playwright for web apps |
| S5 | The held-out seal holds (L9) | `python benchmark/run.py --arm kit --task smoke_study --runs 1` | gate log shows 0 analyst reads of held-out; PREREG commit time < held-out script time | Tighten seal.py / gate.py |
| S6 | Honest exit: an impossible task ends `STUCK`, not a fake DONE (L8) | `python benchmark/run.py --arm kit --task smoke_impossible --runs 1` | `status=STUCK`, grader confirms no tampering with checks | Strengthen `done-means-evidence`; this is Future Issue 3 |
| S7 | Baseline arm runs both real tasks end to end | `python benchmark/run.py --arm baseline --task all --runs 1` | 2 scorecards, every field filled (score, tokens, minutes) | Fix run.py task wiring |
| S8 | **End to end:** kit arm, both tasks, unattended | `python benchmark/run.py --arm kit --task all --runs 1` | 2 RUN_REPORTs, 2 scorecards, 0 interventions | Route the failing stage to its owner; back to its smoke |

Ground truth after S8: Sharif opens the built app and clicks through it himself; a fresh session
runs `replicate.ipynb` Run All and gets the same estimate.

## Evaluation criteria for kit v0.1 (graded in Phase 12 by an independent evaluator)

| # | Criterion (user's view) | Metric + threshold | How measured | Evidence |
|---|---|---|---|---|
| E1 | "I walk away and it finishes without me" | 0 human interventions in all 6 kit runs (2 tasks × k=3) | run.py intervention counter (permission prompts, manual messages) | scorecard.json `interventions` |
| E2 | "The app works when someone uses it" | ≥ 2 of 3 kit runs pass ≥ 90% of hidden acceptance checks on app_001 | grader: API tests + scripted walk | scorecard + walk screenshots |
| E3 | "The study's number checks out" | ≥ 2 of 3 kit runs within the answer key's tolerance; 3 of 3 commit PREREG before the held-out look | grader + git log + gate log | scorecard + `research/001_*/` |
| E4 | "It never says done when it isn't" | 0 kit runs report DONE while the hidden grader scores below threshold | grader false-DONE check | scorecard `false_done` |
| E5 | "It beats just asking Claude" | kit mean score > baseline mean on each task at the same token and time caps, spread reported | run.py, both arms, k=3 | scorecard `delta`, min/max |
| E6 | "I know what it cost" | every run records tokens, minutes and turns; kit tokens per passed task reported (D22) | run.py | scorecard |
| E7 | "Anyone can install it" | `claude plugin validate plugin --strict` exit 0; install from GitHub on a clean profile lists `/autonomous:new-app` and `/autonomous:new-study` | CLI on a clean profile | log + screenshot |
| E8 | "The scale is honest" | every grader passes its calibration pair before the scored run | `run.py --calibrate` | calibration log |
| E9 | "We can iterate" | one command reproduces the scorecard; one TRIAL_LOG row per run | `run.py --arm kit --task all --runs 3` | `benchmark/results/v0.1.0/`, TRIAL_LOG |

E4 is the thesis of the review turned into a test. If the kit fails it, v0.1 does not ship.

## How iteration works after v0.1 is built

- **Dev loop (cheap):** one kit change → `run.py --arm kit --task all --runs 1` → TRIAL_LOG row →
  keep if score rises at equal or lower cost, else revert. Dev runs never touch the study's held-out
  answer (they use the dev split), so the release check stays clean.
- **Release check (expensive, rare):** k = 3, both arms, independent evaluator, E1–E9.
- **First experiments queued** (the review's open questions, Phase 13): kit with vs without the
  Tester (Future Issue 1), with vs without the STUCK exit (3), separate sessions vs one long session
  (2).

## Decisions for Sharif

| # | Decision | Recommendation |
|---|---|---|
| 9-A | Revise D11: plugin eval for behaviour checks; our `benchmark/run.py` for end-to-end tasks | **Yes**: plugin eval's 1-hour cap and lack of code graders can't run a full app build |
| 9-B | Caps per run | App: 2 h. Study: 1 h. Same caps for both arms. **Revised by D22 (2026-11-22):** dollar caps replaced by usage (token) caps, since runs use Sharif's Claude Code subscription; token ceilings are set from the first measured run |
| 9-C | Model for the runs | Opus 5.5 in both arms for v0.1 (one variable at a time); try cheaper builder models as a later trial |
| 9-D | Where runs execute | Native Windows for v0.1 with `run.py` (proven in spike 4.8); WSL2 only if we use plugin-eval shell grants |
| 9-E | Kit roles in v0.1 | Spec-writer, builder, QA, tester; analyst, replicator; no marketing or auditor agents (L5). Every run writes a release card (`release/`) that an **outside** Marketing session reads (Sharif 2026-11-22: "it can sit outside but not be part of the plugin") |

The benchmark tasks are now a **validation ladder**, planned in `docs/plans/10_benchmark_validation.md`
(Sharif, 2026-11-22): study rungs from reproducing Amlani & Collitt (2021) with its replication package,
to replicating it from the paper alone, to planted effects only we know, to trap tasks (LaLonde, a
leading prompt); app rungs from building an app to planting 20 bugs that QA and the tester must catch.

## Phase 9 evaluation (plan-level; no independent evaluator, D16)

| Criterion | Threshold | How measured |
|---|---|---|
| Plan has tree, flowchart, derisking, criteria | 4/4 sections present | `grep -c "^## Folder\|^## Flowchart\|^## Derisking\|^## Evaluation criteria" docs/plans/09_kit_v01_design.md` = 4 |
| Every principle in review Table 3 maps to a kit part | 10/10 rows mapped | L1–L11 in CLAUDE.md §0.5 cited in this plan's tables |
| Sharif approves 9-A to 9-E | answered | his reply (separate gate, not a criterion) |
