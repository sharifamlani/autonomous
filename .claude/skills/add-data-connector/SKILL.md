---
name: add-data-connector
description: Use when adding any new data source or API to the trading repo, or when Sharif names a vendor (Moody's Data Buffet, FRED-like APIs, OECD/IMF/ECB, USDA, SEC, CFTC, a CSV/ZIP on an official site). Scaffolds a connector on the connector kit so the work is "inject a small adapter", never "write a connector from scratch".
---

# Add a data connector (connector kit)

Sharif's directive (2026-10-19): every fund has the same models, **the edge is the data**, and we do not rewrite code for the sake of rewriting code. The kit in `packages/trading/connectors/kit/` already contains auth, rate limiting, retries, pagination, raw-kept, de-duplication, revisions, cursors, probe, CLI, scheduling and verification. A new source supplies only three small functions.

Do NOT refactor the 11 older connectors (tiingo, fred, sharadar, coinbase, kalshi, gdelt, noaa, fomc, benchmarks...). They work. New sources use the kit.

## The process (do the steps in order; commit after each with `bash scripts/dev/commit_paths.sh "<vendor>: <msg>" <paths>`)

1. **Catalog and priority.** Look for the vendor in `docs/data_catalog/` (`catalog.yaml`, owned by the data-catalog track; if the folder does not exist yet, say so in your notes and continue). Take its priority, cost, access method and licence from there. ROADMAP.md first: new work needs a section 3 row.
2. **Licence and cost gate (CLAUDE.md section 7).**
   - Free and public: go on.
   - Paid, a subscription, or a free account/API key: **Sharif's explicit approval** is needed to buy; **Sharif creates every account and signs in himself** (Claude never creates accounts or types passwords); Sharif pastes the key into `.env` (gitignored). Claude never prints, greps or commits a secret; read it only with `trading.envfile.get_secret`.
   - **The gate is enforced by code:** the scaffold ships `licence: TODO ...`; while it is empty or TODO, `probe_<vendor>.py` prints `FAIL licence recorded in yaml`, `ingest_<vendor>.py` refuses (exit 2), the daily runner reports `BLOCKED`, the scheduler adds no release job, and `verify_data.py` fails `kit licence recorded`. Replace it with the real terms first.
   - Write the licence terms into the vendor yaml `licence:` field and `<data dir>/raw/<vendor>/_LICENSE.md` (section 8: data is never deleted; if a licence demands deletion on cancel, say that keeping the subscription is the compliant way to keep the data).
3. **Scaffold.**
   `poetry run python scripts/new_connector.py <vendor> --protocol rest|bulk|socrata|sdmx|xbrl [--base-url URL] [--secret-env NAME] [--dataset NAME] [--keys a,b] [--out DIR] [--data-dir DIR] [--dry-run]`
   **The script targets the repo it lives in, NOT your current folder** (running it by absolute path or `poetry --directory <repo> run` from a scratch folder still writes into the repo and TRADING_DATA_DIR). It prints a `TARGET repo tree` / `TARGET data dir` banner first. For a trial run add `--out <scratch folder>` (repo-shaped tree under that folder, licence stub in `<out>/_data`; the repo and the real data dir are untouched), or `--dry-run`.
   Writes the adapter module, the vendor yaml (with the `kit:` block), `scripts/ingest_<vendor>.py`, `scripts/probe_<vendor>.py`, a fixture test and the licence stub. It passes its own tests immediately; then you make it real.
   - **`--out` trees are for reading the generated code only.** Their tests and probe cannot run there (`trading` resolves to the repo package, which has no module for the toy vendor). To exercise a throwaway connector end to end, scaffold into the repo with `--data-dir <scratch>` so no real data is touched, run its tests, then delete the toy files you created before committing anything.
   - **A scaffolded vendor turns the shared `verify_data.py` red** (`FAIL <vendor> kit licence recorded`) until its licence is filled in (step 2). This is deliberate (the licence gate), so fill the licence first and never leave a half-built connector uncommitted at the end of a session.
4. **Inject the adapter.** In `packages/trading/connectors/<vendor>.py` edit only: `fetch_main(conn, since, end)` (yield `Payload`s, raw bytes untouched), `normalise_main(payload)` (tidy rows), `sample_main(conn)` (a few rows for the probe) and the `DatasetSpec` line. Choose `knowledge_time` with the table below. Fill the yaml `description`, `keys`, `rate_limit` (the vendor's stated limit, with margin), `kit.schedule`.
5. **Record a fixture and test (Tier 1/2).** Save one real response to `tests/fixtures/<vendor>/` (small: trim to a few rows; never include a key). Tighten `tests/connectors/test_<vendor>.py`: exact row count, a known value, the knowledge_time of one row computed by hand. Run `poetry run pytest tests/connectors/test_<vendor>.py -q`.
6. **Probe (Tier 4).** `poetry run python scripts/probe_<vendor>.py` must end with a `PASS` line (it proves auth, reachability, parse, no look-ahead, unique keys). A FAIL line names the check.
7. **Backfill (background, rate limited).** Start with a documented subset (set `default_start` in the spec to the subset start), run `poetry run python scripts/ingest_<vendor>.py --full` in the background and poll; the kit keeps every raw page. Cap one session at about 150 minutes: if the full history is larger, ingest the subset and leave the full command in the notes (`--since 1990-01-01`).
8. **Tier 5 ground truth.** `poetry run python scripts/verify_data.py`: the old checks must keep their PASS count and the new vendor adds its own (raw per batch, no look-ahead, no duplicate keys, key columns, freshness). Spot-check a few values against the vendor's own website.
9. **Schedule.** Nothing to edit: the `kit:` block in the vendor yaml is auto-discovered by `packages/trading/connectors/kit/runner.py` (the `ingest_registered` step of `config/pipeline.yaml`), by `deploy/scheduler.py` (`on-release` + `release_cron` gets its own job) and by `verify_data.py`. Check with `poetry run python deploy/scheduler.py --dry-run` (a `KIT <vendor>` line) and `poetry run python packages/trading/connectors/kit/runner.py --dry-run`.
10. **Hook it to the models (next section) and record it** in `docs/data_catalog/catalog.yaml`: on each connected entry set the free-string field `already_connected:` (the file has no list format) to `'yes: packages/trading/connectors/<vendor>.py (dataset <store dataset>, from <start>; <date>; commit <sha>)'`. Existing examples: the `cftc_cot_*` and `sec_xbrl_companyfacts` entries.

## Hook-up to the bake-off engine

`packages/trading/factory/bakeoff/datasets.py` is the registry. An adapter is one function and one decorator (check this note against the file when its API changes; last checked 2026-10-19):

```python
from trading.connectors.kit.reader import read_guarded
from trading.factory.bakeoff.datasets import adapter, AdapterCtx, SourceData, known_on_calendar, _kdate, _max_kt

@adapter("cftc_cot", store_datasets=("cftc_cot_legacy",), needs_calendar=True,
         doc="CFTC Commitments of Traders net speculative position (% of open interest), by market code")
def cftc_cot(ctx: AdapterCtx, markets: list[str]) -> SourceData:
    # read_guarded, NOT read_asof: it applies the dataset's knowledge_guard (yaml) before the as-of cut
    df = read_guarded(ctx.store, "cftc_cot_legacy", keys=["cftc_contract_market_code", "event_time"],
                      as_of=ctx.as_of,
                      columns=["cftc_contract_market_code", "event_time", "noncomm_positions_long_all",
                               "noncomm_positions_short_all", "open_interest_all"],
                      where="cftc_contract_market_code IN (" + ", ".join(f"'{m}'" for m in markets) + ")")
    out = {}
    for code, g in df.groupby("cftc_contract_market_code"):
        net = (g["noncomm_positions_long_all"] - g["noncomm_positions_short_all"]) / g["open_interest_all"]
        out[f"cot_net_{code}"] = known_on_calendar(net, _kdate(g["knowledge_time"]), ctx.calendar)
    return SourceData({}, out, len(df), _max_kt(df))
```

Rules: read through `read_asof` (it applies `knowledge_time <= as_of`) for ordinary datasets, and through `trading.connectors.kit.reader.read_guarded` for any dataset whose yaml declares `knowledge_guard:` (it applies the guard to every stored version first); put slow data on the decision calendar with `known_on_calendar` (by the date it became knowable, never by `event_time`); list the store datasets in `store_datasets` so the panel cache refreshes when new batches land. Then add the adapter name to a bake-off config `dataset.sources` and use `field:<name>` features. Per-company data (SEC XBRL) uses `trading.connectors.kit.xbrl.facts_as_of` to get one value per (cik, tag, unit, period) and a ticker to CIK map.

## knowledge_time rules by data type (round LATER when unsure; early = fake alpha)

| Data type | knowledge_time | Helper | Example |
|---|---|---|---|
| Daily price bar | bar close (event day + 1 day 00:00 UTC if no time) | `next_day_start_utc` | Tiingo, Coinbase |
| Macro release (CPI, jobs) | the scheduled release instant; revisions are new rows at their vintage date | vendor vintage, `add_lag_days` | ALFRED `realtime_start` |
| Positioning report (CFTC COT) | Friday 15:30 ET after the Tuesday report date; holiday week: following Monday | `cftc_release_time` | cftc_cot_* |
| SEC filing fact | 23:59:59 ET on the `filed` date (acceptance time is not in companyfacts); `event_time` clamped to the filing day if the period end is later (vendor typo) | `end_of_day_et`, `xbrl.filed_knowledge_time` | sec_xbrl_facts |
| SEC frames cross-section | the time we fetched it (no filing date in frames); forward-only, never for history | `xbrl.normalise_frame` | sec_xbrl_frames |
| Agency statistics (OECD/IMF/ECB SDMX) | period end + the agency's publication lag in days | `add_lag_days`, `sdmx.normalise_sdmx_csv` | HICP, GDP |
| Scheduled calendar (FOMC dates) | when the schedule was published, not the meeting date | vendor | fomc_meetings |
| Snapshot / metadata (no history) | the time we fetched it | `pd.Timestamp.now(tz="UTC")` | ticker lists |
| Vendor revises a value | `max(computed, time we first saw the revised value)` | automatic in `dedupe_new` | any |

`event_time` is what the value describes (period end). A row must never have `knowledge_time < event_time`; `verify_data` fails it.

## Choosing the protocol

| Protocol | Use when | Kit helper |
|---|---|---|
| `rest` | JSON/CSV API with an endpoint per query | `RestConnector.get/get_json/paginate_*` |
| `socrata` | CFTC, USDA, any `*.gov` open-data portal ("/resource/xxxx-xxxx.json") | `SocrataConnector.resource/payloads`, `rows_to_frame` |
| `sdmx` | OECD, IMF, ECB, BIS, Eurostat statistical agencies | `SdmxConnector.flow`, `normalise_sdmx_csv` |
| `xbrl` | SEC data.sec.gov (companyfacts, frames) | `kit.xbrl` |
| `bulk` | CSV/ZIP/XLSX file on an official site (Ken French, AQR, BLS flat files) | `BulkDownloader`, `parse_table` (xlsx needs openpyxl, not installed yet) |

**Known exception (CFTC, QA cycles 1-2):** COT releases were suspended during the Oct-Nov 2025 shutdown; `timing.CFTC_RELEASE_FLOORS` floors those report dates at 2026-01-09 (UNVERIFIED, deliberately late). Rows stored before the floor keep their early knowledge_time (append-only; `as_of` cannot un-know them: 2072/2072 legacy, 457/457 tff and 1615 disagg rows were stored early). The three `cftc_cot_*` datasets therefore declare `knowledge_guard: cftc_release` in `config/data_sources/cftc.yaml`, and **every reader must use `trading.connectors.kit.reader.read_guarded`**, never `store.as_of` or `datasets.read_asof` directly. The generic `kit_dataset` adapter in `packages/trading/factory/bakeoff/datasets.py` (owned by the bake-off track) still calls `read_asof`: until it is switched to `read_guarded` for datasets with a guard (`kit.reader.guard_for(dataset)` is not None), do not feed `cftc_cot_*` through `kit_dataset`; use the `cftc_cot` example above.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `RuntimeError: NAME is not set` | key not in `.env` | Sharif adds it; never paste it into chat or code |
| `HTTP 403` from SEC | missing/undescriptive User-Agent | SEC needs a descriptive User-Agent with contact email in the header only |
| `HTTP 429` loops, `gave up after 6 attempts` | rate limit too high or shared IP | lower `rate` / yaml `rate_limit`; exit 3 makes the daily run WARN |
| verify_data: `raw payload for each batch` FAIL | batch written without raw | always write through `ingest_payloads` (it names clean batch == raw stem) |
| verify_data: `no duplicate keys in batch` FAIL | yaml `keys` do not identify a row version | add the missing column (e.g. `accn`, `start`) to `keys` in the yaml AND the spec |
| verify_data: `no look-ahead` FAIL | `knowledge_time < event_time` (scheduled data, wrong time zone) | fix the rule; for forward-known schedules set event_time = knowledge date |
| Re-run writes 0 new rows | working as designed: unchanged rows are skipped | `--full` re-fetches; only changed rows are appended |
| Revised values appear as new rows | working as designed: revision rule | `ParquetStore.as_of` returns the value known at the time |
| `KeyError` in normalise on a new field | vendor changed schema | keep the raw page, add the field, re-run; old raw stays |
| Probe `yaml datasets match specs` FAIL | spec names differ from yaml | make the names identical |
| Scheduler dry-run shows no `KIT <vendor>` line | no `kit:` block or yaml parse error | check `protocol`, `schedule`, `ingest` keys in the yaml |
| xlsx parse error | openpyxl not installed | list it under `deps_needed`; do not `poetry add` |

## Worked example: CFTC Commitments of Traders (Socrata, public, no key)

```
poetry run python scripts/new_connector.py cftc --protocol socrata --base-url https://publicreporting.cftc.gov \
    --dataset cftc_cot_legacy --keys cftc_contract_market_code,event_time
# then inject: RESOURCE_ID per dataset (6dca-aqww legacy, 72hh-3qpy disaggregated, gpe5-46if TFF),
# normalise: event_time = report_date_as_yyyy_mm_dd, knowledge_time = cftc_release_time(event_time), text codes kept as text
poetry run pytest tests/connectors/test_cftc.py -q
poetry run python scripts/probe_cftc.py            # PASS
poetry run python scripts/ingest_cftc.py --full    # backfill subset from default_start, background
poetry run python scripts/verify_data.py           # PASS
```

SEC XBRL (`sec_xbrl`, protocol `xbrl`) was built the same way. Its only extras: a ticker to CIK map from `https://www.sec.gov/files/company_tickers.json`, the SEC User-Agent, and 8 requests/second.

What the real runs taught (2026-10-19), so the next connector does not repeat them:
- CFTC rows are ~4.6 KB (130-190 columns): the Socrata default page of 50000 rows is a 230 MB request. `PAGE = 5000` on the connector. Backfill subset = reports from 2018-01-01 (263,564 rows, about 1.3 GB raw JSON).
- verify_data (Tier 5) caught 2 SEC facts whose period end is after their filing date (vendor typos). Rule now in `kit.xbrl.normalise_companyfacts`: clamp `event_time` to the filing day. The two already-stored rows were fixed with `ingest_sec_xbrl.py --repair-look-ahead` (original Parquet moved to `<data dir>/quarantine/`, never deleted).
- pandas 3 returns `str` dtype, not `object`: use `pd.api.types.is_string_dtype`, never `dtype == object`.
- Numeric-looking codes ("001602") must stay text: pass `text_cols=` to `rows_to_frame`.

## Checklist before saying DONE

- [ ] `pytest` for the connector and the whole suite green; probe PASS; backfill stored; `verify_data` PASS with the old checks unchanged
- [ ] `knowledge_time` rule written at the top of the connector and in the yaml description
- [ ] licence in yaml and `_LICENSE.md`; no secret in any file; no live or paid action taken
- [ ] bake-off adapter added by the bake-off owner (or noted in action items), catalog `already_connected` updated
- [ ] every step committed and pushed; nothing of yours left uncommitted
