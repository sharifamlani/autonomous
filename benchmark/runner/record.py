"""Write what a batch did: scorecard.json/.md, TRIAL_LOG rows, weekly usage before/after (cc.py)."""
import datetime as dt
import json
import subprocess
import sys

from tasks import BENCH, ROOT

TRIAL_LOG = ROOT / "research" / "TRIAL_LOG.tsv"
COLS = ["task", "run_id", "status", "pass", "score", "tokens", "output_tokens", "minutes", "turns", "flags"]


def batch_dir(arm, ts):
    d = BENCH / "results" / arm / ts
    (d / "raw").mkdir(parents=True, exist_ok=True)               # raw/ is gitignored
    return d


def grade(task, outputs):
    """Run the task's grader in its own process; it prints one JSON object."""
    if task["grader"] == "none":
        return {"pass": None, "score": None, "details": "no grader (status decides)"}
    g = BENCH / "grade" / f"{task['grader']}.py"
    p = subprocess.run([sys.executable, str(g), str(task["dir"]), str(outputs)],
                       capture_output=True, text=True, encoding="utf-8", timeout=600)
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"pass": False, "score": 0, "details": f"grader crashed: {(p.stderr or p.stdout)[-500:]}"}


def usage(label):
    """Weekly usage via the local .packages/Claude_code/cc.py, when this machine has it."""
    sys.path.insert(0, str(ROOT / ".packages" / "Claude_code"))
    try:
        import cc
        return cc.log_usage(label)["limits"]
    except Exception as e:                                       # optional: never fails a batch
        return [{"name": "unavailable", "pct": None, "resets": str(e)[:100]}]


def write(bdir, meta, rows):
    (bdir / "scorecard.json").write_text(json.dumps({"meta": meta, "runs": rows}, indent=2), encoding="utf-8")
    md = [f"# Scorecard {meta['arm']} {meta['ts']}", "",
          f"model {meta['model']} · claude {meta['claude_version']} · room check: {meta['room_check']}", "",
          "Weekly usage before: " + "; ".join(f"{u['name']} {u['pct']}%" for u in meta["usage_before"]),
          "Weekly usage after:  " + "; ".join(f"{u['name']} {u['pct']}%" for u in meta.get("usage_after", [])), "",
          "| " + " | ".join(COLS) + " |", "|" + "---|" * len(COLS)]
    for r in rows:
        md.append("| " + " | ".join(str(r.get(c, "")) for c in COLS) + " |")
    (bdir / "scorecard.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")


def trial_log(meta, rows):
    """One row per scored run (smoke runs are not trials)."""
    with TRIAL_LOG.open("a", encoding="utf-8", newline="\n") as f:
        for r in rows:
            if r["task"].startswith("smoke_"):
                continue
            f.write("\t".join(str(x) for x in [
                dt.date.today().isoformat(), "benchmark", r["run_id"], meta["arm"],
                f"model={meta['model']};claude={meta['claude_version']}", r["task"], "pass",
                int(bool(r["pass"])), r["tokens"], r["minutes"], r.get("cost_usd_api", ""),
                f"status={r['status']};flags={','.join(r['flags'])}"]) + "\n")
