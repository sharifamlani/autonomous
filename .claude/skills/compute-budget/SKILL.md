---
name: compute-budget
description: Use before launching subagents, workflows, model training, backtest sweeps or backfills in this repo, whenever the machine feels slow, and whenever Claude usage (the weekly allowance) matters. Sets how many agents and threads may run at once on Sharif's workstation, how to use the GPU, and how the main agent monitors CPU, RAM and GPU while work runs. Written after parallel workflows crashed the machine on 2026-10-19.
---

# Compute budget (Sharif 2026-10-19)

On 2026-10-19 three workflows ran at once (wave 17, the bake-off engine, the data platform), each
allowed up to 14 agents, several of them training models on every core. The workstation crashed.
The rules below keep work fast **and** keep the machine alive.

## The machine

| Part | Spec | What it means |
|---|---|---|
| CPU | i9-9980HK, 8 cores / 16 threads | 12 threads for work, 4 always free for Windows, Dropbox, the editor and Claude |
| RAM | 32 GB | keep at least 6 GB free before starting a heavy job |
| GPU | NVIDIA GTX 1650, 4 GB, driver 555.99 | torch uses it through the cu126 build; one GPU job at a time; small nets only (MLP, LSTM, TCN, small transformers) |

## Rules (binding)

1. **Several workflows may run at once, but only while the monitor says there is room** (Sharif
   2026-10-19: "you don't have to do one workflow at a time... you just have to monitor CPU, RAM, and
   memory closely"). Before launching each workflow or each new batch of agents, `resource_monitor.py
   gate` must print `GATE OK`, and the watcher (below) must be running.
2. **Machine-wide caps, across ALL running workflows together:** at most **2 heavy-compute jobs** at a
   time (model training, backtest sweeps, big backfills: 6 threads each) and at most **6 agents** in
   total. Light agents (research, writing, QA reading code, network-bound ingest) count toward the 6
   but not toward the 2. Inside a workflow, run tracks in batches so the caps hold.
3. **Every heavy job sets its budget first:**
   ```python
   from trading import compute
   b = compute.apply(compute.budget())     # threads from TRADING_THREADS (default 6), GPU allowed
   dev = compute.device(b)                  # "cuda" or "cpu"
   lgb = lightgbm.LGBMRegressor(**compute.lgbm_params(b), ...)
   ```
   Two heavy jobs: `TRADING_THREADS=6` each. One heavy job alone: `TRADING_THREADS=12`.
   joblib fan-out: `n_jobs=b.threads` with 1 thread per worker inside (`compute.apply` sets the
   BLAS/OpenMP caps that child processes inherit).
4. **Gate before launch.** `poetry run python scripts/dev/resource_monitor.py gate` must print
   `GATE OK` before a heavy job or a new workflow starts. `GATE WAIT` means wait or shrink the job.
5. **GPU:** neural and sequence models train on `compute.device()`. Trees (LightGBM, random forest) and
   linear models stay on CPU (the pip LightGBM wheel has no GPU build). Batch sizes must fit 4 GB; on a
   CUDA out-of-memory error halve the batch, never fall back to grabbing all CPU threads.
   **Reproducibility:** a study pre-registered on CPU finishes on CPU (`TRADING_DEVICE=cpu`); GPU runs
   record `device` in their manifest, and parity is checked within tolerance, not bit-for-bit.
6. **Full test suites run one at a time.** The root `conftest.py` takes a machine-wide lock
   (`TRADING_DATA_DIR/state/full_suite.lock`) for any run that collects 400+ tests, so concurrent QA
   agents queue instead of stacking 1-1.5 GB suites (5 at once pushed free RAM under 4 GB on
   2026-10-19). Targeted runs (one file or folder) never wait. Prefer targeted runs; run the full
   suite once per track before its final commit.
7. **Long jobs run in the background** and are capped (a study stage over about 60 minutes is split
   into resumable stages with saved checkpoints).

## The main agent monitors while work runs

- Start the watcher once per session, in the background:
  `poetry run python scripts/dev/resource_monitor.py watch --interval 30 --alert-cpu 95 --alert-ram-gb 4 --sustain 3`
  It logs every sample to `TRADING_DATA_DIR/state/resource_monitor.jsonl` and prints `ALERT` lines
  only when CPU >= 95%, free RAM <= 4 GB or GPU memory >= 95% for 3 samples in a row (single spikes from test runs are normal), then one `CLEARED` line. Before adding agents, also require at least 6 GB free RAM: Cursor, Chrome and Dropbox hold about 12 GB on their own.
- Check `resource_monitor.py snapshot` before each new batch of agents and when an alert appears.
- On an ALERT: do not start anything new; if it persists for 3 samples, stop the newest heavy job
  (its stages are resumable) and tell Sharif in one line.

## Workflow script pattern (batches, not a free-for-all)

```js
// run tracks two at a time instead of all at once
for (let i = 0; i < TRACKS.length; i += 2) {
  await pipeline(TRACKS.slice(i, i + 2), devStage, qaStage)
}
```
Prompts tell each agent its thread budget (`TRADING_THREADS`) and to run
`scripts/dev/resource_monitor.py gate` before any heavy stage.

## Usage budget: the Claude allowance is a resource too (Sharif 2026-10-19)

From the Sunday 07:00 reset to Monday afternoon, 40% of the weekly Max allowance was spent. About 89% came from
subagent workflows (12,279 agent steps) and 11% from the main chat (975 calls). The Python code itself
costs nothing; the AI agents that write, test and review it do. Measured causes, worst first:
the crash (about 23% wasted and redone), long-lived agents re-reading a 300k+ token history on every
step (cost is roughly steps x context size), the Dev+QA+fix+QA+reviewer multiplier (2-4x per track),
the top model used for every role, and 30-minute watcher wake-ups re-reading the huge main chat.

**Binding rules for every workflow and session:**

1. **Model per role.** The top model only for core design, study/engine code and final verdicts. Use a
   cheaper model (`model: 'sonnet'`, or `'haiku'` for mechanical work) for QA, report writing and
   review, literature/web research, connector builds from the kit, parity reruns and status checks.
2. **Small, fresh agents per stage.** Split a study into stages (prereg, build, run, write-up), each
   a new agent given only what it needs (file paths, not pasted history). Never one agent for a whole
   study. Aim for under about 150 steps per agent.
3. **One QA round by default.** A second round only if the first finds BUGS; a third only for money-path
   or holdout-critical code. Routine reports get `check_report.py` only, no reviewer agent, unless the
   report is for an outside audience.
4. **Engines first, bespoke code last.** A new question about models or strategies is a config for the
   bake-off or strategy engine (`rerun-bakeoff`, `rerun-strategy` skills) run by one small agent, not
   a new study codebase.
5. **No crash, no rework.** Follow the compute rules above; resumable stages with checkpoints; never
   relaunch a workflow from scratch when a resume is possible.
6. **Silent watching.** Run the watcher as a background command that exits ONLY on a sustained alert
   (one notification, no periodic wake-ups). Do not re-arm a 30-minute monitor overnight just to report
   "quiet". Check status only when a workflow finishes.
7. **Keep the main chat small.** Compact before a long autonomous run; keep status updates short; read
   workflow results from journals with a script rather than pasting them in full.
8. **Fewer, higher-prior studies.** Run a study only when its prior and expected value justify the
   agents; queue the rest on the ROADMAP. Budget each workflow up front (agents x expected steps) and
   say the estimate in the plan.
9. **Check the meter.** Before a big launch, ask Sharif for the current weekly usage if it is not
   known; above about 60% weekly use, launch only what Sharif names.

## Troubleshooting

| Symptom | Likely cause | Do this |
|---|---|---|
| Machine freezes, fans max | too many concurrent training jobs | stop the newest job; run in batches of 2 |
| `torch.cuda.is_available()` is False | CPU torch wheel installed | `poetry install --with models` (pyproject pins cu126 on Windows) |
| CUDA out of memory | batch too large for 4 GB | halve the batch size |
| LightGBM uses every core | no `n_jobs` | use `compute.lgbm_params(b)` |
| A study's numbers moved slightly on GPU | GPU kernels are not bit-identical | run pre-registered CPU studies with `TRADING_DEVICE=cpu` |
