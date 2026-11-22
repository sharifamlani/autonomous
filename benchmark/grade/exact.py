"""Grader `exact`: one output file must hold exactly the expected text (after trimming whitespace).

Used by smoke tasks. Config in task.toml:  [grade] file = "answer.txt"  expect = "hello"
Usage: python benchmark/grade/exact.py <task_dir> <outputs_dir>   -> prints one JSON object
"""
import json
import sys
import tomllib
from pathlib import Path

task_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
g = tomllib.loads((task_dir / "task.toml").read_text(encoding="utf-8"))["grade"]
f = out / g["file"]
if not f.exists():
    res = {"pass": False, "score": 0, "details": f"missing {g['file']}"}
else:
    got = f.read_text(encoding="utf-8", errors="replace").strip()
    ok = got == g["expect"]
    res = {"pass": ok, "score": int(ok), "details": f"expected {g['expect']!r}, got {got[:80]!r}"}
print(json.dumps(res))
