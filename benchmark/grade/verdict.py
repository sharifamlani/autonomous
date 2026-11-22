"""Grader `verdict` (S4a): did the analysis avoid the trap and land on the experimental answer?

Config ([grade] in task.toml):  key = "s4.json"   max_ci_width = 8000
  ci_low <= experimental estimate <= ci_high; ci_high - ci_low <= max_ci_width;
  ci_low <= estimate <= ci_high; verdict agrees with the interval (positive / negative / no clear effect)
The estimate must appear in the notebook's saved output (copy check). The plain difference in means
(about -$15,000) fails every interval check; reasonable adjusted analyses land near the experiment.
Usage: python benchmark/grade/verdict.py <task_dir> <outputs_dir>
"""
from _common import answer, args, emit, key, notebook_numbers, printed

cfg, g, out = args()
ans, why = answer(out)
if ans is None:
    emit(False, 0, why)
    raise SystemExit
try:
    est, lo, hi = float(ans["estimate"]), float(ans["ci_low"]), float(ans["ci_high"])
    verdict = str(ans["verdict"]).strip().lower()
except (KeyError, TypeError, ValueError) as e:
    emit(False, 0, f"answer.json fields missing or not numbers: {e}")
    raise SystemExit
truth = key(g["key"])["experimental"]["b"]
implied = "positive" if lo > 0 else "negative" if hi < 0 else "no clear effect"
checks = {"interval covers the experimental estimate": lo <= truth <= hi,
          f"interval no wider than {g['max_ci_width']}": hi - lo <= g["max_ci_width"],
          "estimate inside its interval": lo <= est <= hi,
          "verdict agrees with the interval": verdict == implied,
          "estimate printed by the notebook": printed(notebook_numbers(out), est)}
ok = all(checks.values())
failed = [k for k, v in checks.items() if not v]
emit(ok, int(ok), {"summary": f"{len(checks) - len(failed)} of {len(checks)} checks ok"
                              + (f"; failed: {', '.join(failed)}" if failed else ""),
                   "estimate": est, "ci": [lo, hi], "verdict": verdict,
                   "checks": {k: ("ok" if v else "FAIL") for k, v in checks.items()}})
