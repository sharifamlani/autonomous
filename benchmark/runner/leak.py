"""Leak check: no answer value may appear in what a benchmark agent is given (plan 10, smoke D2).

Lifted from scripts/benchmark/check_inputs.py; the key and phrases now come from each task.toml
(`leak_key`, `leak_phrases`) instead of a table in the script.

Reads the local answer key, renders every key estimate the way a paper or log might print it, and
searches each text file in the task's agent-visible inputs. Binary data files are listed but not
searched (data are inputs, not answers).
"""
import json
import re

from tasks import BENCH

TEXT = {".md", ".txt", ".tex", ".csv", ".tsv", ".json", ".r", ".py", ".ipynb", ".html"}


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


def check(task):
    """Return (lines to print, hits). A task with no leak_key has nothing to check."""
    if not task.get("leak_key"):
        return [f"{task['id']}: no answer key to check against"], []
    inputs = task["dir"] / task.get("inputs", "inputs_local")
    if not inputs.exists():
        raise SystemExit(f"no inputs at {inputs}; build them first")
    vals = key_values(json.loads((BENCH / "keys" / task["leak_key"]).read_text(encoding="utf-8")))
    phrases = task.get("leak_phrases", [])
    pats = [(v, re.compile(r"(?<![\d.])" + re.escape(v.lstrip("-")) + r"(?![\d])")) for v in sorted(vals)]
    out, hits, searched = [], [], []
    for f in sorted(inputs.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix.lower() not in TEXT:
            out.append(f"  not searched (binary data): {f.name}")
            continue
        searched.append(f.name)
        t = f.read_text(encoding="utf-8", errors="replace")
        for v, p in pats:
            for m in p.finditer(t):
                hits.append(f"{f.name}: key value {v} -> ...{t[max(0, m.start()-60):m.end()+40]!r}...")
        for ph in phrases:
            if ph in t:
                hits.append(f"{f.name}: headline phrase {ph!r}")
    out.append(f"{task['id']}: searched {len(searched)} text file(s) for {len(vals)} key values and {len(phrases)} phrases")
    out += [f"  LEAK {h}" for h in hits]
    out.append(f"{len(hits)} answer values found in inputs")
    return out, hits
