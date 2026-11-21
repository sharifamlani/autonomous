---
name: rerun-bakeoff
description: Rerun the model/feature bake-off engine (packages/trading/factory/bakeoff, configs in config/bakeoff) when new data has landed in the store, a new dataset adapter or feature was added, a model was added, or Sharif asks to retest models or features. Covers ingest + verify, adding an adapter/feature, validate, plan, pre-registration, incremental run, verification, comparison with the previous run, the forward-test evidence rule, committing, and troubleshooting.
---

# Rerun the bake-off (new data, new feature, new model)

The engine turns every wave-17-style model/feature test into a CONFIG (`config/bakeoff/<name>.yaml`).
Nothing is bespoke code. A rerun on new data is a short, mostly-cached command sequence. This skill is
the one process; follow it in order. ROADMAP row 13.15.

```
 new data lands --> ingest + verify_data --> [new source? add adapter + features + config]
        --> bakeoff.py validate --> bakeoff.py plan --> [PREREG note if new/changed config]
        --> bakeoff.py run (incremental) --> verify_bakeoff_run.py --> bakeoff.py compare
        --> commit summary + manifest --> ROADMAP / research-report if a verdict changes
```

All commands run from the repo root with `poetry run python ...` (on this machine the venv python is
faster to start than `poetry run`; either works). `<cfg>` is a name in `config/bakeoff/` (no `.yaml`).

## 0. What the engine guarantees (so you do not re-check it)

- **No look-ahead.** Slow data (macro vintages, fundamentals, S&P 500 membership) is placed on the decision
  calendar by the date it became KNOWABLE. Every feature is checked by truncating the panel at probe dates:
  values at dates <= the cut must not change (`validate` runs this; `run` runs it once per feature version).
  This guard is a PROBABILISTIC backstop, not a proof: it uses spread cuts, 64 consecutive cuts and about n/6 seeded
  random cuts (time-budgeted). A one-day peek on ~1% of dates is caught with >99% probability on a 3000-date panel,
  but a much sparser peek can still pass. The real defences are the declared `lag` and knowledge-time placement; write
  features from `P.wide(...)` with only backward-looking ops (no `shift(-k)`, centred windows, or full-sample stats).
- **One cost model.** Net scores go through `trading.backtest.costs` (`round_trip_bps`, `carry_cost`) at 0.5/1/2x
  and `trading.backtest.tax` for after-tax. Gross-only numbers are never headline numbers.
- **Everything is a registered trial** (`trading.factory.trial_log`) BEFORE it runs; the holdout goes through
  `trading.factory.holdout` (one look per family); the gate uses the true cumulative trial count.
- **Caches are derived and rebuildable** (`<TRADING_DATA_DIR>/derived_cache/bakeoff/`), never inside the
  append-only store; the engine never deletes anything.

## 1. New data lands

Ingest with the existing scripts (e.g. `scripts/update_daily.py`, `scripts/ingest_tiingo.py`,
`scripts/ingest_fred.py`, `scripts/ingest_sharadar.py`, `scripts/ingest_crypto.py`, `scripts/ingest_kalshi.py`),
then:

```bash
poetry run python scripts/verify_data.py
```

Stop here if verify fails; fix the data first. Do not run models on data that failed verification.

## 2. Is it a NEW source?

| Situation | What to do |
|---|---|
| More rows of a source an existing config already reads | Nothing to add. Go to step 3. |
| New columns/series of an existing source | Add the names to the adapter params in the config (e.g. `fred_series.series`). `field:<column>` features need no code. |
| A brand-new vendor/dataset | First follow `.claude/skills/add-data-connector/SKILL.md` (connector kit: ingest, probe, `config/data_sources/<vendor>.yaml` with a `kit:` block, verify). Do not re-document that here. Then read it in the engine with the generic adapter: `{adapter: kit_dataset, params: {dataset: <store dataset>, value_cols: [...], asset_col: <col or omit for a global series>, prefix: x_}}`. Values are placed by KNOWLEDGE date; every `value_col` becomes `field:<prefix><col>` (per asset) or `series:<prefix><col>`. |
| A source the generic adapter cannot express | Add ONE adapter function + decorator in `packages/trading/factory/bakeoff/datasets.py` (template below), then a config source entry. |
| A new feature idea | Add ONE `@feature(...)` function in `packages/trading/factory/bakeoff/features.py` (template below), then list its name in a feature set. |
| A new model | Add one `@model(...)` factory in `models.py`, then list it under `models:` in the config. |

**Adapter template** (turns the point-in-time store into a Panel; knowledge time must be respected):

```python
@adapter("my_vendor_daily", needs_calendar=False, store_datasets=("my_dataset",),
         doc="what it holds")
def my_vendor_daily(ctx: AdapterCtx, tickers: list[str], start: str | None = None) -> SourceData:
    df = read_asof(ctx, "my_dataset", keys=["ticker", "event_time"],
                   columns=["ticker", "event_time", "my_col"], where=_in_list("ticker", tickers))
    return SourceData({"my_col": wide(df, "my_col")}, {}, len(df), _max_kt(df))
```

- Price-like sources define the decision calendar (`needs_calendar=False`). Slow sources (`needs_calendar=True`)
  must place values by KNOWLEDGE date: use `known_on_calendar(values, kdates, ctx.calendar)`.
- `store_datasets` lists the store datasets read, so the panel cache invalidates when a new batch lands.
- A panel field named `my_col` is immediately usable as the feature `field:my_col` (zero extra code).

**Feature template** (pure function of the panel; the registry enforces no look-ahead):

```python
@feature("my_skip1_ret_{n}d", label="{n}-day return skipping the latest day", family="price",
         lookback=lambda n: n + 1, inputs=("adjClose",), lag=0, grid={"n": [5, 21, 63]})
def f_skip1_ret(P, n):
    px = P.wide("adjClose")
    return (px.shift(1) / px.shift(n + 1) - 1)                     # wide frame (date x asset), or a Series to broadcast
```

Pick a NAME THAT IS NOT ALREADY REGISTERED (grep `@feature(` in features.py): the built-in `ret_{n}d`, `max_ret_21d`, etc. exist, and re-registering a name raises
`already registered`.

Declare `inputs` (panel field names; `series:<name>` for global series) so the feature cache invalidates only
when ITS inputs change. Declare `lag` for publication delay. Never use `shift(-k)`, centred windows, or
full-sample statistics: the guard rejects them.

**Config.** Copy `config/bakeoff/etf_smoke.yaml`, edit `dataset.sources`, `feature_sets`, `models`,
`walk_forward`, `governance` (`prereg_required: true`, `log_target: shared` for real research).
Feature sets are grouped into FAMILIES; ablation (`ablation.enabled: true`) builds the engine's
`__all` / `__all_minus_<family>` cells automatically.

## Compute (binding)

The runner calls `compute.apply(compute.budget())` at the start of every run (TRADING_THREADS, default 6, never
raise it). The config's `compute:` section is mapped onto that budget: `n_jobs` is capped at the budget threads and
`n_jobs x lgbm_jobs` never exceeds it. Before a heavy run: `poetry run python scripts/dev/resource_monitor.py gate`
and proceed only on `GATE OK`. The manifest records `compute` (threads, n_jobs, lgbm_jobs, torch_threads, device).
The torch forecasters in `trading.models.ml` are CPU-only today, so `device_used` is `cpu` even when CUDA exists.

## 3. Validate, then plan

```bash
poetry run python scripts/bakeoff.py validate <cfg>     # schema, names resolve, cost schedule, no-look-ahead guard -> VALIDATE PASS
poetry run python scripts/bakeoff.py plan <cfg>         # cells, cache status per cell, origins to fit, estimated fits (fits nothing)
```

`plan` statuses: `hit` (nothing to fit), `partial` (new origins only), `miss` (first time), `refit:history revised`
(the vendor revised old rows, so that cell refits into a new cache generation), `refit:origin grid changed`.
A pure data refresh should show `partial`/`hit` everywhere. Many `miss`/`refit` rows after a pure refresh
mean something upstream changed: stop and read the reason.

## 4. Pre-registration rule

| Change | PREREG needed? |
|---|---|
| Pure data refresh of an UNCHANGED config | No new note. Still a logged trial set (every cell and ensemble is registered per run). |
| New config, or any material change (features, models, target, walk-forward, rule, costs, universe) | YES: dated note `research/bakeoffs/<cfg>/PREREG.md`, committed BEFORE the run. |

The engine refuses to run a `prereg_required` config whose PREREG.md is missing, uncommitted or edited.
Use `scripts/dev/commit_paths.sh "bakeoff: <cfg> PREREG <date>" research/bakeoffs/<cfg>/PREREG.md`.

Template (`research/bakeoffs/<cfg>/PREREG.md`):

```markdown
# Bake-off pre-registration: <cfg> (<YYYY-MM-DD>)
| Field | Entry |
|---|---|
| Config | config/bakeoff/<cfg>.yaml, sha256 <first 12 of `validate` output> |
| What changed vs the previous version | <new data source / new features / new models / nothing (data refresh)> |
| Hypothesis | <which feature family or model should help, and the mechanism> |
| Primary metric | dev R2_OOS vs the causal historical mean; rank IC (NW t); net Sharpe at 1x costs |
| Pass thresholds | BY q=10% on the feature screen; gate: t>3, DSR>=0.95, PBO<0.2, survives 2x costs |
| Evidence window | first run: last 20% of dates (one look). Reruns: ONLY dates after the previous run's last date |
| Trial budget | <n cells + ensembles>; cumulative count is read from the trial log |
| Abandonment rule | <e.g. a feature family with no BY survivor and non-positive ablation delta is dropped> |
```

## 5. Run (incremental)

```bash
poetry run python scripts/bakeoff.py run <cfg>                  # default --incremental: cached cells reuse history, fit only NEW origins
poetry run python scripts/bakeoff.py run <cfg> --as-of 2026-10-16   # knowledge cut-off (default: latest in the store)
poetry run python scripts/bakeoff.py run <cfg> --cells 'ridge__*'   # subset of cells (comma-separated globs on cell ids)
poetry run python scripts/bakeoff.py run <cfg> --full               # refit every cell from scratch into a new cache generation
```

Cell ids: `<model>__<feature set>`; feature-free baselines are just `<model>`; ablation cells are
`<model>____all` and `<model>____all_minus_<family>`. Outputs: `research/bakeoffs/<cfg>/runs/<run_id>/`
(see `research/bakeoffs/_README.md`). Compute caps come from the config (`compute.n_jobs`, `torch_threads`,
`lgbm_jobs`): keep them at 2-3 on the shared 16-core, no-GPU machine.

## 6. Verify the run

```bash
poetry run python scripts/verify_bakeoff_run.py <cfg>     # latest run; or <cfg>/<run_id>, or a run directory
```

Must print `VERIFY PASS`. It re-reads every artifact, checks it exists, parses and matches its manifest sha256,
and that `config.json` hashes to the manifest's config sha256.

## 7. Compare with the previous run

```bash
poetry run python scripts/bakeoff.py compare <cfg>/<previous_run_id> <cfg>/<new_run_id>
poetry run python scripts/bakeoff.py report <cfg>          # writes SUMMARY.md in the latest run
```

The comparison says in plain English which data fingerprints changed (new dates, revised content, new
sources), which cells were cached vs refit, how each model's and feature's dev scores moved, which features
joined or left the BY-survivor list, and what the forward window showed.

## 8. What counts as evidence

- **First run of a config:** the last 20% of dates is the holdout, looked at ONCE (family = config name).
- **Reruns on new data:** the engine opens a NEW family `<cfg>@<last date>` over ONLY the dates after the previous
  opened window. That forward window is the only new evidence. A window of fewer than 10 new dates is not opened
  (it waits and grows). Dev scores stay frozen at the first window's start and are descriptive.
- The engine **refuses** to score any date range an earlier family opened (`WindowReopenedError`) and refuses an
  `--as-of` earlier than the last opened date. Never work around this; a "second look" is a logged trial.
- Read forward results as: net of costs (1x and 2x), with the cumulative trial count, never gross. A strategy only
  moves toward paper trading through the CLAUDE.md section 6 ladder; the bake-off alone promotes nothing.

## 9. Commit

```bash
bash scripts/dev/commit_paths.sh "bakeoff: <cfg> run <run_id> (<what changed>)" \
  research/bakeoffs/<cfg>/runs/<run_id> research/bakeoffs/<cfg>/LATEST
```

Add `trial_log.tsv` for `log_target: local` configs. If a verdict changes, update ROADMAP.md (flip the row with
date + SHA, refresh section 0, add a section 6 changelog line, bump the version).

## 10. Optional: write-up

Feed `scoreboard.json`, `feature_screen.json`, `MANIFEST.json` to the `research-report` skill
(`.claude/skills/research-report/`); every quoted number must come from the saved outputs.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `LookAheadError: feature X uses future data` | The feature changes when later rows are removed | Remove `shift(-k)`/centred windows/full-sample z-scores; use causal expanding stats |
| `MissingInput: feature needs panel input ...` | Feature reads a field/series the config's sources do not provide | Add the source/series to `dataset.sources`, or drop the feature |
| `AdapterError: dataset ... is not in the store` | Data never ingested | Run the ingest script, then `verify_data.py` |
| `PreregMissing` | prereg_required config with no committed note | Write + commit `research/bakeoffs/<cfg>/PREREG.md` |
| `WindowReopenedError` | `--as-of` before an opened window, or a manual attempt to rescore it | Use a later `--as-of`; do not reopen windows |
| Every cell `refit:history revised` after a refresh | The vendor revised old rows (or a feature's code changed, which changes its version) | Expected after a vendor revision; otherwise check `git diff` on features.py |
| `plan` shows `miss` for all cells | Config changed materially (new cell hashes) or a new cache generation | Expected for a new config; add a PREREG note |
| `skipped_cells` lists a model | Optional dependency missing (e.g. Chronos: set `CHRONOS_DEPS_DIR`) | Install per research/016 RESULT.md, or ignore |
| Run is slow | Too many origins x grid points x seeds | Raise `refit_every`, shrink grids, `compute.subsample_dates`, cut `n_estimators` |
| `not enough data: first origin ...` | `walk_forward.min_train` too large for the panel | Lower `min_train` or add history |
| `trial log is locked` | Another process holds the DuckDB writer lock | Retry; do not delete the lock file |

## Cache and prune rules

- Location: `<TRADING_DATA_DIR>/derived_cache/bakeoff/{features,cells,panels,lookahead_ok,runs_big,state}`.
  Set `BAKEOFF_CACHE_DIR=<empty dir>` to use a FRESH cache while still reading the real store. This is how to
  time a cold run (do not repoint `TRADING_DATA_DIR`: that moves the store too). Cold vs warm timing test:
  `BAKEOFF_CACHE_DIR=$(mktemp -d) poetry run python scripts/bakeoff.py run etf_smoke` twice with the same value;
  compare `timings.total` in the two MANIFEST.json files (each run also adds a logged trial set).
- Keys: features = sha256(name + code version + params + hash of ITS inputs + effective as_of); cells = sha256(model,
  grid, feature ids + their code versions, target, walk-forward, seeds, universe, sources); panels = sources + as_of
  + file listing of the store datasets read. New data invalidates only what its inputs touch.
- The engine only ever creates files (exclusive create); a changed input writes a new key or generation.
- To reclaim disk: `poetry run python scripts/bakeoff.py prune --days 90` PRINTS what it would remove. Only a human
  adds `--yes`. The append-only data store is never touched by prune.
- Do not delete `state/` (it holds isolated trial logs and holdout windows for `log_target: local` configs).

## Where things live

```
packages/trading/factory/bakeoff/   config, datasets, features, models, ensembles, runner, scoring, features_test,
                               governance, compare, manifest, cache
config/bakeoff/<cfg>.yaml      the bake-off definitions (etf_smoke = fast template, synthetic_planted = engine test)
scripts/bakeoff.py             validate | plan | run | compare | report | list | features | prune
scripts/verify_bakeoff_run.py  artifact + checksum verification
research/bakeoffs/<cfg>/       PREREG.md, LATEST, runs/<run_id>/ (MANIFEST.json + artifacts)
tests/factory/bakeoff/         engine tests; tests/qa/test_eng_bakeoff_etf_smoke.py = real-store Tier 5
```
