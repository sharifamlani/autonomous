# research/_templates/

Starting files for a new study. `python scripts/new_study.py <slug> --title "<title>"` copies them
into `research/NNN_<slug>/`:

| File | Role |
|---|---|
| `PREREG.md` | Pre-registration; commit it before any result exists (CLAUDE.md §5 step 1) |
| `RESULT.md` | Result write-up against the pre-registered thresholds, with the bias checklist |
| `replicate.ipynb` | **The single entry point for the study's code** (Sharif directive 2026-10-27): annotated, Run All reproduces everything. Still Trading's version (kernel, `trading.compute`); adapted to this repo in ROADMAP Phase 3, whose first smoke is a headless Run All of this template |

Notebook skeleton (cell order): title -> how to run -> setup (RERUN flag, repo root, seeds) -> helpers
(cache, checksum, `save_figure`) -> load data -> compute (cached) -> headline table -> figures ->
`key_numbers.json` -> verify checksums (PASS/FAIL). Standard: the `research-report` skill,
"Replication notebook standard".
