"""The benchmark runner (plan 10 Part 2): an exam proctor for Claude Code.

Seats Claude Code in a clean room with only the task and its inputs, keeps the clock, stops it at a
cap, and hands what it made to a grader in a separate process that holds the answer key.

  python benchmark/run.py --arm baseline --task <id|smoke|study|app|v0.1> --runs 1
  python benchmark/run.py --check-inputs --task all       # leak check only
  python benchmark/run.py --calibrate --task study        # graders vs known-good/bad answers, no agent
  python benchmark/run.py --task smoke_hello --dry-run [--context]   # build the room, print the launch
  python benchmark/run.py --regrade baseline/<ts>         # re-grade saved outputs, compare

Every batch starts with the clean-room check (/context inside an empty room; 0 tokens) and aborts if
the room is not stock Claude Code. Statuses: DONE, CAP, STUCK, FLAGGED, ERROR. CAP, FLAGGED and
ERROR always score FAIL; a flagged run (reaching for the original package, the repo or another run)
is a cheat (D23).
"""
import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "runner"))
import launch  # noqa: E402
import leak  # noqa: E402
import record  # noqa: E402
import room as rooms  # noqa: E402
import watch  # noqa: E402
from tasks import BENCH, select  # noqa: E402

MODEL = "claude-opus-5-5"                                   # D19: Opus 5.5 in both arms


def short(task_id):
    for p in ("smoke_", "study_", "app_"):
        task_id = task_id.removeprefix(p)
    return task_id[:14]


def room_check(bdir=None):
    text = launch.context(rooms.probe())
    problems = rooms.clean_check(text)
    if bdir:
        (bdir / "room_check.txt").write_text(text + "\n\nproblems: " + json.dumps(problems) + "\n", encoding="utf-8",
                                             newline="\n")
    return text, problems


def check_inputs(tasks):
    bad = 0
    for t in tasks:
        lines, hits = leak.check(t)
        print("\n".join(lines))
        bad += len(hits)
    return 1 if bad else 0


def calibrate(tasks):
    """Each grader must PASS its known-good answer and FAIL its known-bad one (L11)."""
    failures, missing, checked = [], [], 0
    for t in tasks:
        cal = BENCH / "keys" / "calibration" / t["id"]          # local only: holds key values
        if t["grader"] == "none":
            continue
        if not cal.exists():
            missing.append(f"{t['id']}: no calibration pair at {cal}")
            continue
        for kind, want in (("good", True), ("bad", False)):
            for case in sorted(p for p in (cal / kind).iterdir() if p.is_dir()) or [cal / kind]:
                g = record.grade(t, case)
                checked += 1
                ok = bool(g.get("pass")) == want
                print(f"{'ok  ' if ok else 'FAIL'} {t['id']} {kind}/{case.name}: pass={g.get('pass')} ({g.get('details')})")
                if not ok:
                    failures.append(f"{t['id']} {kind}/{case.name}")
    print(f"calibration: {checked - len(failures)} of {checked} cases as expected")
    for f in failures + missing:
        print("  FAIL", f)
    return 1 if failures or missing else 0


def status_of(out, made, task):
    if out["stop"] == "FLAGGED":
        return "FLAGGED"
    if out.get("limit_status") not in (None, "allowed", "allowed_warning"):
        return "ERROR"                                      # cut off by the usage limit, not the task
    if out["stop"] and out["stop"].startswith("CAP"):
        return "CAP"
    if "STUCK.md" in made:
        return "STUCK"
    r = out["result"] or {}
    return "DONE" if r.get("subtype") == "success" and not r.get("is_error") else "ERROR"


def totals(out):
    r = out["result"] or {}
    mu = r.get("modelUsage") or {}
    if mu:
        tok = sum(m.get(k, 0) or 0 for m in mu.values()
                  for k in ("inputTokens", "outputTokens", "cacheReadInputTokens", "cacheCreationInputTokens"))
        # turns = model calls seen in the stream; the result's num_turns counts conversation turns (S1 run:
        # 2, for 11 model calls), so it is not used
        return tok, sum(m.get("outputTokens", 0) or 0 for m in mu.values()), out["turns_live"], r.get("total_cost_usd")
    t = out["tokens_live"]
    return sum(t.values()), t["output_tokens"], out["turns_live"], None


def run_one(task, arm, k, ts, bdir, model, caps_override):
    run_id = f"{ts}-{short(task['id'])}-{arm[0]}{k}"
    lines, hits = leak.check(task)
    if hits:
        return {"task": task["id"], "run_id": run_id, "status": "ERROR", "pass": False, "score": 0,
                "tokens": 0, "output_tokens": 0, "minutes": 0, "turns": 0, "flags": ["leak-in-inputs"]}
    swept_before = rooms.sweep()                          # nothing from an earlier run survives
    room = rooms.build(task, run_id)
    caps = {**task["caps"], **{k2: v for k2, v in caps_override.items() if v is not None}}
    prompt = (room / "task.md").read_text(encoding="utf-8")
    on_tool = lambda b: watch.flags(b, room.name, task["watch"], task["watch_net"])
    print(f"[{run_id}] started in {room} (caps {caps})", flush=True)
    out = launch.run(launch.command(model), prompt, room, caps, on_tool, bdir / "raw" / f"{run_id}.jsonl",
                     tmp=rooms.tmpdir(run_id))
    dest = bdir / "raw" / run_id
    dest.mkdir(parents=True, exist_ok=True)
    # an app is graded where it was built, with its installed dependencies; collect skips those folders
    g = record.grade(task, room) if task.get("kind") == "app" else None
    made = rooms.collect(task, room, dest)
    rooms.remove(room)
    swept_after = rooms.sweep()                           # e.g. scratch the agent left beside its room
    status = status_of(out, made, task)
    g = g or record.grade(task, dest)
    (dest / "grade.json").write_text(json.dumps(g, indent=2) + "\n", encoding="utf-8", newline="\n")
    missing = [a for a in task["answer"] if a not in made]
    passed = bool(g.get("pass")) and status in ("DONE", "STUCK") and not missing and not out["flags"]
    tok, out_tok, turns, cost = totals(out)
    row = {"task": task["id"], "run_id": run_id, "status": status, "pass": passed,
           "score": g.get("score") if passed else 0,
           "tokens": tok, "output_tokens": out_tok, "minutes": out["minutes"], "turns": turns,
           "flags": out["flags"], "stop": out["stop"], "missing": missing, "made": made,
           "grader": record.public(g), "cost_usd_api": cost, "processes": out["processes"], "orphans_killed": out["orphans_killed"],
           "orphans_left": out["orphans_left"], "exit": out["exit"], "caps": caps,
           "swept_before": swept_before, "swept_after": swept_after,
           "week_util": out["week_util"], "limit_status": out["limit_status"]}
    print(f"[{run_id}] {status} pass={passed} tokens={tok} min={out['minutes']} turns={turns} flags={out['flags']} "
          f"orphans_left={out['orphans_left']}", flush=True)
    return row


def regrade(spec):
    bdir = BENCH / "results" / spec
    card = json.loads((bdir / "scorecard.json").read_text(encoding="utf-8"))
    diffs = 0
    for r in card["runs"]:
        t = select(r["task"])[0]
        g = record.grade(t, bdir / "raw" / r["run_id"])
        same = g.get("score") == r["grader"].get("score") and g.get("pass") == r["grader"].get("pass")
        diffs += not same
        print(f"{'same' if same else 'DIFF'} {r['run_id']}: was {r['grader'].get('pass')}/{r['grader'].get('score')}, "
              f"now {g.get('pass')}/{g.get('score')}")
    print(f"regrade: {len(card['runs']) - diffs} of {len(card['runs'])} identical")
    return 1 if diffs else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arm", choices=["baseline", "kit"], default="baseline")
    ap.add_argument("--task", default="smoke_hello")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--max-min", type=float)
    ap.add_argument("--max-turns", type=int)
    ap.add_argument("--max-tokens", type=int)
    ap.add_argument("--check-inputs", action="store_true")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--context", action="store_true", help="with --dry-run: run the clean-room check")
    ap.add_argument("--regrade", metavar="ARM/TS")
    a = ap.parse_args()

    if a.regrade:
        return regrade(a.regrade)
    tasks = select(a.task)
    if a.check_inputs:
        return check_inputs(tasks)
    if a.calibrate:
        return calibrate(tasks)
    if a.arm == "kit":
        raise SystemExit("the kit arm arrives with the kit (Phase 11)")
    if a.dry_run:
        if a.context:
            text, problems = room_check()
            print("\n".join(l for l in text.splitlines() if l.startswith("**Tokens")))
            print("clean room:", "PASS (stock Claude Code)" if not problems else "FAIL")
            for p in problems:
                print("  ", p)
            if problems:
                return 1
        for t in tasks:
            r = rooms.build(t, f"dryrun-{short(t['id'])}")
            print(f"{t['id']}: room {r} holds {sorted(p.name for p in r.iterdir())}")
            print("  launch:", subprocess.list2cmdline(launch.command(a.model)), "< task.md")
            rooms.remove(r)
        return 0

    ts = dt.datetime.now().strftime("%y%m%d-%H%M%S")
    bdir = record.batch_dir(a.arm, ts)
    _, problems = room_check(bdir)
    if problems:
        print("clean room FAIL; nothing runs:", *problems, sep="\n  ")
        return 1
    version = subprocess.run([launch.exe(), "--version"], capture_output=True, text=True).stdout.strip()
    meta = {"arm": a.arm, "ts": ts, "model": a.model, "claude_version": version, "room_check": "PASS",
            "task_spec": a.task, "runs": a.runs, "usage_before": record.usage(f"before {a.arm} {ts}")}
    caps = {"minutes": a.max_min, "turns": a.max_turns, "tokens": a.max_tokens}
    rows = [run_one(t, a.arm, k, ts, bdir, a.model, caps) for t in tasks for k in range(1, a.runs + 1)]
    meta["usage_after"] = record.usage(f"after {a.arm} {ts}")
    record.write(bdir, meta, rows)
    record.trial_log(meta, rows)
    print(f"scorecard: {bdir.relative_to(BENCH.parent)}/scorecard.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
