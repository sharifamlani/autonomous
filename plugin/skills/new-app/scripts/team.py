"""team.py: the kit's launcher (plan 09, row 11.3a). One `claude -p` per role, team-wide caps, a fixed order.

  python team.py app "<idea, or a path to a spec file>"     the whole team: spec-writer -> builder -> qa || tester,
                                                           up to 3 rounds; writes <run>/RUN_REPORT.md
  python team.py init app "<idea>"                         just make the run folder
  python team.py run <role> --run <dir> [--round N]        one role session (for debugging a single role)

Options: --run DIR (default ./autonomous-run-<time>), --model, --max-min, --max-tokens, --rounds,
--roles DIR (role prompts; default the plugin's agents/).

The order is fixed here, not chosen by a model (rule L7). Every child runs with AUTONOMOUS_ROLE and
AUTONOMOUS_RUN set, so the plugin's gate.py fences it, and inside its own Windows job object (a process group
elsewhere), so a cap stops everything it started. Tokens are summed live across all children into one ledger;
the team cap is the sum, not per role. Status: DONE | STUCK | CAP:<what> | FAIL | ERROR.
Main starts this in the background (the Bash tool cuts foreground commands at 10 minutes) and waits.
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
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[3]
CAPS = {"app": {"minutes": 120, "tokens": 15_000_000}}            # D26: same caps as the baseline arm
FOLDERS = {"app": ["spec", "checks", "app", "evidence", "verdicts", "handoffs"]}
CWD = {"spec-writer": "spec", "builder": "app", "qa": "verdicts", "tester": "evidence"}
PORT = {"builder": "8100", "qa": "8101", "tester": "8102"}         # parallel roles never share a port
TOOLS = "Bash,Read,Write,Edit,Glob,Grep,WebFetch"
CLEAN = ["--setting-sources", "project,local", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
STRIP = {"CLAUDECODE", "CLAUDE_PID", "CLAUDE_EFFORT", "AI_AGENT", "CLAUDE_AGENT_SDK_VERSION"}
TOKEN_FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
VERDICT = re.compile(r"^\s*VERDICT:\s*(APPROVE|FAIL)\b", re.I | re.M)


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


# ---- the ledger: one team-wide budget ---------------------------------------------------------------------
class Ledger:
    """<run>/.team/team.json. Live token totals per session; the team cap is checked against their sum."""

    def __init__(self, run):
        self.path = run / ".team/team.json"
        self.data = json.loads(self.path.read_text(encoding="utf-8"))
        self.lock = threading.Lock()
        self.live = {}

    def save(self):
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.data, indent=1), encoding="utf-8")
        os.replace(tmp, self.path)

    def tokens(self):
        done = sum(s.get("tokens", 0) for s in self.data["sessions"])
        return done + sum(self.live.values())

    def minutes(self):
        return (time.time() - self.data["started"]) / 60

    def over(self):
        c = self.data["caps"]
        if c.get("minutes") and self.minutes() > c["minutes"]:
            return "CAP:minutes"
        if c.get("tokens") and self.tokens() > c["tokens"]:
            return "CAP:tokens"
        return None

    def set_live(self, key, n):
        with self.lock:
            self.live[key] = n

    def close_session(self, key, row):
        with self.lock:
            self.live.pop(key, None)
            self.data["sessions"].append(row)
            self.save()

    def status(self, s, **extra):
        with self.lock:
            self.data.update(status=s, **extra)
            self.save()


# ---- one role session ------------------------------------------------------------------------------------
def role_prompt(roles, role, run):
    """The role file's body (frontmatter dropped), saved where the child's --append-system-prompt-file reads it."""
    text = (roles / f"{role}.md").read_text(encoding="utf-8")
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    out = run / ".team/prompts" / f"{role}.md"
    out.write_text(text, encoding="utf-8")
    return out


def child_env(role, run):
    e = {k: v for k, v in os.environ.items() if not (k.startswith("CLAUDE_CODE_") or k in STRIP)}
    e.update(AUTONOMOUS_ROLE=role, AUTONOMOUS_RUN=str(run), PORT=PORT.get(role, "8100"))
    return e


def run_role(run, ledger, role, task, rnd, a):
    """Run one role to completion or the team cap. Returns its ledger row."""
    key = f"{role}-r{rnd}"
    pfile = role_prompt(Path(a.roles), role, run)
    cmd = [exe(), "-p", "--output-format", "stream-json", "--verbose", "--model", a.model,
           "--permission-mode", "acceptEdits", "--permission-prompts", "none", "--allowedTools", TOOLS,
           "--no-session-persistence", "--plugin-dir", str(PLUGIN), "--append-system-prompt-file", str(pfile), *CLEAN]
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

    usage, result, stop = {}, None, None
    with open(run / ".team/logs" / f"{key}.jsonl", "w", encoding="utf-8", newline="\n") as log:
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
                if ev.get("type") == "assistant":
                    m = ev.get("message", {})
                    u = usage.setdefault(m.get("id"), {})
                    for k in TOKEN_FIELDS:
                        u[k] = max(u.get(k, 0), (m.get("usage") or {}).get(k, 0) or 0)
                    ledger.set_live(key, sum(sum(x.values()) for x in usage.values()))
                elif ev.get("type") == "result":
                    result = ev
            stop = ledger.over() or ledger.data.get("abort")
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
    row = {"role": role, "round": rnd, "session_id": (result or {}).get("session_id"),
           "stop": stop or ("DONE" if result and not result.get("is_error") else "ERROR"),
           "minutes": round((time.time() - t0) / 60, 2), "turns": len(usage), "tokens": sum(tokens.values()),
           "tokens_by_kind": tokens, "exit": proc.returncode, "orphans_left": left,
           "stderr": "".join(err)[-500:]}
    ledger.close_session(key, row)
    return row


# ---- the run folder and the pipeline ---------------------------------------------------------------------
def init(kind, idea, a):
    run = Path(a.run or f"autonomous-run-{time.strftime('%y%m%d-%H%M%S')}").resolve()
    for f in FOLDERS[kind] + [".team/logs", ".team/prompts"]:
        (run / f).mkdir(parents=True, exist_ok=True)
    src = Path(idea)
    (run / "idea.md").write_text(src.read_text(encoding="utf-8") if src.is_file() else idea, encoding="utf-8")
    caps = {"minutes": a.max_min or CAPS[kind]["minutes"], "tokens": a.max_tokens or CAPS[kind]["tokens"]}
    (run / ".team/team.json").write_text(json.dumps(
        {"kind": kind, "model": a.model, "caps": caps, "started": time.time(), "status": "RUNNING",
         "sessions": []}, indent=1), encoding="utf-8")
    return run


def verdict(run, role, rnd):
    f = run / "verdicts" / f"{role}-r{rnd}.md"
    m = VERDICT.search(f.read_text(encoding="utf-8", errors="replace")) if f.exists() else None
    return m[1].upper() if m else "MISSING"


TASKS = {
    "spec-writer": "Write the spec and the hidden acceptance checks for the idea in ../idea.md, as your role says.",
    "builder": "Build round {r}: build or fix the app in this folder from ../spec/spec.md, as your role says.{fb}",
    "qa": "Review round {r}: check the app in ../app against ../spec/spec.md. Write ../verdicts/qa-r{r}.md.",
    "tester": "Walk round {r}: run the app in ../app and walk it as a user. Write ../verdicts/tester-r{r}.md.",
}


def app(idea, a):
    run = init("app", idea, a)
    ledger = Ledger(run)
    print(f"run folder: {run}", flush=True)

    def stopped(row):
        if row["stop"].startswith("CAP") or row["stop"] == "abort":
            return row["stop"]
        return None

    rounds, status, note = [], None, ""
    row = run_role(run, ledger, "spec-writer", TASKS["spec-writer"], 0, a)
    status = stopped(row)
    if not status and not ((run / "spec/spec.md").exists() and any((run / "checks").iterdir())):
        status, note = "FAIL", "the spec-writer left no spec/spec.md or no checks"
    for r in range(1, a.rounds + 1):
        if status:
            break
        fb = "" if r == 1 else (f" Round {r - 1} failed review: read ../verdicts/qa-r{r - 1}.md and "
                                f"../verdicts/tester-r{r - 1}.md and fix what they found.")
        status = stopped(run_role(run, ledger, "builder", TASKS["builder"].format(r=r, fb=fb), r, a))
        if status:
            break
        if (run / "app/STUCK.md").exists():
            status, note = "STUCK", "the builder wrote app/STUCK.md"
            break
        rows = {}
        threads = [threading.Thread(target=lambda ro=ro: rows.__setitem__(ro, run_role(
            run, ledger, ro, TASKS[ro].format(r=r), r, a))) for ro in ("qa", "tester")]
        [t.start() for t in threads]
        [t.join() for t in threads]
        status = next((s for s in (stopped(x) for x in rows.values()) if s), None)
        v = {ro: verdict(run, ro, r) for ro in ("qa", "tester")}
        rounds.append({"round": r, **v})
        if status:
            break
        if all(x == "APPROVE" for x in v.values()):
            status = "DONE"
        elif r == a.rounds:
            status, note = "FAIL", f"not approved after {a.rounds} rounds"
    ledger.status(status, rounds=rounds, note=note, minutes=round(ledger.minutes(), 2), tokens=ledger.tokens())
    report(run, ledger)
    print(f"status: {status}  tokens: {ledger.tokens():,}  minutes: {ledger.minutes():.1f}  report: "
          f"{run / 'RUN_REPORT.md'}", flush=True)
    return status


def report(run, ledger):
    d = ledger.data
    by_role = {}
    for s in d["sessions"]:
        by_role[s["role"]] = by_role.get(s["role"], 0) + s["tokens"]
    lines = [f"# Run report: {d['status']}", "",
             f"- Status: **{d['status']}**" + (f" ({d['note']})" if d.get("note") else ""),
             f"- Rounds: {len(d.get('rounds', []))}; minutes: {d.get('minutes')}; tokens: {d.get('tokens'):,} "
             f"(caps {d['caps']['minutes']} min, {d['caps']['tokens']:,} tokens)", "",
             "| Round | QA | Tester |", "|---|---|---|"]
    lines += [f"| {x['round']} | {x['qa']} | {x['tester']} |" for x in d.get("rounds", [])]
    lines += ["", "| Role | Tokens |", "|---|---|"] + [f"| {k} | {v:,} |" for k, v in by_role.items()]
    lines += ["", "Verdicts and evidence: `verdicts/`, `evidence/`. The app: `app/`. Session log: `.team/team.json`."]
    (run / "RUN_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["app", "init", "run"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--run")
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--max-min", type=float)
    ap.add_argument("--max-tokens", type=int)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--roles", default=str(PLUGIN / "agents"))
    a = ap.parse_args()
    if a.cmd == "app":
        status = app(" ".join(a.args), a)
        sys.exit(0 if status == "DONE" else 1)
    if a.cmd == "init":
        print(init(a.args[0], " ".join(a.args[1:]), a))
        return
    role = a.args[0]
    run = Path(a.run).resolve()
    row = run_role(run, Ledger(run), role, TASKS[role].format(r=a.round, fb=""), a.round, a)
    print(json.dumps(row, indent=1))


if __name__ == "__main__":
    main()
