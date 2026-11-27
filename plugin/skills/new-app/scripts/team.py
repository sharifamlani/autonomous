"""team.py: the kit's conductor (plan 09 architecture §1-§8). The players are agents; the score is this file.

  python team.py app "<idea, or a path to a spec file>"     the whole team; writes RUN_REPORT.md and release/
  python team.py init app "<idea>"                         just make the run folder
  python team.py run <role> --run <dir> [--round N]        one role step (for debugging a single role)

Options: --run DIR (default ./runs/<YYMMDD-HHMM>-<slug>), --model, --max-min, --max-tokens, --rounds,
--roles DIR (role prompts; default the plugin's agents/). Defaults come from the plugin's kit.toml, which is
copied into every run folder (the iteration knob, architecture §10).

The flow is a fixed state machine, not a model's choice (rule L7):
  SPEC -> BUILD(r) -> CHECK(r): qa || tester -> both PASS: DONE | any FAIL, r < R: BUILD(r+1) | r = R: STUCK
  any role writes STUCK.md: STUCK.   token, minute or turn cap: CAP.   then RUN_REPORT.md and release/.
team.py moves on only on a verdict file, never on an agent saying "done". A verdict passes only if every
check passed, each check's evidence file exists, and (tester) each check was observed in the running app
(L2). A missing or malformed verdict is a FAIL, said loudly (L8). The builder keeps its context across
rounds (--resume); checkers start fresh every round (L4).

Every child runs with AUTONOMOUS_ROLE and AUTONOMOUS_RUN set, so the plugin's gate.py fences it, inside its
own Windows job object (a process group elsewhere), so a cap stops everything it started. Tokens are summed
live across all children against one team cap (a parent's totals omit its children, spike 4.8).
Main starts this in the background with a long Bash timeout (a background command's default limit is 10
minutes, scripts/kit/check_bg_wait.py) and waits.
"""
import argparse
import json
import os
import queue
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
import tomllib
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[3]
FOLDERS = {"app": ["spec", "checks", "app", "evidence", "verdicts", "handoffs", "team-records/logs", "prompts"]}
CWD = {"spec-writer": "spec", "builder": "app", "qa": "app", "tester": "."}      # architecture §7
PORT = {"builder": "8100", "qa": "8101", "tester": "8102"}                       # parallel checkers never collide
TOOLS = "Bash,Read,Write,Edit,Glob,Grep,WebFetch"
CLEAN = ["--setting-sources", "project,local", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
STRIP = {"CLAUDECODE", "CLAUDE_PID", "CLAUDE_EFFORT", "AI_AGENT", "CLAUDE_AGENT_SDK_VERSION"}
TOKEN_FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")


def exe():
    """claude.exe itself on Windows: the npm `claude.cmd` wrapper would route arguments through cmd.exe quoting."""
    w = shutil.which("claude")
    if not w:
        raise SystemExit("claude is not on PATH")
    real = Path(w).parent / "node_modules/@anthropic-ai/claude-code/bin/claude.exe"
    return str(real) if w.lower().endswith(".cmd") and real.exists() else w


# ---- kill everything a child started (copied from benchmark/runner/launch.py, smoke R3) -------------------
if os.name == "nt":
    import ctypes
    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _k32.CreateJobObjectW.restype = ctypes.c_void_p
    _k32.OpenProcess.restype = ctypes.c_void_p

    class _BasicLimit(ctypes.Structure):
        _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                    ("LimitFlags", ctypes.c_uint32), ("MinimumWorkingSetSize", ctypes.c_size_t),
                    ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", ctypes.c_uint32),
                    ("Affinity", ctypes.c_size_t), ("PriorityClass", ctypes.c_uint32),
                    ("SchedulingClass", ctypes.c_uint32)]

    class _ExtendedLimit(ctypes.Structure):
        _fields_ = [("Basic", _BasicLimit), ("IoInfo", ctypes.c_uint64 * 6), ("ProcessMemoryLimit", ctypes.c_size_t),
                    ("JobMemoryLimit", ctypes.c_size_t), ("PeakProcessMemoryUsed", ctypes.c_size_t),
                    ("PeakJobMemoryUsed", ctypes.c_size_t)]

    class _Accounting(ctypes.Structure):
        _fields_ = [("TotalUserTime", ctypes.c_int64), ("TotalKernelTime", ctypes.c_int64),
                    ("ThisPeriodTotalUserTime", ctypes.c_int64), ("ThisPeriodTotalKernelTime", ctypes.c_int64),
                    ("TotalPageFaultCount", ctypes.c_uint32), ("TotalProcesses", ctypes.c_uint32),
                    ("ActiveProcesses", ctypes.c_uint32), ("TotalTerminatedProcesses", ctypes.c_uint32)]


class Job:
    """Every process a child starts stays inside its job, even when its parent dies (Git Bash programs lose
    their parent link, so a process-tree kill misses them). Killing the job kills them all. On POSIX the
    child leads its own process group instead."""

    def __init__(self, proc):
        self.proc = proc
        if os.name != "nt":
            return
        self.h = ctypes.c_void_p(_k32.CreateJobObjectW(None, None))
        info = _ExtendedLimit()
        info.Basic.LimitFlags = 0x2000                                  # KILL_ON_JOB_CLOSE
        if not _k32.SetInformationJobObject(self.h, 9, ctypes.byref(info), ctypes.sizeof(info)):
            raise OSError(ctypes.get_last_error(), "SetInformationJobObject")
        ph = ctypes.c_void_p(_k32.OpenProcess(0x0101, False, proc.pid))  # SET_QUOTA | TERMINATE
        ok = _k32.AssignProcessToJobObject(self.h, ph)
        _k32.CloseHandle(ph)
        if not ok:
            raise OSError(ctypes.get_last_error(), "AssignProcessToJobObject")

    def active(self):
        if os.name != "nt":
            try:
                os.killpg(self.proc.pid, 0)
                return 1
            except (ProcessLookupError, PermissionError):
                return 0
        a = _Accounting()
        _k32.QueryInformationJobObject(self.h, 1, ctypes.byref(a), ctypes.sizeof(a), None)
        return a.ActiveProcesses

    def kill(self):
        if os.name == "nt":
            _k32.TerminateJobObject(self.h, 1)
        else:
            try:
                os.killpg(self.proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        for _ in range(50):
            if not self.active():
                break
            time.sleep(0.1)
        return self.active()

    def close(self):
        if os.name == "nt":
            _k32.CloseHandle(self.h)


# ---- the run's books: run.json (state), registry.json (role steps), ledger.tsv (append-only usage) ------
class Books:
    def __init__(self, run):
        self.run = run
        self.state = json.loads((run / "run.json").read_text(encoding="utf-8"))
        self.kit = tomllib.loads((run / "kit.toml").read_text(encoding="utf-8"))
        self.lock = threading.Lock()
        self.live = {}

    def _write(self, name, obj):
        tmp = self.run / f"{name}.tmp"
        tmp.write_text(json.dumps(obj, indent=1), encoding="utf-8")
        os.replace(tmp, self.run / name)

    def registry(self):
        return json.loads((self.run / "registry.json").read_text(encoding="utf-8"))

    def tokens(self):
        return sum(s["tokens"] for s in self.registry()) + sum(self.live.values())

    def minutes(self):
        return (time.time() - self.state["started"]) / 60

    def over(self):
        c = self.state["caps"]
        if c["minutes"] and self.minutes() > c["minutes"]:
            return "CAP:minutes"
        if c["tokens"] and self.tokens() > c["tokens"]:
            return "CAP:tokens"
        return None

    def set_live(self, key, n):
        with self.lock:
            self.live[key] = n

    def close_step(self, key, row):
        with self.lock:
            self.live.pop(key, None)
            reg = self.registry() + [row]
            self._write("registry.json", reg)
            total = sum(s["tokens"] for s in reg)
            with open(self.run / "ledger.tsv", "a", encoding="utf-8", newline="\n") as f:
                f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')}\t{key}\t{row['stop']}\t{row['tokens']}\t{total}\n")

    def set_state(self, **kv):
        with self.lock:
            self.state.update(kv)
            self._write("run.json", self.state)


# ---- one role step ---------------------------------------------------------------------------------------
def role_prompt(roles, role, run):
    """The role file's body (frontmatter dropped), saved where the child's --append-system-prompt-file reads it."""
    text = (roles / f"{role}.md").read_text(encoding="utf-8")
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    out = run / "prompts" / f"{role}.md"
    out.write_text(text, encoding="utf-8")
    return out


def child_env(role, run):
    e = {k: v for k, v in os.environ.items() if not (k.startswith("CLAUDE_CODE_") or k in STRIP)}
    e.update(AUTONOMOUS_ROLE=role, AUTONOMOUS_RUN=str(run), PORT=PORT.get(role, "8100"))
    return e


def run_role(run, books, role, task, rnd, roles, resume=None):
    """Run one role step to completion or a cap. Returns its registry row."""
    key = f"r{rnd}-{role}"
    kit = books.kit
    model = kit["models"].get(role, books.state["model"])
    cmd = [exe(), "-p", "--output-format", "stream-json", "--verbose", "--model", model,
           "--permission-mode", "acceptEdits", "--permission-prompts", "none", "--allowedTools", TOOLS,
           "--plugin-dir", str(PLUGIN), "--append-system-prompt-file", str(role_prompt(roles, role, run)), *CLEAN]
    if resume:
        cmd += ["--resume", resume]
    max_turns = kit["turns"].get(role, 0)
    t0 = time.time()
    proc = subprocess.Popen(cmd, cwd=run / CWD[role], env=child_env(role, run), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", bufsize=1,
                            start_new_session=os.name != "nt")
    job = Job(proc)                                         # before the child can start anything
    proc.stdin.write(task)
    proc.stdin.close()
    lines, err = queue.Queue(), []
    threading.Thread(target=lambda: ([lines.put(l) for l in proc.stdout], lines.put(None)), daemon=True).start()
    threading.Thread(target=lambda: err.extend(proc.stderr), daemon=True).start()

    usage, result, stop, sid = {}, None, None, None
    with open(run / "team-records/logs" / f"{key}.jsonl", "w", encoding="utf-8", newline="\n") as log:
        while True:
            try:
                line = lines.get(timeout=1)
            except queue.Empty:
                line = ""
            if line is None:
                break
            if line.strip():
                log.write(line)
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    ev = {}
                sid = sid or ev.get("session_id")
                if ev.get("type") == "assistant":
                    m = ev.get("message", {})
                    u = usage.setdefault(m.get("id"), {})
                    for k in TOKEN_FIELDS:
                        u[k] = max(u.get(k, 0), (m.get("usage") or {}).get(k, 0) or 0)
                    books.set_live(key, sum(sum(x.values()) for x in usage.values()))
                elif ev.get("type") == "result":
                    result = ev
            stop = books.over() or ("CAP:turns" if max_turns and len(usage) > max_turns else None)
            if stop:
                break

    if proc.poll() is None:
        job.kill()
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        job.kill()
    left = job.kill()                                       # e.g. a server the role left running
    job.close()
    tokens = {k: sum(u.get(k, 0) for u in usage.values()) for k in TOKEN_FIELDS}
    row = {"step": key, "role": role, "round": rnd, "session_id": sid, "resumed": bool(resume),
           "stop": stop or ("DONE" if result and not result.get("is_error") else "ERROR"),
           "started": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t0)),
           "minutes": round((time.time() - t0) / 60, 2), "turns": len(usage), "tokens": sum(tokens.values()),
           "tokens_by_kind": tokens, "exit": proc.returncode, "orphans_left": left,
           "stderr": "".join(err)[-500:]}
    books.close_step(key, row)
    return row


# ---- verdicts: the only thing team.py acts on (architecture §6) --------------------------------------------
def verdict(run, role, rnd):
    """(PASS | FAIL, reason, checks). PASS needs every check PASS with an existing evidence file; the tester's
    checks must also be observed in the running app, not inferred from code."""
    f = run / "verdicts" / f"r{rnd}-{role}.json"
    if not f.exists():
        return "FAIL", f"no verdict file {f.name}", []
    try:
        v = json.loads(f.read_text(encoding="utf-8"))
        checks = v["checks"]
        said = str(v["verdict"]).upper()
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        return "FAIL", f"malformed verdict {f.name}: {e}", []
    if said != "PASS":
        return "FAIL", f"{role} said {said}", checks
    if not checks:
        return "FAIL", f"{role} said PASS with no checks", checks
    for c in checks:
        if str(c.get("status", "")).upper() != "PASS":
            return "FAIL", f"{role} said PASS but check {c.get('id')} is {c.get('status')}", checks
        ev = c.get("evidence")
        if not ev or not (run / ev).is_file():
            return "FAIL", f"{role} said PASS but check {c.get('id')} has no evidence file ({ev})", checks
        if role == "tester" and str(c.get("basis", "")).lower() != "observed":
            return "FAIL", f"tester said PASS but check {c.get('id')} was not observed", checks
    return "PASS", f"{len(checks)} checks passed with evidence", checks


def stuck_file(run):
    hits = [p for p in run.glob("*/STUCK.md")]
    return hits[0].relative_to(run).as_posix() if hits else None


# ---- the run folder and the pipeline ---------------------------------------------------------------------
SEED_SKIP = {"runs", ".git", "node_modules", ".venv", "venv", "__pycache__"}
SEED_MAX = 500


def seed(folder, idea_file, app):
    """Files already in the folder the idea file sits in (a given test suite, data, an existing codebase) are the
    app's starting point: copied into app/, where the builder works and the checkers look."""
    files = [p for p in folder.rglob("*") if p.is_file() and p != idea_file and p.name != "autonomous-idea.md"
             and not (set(p.relative_to(folder).parts) & SEED_SKIP)]
    if len(files) > SEED_MAX:
        raise SystemExit(f"{folder} holds {len(files)} files (more than {SEED_MAX}): start from a project folder")
    for p in files:
        dest = app / p.relative_to(folder)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)


def init(kind, idea, a):
    slug = re.sub(r"[^a-z0-9]+", "-", Path(idea).stem.lower() if Path(idea).is_file() else idea.lower())[:24].strip("-")
    run = Path(a.run or f"runs/{time.strftime('%y%m%d-%H%M')}-{slug or kind}").resolve()
    for f in FOLDERS[kind]:
        (run / f).mkdir(parents=True, exist_ok=True)
    src = Path(idea)
    (run / "idea.md").write_text(src.read_text(encoding="utf-8") if src.is_file() else idea, encoding="utf-8")
    if src.is_file():
        seed(src.resolve().parent, src.resolve(), run / "app")
    shutil.copy(a.kit, run / "kit.toml")
    kit = tomllib.loads((run / "kit.toml").read_text(encoding="utf-8"))
    caps = {"minutes": a.max_min or kit["caps"][f"{kind}_minutes"], "tokens": a.max_tokens or kit["caps"][f"{kind}_tokens"]}
    (run / "run.json").write_text(json.dumps(
        {"id": run.name, "kind": kind, "model": a.model or kit["models"]["default"], "caps": caps,
         "max_rounds": a.rounds or kit[kind]["max_rounds"], "started": time.time(), "state": "INIT",
         "status": "RUNNING"}, indent=1), encoding="utf-8")
    (run / "registry.json").write_text("[]", encoding="utf-8")
    (run / "ledger.tsv").write_text("time\tstep\tevent\ttokens\tcumulative_tokens\n", encoding="utf-8")
    return run


TASKS = {
    "spec-writer": "SPEC: write the spec, the rubric and the hidden acceptance checks for the idea in ../idea.md.",
    "builder": "BUILD round {r}: build the app in this folder from ../spec/spec.md and ../spec/rubric.md.",
    "builder_fix": ("BUILD round {r}: round {p} failed its checks. Read ../verdicts/r{p}-qa.json and "
                    "../verdicts/r{p}-tester.json (and any repro in ../handoffs/) and fix what they found."),
    "qa": "CHECK round {r}: review the app in this folder against ../spec/rubric.md. Write ../verdicts/r{r}-qa.json.",
    "tester": "CHECK round {r}: start the app in app/ and walk checks/ as a user. Write verdicts/r{r}-tester.json.",
}


def app(idea, a):
    run = init("app", idea, a)
    books = Books(run)
    roles = Path(a.roles)
    print(f"run folder: {run}", flush=True)
    capped = lambda row: row["stop"] if row["stop"].startswith("CAP") else None
    rounds, status, note, builder_sid = [], None, "", None

    books.set_state(state="SPEC")
    status = capped(run_role(run, books, "spec-writer", TASKS["spec-writer"], 0, roles))
    if not status:
        if stuck_file(run):
            status, note = "STUCK", f"{stuck_file(run)} written at SPEC"
        elif not all((run / p).is_file() for p in ("spec/spec.md", "spec/rubric.md")) or not any((run / "checks").iterdir()):
            status, note = "STUCK", "the spec-writer left no spec/spec.md, spec/rubric.md or checks/"
    R = books.state["max_rounds"]
    for r in range(1, R + 1):
        if status:
            break
        books.set_state(state=f"BUILD({r})")
        task = TASKS["builder"].format(r=r) if r == 1 else TASKS["builder_fix"].format(r=r, p=r - 1)
        row = run_role(run, books, "builder", task, r, roles, resume=builder_sid)
        builder_sid = builder_sid or row["session_id"]
        if (status := capped(row)):
            break
        if stuck_file(run):
            status, note = "STUCK", f"{stuck_file(run)} written in round {r}"
            break
        books.set_state(state=f"CHECK({r})")
        (run / "evidence" / f"r{r}").mkdir(exist_ok=True)
        rows = {}
        threads = [threading.Thread(target=lambda ro=ro: rows.__setitem__(
            ro, run_role(run, books, ro, TASKS[ro].format(r=r), r, roles))) for ro in ("qa", "tester")]
        [t.start() for t in threads]
        [t.join() for t in threads]
        v = {ro: verdict(run, ro, r) for ro in ("qa", "tester")}
        rounds.append({"round": r, **{ro: {"verdict": x[0], "reason": x[1]} for ro, x in v.items()}})
        if (status := next((s for s in (capped(x) for x in rows.values()) if s), None)):
            break
        if all(x[0] == "PASS" for x in v.values()):
            status = "DONE"
        elif r == R:
            status, note = "STUCK", f"not approved after {R} rounds"
    books.set_state(state="REPORT", status=status, note=note, rounds=rounds,
                    minutes=round(books.minutes(), 2), tokens=books.tokens())
    report(run, books)
    release_card(run, books)
    print(f"status: {status}  tokens: {books.tokens():,}  minutes: {books.minutes():.1f}  report: "
          f"{run / 'RUN_REPORT.md'}", flush=True)
    return status


def report(run, books):
    s, reg = books.state, books.registry()
    by_role = {}
    for x in reg:
        by_role[x["role"]] = by_role.get(x["role"], 0) + x["tokens"]
    lines = [f"# Run {s['id']}        status: {s['status']}", "",
             "Idea: " + (run / "idea.md").read_text(encoding="utf-8").strip().splitlines()[0][:200],
             f"Usage {s['tokens']:,} tokens · {s['minutes']} min · {len(s['rounds'])} build round(s) · "
             f"0 interventions (caps {s['caps']['minutes']} min, {s['caps']['tokens']:,} tokens)"]
    if s.get("note"):
        lines.append(f"Why: {s['note']}")
    lines += ["", "| Round | QA | Tester |", "|---|---|---|"]
    lines += [f"| {x['round']} | {x['qa']['verdict']}: {x['qa']['reason']} | {x['tester']['verdict']}: "
              f"{x['tester']['reason']} |" for x in s["rounds"]]
    lines += ["", "| Role | Tokens |", "|---|---|"] + [f"| {k} | {v:,} |" for k, v in by_role.items()]
    lines += ["", "Verdicts: `verdicts/`. Evidence: `evidence/`. The app: `app/` (how to start it: `app/RUN.md`).",
              "Every role step: `registry.json`; usage as it happened: `ledger.tsv`; session and gate logs: `team-records/`.",
              "This report is written by team.py from those files, never by an agent."]
    (run / "RUN_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def release_card(run, books):
    """release/: plain facts for an outside marketer (architecture §6b). Every number names its source."""
    s = books.state
    rel = run / "release"
    (rel / "media").mkdir(parents=True, exist_ok=True)
    last = s["rounds"][-1] if s["rounds"] else None
    checks = verdict(run, "tester", last["round"])[2] if last else []
    nums = [("status", s["status"], "run.json:status"), ("tokens", s["tokens"], "run.json:tokens"),
            ("minutes", s["minutes"], "run.json:minutes"), ("build_rounds", len(s["rounds"]), "run.json:rounds"),
            ("tester_checks", len(checks), f"verdicts/r{last['round']}-tester.json:checks" if last else "-"),
            ("tester_checks_passed", sum(str(c.get("status", "")).upper() == "PASS" for c in checks),
             f"verdicts/r{last['round']}-tester.json:checks[].status" if last else "-")]
    (rel / "numbers.tsv").write_text("name\tvalue\tsource\n" + "".join(f"{n}\t{v}\t{src}\n" for n, v, src in nums),
                                     encoding="utf-8")
    for png in (run / "evidence").rglob("*.png"):
        shutil.copy(png, rel / "media" / f"{png.parent.name}-{png.name}")
    card = [f"# {s['id']}: {s['status']}", "",
            "What: " + (run / "idea.md").read_text(encoding="utf-8").strip().splitlines()[0][:200],
            f"How it was checked: {nums[5][1]} of {nums[4][1]} tester checks passed, observed in the running app; "
            f"QA reviewed against spec/rubric.md.",
            f"Usage: {s['tokens']:,} tokens, {s['minutes']} minutes, {len(s['rounds'])} build round(s), 0 interventions.",
            "Run it: see app/RUN.md. Every number above is in numbers.tsv with its source file."]
    (rel / "card.md").write_text("\n".join(card) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["app", "init", "run"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--run")
    ap.add_argument("--model")
    ap.add_argument("--max-min", type=float)
    ap.add_argument("--max-tokens", type=int)
    ap.add_argument("--rounds", type=int)
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--roles", default=str(PLUGIN / "agents"))
    ap.add_argument("--kit", default=str(PLUGIN / "kit.toml"))
    a = ap.parse_args()
    if a.cmd == "app":
        status = app(" ".join(a.args), a)
        sys.exit(0 if status == "DONE" else 1)
    if a.cmd == "init":
        print(init(a.args[0], " ".join(a.args[1:]), a))
        return
    role, run = a.args[0], Path(a.run).resolve()
    print(json.dumps(run_role(run, Books(run), role, TASKS[role].format(r=a.round), a.round, Path(a.roles)), indent=1))


if __name__ == "__main__":
    main()
