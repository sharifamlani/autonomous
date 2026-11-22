"""Shared grader helpers: read the task config, the answer file, and the numbers a notebook printed."""
import json
import re
import sys
import tomllib
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
NUM = re.compile(r"-?\d+\.\d+(?:[eE][-+]?\d+)?")


def args():
    task_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
    cfg = tomllib.loads((task_dir / "task.toml").read_text(encoding="utf-8"))
    return cfg, cfg["grade"], out


def key(name):
    return json.loads((BENCH / "keys" / name).read_text(encoding="utf-8"))


def answer(out):
    """The parsed answer.json, or (None, reason)."""
    f = out / "answer.json"
    if not f.exists():
        return None, "missing answer.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")), ""
    except json.JSONDecodeError as e:
        return None, f"answer.json is not valid JSON: {e}"


def notebook_numbers(out, name="replicate.ipynb"):
    """Every decimal number in the notebook's saved outputs, or None if it has no outputs.

    The copy check: a reported number must have been printed by the agent's own code, not typed in.
    """
    f = out / name
    if not f.exists():
        return None
    try:
        nb = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    texts = []
    for c in nb.get("cells", []):
        for o in c.get("outputs", []) or []:
            if "text" in o:
                texts.append("".join(o["text"]) if isinstance(o["text"], list) else o["text"])
            for v in (o.get("data") or {}).values():
                texts.append("".join(v) if isinstance(v, list) else str(v))
    if not texts:
        return None
    return [float(m) for m in NUM.findall("\n".join(texts))]


def printed(nums, x, tol=0.0051):
    """True if the notebook printed x, at 2 or more decimals. A tolerance, not rounded equality: rounding
    a 4-decimal printout to 3 can land one digit off (calibration R6, 2026-11-22)."""
    return nums is not None and any(abs(n - x) <= tol for n in nums)


def emit(passed, score, details):
    print(json.dumps({"pass": bool(passed), "score": score, "details": details}))
