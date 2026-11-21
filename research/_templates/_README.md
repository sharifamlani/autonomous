# research/_templates/

Starting files for a new study. Copy into `research/NNN_<slug>/`:

| File | Role |
|---|---|
| `PREREG.md` | Pre-registration; commit it before any result exists (CLAUDE.md §5 step 1) |
| `RESULT.md` | Result write-up against the pre-registered gate |
| `replicate.ipynb` | **The single entry point for the study's code** (Sharif directive 2026-10-27): annotated, Run All reproduces everything. Kernel "Trading (Poetry)". The template runs a toy demo on synthetic data and writes to a temp folder; set `STUDY_SLUG` in the setup cell and replace the step bodies |

Notebook skeleton (cell order): title -> how to run -> setup (RERUN flag, repo root, seeds, `trading.compute`)
-> helpers (cache, checksum, `save_figure`) -> load data -> compute (cached) -> headline table -> figures ->
`key_numbers.json` -> verify checksums (PASS/FAIL). Standard: `.claude/skills/research-report/SKILL.md`,
"Replication notebook standard". The template is committed executed; re-execute it after editing:
`poetry run jupyter nbconvert --to notebook --execute --inplace research/_templates/replicate.ipynb`.
