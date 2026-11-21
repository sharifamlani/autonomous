---
name: research-report
description: Write the final research report for a finished study in research/NNN_<slug>/ as a short LaTeX white paper (PDF, max 5 pages before the appendix) with figures and tables built from the study's saved outputs. Use when a study has a RESULT.md and saved outputs and needs its final_report/, or when asked to report, write up or publish a study.
---

# Research report protocol (Sharif directive 2026-10-18)

Every study that finishes from 2026-10-18 onward gets a short white paper in
`research/NNN_<slug>/final_report/`. No backfill of earlier studies. Killed and parked studies get
reports too; an honest library of failures is what gives the successes credibility.

## Output

```
research/NNN_<slug>/
├── replicate.ipynb    # THE entry point: all study code in one annotated notebook, saved executed (see "Replication notebook standard")
├── PREREG.md, RESULT.md, output/   # pre-registration, result, saved outputs (written by the notebook)
└── final_report/
    ├── key_numbers.json   # every number the paper quotes, written by replicate.ipynb from the study's saved outputs
    ├── numbers.tex        # generated from key_numbers.json (LaTeX macros); never hand-edited
    ├── report.tex         # from template/report.tex
    ├── refs.bib           # from template/refs.bib plus the study's sources
    ├── figures/*.pdf      # built by replicate.ipynb (or make_figures.py) from saved data, plus figures/manifest.json
    ├── replication.json   # datasets used (vendor, filter, as_of) and the exact commands that produced the results
    ├── replication/       # the replication package, like an academic archive (make_replication.py)
    │   ├── README.md      #   how to reproduce: open replicate.ipynb, select the Trading (Poetry) kernel, Run All; environment, data access, runtime
    │   ├── MANIFEST.json  #   git commit, Python + poetry.lock fingerprints, sha256 of the notebook, code and saved outputs
    │   ├── reproduce.py   #   --verify (checksums) or --run (execute the notebook headless with nbclient, then verify)
    │   ├── replicate.ipynb#   copy of the study's notebook (also in code/ with PREREG.md and RESULT.md)
    │   └── code/          #   copies of the study's code (older studies: their .py scripts), PREREG.md and RESULT.md
    └── report.pdf         # built and checked
```

**Data is never included in the replication package.** Sharadar, Tiingo and Kalshi data are licensed
and cannot be redistributed; the README tells a reader exactly which datasets, filters and as-of dates
to pull with their own access. Public sources (FRED, French, NOAA, GDELT) are named the same way.

## Replication notebook standard (binding; Sharif 2026-10-27)

Sharif's directive (verbatim): "replication code should always be written in a Python Jupyter notebook.
When I come to it and I hit Run or Play, it should run everything, all the code, and produce all the
figures and everything. Right now, you've been putting it into individual .py files, which is fine, but I
don't want you to do that anymore. I want you to put it into a Python notebook that's written and
annotated with the code and that runs smoothly."

- **One notebook per study: `research/NNN_<slug>/replicate.ipynb`**, the single entry point. "Run All" in
  VS Code / Cursor / Jupyter, top to bottom, on the project's Poetry environment (kernel **Trading (Poetry)**,
  name `trading`; register once with `poetry run python scripts/dev/register_kernel.py`), loads the data from
  the store, computes every result, writes the saved outputs (`output/`), builds every figure
  (`final_report/figures/`) and the numbers file (`final_report/key_numbers.json`), and prints the headline
  table. **No study-specific `.py` scripts** for new studies. Reusable logic still belongs in
  `packages/trading/` (CLAUDE.md §8) and is imported by the notebook; the notebook holds the study-specific steps.
- **Annotated.** A title cell (study, question, PREREG commit, verdict once known); a "How to run" cell (kernel,
  Run All, runtime, data needed and licences, the `RERUN` flag); then for every step a markdown cell saying what
  the step does, why, its inputs and outputs, followed by the code cell. Inside cells follow
  `.claude/skills/sharif-code-style` (header block in the first code cell, section comments, `SEED = 1993`).
- **Runs smoothly.** The first code cell finds the repo root by walking up to `pyproject.toml`
  (`.claude/skills/portable-python-paths`), adds `packages/` to `sys.path`, sets the seeds and caps threads and
  memory through `trading.compute`. Heavy steps cache their outputs and skip recomputation unless
  `RERUN = True` (set at the top), so Run All on a finished study is fast and rebuilds the figures from saved
  outputs. No interactive prompts. No hidden state: each cell depends only on earlier cells. The final cell
  verifies `output/` against the manifest checksums and prints PASS / FAIL (it raises on FAIL).
- **Saved executed.** The committed notebook has its outputs and figures visible and contains no error
  outputs. Do not strip outputs (no nbstripout).
- **PREREG first.** `PREREG.md` is still its own commit before the notebook computes any result; the notebook
  title cell names that commit.
- **Start from** `research/_templates/replicate.ipynb` (setup cell with `RERUN`, cache helpers,
  `save_figure` implementing the visualization standard, `key_numbers.json` cell, verify cell). Re-execute
  headless with `poetry run jupyter nbconvert --to notebook --execute --inplace research/NNN_<slug>/replicate.ipynb`
  before committing.
- **Enforced** by `check_report.py`: for studies whose PREREG is dated 2026-10-28 or later (or with
  `--require-notebook`) it fails when `replicate.ipynb` is missing, has error outputs, was not saved executed,
  has no `RERUN` flag, or its last cell did not print PASS; `--execute` also runs it headless and fails if the
  run fails or any `output/` checksum changes. Studies 002-053 keep their `.py` scripts (Study 053 also has a
  notebook as the worked example).
- **Replication package:** `make_replication.py` copies `replicate.ipynb` into `final_report/replication/`
  with PREREG / RESULT, hashes it, and writes a README that says: open `replicate.ipynb`, select the Poetry
  kernel, Run All. `reproduce.py --run` executes the notebook headless, then verifies.

## Wave reports (Sharif 2026-10-18)

When Sharif asks for one report for a whole wave (first: wave 17, the model bake-off, Studies 030+),
the wave report replaces the per-study reports for those studies. It lives in
`research/waveNN_<slug>/final_report/` (the folder also holds a `_README.md` naming its studies),
uses the same structure, rules and visualization standard, and allows **at most 20 pages before the
appendix**. Pass the member studies to the tools:
`make_replication.py research/waveNN_<slug> --studies research/030_a,research/031_b` (code copied to
`replication/code/<study>/`, outputs hashed repo-relative) and
`check_report.py research/waveNN_<slug> --max-pages 20 --studies research/030_a,research/031_b`
(key numbers may trace to any member study's RESULT.md or output json).

## Structure (main article, at most 5 pages before the appendix)

1. **Abstract** (5 sentences max): question, data, method, the verdict, what it changes.
2. **Introduction**: the question and why it matters for the goal (compounded net return).
3. **Literature review** (short): cite by literature ID and paper; what was claimed, gross or net.
4. **Theory**: the mechanism and who pays the edge; the prior before testing.
5. **Methods**: data, universe, period, point-in-time rules, cost model, split and holdout, trial
   count, gate thresholds. State that the plan was pre-registered and give the PREREG commit.
6. **Findings**: lead with what failed. One equity-curve figure, one drawdown figure, one results
   table (gross, net at 0.5x/1x/2x, after tax, versus the benchmark), the gate table.
7. **Conclusions**: the verdict (promote / park / kill) in one paragraph.
8. **Implications for our trading schema**: what changes in the portfolio, the roadmap, the cost
   model or the hypothesis queue. Concrete, one paragraph or a short list.

**Appendix** (unlimited): full tables, sub-periods, robustness and cost sensitivity, the section-5
bias checklist, the trial list, data provenance, the disclaimer.

## Data visualization standard (binding; Sharif 2026-10-18)

Clear, readable figures matter as much as correct numbers. A reader who sees only the figure and its
caption should understand what it shows.

- **Plain-English legends, never column codes.** `spy_bh` becomes "SPY buy-and-hold"; `combo_c05`
  becomes "Trend filter + 5% crypto sleeve". `make_figures.py` requires `--labels` for every series and
  refuses code-like labels (underscores, pipes, bare lowercase tokens).
- **Every figure has a title, labelled axes with units** (%, $, years), readable dates, and a caption
  that says what to look at ("Look at: ...").
- **Benchmark first and visually distinct** (dark grey); candidates in a colour-blind-safe palette; at
  most 5 series per figure; use panels rather than crowd one chart.
- **Tables use readable row and column names** (never variable names), units in the headers, and the
  same plain-English names as the figures.
- **Custom figures** (made outside `make_figures.py`) must add an entry to `figures/manifest.json`
  (`title`, `xlabel`, `ylabel`, `legend`). `check_report.py` fails any included figure that has no entry
  or has code-like legend labels.

## Rules (binding)

- **Numbers come only from saved outputs** (`RESULT.md`, `output/*.json`, `output/*.parquet`).
  Never re-run the study to get a number; never round in the study's favor. Put every quoted number in
  `key_numbers.json`, generate `numbers.tex`, and reference macros in the text (`\NetSharpeOneX`),
  never typed digits for results.
- **Failures first**, net of costs and after tax next to gross, always with the benchmark (SPY or the
  study's benchmark) in the same table.
- Plain English in the abstract, introduction and implications; technical detail in methods and the
  appendix. Short sentences.
- Every figure has a caption that says what to look at.
- Keep the disclaimer in the appendix: research only, hypothetical backtested results, not
  investment, tax or legal advice. Public use needs a securities-law check first (SEC marketing rule).
- Do not edit the study's other files (the study is frozen once its RESULT.md is committed).

## Steps

0. Code: the study's analysis lives in `replicate.ipynb` (see the standard above); run it headless and save
   it executed before writing the report. Figures and `key_numbers.json` come from that notebook.
1. Read the study's `PREREG.md`, `RESULT.md` and `output/` listing.
2. Copy the template: `cp -r .claude/skills/research-report/template research/NNN_<slug>/final_report`.
3. `key_numbers.json` (written by the notebook; or by hand for older studies; flat `{"MacroName": "value-as-printed-in-RESULT"}`; macro names letters
   only), then `poetry run python .claude/skills/research-report/numbers_to_tex.py research/NNN_<slug>/final_report`.
4. Figures: built by the notebook (`save_figure`). For older studies or quick equity/drawdown plots: `poetry run python .claude/skills/research-report/make_figures.py research/NNN_<slug> --cols spy_bh,combo_c05 --labels "spy_bh=SPY buy-and-hold;combo_c05=Trend filter + 5% crypto sleeve"`
   (equity curves and drawdowns from `output/equity_curves.parquet`; benchmark first; add `--returns`
   if the columns are returns). Study-specific figures go in `final_report/figures/` with a manifest
   entry (see the visualization standard).
5. Write `report.tex` sections; fill `refs.bib`. In the appendix, add a short "Replication" section
   pointing to `replication/README.md` and quoting the commit.
5b. Replication package: write `final_report/replication.json` (datasets with vendor, filter and
   as_of; runtime; `steps` are optional when `replicate.ipynb` exists, the default step is the headless notebook run; older studies list their exact commands), then
   `poetry run python .claude/skills/research-report/make_replication.py research/NNN_<slug>`.
6. Build and check: `poetry run python .claude/skills/research-report/check_report.py research/NNN_<slug>` (add `--execute` to re-run the notebook headless; `--notebook-only` while building).
   It runs latexmk, then fails if the main article exceeds 5 pages, a figure is missing, LaTeX left
   undefined references, any value in `key_numbers.json` does not appear in RESULT.md or the saved
   JSON outputs, any figure lacks a readable title, axis labels or plain-English legend, or the
   replication package is incomplete or its checksums do not match the saved outputs. Fix and rerun
   until it prints `PASS`.
7. Commit only `research/NNN_<slug>/final_report/` with `scripts/dev/commit_paths.sh "report: Study NNN final report"`.
