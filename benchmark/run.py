"""The benchmark runner (plan 10 Part 2): an exam proctor for Claude Code.

Seats Claude Code in a clean room with only the task and its inputs, keeps the clock, stops it at a
cap, and hands what it made to a grader in a separate process that holds the answer key.

  python benchmark/run.py --arm baseline --task <id|smoke|study|app|v0.1> --runs 1
  python benchmark/run.py --arm kit --task app_a1_build --runs 1      # the kit: /autonomous:new-app task.md
  python benchmark/run.py --check-inputs --task all       # leak check only
  python benchmark/run.py --calibrate --task study        # graders vs known-good/bad answers, no agent
  python benchmark/run.py --task smoke_hello --dry-run [--context]   # build the room, print the launch
  python benchmark/run.py --regrade baseline/<ts>         # re-grade saved outputs, compare

Every batch starts with the clean-room check (/context inside an empty room; 0 tokens) and aborts if
the room is not stock Claude Code. Statuses: DONE, CAP, STUCK, FLAGGED, ERROR. CAP, FLAGGED and
ERROR always score FAIL; a flagged run (reaching for the original package, the repo or another run)
is a cheat (D23).

Kit arm (Phase 11): the same room, model, tools and caps, plus `--plugin-dir plugin`, and the prompt
`/autonomous:new-app task.md`. Main starts team.py, whose roles are separate sessions the stream here
cannot see, so after the run: the app is graded and collected from runs/<id>/app/, the roles' tokens
are added from registry.json, the cheat watch is run over their logs, and the status is the team's.
Kit arm tasks: app builds (A1, A3, A4). A2 is a review task with no kit entry yet; studies need new-study.
"""
import argparse
import datetime as dt
import json
import shutil
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
PLUGIN = BENCH.parent / "plugin"
# the kit arm loads a fresh copy from outside the repo: ${CLAUDE_SKILL_DIR} would otherwise put the repo's path
# into Main's first command, which the cheat watch rightly flags (and a user's installed copy lives elsewhere too)
KIT_COPY = Path("C:/akit/plugin")
KIT_TASKS = {"app_a1_build", "app_a3_impossible", "app_a4_rota"}


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
    if arm == "kit":
        prompt = "/autonomous:new-app task.md"
    print(f"[{run_id}] started in {room} (caps {caps})", flush=True)
    if arm == "kit":
        shutil.rmtree(KIT_COPY, ignore_errors=True)
        shutil.copytree(PLUGIN, KIT_COPY, ignore=shutil.ignore_patterns("__pycache__"))
    out = launch.run(launch.command(model, KIT_COPY if arm == "kit" else None), prompt, room, caps, on_tool,
                     bdir / "raw" / f"{run_id}.jsonl", tmp=rooms.tmpdir(run_id))
    dest = bdir / "raw" / run_id
    dest.mkdir(parents=True, exist_ok=True)
    kit = kit_after(task, room, dest, on_tool) if arm == "kit" else None
    work = kit["app"] if kit else room
    # an app is graded where it was built, with its installed dependencies; collect skips those folders
    g = record.grade(task, work) if task.get("kind") == "app" else None
    made = rooms.collect(task, work, dest)
    rooms.remove(room)
    swept_after = rooms.sweep()                           # e.g. scratch the agent left beside its room
    status = status_of(out, made, task)
    if kit:
        out["flags"] += kit["flags"]
        status = "FLAGGED" if kit["flags"] else kit["status"] if status in ("DONE", "STUCK") else status
    g = g or record.grade(task, dest)
    (dest / "grade.json").write_text(json.dumps(g, indent=2) + "\n", encoding="utf-8", newline="\n")
    missing = [a for a in task["answer"] if a not in made]
    passed = bool(g.get("pass")) and status in ("DONE", "STUCK") and not missing and not out["flags"]
    tok, out_tok, turns, cost = totals(out)
    if kit:
        tok, out_tok, turns = tok + kit["tokens"], out_tok + kit["output_tokens"], turns + kit["turns"]
    row = {"task": task["id"], "run_id": run_id, "status": status, "pass": passed,
           "score": g.get("score") if passed else 0,
           "tokens": tok, "output_tokens": out_tok, "minutes": out["minutes"], "turns": turns,
           "flags": out["flags"], "stop": out["stop"], "missing": missing, "made": made,
           "grader": record.public(g), "cost_usd_api": cost, "processes": out["processes"], "orphans_killed": out["orphans_killed"],
           "orphans_left": out["orphans_left"], "exit": out["exit"], "caps": caps,
           "swept_before": swept_before, "swept_after": swept_after,
           "week_util": out["week_util"], "limit_status": out["limit_status"],
           "kit": {k: v for k, v in kit.items() if k != "app"} if kit else None}
    print(f"[{run_id}] {status} pass={passed} tokens={tok} min={out['minutes']} turns={turns} flags={out['flags']} "
          f"orphans_left={out['orphans_left']}", flush=True)
    return row


def kit_after(task, room, dest, on_tool):
    """After a kit-arm run: find the team's run folder, pull the app and the team's books, add the roles'
    usage, and run the cheat watch over the roles' logs (their tool calls never reach this stream)."""
    runs = sorted((room / "runs").glob("*/run.json")) if (room / "runs").exists() else []
    if not runs:
        return {"app": room, "status": "ERROR", "team_status": None, "tokens": 0, "output_tokens": 0, "turns": 0,
                "flags": [], "note": "no runs/<id>/run.json: team.py never started"}
    run = runs[-1].parent
    state = json.loads((run / "run.json").read_text(encoding="utf-8"))
    reg = json.loads((run / "registry.json").read_text(encoding="utf-8"))
    app = run / "app"
    stuck = sorted(run.glob("*/STUCK.md"))
    if stuck and not (app / "STUCK.md").exists():          # the spec-writer may be the one who stopped
        shutil.copy2(stuck[0], app / "STUCK.md")
    books = dest / "kit"
    books.mkdir(parents=True, exist_ok=True)
    for f in ("run.json", "registry.json", "ledger.tsv", "RUN_REPORT.md", "kit.toml"):
        if (run / f).exists():
            shutil.copy2(run / f, books / f)
    for d in ("spec", "checks", "verdicts", "evidence", "handoffs", "release", "team-records"):
        if (run / d).exists():
            shutil.copytree(run / d, books / d, dirs_exist_ok=True)
    flags = []
    for log in (run / "team-records/logs").glob("*.jsonl"):
        for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "assistant":
                for b in ev.get("message", {}).get("content", []):
                    if b.get("type") == "tool_use":
                        flags += [f"{log.stem}:{f}" for f in on_tool(b)]
    s = str(state.get("status"))
    status = "DONE" if s == "DONE" else "STUCK" if s == "STUCK" else "CAP" if s.startswith("CAP") else "ERROR"
    return {"app": app, "status": status, "team_status": s, "team_note": state.get("note"),
            "rounds": state.get("rounds"), "tokens": sum(r["tokens"] for r in reg),
            "output_tokens": sum(r["tokens_by_kind"]["output_tokens"] for r in reg),
            "turns": sum(r["turns"] for r in reg), "roles": [[r["step"], r["stop"], r["tokens"]] for r in reg],
            "flags": sorted(set(flags))}


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
    if a.arm == "kit" and not {t["id"] for t in tasks} <= KIT_TASKS:
        raise SystemExit(f"the kit arm runs only {sorted(KIT_TASKS)} so far (A2 has no kit entry; studies need new-study)")
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
            kit = a.arm == "kit"
            print("  launch:", subprocess.list2cmdline(launch.command(a.model, PLUGIN if kit else None)),
                  "<<< /autonomous:new-app task.md" if kit else "< task.md")
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
