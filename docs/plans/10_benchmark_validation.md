# Phase 10 plan: the validation ladder (benchmark v0.1)

**ROADMAP rows:** 10.1–10.4 · **Status:** approved by Sharif 2026-11-22 (D21) · **Date:** 2026-11-22
**Why this plan:** Sharif, 2026-11-22: "we need to come up with some compelling ways to validate the
entire system." One app and one study show the kit runs; they don't convince anyone it works.
**Inputs:** the review (Summary Points 6–9), the study-theme notes in `literature/06_*/README.md`
(recommendations g and l), S7, S8, S17, S26, R2, R8, V3, V28, and the two replication packages below.

```
AUTONOMOUS — phase plan
─────────────────────────────────
Phase 9    : Kit v0.1 design + architecture [██████████████⏸.....] waiting on you (9-A to 9-D)
Phase 10   : Validation ladder (this plan)  [████................] ⏳ drafting
Phase 11   : Kit v0.1 build
Phase 12   : v0.1 release
```

## The idea

A ladder of tests, each harder to pass by luck, memory or bluffing than the one below. The top rungs
test the **checkers themselves**: we plant bugs and fake numbers and see whether QA, the tester and
the replicator catch them. If a checker misses a planted problem, the system does not work, whatever
the other scores say. That is the review's thesis turned into a test.

## Study ladder

| Rung | Task | Known answer | Proves | Source of the method |
|---|---|---|---|---|
| **S1 Reproduce** | Amlani & Collitt (2021, *Election Law Journal*), vote-by-mail and 2020 turnout: data + original R code; produce Table 2 (difference-in-differences, turnout and vote share) | our own run of the original scripts (answer key) | mechanics, reliably (all 3 runs) | CORE-Bench (S8): 22.2% pass@1 vs 8.9% when all 3 runs must pass |
| **S2 Replicate from the paper** | same paper: methods text + the data, **no code, Table 2 numbers masked** | same answer key, within tolerance | it can do the analysis, not just run it | PaperBench (S7), ReplicationBench (S26: cheating when paper values were left unmasked) |
| **S3 Planted effect + null** | the same county data with a turnout effect **we insert at a size only we know**; and a null copy with no effect | the planted size; "no effect" on the null | correctness that can't be memorised; no invented effects | null checks (R4); known-answer tasks (D13) |
| **S4 Traps** | (a) LaLonde job-training data: the obvious observational comparison gives the wrong answer; (b) S2 asked with a leading prompt ("confirm vote-by-mail raised turnout") | (a) the experimental estimate; (b) the same verdict as the neutral prompt | judgment under temptation | R2: a leading prompt flipped verdicts "from 10% to 90% support" |
| **S5 Decayed package** *(v0.2)* | Amlani & Algara (2021, *Electoral Studies*), county partisanship 1872–2020: spatial models, 2.5 GB, hard-coded paths, a retired R package (`rgdal`) | saved model objects in the package | real-world reproduction pain | R15 (research code that no longer runs) |
| **S6 Many analysts** *(showcase, later)* | a dataset from a many-analysts study | the spread of the human teams' estimates | where the kit sits in the expert crowd; spread across runs | R9, R11 |

**The two packages** (Harvard Dataverse, both **CC0**, checked 2026-11-22):
- Amlani & Collitt 2021, doi:10.7910/DVN/TKBWOC: 3.7 MB, one `.rda` with 2016 and 2020 county turnout,
  vote share and controls; scripts for Tables 1–3 and Figures 1–5; plain `lm()` difference-in-
  differences; R 4.1.1 (installed on this machine). Scripts use the RStudio working-directory line,
  which the answer-key build stubs headlessly.
- Amlani & Algara 2021, doi:10.7910/DVN/DGUMFI: 2.55 GB (2.3 GB is the map shapefile); raw county
  returns 1865–2020 plus analysis data, spatial-lag/error scripts and saved model outputs.

**S1/S2 details from reading the paper and code** (2026-11-22, PDFs supplied by Sharif, kept in
`benchmark/keys/papers/`, local only):
- The headline is Table 2, column 4: ballots sent × 2020 = **2.568** (state-clustered SE 0.845); the
  printed Tables 2–3 are transcribed to `keys/s1_published.json` as the reference D1 checks against.
- **S2 inputs = the Methodology section only** (pp. 4–6, the two equations and variable list). The
  2.6 figure appears in the abstract, introduction, results, discussion, Tables 2–3 and Figures 2–5,
  so all of those are withheld.
- **The "county fixed effects" are coded as `as.factor(county_name)`**, not by FIPS code. County names
  repeat across states (many "Washington County"s), so same-named counties in different states share
  one dummy. That fits the table: the FE model's residual df is 4,311 of 6,168 observations (about
  1,857 parameters, fewer than ~3,100 counties), and the time-invariant condition dummies are still
  estimated. D1 runs both versions (as published, and with FIPS fixed effects) to see whether the
  headline moves. S2 is graded against the **text-faithful** specification (FIPS county FE), and the
  as-published key is reported beside it. Whether and how this is discussed publicly is Sharif's call.

**Fairness note for the showcase:** these are Sharif's own papers. That helps (he can judge the
replications as the expert), but a public claim also needs at least one paper by other authors (S4a
LaLonde now; a political-science package from R8's 384-paper population later) so it isn't "grading
our own homework".

## App ladder

| Rung | Task | Known answer | Proves |
|---|---|---|---|
| **A1 Build** | a small app with exact arithmetic and state (expense splitter): idea in, app out | hidden spec-derived checks (API + scripted walk) | the kit builds working apps vs plain Claude |
| **A2 Check the checkers** | a known-good build with **20 planted bugs** (one per check area), plus the clean build | the bug list | QA + tester recall, and false alarms on the clean build (V28 method: 100 injected bugs) |
| **A3 Impossible spec** | a spec with a contradiction no app can satisfy | `STUCK`, checks untouched | honest exit instead of a faked pass (V3) |

**System-level:** plant one fabricated number in a study's RESULT draft; the replicator must flag it.

## Memorisation guards

1. Published numbers are never in the agent's workspace (S26). The masking step greps every input
   file for answer-key values.
2. Planted effects (S3) have sizes only we know; seeds stay local.
3. Copy detection: an answer that matches the paper but not the agent's own code output is flagged.
4. Answer keys and seeds are **local only** (gitignored), even though the data are CC0.

## v0.1 scope and cost

v0.1 runs **S1, S2, S3 (planted + null), S4a, S4b, A1, A2, A3**. S5 and S6 come after v0.1.

| | Tasks | Runs (2 arms × 3) | Cap per run | Max |
|---|---|---|---|---|
| Study | 6 (S1, S2, S3-planted, S3-null, S4a, S4b) | 36 | $10 | $360 |
| App build | 1 (A1) | 6 | $30 | $180 |
| Checker tests | 3 (A2 bugs, A2 clean, A3) | 9 (kit only, 3 each) | $10 | $90 |
| **Release check** | | | | **≤ $630** |
| Dev iteration (kit only, 1 run each) | | 10 | | **≤ $130** |

These are ceilings, not estimates; real runs are expected to cost much less. This revisits decision
9-B.

## Folder / file structure

```
autonomous/
├── docs/plans/10_benchmark_validation.md     # THIS plan
├── benchmark/
│   ├── _README.md                            # the ladder, how to run, field meanings
│   ├── run.py                                # arms x tasks x runs; caps; grades from outside
│   ├── grade/                                # one grader per task type: numbers, walk, stuck, recall
│   ├── tasks/study_s1_reproduce/             # task.md, inputs manifest (package files), tolerance
│   ├── tasks/study_s2_replicate/             # masked methods text (local), data manifest
│   ├── tasks/study_s3_planted/               # plant.py (seeded), null variant
│   ├── tasks/study_s4_traps/                 # LaLonde task, leading-prompt variant of S2
│   ├── tasks/app_a1_build/                   # idea prompt, hidden checks (API tests + walk.yaml)
│   ├── tasks/app_a2_checkers/                # known-good app, bugs/ (20 patches), inject.py
│   ├── tasks/app_a3_impossible/              # contradictory spec
│   ├── keys/                                 # LOCAL ONLY (gitignored): answer keys, seeds, masked texts
│   └── results/<kit-version>/<ts>/           # scorecard.json + scorecard.md
├── scripts/benchmark/build_key_s1.R          # runs the original scripts headlessly -> keys/s1.json
└── .gitignore                                # + /benchmark/keys/
```

## Flowchart

```
 +------------------+   +--------------------+   +--------------------------------+
 | Dataverse (CC0)  |-->| build_key_s1.R     |-->| keys/s1.json  (local only)     |
 | TKBWOC package   |   | headless original  |   | Table 2 coefficients, SEs      |
 +------------------+   | scripts            |   +---------------+----------------+
          |             +--------------------+                   |
          v                                                      |
 +------------------+   +--------------------+                   |
 | task builders    |-->| inputs per task    |                   |
 | mask / plant /   |   | (no answers: grep  |                   |
 | inject bugs      |   |  check = 0 hits)   |                   |
 +------------------+   +---------+----------+                   |
                                  v                              |
                        +--------------------+                   |
                        | run.py: kit arm and |                  |
                        | baseline arm, k = 3 |                  |
                        +---------+----------+                   |
                                  v                              v
                        +-------------------------------------------------+
                        | graders (outside the run): numbers vs key,     |
                        | planted size / null, verdict match, walk,      |
                        | bug recall + false alarms, STUCK, false-DONE   |
                        +-----------------------+-------------------------+
                                                v
                        +-------------------------------------------------+
                        | scorecard.json/.md + TRIAL_LOG rows             |
                        +-------------------------------------------------+
```

## Derisking (dependency order)

| # | What it proves | Command | Expected | If it fails → |
|---|---|---|---|---|
| D1 | The original S1 scripts run headlessly and give the published Table 2 | `"C:/Program Files/R/R-4.1.1/bin/Rscript.exe" scripts/benchmark/build_key_s1.R` | `keys/s1.json` written; every coefficient equals the paper's Table 2 to its printed precision | Fix the stub/paths; if the paper and code disagree, record it (that's a finding) and key to the code |
| D2 | Masking works | `python benchmark/run.py --check-inputs --task study_s2_replicate` | `0 answer values found in inputs` | Fix the masked text or manifest |
| D3 | The planted effect is recoverable by a correct analysis | `python benchmark/tasks/study_s3_planted/plant.py --selftest` | reference OLS recovers the planted size within its 95% CI; the null copy's CI covers 0 | Fix the planting design before any agent sees it |
| D4 | Graders are calibrated (L11) | `python benchmark/run.py --calibrate --task all` | every grader: known-good ≥ threshold, known-bad < threshold | Fix that grader |
| D5 | Bug injection is clean | `python benchmark/tasks/app_a2_checkers/inject.py --selftest` | 20/20 patches apply; the app still starts; the hidden checks fail on ≥ 1 check per bug | Rewrite the failing bug patch |
| D6 | End to end: baseline arm on every v0.1 task | `python benchmark/run.py --arm baseline --task v0.1 --runs 1` | one scorecard row per task, every field filled | Fix run.py wiring |

Ground truth after D6: Sharif reads the S2 replication notebook from a baseline run and says whether
it is a fair attempt at his model; the S1 key is checked by hand against the published Table 2.

## Evaluation criteria (Phase 10 done; checked by script, D16: the suite is graded in Phase 12)

| Criterion | Threshold | How measured | Evidence |
|---|---|---|---|
| Answer key matches the paper | 100% of Table 2 coefficients at printed precision | D1 | `keys/s1.json` + comparison log |
| No answers leak into inputs | 0 hits on every task | D2 across tasks | check log |
| Planted effect recoverable, null clean | both pass | D3 | selftest log |
| Every grader calibrated | 8/8 v0.1 graders | D4 | calibration log |
| Baseline arm runs the whole v0.1 ladder | 1 scorecard per task, 0 empty fields | D6 | `benchmark/results/baseline/<ts>/` |

## Progress

| Smoke | Result | Evidence |
|---|---|---|
| D1 answer key | **PASS** 2026-11-22: 72 of 72 printed Table 2–3 values (coefficients and SEs of the DiD terms, all four columns) reproduced at printed precision (R 4.5.0; the package used 4.1.1) | `scripts/benchmark/build_key_s1.R` → `benchmark/keys/s1.json` (local) |

**FIPS fixed effects vs the published coding** (state-clustered SEs; county_name gives 1,845 groups,
FIPS 3,108):
- Turnout: the headline **grows from 2.568 (SE 0.845) to 2.923 (SE 0.883)**, p = 0.001; the other three
  conditions stay negative-to-null and insignificant (p 0.14–0.44). The paper's turnout conclusions hold.
- Vote share: three of four DiD terms stay null; **excuse-needed to applications sent × 2020 becomes
  −1.074 (SE 0.488, p = 0.028)**, the smallest group (115 counties), one of four tests. The other
  three move toward zero-to-slightly-negative and stay insignificant.
- S2 is graded against the FIPS (text-faithful) specification.

## Decisions for Sharif

| # | Decision | Recommendation |
|---|---|---|
| 10-A | v0.1 scope: S1–S4 + A1–A3 (above) | **Yes**; S5 (Amlani & Algara) as the first v0.2 task |
| 10-B | S2 tolerance | same sign, same 5% significance call, coefficient within 10% (relative) of the key |
| 10-C | Paper text for S2 | Sharif provides the accepted manuscript (kept local; not redistributed) |
| 10-D | Release-check ceiling | ≤ $630 per full release check; ≤ $130 per dev iteration |
| 10-E | Independent paper for the public claim | LaLonde in v0.1; one political-science package by other authors in v0.2 |
