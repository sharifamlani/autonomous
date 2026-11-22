"""Leak check: no answer value may appear in what a benchmark agent is given (plan 10, smoke D2).

Reads the local answer key, renders every key estimate the way a paper or log might print it, and
searches each text file in the task's agent-visible inputs. Binary data files are listed but not
searched (data are inputs, not answers). Exit 1 on any hit.

Usage (repo root):  python scripts/benchmark/check_inputs.py --task study_s2_replicate
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEYS = {"study_s2_replicate": ROOT / "benchmark/keys/s1.json"}
TEXT = {".md", ".txt", ".tex", ".csv", ".tsv", ".json", ".r", ".py", ".ipynb", ".html"}
# phrasings of the headline the paper itself uses outside its tables
PHRASES = ["2.6 percent", "2.6 +", "7.3 percent", "4.7 +", "1.4 percent", "1.2 percent"]


def key_values(key):
    vals = set()
    def walk(x):
        if isinstance(x, dict):
            if "b" in x and isinstance(x["b"], (int, float)):
                for v in (x["b"], x.get("se")):
                    if isinstance(v, (int, float)):
                        vals.add(f"{v:.3f}")
                        vals.add(f"{v:.2f}")
                        if abs(v) >= 1:
                            vals.add(f"{v:.1f}")
            for v in x.values():
                walk(v)
    walk(key)
    return {v for v in vals if v not in {"0.00", "0.000", "-0.00", "-0.000"}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=sorted(KEYS))
    a = ap.parse_args()
    inputs = ROOT / "benchmark/tasks" / a.task / "inputs_local"
    if not inputs.exists():
        sys.exit(f"no inputs at {inputs}; build them first")
    vals = key_values(json.loads(KEYS[a.task].read_text(encoding="utf-8")))
    pats = [(v, re.compile(r"(?<![\d.])" + re.escape(v.lstrip("-")) + r"(?![\d])")) for v in sorted(vals)]
    hits, searched = [], []
    for f in sorted(inputs.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix.lower() not in TEXT:
            print(f"  not searched (binary data): {f.name}")
            continue
        searched.append(f.name)
        t = f.read_text(encoding="utf-8", errors="replace")
        for v, p in pats:
            for m in p.finditer(t):
                hits.append(f"{f.name}: key value {v} -> ...{t[max(0, m.start()-60):m.end()+40]!r}...")
        for ph in PHRASES:
            if ph in t:
                hits.append(f"{f.name}: headline phrase {ph!r}")
    print(f"searched {len(searched)} text file(s) for {len(vals)} key values and {len(PHRASES)} phrases")
    for h in hits:
        print("  LEAK", h)
    print(f"{len(hits)} answer values found in inputs")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
