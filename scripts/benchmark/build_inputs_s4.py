"""Build the inputs and answer key for benchmark task S4a (the LaLonde trap).

The National Supported Work (NSW) job-training programme was a randomised experiment, so the
experimental estimate of its effect on 1978 earnings is known: treated mean minus control mean in the
Dehejia & Wahba (1999) subsample. LaLonde (1986) showed that comparing the same treated workers with a
non-experimental comparison group from a national survey (here PSID-1) gives a badly wrong answer
unless the analysis handles the very different populations. S4a hands the agent only the treated
workers and the survey comparison group; the experimental control group stays here, local, as the key.

  download: benchmark/keys/s4/raw/          (Dehejia's public text files, local only)
  key:      benchmark/keys/s4.json          (experimental estimate and SE, naive estimate)
  inputs:   benchmark/tasks/study_s4a_lalonde/inputs_local/jobs.csv   (treated + PSID-1, no source names)

Source: https://users.nber.org/~rdehejia/data/ (Dehejia & Wahba 1999, 2002; LaLonde 1986).
Run from the repo root:  python scripts/benchmark/build_inputs_s4.py
Then check for leaks:   python benchmark/run.py --check-inputs --task study_s4a_lalonde
"""
import csv
import json
import math
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "benchmark/keys/s4/raw"
KEY = ROOT / "benchmark/keys/s4.json"
OUT = ROOT / "benchmark/tasks/study_s4a_lalonde/inputs_local"
URL = "https://users.nber.org/~rdehejia/data/{}"
FILES = ["nswre74_treated.txt", "nswre74_control.txt", "psid_controls.txt"]
COLS = ["treat", "age", "educ", "black", "hispanic", "married", "nodegree", "re74", "re75", "re78"]


def fetch():
    RAW.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        dest = RAW / name
        if not dest.exists():
            req = urllib.request.Request(URL.format(name), headers={"User-Agent": "autonomous-benchmark/0.1"})
            with urllib.request.urlopen(req, timeout=60) as r:
                dest.write_bytes(r.read())
        print(f"  {name}: {dest.stat().st_size:,} bytes")


def rows(name):
    out = []
    for line in (RAW / name).read_text(encoding="ascii").splitlines():
        vals = [float(v) for v in line.split()]
        if vals:
            if len(vals) != len(COLS):
                raise SystemExit(f"{name}: expected {len(COLS)} columns, got {len(vals)}")
            out.append(dict(zip(COLS, vals)))
    return out


def diff(a, b):
    ya, yb = [r["re78"] for r in a], [r["re78"] for r in b]
    ma, mb = sum(ya) / len(ya), sum(yb) / len(yb)
    va = sum((y - ma) ** 2 for y in ya) / (len(ya) - 1)
    vb = sum((y - mb) ** 2 for y in yb) / (len(yb) - 1)
    return ma - mb, math.sqrt(va / len(ya) + vb / len(yb))


def main():
    fetch()
    treated, control, psid = rows(FILES[0]), rows(FILES[1]), rows(FILES[2])
    exp_b, exp_se = diff(treated, control)
    naive_b, naive_se = diff(treated, psid)
    key = {"experimental": {"b": exp_b, "se": exp_se, "n_treated": len(treated), "n_control": len(control)},
           "naive_psid": {"b": naive_b, "se": naive_se, "n_comparison": len(psid)}}
    KEY.write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "jobs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for r in treated + psid:
            w.writerow([int(r[c]) if c != "re74" and c != "re75" and c != "re78" else round(r[c], 2) for c in COLS])
    print(f"treated {len(treated)}, experimental controls {len(control)} (key only), comparison {len(psid)}")
    print(f"wrote {KEY.relative_to(ROOT)} and {(OUT / 'jobs.csv').relative_to(ROOT)} (local only)")


if __name__ == "__main__":
    main()
