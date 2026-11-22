"""Build the calibration answers for the study graders (plan 10, D4 / smoke R6; rule L11).

Every grader must PASS each known-good answer and FAIL each known-bad one before its scores count. The
answers are built from the answer keys, so they are written under benchmark/keys/calibration/ (local
only, gitignored), never committed.

  benchmark/keys/calibration/<task>/good/<case>/{answer.json, replicate.ipynb}
  benchmark/keys/calibration/<task>/bad/<case>/{answer.json, replicate.ipynb}

Run from the repo root:  python scripts/benchmark/build_calibration.py
Then:                     python benchmark/run.py --calibrate --task study
"""
import copy
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEYS = ROOT / "benchmark/keys"
OUT = KEYS / "calibration"
TERMS = ["excuse_to_noexcuse_x2020", "excuse_to_apps_x2020", "noexcuse_to_apps_x2020", "noexcuse_to_ballots_x2020"]


def notebook(lines):
    """A minimal executed notebook whose one cell printed `lines` (empty = a notebook with no output)."""
    outputs = [{"output_type": "stream", "name": "stdout", "text": [l + "\n" for l in lines]}] if lines else []
    return {"cells": [{"cell_type": "code", "execution_count": 1 if lines else None, "metadata": {},
                       "outputs": outputs, "source": ["# analysis\n"]}],
            "metadata": {}, "nbformat": 4, "nbformat_minor": 5}


def case(task, kind, name, ans, printed):
    d = OUT / task / kind / name
    d.mkdir(parents=True)
    if ans is not None:
        (d / "answer.json").write_text(json.dumps(ans, indent=2), encoding="utf-8")
    (d / "replicate.ipynb").write_text(json.dumps(notebook(printed), indent=1), encoding="utf-8")


def did_answer(spec):
    k = json.loads((KEYS / "s1.json").read_text(encoding="utf-8"))[spec]
    return {oc: {t: dict(k[oc]["county_fe_state_cluster"]["terms"][t]) for t in TERMS} for oc in ("turnout", "rep_share")}


def did_lines(ans):
    return [f"{oc} {t}: b = {v['b']:.4f}  se = {v['se']:.4f}  p = {v['p']:.4f}"
            for oc, terms in ans.items() for t, v in terms.items()]


def main():
    shutil.rmtree(OUT, ignore_errors=True)

    # S1: the package's own coding, graded at printed precision
    pub = did_answer("published")
    case("study_s1_reproduce", "good", "exact", pub, did_lines(pub))
    wrong = copy.deepcopy(pub); wrong["turnout"]["noexcuse_to_ballots_x2020"]["b"] += 0.1
    case("study_s1_reproduce", "bad", "one_term_off", wrong, did_lines(wrong))
    case("study_s1_reproduce", "bad", "not_printed", pub, ["model fitted", "see answer.json"])
    case("study_s1_reproduce", "bad", "no_answer_file", None, did_lines(pub))

    # S2: the text-faithful (FIPS) coding, graded with decision 10-B's tolerance
    fips = did_answer("fips")
    case("study_s2_replicate", "good", "exact", fips, did_lines(fips))
    close = copy.deepcopy(fips)
    for terms in close.values():
        for v in terms.values():
            v["b"] *= 1.05                                    # 5% off, every p unchanged: inside 10-B
    case("study_s2_replicate", "good", "five_percent_off", close, did_lines(close))
    case("study_s2_replicate", "bad", "published_coding", pub, did_lines(pub))   # county-name FE: headline 12% off
    unclustered = copy.deepcopy(fips)
    for terms in unclustered.values():
        for v in terms.values():
            v["se"] /= 3; v["p"] = 0.001                      # unclustered SEs: every term "significant"
    case("study_s2_replicate", "bad", "unclustered_ses", unclustered, did_lines(unclustered))

    # S3: the reference analysis from plant_s3.R --selftest, and wrong answers
    s3 = json.loads((KEYS / "s3.json").read_text(encoding="utf-8"))["reference"]
    def s3_case(task, kind, name, est, lo, hi, verdict):
        case(task, kind, name, {"estimate": est, "ci_low": lo, "ci_high": hi, "verdict": verdict},
             [f"estimate {est:.4f}, 95% CI [{lo:.4f}, {hi:.4f}]"])
    p, n = s3["planted"], s3["null"]
    s3_case("study_s3_planted", "good", "reference", p["b"], p["lo"], p["hi"], "effect")
    s3_case("study_s3_planted", "bad", "missed_effect", 0.40, -0.90, 1.70, "no effect")
    s3_case("study_s3_planted", "bad", "wrong_size_overconfident", 1.00, 0.80, 1.20, "effect")
    s3_case("study_s3_null", "good", "reference", n["b"], n["lo"], n["hi"], "no effect")
    s3_case("study_s3_null", "bad", "false_positive", 0.90, 0.30, 1.50, "effect")

    n_cases = sum(1 for _ in OUT.glob("*/*/*"))
    print(f"wrote {n_cases} calibration cases under {OUT.relative_to(ROOT)} (local only)")


if __name__ == "__main__":
    main()
