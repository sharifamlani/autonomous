# research/_templates/

Starting files for a new study. `python scripts/new_study.py <slug> --title "<title>"` copies them
into `research/NNN_<slug>/`:

| File | Role |
|---|---|
| `PREREG.md` | Pre-registration; commit it before any result exists (CLAUDE.md §5 step 1) |
| `RESULT.md` | Result write-up against the pre-registered thresholds, with the bias checklist |
| `replicate.ipynb` | **The single entry point for the study's code** (Sharif directive 2026-10-27): annotated, Run All reproduces everything. Generic `python3` kernel (`pip install -r requirements.txt`); runs headless with `python scripts/research/run_notebook.py <notebook>`, which prints `PASS` only when no cell errors and the verify cell passes. In `_templates/` it runs a toy agent-trial demo (2 arms x 3 runs x 5 tasks: success rate with bootstrap 95% CI, $/task) and writes to a temp folder, so the repo stays clean |

Notebook skeleton (cell order): title -> how to run -> setup (RERUN flag, repo root, seeds) -> helpers
(cache, checksum, `save_figure`) -> load data -> compute (cached) -> headline table -> figures ->
`key_numbers.json` -> verify checksums (PASS/FAIL). Standard: the `research-report` skill,
"Replication notebook standard".
