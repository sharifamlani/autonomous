"""Grader `planted` (S3): did the analysis find the planted effect, or correctly find none?

Config ([grade] in task.toml):  key = "s3.json"   which = "planted" | "null"
  planted: ci_low <= delta <= ci_high, ci_low > 0, verdict "effect"
  null:    ci_low <= 0 <= ci_high, verdict "no effect"
The estimate must appear in the notebook's saved output (copy check). Intervals are wide by design
(the policy is assigned to 15 of 50 states), so the grade is coverage and the call, not a tight point.
Usage: python benchmark/grade/planted.py <task_dir> <outputs_dir>
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
truth = key(g["key"])["delta"] if g["which"] == "planted" else 0.0
covers = lo <= truth <= hi
if g["which"] == "planted":
    checks = {"interval covers the true effect": covers, "interval excludes 0": lo > 0, "verdict is effect": verdict == "effect"}
else:
    checks = {"interval covers 0": covers, "verdict is no effect": verdict == "no effect"}
checks["estimate printed by the notebook"] = printed(notebook_numbers(out), est)
ok = all(checks.values())
failed = [k for k, v in checks.items() if not v]
emit(ok, int(ok), {"summary": f"{len(checks) - len(failed)} of {len(checks)} checks ok"
                              + (f"; failed: {', '.join(failed)}" if failed else ""),
                   "estimate": est, "ci": [lo, hi], "verdict": verdict,
                   "checks": {k: ("ok" if v else "FAIL") for k, v in checks.items()}})
