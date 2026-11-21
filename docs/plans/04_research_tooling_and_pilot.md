# Phase 4 plan — Research tooling, notebook spike and pilot scout

> ROADMAP Phase 4 (rows 4.1–4.7). Written 2026-11-21. Rows 4.1–4.5 are setup; row 4.6 (the first scout
> run) is the start of research and waits on Sharif's go.

## Goal

Prove that research can run unattended before any of it is done: the study notebook runs top to
bottom with nobody pressing anything (promise 2's mechanism), the literature tools catch bad entries
and fetch real papers, and one scout fills one theme to the contract.

## Folder / file structure (only what this phase touches)

```
autonomous/
├── requirements.txt                          # NEW  Python deps for scripts + notebooks (pandas, matplotlib, nbclient, ipykernel, requests)
├── research/_templates/
│   ├── replicate.ipynb                       # EDIT 4.1  Trading's template adapted: generic kernel, repo-root finder, toy agent-trial data
│   └── _README.md                            # EDIT 4.1  drop the "still Trading's version" note
├── scripts/
│   ├── research/run_notebook.py              # NEW  4.1  headless Run All; PASS only if 0 error cells and the verify cell prints PASS
│   └── literature/
│       ├── verify_literature.py              # EDIT 4.2  + README sections, unique IDs, papers.tsv rows, PDF integrity, candidates TSV; --all fixed
│       ├── fetch_papers.py                   # NEW  4.3  papers.tsv -> local PDFs, %PDF check, idempotent
│       └── smoke_sources.py                  # NEW  4.4  arXiv returns %PDF; gh api returns stars/license/archived/pushed_at
├── tests/literature/                         # NEW  4.2–4.3  fixtures with planted defects + pytest for the checker and fetcher
├── .claude/agents/research-scout.md          # NEW  4.5  LOCAL (gitignored): one theme -> folder README + papers.tsv rows + candidates TSV
├── literature/02_Claude_Code_and_Harness_Engineering/   # NEW 4.6 (after go)  README + PDFs (PDFs local only)
├── literature/papers.tsv                     # EDIT 4.6  + theme 02 rows
├── public/_candidates/02.tsv                 # NEW  4.6  repo candidates with gh api metadata
└── docs/plans/04_research_tooling_and_pilot.md   # this plan; scorecard appended at close
```

## Flowchart

```
 SETUP (4.1–4.5, parallel tracks)                          RESEARCH (4.6–4.7, after Sharif's go)
 +-------------------------------+
 | Track A: notebook spike       |
 | adapt replicate.ipynb         |
 |   --> run_notebook.py (headless)--> PASS? --no--> fix, rerun
 +-------------------------------+        |yes
                                          v
 +-------------------------------+   +-----------+     +------------------+     +------------------+
 | Track B: literature tooling   |   | Evaluator |     | Sharif: "go"     |     | research-scout   |
 | verify_literature.py checks   |-->| grades    |---->| (Main asks once) |---->| theme 02         |
 |   --> fetch_papers.py         |   | C1–C5     |     +------------------+     | arXiv / docs /   |
 |   --> smoke_sources.py        |   | (fresh    |                              | gh api           |
 +-------------------------------+   |  context) |                              +--------+---------+
 +-------------------------------+   +-----------+                                       |
 | Track C: research-scout agent |-->      ^ FAIL -> builder fixes, re-grade             v
 | output contract + rules       |                                     folder 02 README, papers.tsv,
 +-------------------------------+                                     _candidates/02.tsv, PDFs (local)
                                                                                         |
                                                                                         v
                                                                  verify_literature.py --all --> Evaluator
                                                                  re-fetches 3 papers, grades C6–C7 --> close
```

## Derisking (in dependency order; smoke N+1 starts only after smoke N passes)

| # | What it proves | Command | Expected | If it fails → |
|---|---|---|---|---|
| S1 | Python can execute a notebook headless on this machine | `python -c "import nbclient, ipykernel"` | exit 0 | `pip install -r requirements.txt`, re-run |
| S2 | The adapted template runs top to bottom unattended (promise 2) | `python scripts/research/run_notebook.py research/_templates/replicate.ipynb` | `PASS: 0 error cells, verify cell PASS` | read the first error cell; fix that step only |
| S3 | The checker catches bad literature entries | `python -m pytest tests/literature -q` | all pass; each planted defect reported | fix the check that missed its defect |
| S4 | The checker passes the real (empty) library | `python scripts/literature/verify_literature.py --all` | exit 0 | fix the false positive |
| S5 | arXiv and GitHub return the data the scout needs | `python scripts/literature/smoke_sources.py` | `arxiv: %PDF ok` and `gh: stars=… license=… archived=… pushed_at=…` | check network / `gh auth status` |
| S6 | Papers can be re-downloaded from the catalogue | `python scripts/literature/fetch_papers.py --tsv tests/literature/fixtures/one_paper.tsv --dest <scratch>` twice | 1st: `fetched 1`; 2nd: `skipped 1`; file starts `%PDF` | inspect URL resolution (abs → pdf) |
| S7 | The scout prompt carries the whole contract | `python scripts/literature/verify_literature.py --agent .claude/agents/research-scout.md` | `agent contract: PASS` | add the missing field to the prompt |
| S8 (after go) | End to end: one scout fills theme 02 to the contract | run the scout; then `verify_literature.py --all` | exit 0; ≥ 8 verified rows for folder 02 | evaluator recommendations → tighten prompt, re-run once |

## Evaluation criteria (definition of done; graded by an independent evaluator)

| # | Criterion | Metric + threshold | How measured | Evidence |
|---|---|---|---|---|
| C1 | A study notebook runs to the end with nobody pressing anything | exit 0; 0 error cells; verify cell prints PASS; 0 matches of `trading` (case-insensitive) in the notebook | `run_notebook.py` on a fresh copy; `grep -ci trading` | run log line in the scorecard |
| C2 | The checker catches each kind of bad entry | 5/5 planted defects flagged (missing README section, duplicate ID, short `papers.tsv` row, non-PDF file, short candidates row); clean fixture exits 0 | `pytest tests/literature -q` | pytest pass line |
| C3 | The real library passes the checker | exit 0 | `verify_literature.py --all` | output tail |
| C4 | Papers come back from the catalogue | 1 real arXiv PDF fetched, starts `%PDF`; 2nd run skips it; bad URL exits non-zero | `fetch_papers.py` on fixture TSVs | output lines |
| C5 | The scout's sources answer | arXiv `%PDF` ok; `gh api` returns all 4 fields for `anthropics/claude-code` | `smoke_sources.py` | output lines |
| C6 | The scout prompt carries the full contract | 4 README sections, 10 `papers.tsv` columns, 8 candidates columns, file-name pattern, "no citation without a fetched source" all present | `verify_literature.py --agent` | PASS line |
| C7 | Nothing private or redistributed reaches the public repo | gitleaks 0 leaks; `git ls-files '*.pdf'` = 0 | gitleaks; git | output |
| C8 (after go) | One scout fills theme 02 correctly | folder 02 passes `--all`; ≥ 8 rows `verified=yes`; 0 short candidates rows; evaluator re-fetches 3 random papers and title/author/year match 3/3 | evaluator, independently | scorecard rows |

Setup closes on C1–C7 PASS from the evaluator. The phase closes on C1–C8.

## Implementation steps

1. Track A (builder): 4.1 notebook adaptation (copy-don't-rewrite: only kernel name, imports, root
   finder, and the toy data block change) + `run_notebook.py` + `requirements.txt`.
2. Track B (builder): 4.2 checker + tests, 4.3 fetcher, 4.4 smoke script.
3. Track C (Main): 4.5 `research-scout` agent prompt.
4. Evaluator (fresh context) grades C1–C7; fix rounds until all PASS.
5. ROADMAP flips for 4.1–4.5; Main asks Sharif for the go on 4.6.
6. After go: 4.6 scout run, 4.7 evaluator grades C8; scorecard appended here.
