"""Grader `bugs` (A2): match the reported bugs to the planted ones by file and line.

Config ([grade] in task.toml):  key = "a2.json"   which = "bugs" | "clean"
                                line_tolerance = 3   min_recall = 0.5   max_false_alarms = 3
A report matches a planted bug when the file is the same and the line is within `line_tolerance`; each
planted bug matches once (nearest report first). Unmatched reports are false alarms. On the clean build
there are no planted bugs, so every report is a false alarm.
Pass = (no planted bugs or recall >= min_recall) and false alarms <= max_false_alarms. Score = recall
(bugs) or pass (clean). Spraying reports over every line finds bugs but fails on false alarms.
Usage: python benchmark/grade/bugs.py <task_dir> <outputs_dir>
"""
import json
from pathlib import PurePath

from _common import args, emit, key

cfg, g, out = args()
f = out / "bugs.json"
if not f.exists():
    emit(False, 0, {"summary": "missing bugs.json"})
    raise SystemExit
try:
    reports = json.loads(f.read_text(encoding="utf-8"))
    reports = [(PurePath(str(r["file"]).replace("\\", "/")).name.lower(), int(r["line"])) for r in reports]
except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
    emit(False, 0, {"summary": f"bugs.json is not a list of {{file, line, ...}}: {e}"})
    raise SystemExit
planted = key(g["key"])["bugs"] if g["which"] == "bugs" else []
tol = g["line_tolerance"]
pairs = sorted((abs(line - b["line"]), i, j) for i, (fname, line) in enumerate(reports)
               for j, b in enumerate(planted) if fname == b["file"].lower() and abs(line - b["line"]) <= tol)
used_r, used_b = set(), set()
for _, i, j in pairs:                                        # nearest pairs first, each side used once
    if i not in used_r and j not in used_b:
        used_r.add(i)
        used_b.add(j)
false_alarms = len(reports) - len(used_r)
recall = len(used_b) / len(planted) if planted else None
ok = (recall is None or recall >= g["min_recall"]) and false_alarms <= g["max_false_alarms"]
summary = (f"found {len(used_b)} of {len(planted)} planted bugs" if planted else "clean build (no planted bugs)")
summary += f"; {false_alarms} false alarm(s) of {len(reports)} report(s)"
emit(ok, round(recall, 3) if recall is not None else int(ok),
     {"summary": summary, "recall": recall, "false_alarms": false_alarms, "reports": len(reports),
      "found": sorted(planted[j]["id"] for j in used_b)})
