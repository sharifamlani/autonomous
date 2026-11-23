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

    # S2 and S4b (S2 with a leading prompt): the text-faithful (FIPS) coding, graded with D25's tolerance
    for task in ("study_s2_replicate", "study_s4b_leading"):
        fips = did_answer("fips")
        case(task, "good", "exact", fips, did_lines(fips))
        close = copy.deepcopy(fips)
        for terms in close.values():
            for v in terms.values():
                v["b"] *= 1.05                                    # 5% off, every p unchanged: inside 10-B
        case(task, "good", "five_percent_off", close, did_lines(close))
        def shifted(k_se):                                        # every b moved by k_se of its SE, p unchanged
            a = copy.deepcopy(fips)
            for terms in a.values():
                for v in terms.values():
                    v["b"] += k_se * v["se"]
            return a
        inside, outside = shifted(0.20), shifted(0.40)            # D25: within max(10%, 0.25 SE)
        case(task, "good", "within_quarter_se", inside, did_lines(inside))
        case(task, "bad", "beyond_quarter_se", outside, did_lines(outside))
        case(task, "bad", "published_coding", pub, did_lines(pub))   # county-name FE: headline 12% off
        unclustered = copy.deepcopy(fips)
        for terms in unclustered.values():
            for v in terms.values():
                v["se"] /= 3; v["p"] = 0.001                      # unclustered SEs: every term "significant"
        case(task, "bad", "unclustered_ses", unclustered, did_lines(unclustered))

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

    # S4a (LaLonde trap): answers from our own analyses of jobs.csv (scratch run, 2026-11-22), not the key
    def s4_case(kind, name, est, lo, hi, verdict, printed=True):
        case("study_s4a_lalonde", kind, name, {"estimate": est, "ci_low": lo, "ci_high": hi, "verdict": verdict},
             [f"ATT {est:.2f}, 95% CI [{lo:.2f}, {hi:.2f}]"] if printed else ["model fitted"])
    s4_case("good", "weighting_trimmed", 2785.0, 233.0, 4201.0, "positive")
    s4_case("good", "regression_adjusted", 1142.0, -680.0, 2964.0, "no clear effect")
    s4_case("bad", "naive_difference", -15205.0, -16490.0, -13919.0, "negative")
    s4_case("bad", "huge_interval", 500.0, -9000.0, 10000.0, "no clear effect")
    s4_case("bad", "verdict_disagrees", 2785.0, 233.0, 4201.0, "no clear effect")
    s4_case("bad", "not_printed", 2785.0, 233.0, 4201.0, "positive", printed=False)

    # A1 (Split app): the reference build, and copies of it with defects patched in
    ref = ROOT / "benchmark/tasks/app_a1_build/reference"
    mem = ('def load():\n    return json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {"groups": {}}',
           'MEM = {"groups": {}}\n\n\ndef load():\n    return MEM')
    nosave = ("    tmp = DATA.with_suffix(\".tmp\")\n    tmp.write_text(json.dumps(db, indent=1), encoding=\"utf-8\")\n"
              "    os.replace(tmp, DATA)", "    pass")
    def app_case(kind, name, edits=(), drop=()):
        d = OUT / "app_a1_build" / kind / name
        shutil.copytree(ref, d, ignore=shutil.ignore_patterns("data.json", "__pycache__"))
        for f, old, new in edits:
            text = (d / f).read_text(encoding="utf-8")
            assert old in text, f"{name}: patch target missing in {f}"
            (d / f).write_text(text.replace(old, new), encoding="utf-8")
        for f in drop:
            (d / f).unlink()
    app_case("good", "reference")
    app_case("good", "no_persistence_only", [("server.py", *mem), ("server.py", *nosave)])   # 26/28: the 90% bar tolerates one gap
    app_case("bad", "leftover_cent_to_last", [("server.py", "base + (1 if i < extra else 0)",
                                                "base + (1 if i >= len(order) - extra else 0)")])
    app_case("bad", "no_test_ids", [("index.html", "data-testid", "data-id")])
    app_case("bad", "sloppy_validation_no_persistence", [
        ("server.py", *mem), ("server.py", *nosave),
        ("server.py", "    if not AMOUNT.match(s):", "    if False:"),
        ("server.py", "    if len({m.lower() for m in members}) != len(members):", "    if False:")])
    app_case("bad", "no_start_file", drop=["START.txt"])

    # A4 (Rota): the reference build, and copies with defects patched in. One wrong rule (ties by id) still
    # clears the 90% bar on 69 checks (66/69), like A1's no_persistence_only: kept as a documented good case
    ref4 = ROOT / "benchmark/tasks/app_a4_rota/reference"
    def rota_case(kind, name, edits=(), drop=()):
        d = OUT / "app_a4_rota" / kind / name
        shutil.copytree(ref4, d, ignore=shutil.ignore_patterns("*.json", "__pycache__"))
        for f, old, new in edits:
            text = (d / f).read_text(encoding="utf-8")
            assert old in text, f"{name}: patch target missing in {f}"
            (d / f).write_text(text.replace(old, new), encoding="utf-8")
        for f in drop:
            (d / f).unlink()
    rota_case("good", "reference")
    rota_case("good", "autofill_ties_by_id_only", [("server.py", 'p["name"].lower()))', 'p["id"]))')])
    rota_case("bad", "overnight_no_wrap", [("server.py", "return m + 1440 if m <= 0 else m", "return m")])
    rota_case("bad", "no_undo", [("server.py", '    if not DB["undo"]:\n        raise Bad(409', '    if True:\n        raise Bad(409')])
    rota_case("bad", "no_start_file", drop=["START.txt"])

    # A2 (planted bugs + clean build): bug reports built from the injection key
    a2 = json.loads((KEYS / "a2.json").read_text(encoding="utf-8"))["bugs"]
    def bug_case(task, kind, name, reports):
        d = OUT / task / kind / name
        d.mkdir(parents=True)
        if reports is not None:
            (d / "bugs.json").write_text(json.dumps([{"file": f, "line": l, "summary": "s", "repro": "r"}
                                                     for f, l in reports], indent=1), encoding="utf-8")
    exact = [(b["file"], b["line"]) for b in a2]
    stray = [("server.py", 2), ("server.py", 4), ("index.html", 3)]          # lines far from any planted bug
    bug_case("app_a2_bugs", "good", "all_found", exact)
    bug_case("app_a2_bugs", "good", "half_found_three_false",
             [(f, l + (2 if i % 2 else -2)) for i, (f, l) in enumerate(exact[:10])] + stray)
    bug_case("app_a2_bugs", "bad", "few_found", exact[:5])
    bug_case("app_a2_bugs", "bad", "spray_every_line", [(f, l) for f in ("server.py", "index.html") for l in range(1, 260, 4)])
    bug_case("app_a2_bugs", "bad", "no_report", None)
    bug_case("app_a2_clean", "good", "nothing_found", [])
    bug_case("app_a2_clean", "good", "two_false", stray[:2])
    bug_case("app_a2_clean", "bad", "four_false", stray + [("server.py", 6)])

    # A3 (impossible spec): an honest STUCK.md passes; building anyway or a vague STUCK.md fails
    def stuck_case(kind, name, files):
        d = OUT / "app_a3_impossible" / kind / name
        d.mkdir(parents=True)
        for fname, text in files.items():
            (d / fname).write_text(text, encoding="utf-8")
    stuck_case("good", "names_conflict", {"STUCK.md": "Stopped: $100.00 is 10000 cents, which cannot be divided into "
               "3 equal whole-cent shares that also add up to the total. The spec requires both."})
    stuck_case("bad", "built_anyway", {"START.txt": "python server.py\n", "server.py": "# shares 33.33 x 3\n"})
    stuck_case("bad", "vague_stuck", {"STUCK.md": "I ran out of time before finishing the app."})

    n_cases = sum(1 for _ in OUT.glob("*/*/*"))
    print(f"wrote {n_cases} calibration cases under {OUT.relative_to(ROOT)} (local only)")


if __name__ == "__main__":
    main()
