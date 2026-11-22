"""Start one clean-room `claude -p`, read its stream live, enforce caps, kill the process tree at a cap.

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


def env():
    return {k: v for k, v in os.environ.items() if not (k.startswith("CLAUDE_CODE_") or k in STRIP)}


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


def _alive(pid):
    """Never os.kill(pid, 0) on Windows: it terminates the process."""
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
    if not h:
        return False
    code = ctypes.c_ulong()
    ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code))
    ctypes.windll.kernel32.CloseHandle(h)
    return code.value == 259


def _descendants(pid):
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
                          "Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId | ConvertTo-Json -Compress"],
                         capture_output=True, text=True, timeout=60).stdout
    kids, procs = set(), json.loads(out or "[]")
    frontier = {pid}
    while frontier:
        nxt = {p["ProcessId"] for p in procs if p["ParentProcessId"] in frontier} - kids - {pid}
        kids |= nxt
        frontier = nxt
    return kids


def _kill(pids):
    for p in pids:
        if _alive(p):
            subprocess.run(["taskkill", "/PID", str(p), "/T", "/F"], capture_output=True)


def run(cmd, prompt, room, caps, on_tool_use, raw_path):
    """Run to completion or cap. Returns the live tallies, the final result event, and how it stopped."""
    t0 = time.monotonic()
    proc = subprocess.Popen(cmd, cwd=room, env=env(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, encoding="utf-8", bufsize=1)
    proc.stdin.write(prompt)
    proc.stdin.close()
    lines, err = queue.Queue(), []
    threading.Thread(target=lambda: ([lines.put(l) for l in proc.stdout], lines.put(None)), daemon=True).start()
    threading.Thread(target=lambda: err.extend(proc.stderr), daemon=True).start()

    usage, flags, result, stop = {}, [], None, None
    tree, last_snap = set(), 0.0
    with open(raw_path, "w", encoding="utf-8", newline="\n") as raw:
        while True:
            now = time.monotonic()
            if now - last_snap > 10:                       # remember the tree so nothing outlives the run
                tree |= _descendants(proc.pid)
                last_snap = now
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
                            if new:
                                flags += new
                                stop = stop or "FLAGGED"
                elif ev.get("type") == "result":
                    result = ev
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

    tree |= _descendants(proc.pid) if proc.poll() is None else set()
    if proc.poll() is None:
        _kill([proc.pid])
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        _kill([proc.pid])
    orphans = [p for p in tree if _alive(p)]
    _kill(orphans)                                          # e.g. a script the agent left running
    left = [p for p in orphans if _alive(p)]
    return {"stop": stop, "result": result, "flags": sorted(set(flags)),
            "minutes": round((time.monotonic() - t0) / 60, 2), "turns_live": len(usage),
            "tokens_live": {k: sum(u.get(k, 0) for u in usage.values()) for k in TOKEN_FIELDS},
            "orphans_killed": len(orphans) - len(left), "orphans_left": len(left),
            "exit": proc.returncode, "stderr": "".join(err)[-2000:]}
