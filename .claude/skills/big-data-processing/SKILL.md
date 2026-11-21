---
name: big-data-processing
description: Use for any job over about 1M rows, any backfill, any parameter sweep, any training-data build, and any time pandas feels slow or memory climbs in the Trading repo. Says where the work should happen (DuckDB SQL, Polars, numpy/numba, GPU), gives recipes using trading.perf (stream, memory guard, pmap, Polars frames, numba kernels, Parquet cache), lists anti-patterns, and quotes measured speed-ups. Written 2026-10-24 after the FTD backfill reached 8.7 GB by accumulating files.
---

# Big-data processing (Sharif 2026-10-24)

The store holds tens of millions of rows (SEC FTD alone is 28.2M). Row-at-a-time pandas is the wrong default.
Toolkit: `packages/trading/perf/` (table of functions in its `_README.md`). Benchmarks:
`docs/perf/bench_2026-10-24.md`. Thread budget: always `trading.compute.budget()`; gate first
(`scripts/dev/resource_monitor.py gate`), max 2 heavy jobs at 6 threads (compute-budget skill).

## Where should the work happen?

| The work is... | Do it in | Why |
|---|---|---|
| Filter, project, join, aggregate, window over store Parquet | **DuckDB SQL** (`store.connect()`) | Predicate/column pushdown, multi-threaded, never loads what it filters out |
| Point-in-time ("as of t") reads | **DuckDB** via `store.as_of` or `perf.scan_dataset(as_of=, keys=)` | One implementation of the dedup rule; never reimplement it |
| Result bigger than ~1 GB | **stream**: `perf.iter_batches` + `write_chunks` | Peak memory = one batch |
| Heavy dataframe transforms after the SQL cut (group-by, joins, string ops) | **Polars** lazy (`perf.groupby_agg`, `scan_dataset(history=True)`) | Multi-threaded, lazy; 4.5x pandas on a 10M group-by |
| Dense numeric panels, vectorizable | **numpy** | Already C speed; avoid Python loops |
| Loops that cannot vectorize (compounding paths, rolling stats with NaN, event windows) | **numba** (`perf.kernels`) | 8x to 39x pandas; numpy fallback exists |
| Many independent items (tickers, folds, seeds, files) | **`perf.pmap`** | Processes for CPU, threads for I/O, budgeted, order-stable |
| Neural nets | **GPU** via `compute.device()` | GTX 1650, 4 GB, small nets only |
| Expensive intermediate reused across runs | **`perf.cached`** | Content-addressed Parquet; reruns are incremental |

Order of preference: push into SQL, then Polars, then numpy, then numba. Convert to pandas only at the edge
(`perf.to_pandas`) for libraries that need it.

## Recipes

```python
from trading import compute
from trading.data.store import ParquetStore
from trading import perf

b = compute.apply(compute.budget())                        # threads, BLAS caps
g = perf.guard(max_rss_gb=8, min_free_gb=6, label="my job") # raises MemoryLimitError, never freezes the box
store = ParquetStore(); con = store.connect()

# 1. Aggregate a huge table without loading it (SQL does the work)
df = con.execute("SELECT symbol, sum(quantity_fails) q FROM sec_fails_to_deliver GROUP BY 1").df()

# 2. Stream rows through Python in bounded batches, write each out before the next
sql = "SELECT symbol, settlement_date, quantity_fails FROM sec_fails_to_deliver WHERE quantity_fails > 0"
perf.write_chunks(perf.iter_batches(con, sql, batch_rows=500_000), out_dir, prefix="ftd", guard=g)

# 3. Backfill without accumulating (windowed: 772 MB peak vs 8.7 GB accumulating)
perf.backfill_windows(windows, fetch=fetch_window, write=write_window, guard=g)

# 4. Polars on a store dataset (point-in-time is mandatory: as_of+keys, or history=True on purpose)
lf = perf.scan_dataset(store, "<dataset>", as_of=t, keys=["<key cols>"], columns=["<cols>"])
out = perf.groupby_agg(lf.collect(), "<key>", {"<col>": ["mean", "std"]})

# 5. Fan out
res = perf.pmap(fit_one, tickers, kind="cpu", progress=True)       # failures raise PmapError(index, item)
files = perf.pmap(download, urls, kind="io")

# 6. Kernels (events x days panel, NaN padded)
paths = perf.compound_paths(R); fwd = perf.forward_gather(panel, t_idx, a_idx, horizon=21)
vol = perf.rolling_std(X, 60, min_periods=30)

# 7. Cache an expensive step
@perf.cached(version="1")
def build_features(prices: pd.DataFrame, lookback: int): ...
```

## Anti-patterns (each one cost real time or RAM here)

- Row loops over a DataFrame (`iterrows`, `itertuples`, `for i in range(len(df))`): vectorize or use a kernel.
- `df.apply(axis=1)` / `Series.apply(python_fn)`: use vectorized ops, Polars expressions or numba.
- Accumulating a list of frames and one `pd.concat` at the end: write each piece out (`backfill_windows`).
- Reading a whole table and then filtering in pandas: filter and project in SQL / `scan_*` first.
- `SELECT *` when you need three columns.
- Re-deriving point-in-time dedup in pandas or Polars: use `store.as_of` / `scan_dataset(as_of=)`.
- Nested parallelism (pmap inside pmap, joblib workers each using 16 BLAS threads, numba parallel inside
  workers): `pmap` pins workers to 1 thread and runs nested calls serially; keep it that way.
- Launching a heavy job without the gate, the budget, or a `MemoryGuard`.
- Unbounded numpy temporaries (sliding windows over big panels): chunk by columns.
- Rewriting stored data to "clean it": the store is append-only; derived output goes to `derived_cache/`.

## Measured (docs/perf/bench_2026-10-24.md; i9-9980HK, TRADING_THREADS=6)

| Task | pandas | toolkit | Speed-up |
|---|---|---|---|
| 10M-row group-by, 5k groups | 0.62 s | 0.14 s (Polars) | 4.5x |
| BHAR compounding 5,000 x 756 | 0.176 s | 0.005 s (numba) | 39x |
| Rolling std 3,000 x 6,000, w=60 | 1.68 s | 0.20 s (numba) | 8.5x |
| FTD 28.2M rows aggregate by symbol | 10.2 s, 3.14 GB peak | 3.9 s, 1.28 GB peak (batches) | 2.6x, 2.5x less RAM |

First numba call compiles (a few seconds, cached under `derived_cache/numba`); run a tiny slice first when timing.
`TRADING_NO_NUMBA=1` forces the numpy fallback (same results, slower).
