"""Start one clean-room `claude -p`, read its stream live, enforce caps, kill everything it started at a cap (a Windows job object).

Clean room (D23): --setting-sources project,local + --strict-mcp-config with no servers, run from a
room outside the home folder, with this session's CLAUDE_CODE_* variables removed so the child is a
fresh top-level session (not a child of whoever started the runner). Both arms get the same tools,
permissions and caps; the kit arm only adds its plugin.

Caps: minutes, turns (unique assistant messages, subagents included) and tokens (input + output +
cache creation + cache read, summed live from the stream). This Claude Code version lists no
--max-turns, so turns are counted and enforced here.
"""
import ctypes
import json
import os
import queue
import shutil
import subprocess
import threading
import time
from pathlib import Path

CLEAN = ["--setting-sources", "project,local", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
TOOLS = "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch"
STRIP = {"CLAUDECODE", "CLAUDE_PID", "CLAUDE_EFFORT", "AI_AGENT", "CLAUDE_AGENT_SDK_VERSION"}
TOKEN_FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")


def exe():
    """claude.exe itself: the npm `claude.cmd` wrapper would route arguments through cmd.exe quoting."""
    w = shutil.which("claude")
    if not w:
        raise SystemExit("claude is not on PATH")
    real = Path(w).parent / "node_modules/@anthropic-ai/claude-code/bin/claude.exe"
    return str(real) if w.lower().endswith(".cmd") and real.exists() else w


def env(tmp=None):
    e = {k: v for k, v in os.environ.items() if not (k.startswith("CLAUDE_CODE_") or k in STRIP)}
    if tmp:                                                 # per-run temp, swept after the run
        e.update(TMP=str(tmp), TEMP=str(tmp), TMPDIR=str(tmp))
    return e


def command(model, plugin_dir=None):
    cmd = [exe(), "-p", "--output-format", "stream-json", "--verbose", "--model", model,
           "--permission-mode", "acceptEdits", "--allowedTools", TOOLS, "--no-session-persistence", *CLEAN]
    if plugin_dir:
        cmd += ["--plugin-dir", str(plugin_dir)]
    return cmd


def context(room):
    """/context as seen from inside the room (0 model turns): the clean-room check."""
    p = subprocess.run([exe(), "-p", "/context", "--output-format", "json", "--no-session-persistence", *CLEAN],
                       cwd=room, env=env(), capture_output=True, text=True, encoding="utf-8", timeout=180)
    return json.loads(p.stdout)["result"]


_k32 = ctypes.WinDLL("kernel32", use_last_error=True)
_k32.CreateJobObjectW.restype = ctypes.c_void_p
_k32.OpenProcess.restype = ctypes.c_void_p


class _BasicLimit(ctypes.Structure):
    _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                ("LimitFlags", ctypes.c_uint32), ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", ctypes.c_uint32),
                ("Affinity", ctypes.c_size_t), ("PriorityClass", ctypes.c_uint32), ("SchedulingClass", ctypes.c_uint32)]


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
    """A Windows job object around the run: every process the agent starts stays inside it, even when
    its parent dies (Git Bash programs lose their parent link, so a process-tree kill misses them;
    smoke R3, 2026-11-22). Killing the job kills them all; closing the handle does too."""

    def __init__(self):
        self.h = ctypes.c_void_p(_k32.CreateJobObjectW(None, None))
        info = _ExtendedLimit()
        info.Basic.LimitFlags = 0x2000                                  # KILL_ON_JOB_CLOSE
        if not _k32.SetInformationJobObject(self.h, 9, ctypes.byref(info), ctypes.sizeof(info)):
            raise OSError(ctypes.get_last_error(), "SetInformationJobObject")

    def add(self, pid):
        ph = ctypes.c_void_p(_k32.OpenProcess(0x0101, False, pid))      # SET_QUOTA | TERMINATE
        ok = _k32.AssignProcessToJobObject(self.h, ph)
        _k32.CloseHandle(ph)
        if not ok:
            raise OSError(ctypes.get_last_error(), "AssignProcessToJobObject")

    def counts(self):
        a = _Accounting()
        _k32.QueryInformationJobObject(self.h, 1, ctypes.byref(a), ctypes.sizeof(a), None)
        return a.TotalProcesses, a.ActiveProcesses

    def kill(self):
        _k32.TerminateJobObject(self.h, 1)
        for _ in range(50):
            if self.counts()[1] == 0:
                break
            time.sleep(0.1)
        return self.counts()[1]

    def close(self):
        _k32.CloseHandle(self.h)


def run(cmd, prompt, room, caps, on_tool_use, raw_path, tmp=None):
    """Run to completion or cap. Returns the live tallies, the final result event, and how it stopped."""
    t0 = time.monotonic()
    proc = subprocess.Popen(cmd, cwd=room, env=env(tmp), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, encoding="utf-8", bufsize=1)
    job = Job()
    job.add(proc.pid)                                       # before the agent can start anything
    proc.stdin.write(prompt)
    proc.stdin.close()
    lines, err = queue.Queue(), []
    threading.Thread(target=lambda: ([lines.put(l) for l in proc.stdout], lines.put(None)), daemon=True).start()
    threading.Thread(target=lambda: err.extend(proc.stderr), daemon=True).start()

    usage, flags, notes, result, stop, limits = {}, [], [], None, None, []
    with open(raw_path, "w", encoding="utf-8", newline="\n") as raw:
        while True:
            try:
                line = lines.get(timeout=1)
            except queue.Empty:
                line = ""
            if line is None:
                break
            if line.strip():
                raw.write(line)
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    ev = {}
                if ev.get("type") == "assistant":
                    m = ev.get("message", {})
                    u = usage.setdefault(m.get("id"), {})
                    for k in TOKEN_FIELDS:
                        u[k] = max(u.get(k, 0), (m.get("usage") or {}).get(k, 0) or 0)
                    for b in m.get("content", []):
                        if b.get("type") == "tool_use":
                            new = on_tool_use(b)
                            notes += [f for f in new if f.startswith("note:")]   # recorded, never a cheat
                            new = [f for f in new if not f.startswith("note:")]
                            if new:
                                flags += new
                                stop = stop or "FLAGGED"
                elif ev.get("type") == "result":
                    result = ev
                elif ev.get("type") == "rate_limit_event":          # weekly-limit share, per run, free
                    limits.append(ev.get("rate_limit_info", {}))
            minutes = (time.monotonic() - t0) / 60
            tokens = sum(sum(u.values()) for u in usage.values())
            if caps["minutes"] and minutes > caps["minutes"]:
                stop = stop or "CAP:minutes"
            if caps["turns"] and len(usage) > caps["turns"]:
                stop = stop or "CAP:turns"
            if caps["tokens"] and tokens > caps["tokens"]:
                stop = stop or "CAP:tokens"
            if stop:
                break

    if proc.poll() is None:
        job.kill()                                          # cap or flag: stop everything now
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        job.kill()
    spawned, active = job.counts()
    leftovers = active                                      # e.g. a server the agent left running
    left = job.kill()
    job.close()
    week = [w.get("unifiedWindows", {}).get("seven_day", {}).get("utilization") for w in limits]
    return {"stop": stop, "result": result, "flags": sorted(set(flags)), "notes": sorted(set(notes)),
            "week_util": [week[0], week[-1]] if week else None,
            "limit_status": limits[-1].get("status") if limits else None,
            "minutes": round((time.monotonic() - t0) / 60, 2), "turns_live": len(usage),
            "tokens_live": {k: sum(u.get(k, 0) for u in usage.values()) for k in TOKEN_FIELDS},
            "processes": spawned, "orphans_killed": leftovers - left, "orphans_left": left,
            "exit": proc.returncode, "stderr": "".join(err)[-2000:]}
