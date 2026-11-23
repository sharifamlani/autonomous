"""Spike for team.py (Phase 11): does an unattended `claude -p` session wait for a background Bash command
that runs longer than 10 minutes, and get its result back?

team.py runs the whole team for an hour or more. The Bash tool cuts a foreground command at 10 minutes, so
Main must start team.py in the background and wait for it. Spike 4.8 found background *subagents* under -p
stop at 10 minutes unless CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0; this checks the same for background Bash.

The session is told to start `sleep <secs> && echo <token> > bg_done.txt` in the background, wait for it,
then copy the file's text into final.txt. PASS = final.txt holds the token and the session ran past 10 min.

  python scripts/kit/check_bg_wait.py                 # ceiling 0 (expected PASS), sleep 660 s
  python scripts/kit/check_bg_wait.py --no-env        # default ceiling (the control)
  python scripts/kit/check_bg_wait.py --secs 30       # quick wiring check
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "benchmark"))
from runner import launch  # noqa: E402  (claude.exe path, clean flags, job object)

PROMPT = """Do exactly this, nothing else:
1. Start this Bash command IN THE BACKGROUND (run_in_background true): sleep {secs} && echo {token} > bg_done.txt
2. Wait for that background command to finish. Do not poll with sleep; you are notified when it completes.
3. When it has finished, read bg_done.txt and write its exact text into final.txt.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--secs", type=int, default=660)
    ap.add_argument("--no-env", action="store_true", help="control: leave the default background-wait ceiling")
    ap.add_argument("--model", default="claude-haiku-5-5")
    a = ap.parse_args()

    room = Path("C:/abench") / f"bgwait-{time.strftime('%H%M%S')}"
    room.mkdir(parents=True)
    token = f"bg-{int(time.time())}"
    env = launch.env()
    if not a.no_env:
        env["CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS"] = "0"
    cmd = [launch.exe(), "-p", "--output-format", "json", "--model", a.model, "--permission-mode", "acceptEdits",
           "--allowedTools", "Bash,Read,Write", "--no-session-persistence", *launch.CLEAN]
    t0 = time.monotonic()
    p = subprocess.Popen(cmd, cwd=room, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, encoding="utf-8")
    job = launch.Job()
    job.add(p.pid)
    out, err = p.communicate(PROMPT.format(secs=a.secs, token=token), timeout=a.secs + 900)
    minutes = (time.monotonic() - t0) / 60
    left = job.kill()
    job.close()
    final = (room / "final.txt").read_text(encoding="utf-8").strip() if (room / "final.txt").exists() else None
    try:
        res = json.loads(out)
    except json.JSONDecodeError:
        res = {"result": out[-500:]}
    ok = final == token and minutes * 60 >= a.secs
    print(f"ceiling={'default' if a.no_env else '0'}  secs={a.secs}  minutes={minutes:.1f}  final={final!r}  "
          f"token={token}  orphans_left={left}  turns={res.get('num_turns')}")
    print(f"result: {str(res.get('result'))[:300]}")
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
