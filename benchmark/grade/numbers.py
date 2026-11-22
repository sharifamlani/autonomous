"""Grader `numbers` (S1, S2): the eight DiD interaction terms against the answer key.

Config ([grade] in task.toml):
  key    = "s1.json"     answer key in benchmark/keys/ (local only)
  spec   = "published" | "fips"   which county fixed-effects coding to grade against
  rule   = "printed"     S1: b and se equal the key at 3 decimals
         | "tolerance"   S2 (decision 10-B): same sign, same 5% call, |b - key| <= max(rel*|key|, abs_se*key_se)
  rel, abs_se            tolerance settings (abs_se = 0 turns the SE-based allowance off)

Every term must pass, and every reported b must appear in the notebook's saved output (copy check).
Score = share of the 8 terms that pass.
Usage: python benchmark/grade/numbers.py <task_dir> <outputs_dir>
"""
from _common import answer, args, emit, key, notebook_numbers, printed

TERMS = ["excuse_to_noexcuse_x2020", "excuse_to_apps_x2020", "noexcuse_to_apps_x2020", "noexcuse_to_ballots_x2020"]
OUTCOMES = ["turnout", "rep_share"]

cfg, g, out = args()
ans, why = answer(out)
if ans is None:
    emit(False, 0, why)
    raise SystemExit
ref = key(g["key"])[g["spec"]]
nums = notebook_numbers(out)
results, ok_n = {}, 0
for oc in OUTCOMES:
    for t in TERMS:
        k = ref[oc]["county_fe_state_cluster"]["terms"][t]
        a = (ans.get(oc) or {}).get(t) or {}
        try:
            b, se, p = float(a["b"]), float(a["se"]), float(a["p"])
        except (KeyError, TypeError, ValueError):
            results[f"{oc}.{t}"] = "missing or not numbers"
            continue
        if g["rule"] == "printed":
            ok = round(b, 3) == round(k["b"], 3) and round(se, 3) == round(k["se"], 3)
            why = f"b {b:.3f} vs {k['b']:.3f}, se {se:.3f} vs {k['se']:.3f}"
        else:
            allow = max(g.get("rel", 0.10) * abs(k["b"]), g.get("abs_se", 0.0) * k["se"])
            same_sign = (b > 0) == (k["b"] > 0)
            same_call = (p < 0.05) == (k["p"] < 0.05)
            close = abs(b - k["b"]) <= allow
            ok = same_sign and same_call and close
            why = (f"b {b:.3f} vs {k['b']:.3f} (allow ±{allow:.3f}: {'ok' if close else 'off'}), "
                   f"sign {'ok' if same_sign else 'differs'}, 5% call {'ok' if same_call else 'differs'}")
        copied = not printed(nums, b)
        if copied:
            ok, why = False, why + "; not in the notebook's saved output"
        ok_n += ok
        results[f"{oc}.{t}"] = ("PASS " if ok else "FAIL ") + why
n = len(OUTCOMES) * len(TERMS)
note = "" if nums is not None else "no executed replicate.ipynb; "
emit(ok_n == n, round(ok_n / n, 3), {"summary": f"{note}{ok_n} of {n} terms pass", "terms": results})
