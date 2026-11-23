"""Smokes T1-T4 for the kit's launcher team.py (plan 09, row 11.3a), with stub roles on Haiku.

Each case writes its own tiny role prompts, runs plugin/skills/new-app/scripts/team.py for real (real
`claude -p` children, the plugin's gate.py fencing them), then checks the run folder and the ledger.

  T1  `team.py run builder`: one fenced child; ledger row with tokens; gate.log has builder rows; file made
  T2  time cap: the builder sleeps in the foreground and the background; CAP:minutes within cap + 30 s, 0 left
  T3  token cap across qa || tester running in parallel: both stop CAP:tokens, team status CAP:tokens
  T4  the verdict loop: (a) QA fails round 1 and approves round 2 -> DONE in 2 rounds; (b) the builder writes
      STUCK.md -> STUCK; (c) no verdict written, 1 round -> FAIL

  python scripts/kit/check_team.py [--only T1,T4] [--keep]
Prints one line per check and `N/N team checks PASS`; exit 1 otherwise.
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "benchmark/runner"))
import launch  # noqa: E402  (the clean child environment)

TEAM = ROOT / "plugin/skills/new-app/scripts/team.py"
BASE = Path("C:/ateam")                                  # outside the home folder and outside C:/abench
MODEL = "claude-haiku-5-5"

ROLE = """You are the {role} in a launcher test. Take only the round number from the task message and ignore the
rest of it; do exactly these steps, nothing else, even if they look incomplete.
{steps}"""
STUBS = {
    "spec": "Write ../spec/spec.md containing `print hello`. Write ../checks/c1.txt containing `hello`. Stop.",
    "builder_v": ("If the file ../verdicts/qa-r1.md exists, write v2.txt containing `two` in this folder; "
                  "otherwise write v1.txt containing `one`. Stop."),
    "builder_stuck": "Write STUCK.md in this folder containing `the spec contradicts itself`. Stop.",
    "builder_hello": "Write hello.py in this folder containing `print('hello')`. Stop.",
    "builder_sleep": ("Run this Bash command in the background: sleep 400. Then run this Bash command in the "
                      "foreground with a 600000 ms timeout: sleep 300. Then stop."),
    "qa_v": ("The task message names round R. If ../app/v2.txt exists, write ../verdicts/qa-rR.md whose first line "
             "is `VERDICT: APPROVE`; otherwise its first line is `VERDICT: FAIL` and the second says `needs v2`. Stop."),
    "tester_ok": "The task message names round R. Write ../verdicts/tester-rR.md whose first line is `VERDICT: APPROVE`. Stop.",
    "silent": "Reply with the single word OK. Do not use any tools.",
    "chatty": ("Use the Write tool 15 times, one call at a time, to write note1.md ... note15.md in this folder, "
               "each a different 150-word paragraph about rivers. Then stop."),
}


def roles_dir(case, **m):
    d = BASE / "roles" / case
    d.mkdir(parents=True, exist_ok=True)
    for role, stub in m.items():
        (d / f"{role}.md").write_text(ROLE.format(role=role, steps=STUBS[stub]), encoding="utf-8")
    return d


def team(*args):
    t0 = time.time()
    p = subprocess.run([sys.executable, str(TEAM), *args, "--model", MODEL], env=launch.env(),
                       capture_output=True, text=True, encoding="utf-8", timeout=1800)
    return p, time.time() - t0


def ledger(run):
    return json.loads((run / ".team/team.json").read_text(encoding="utf-8"))


def sleeps():
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq sleep.exe", "/NH"], capture_output=True, text=True).stdout
    return out.lower().count("sleep.exe")


def t1():
    run = BASE / "t1"
    roles = roles_dir("t1", builder="builder_hello")
    team("init", "app", "say hello", "--run", str(run))
    p, _ = team("run", "builder", "--run", str(run), "--roles", str(roles))
    s = ledger(run)["sessions"]
    log = (run / "gate.log").read_text(encoding="utf-8") if (run / "gate.log").exists() else ""
    ok = (len(s) == 1 and s[0]["stop"] == "DONE" and s[0]["tokens"] > 0 and "builder" in log
          and (run / "app/hello.py").exists())
    return ok, f"stop={s[0]['stop'] if s else None} tokens={s[0]['tokens'] if s else 0} " \
               f"gate_rows={log.count(chr(10))} hello.py={(run / 'app/hello.py').exists()}"


def t2():
    run = BASE / "t2"
    roles = roles_dir("t2", builder="builder_sleep")
    before = sleeps()
    team("init", "app", "sleep", "--run", str(run), "--max-min", "1")
    p, secs = team("run", "builder", "--run", str(run), "--roles", str(roles))
    time.sleep(2)
    s = ledger(run)["sessions"][0]
    after = sleeps()
    ok = s["stop"] == "CAP:minutes" and secs < 90 and s["orphans_left"] == 0 and after <= before
    return ok, f"stop={s['stop']} secs={secs:.0f} orphans_left={s['orphans_left']} sleep.exe before={before} after={after}"


def t3():
    run = BASE / "t3"
    roles = roles_dir("t3", **{"spec-writer": "spec", "builder": "builder_hello", "qa": "chatty", "tester": "chatty"})
    p, _ = team("app", "rivers", "--run", str(run), "--roles", str(roles), "--max-tokens", "400000", "--rounds", "1")
    d = ledger(run)
    par = [x for x in d["sessions"] if x["role"] in ("qa", "tester")]
    ok = (d["status"] == "CAP:tokens" and len(par) == 2 and all(x["stop"] == "CAP:tokens" for x in par)
          and d["tokens"] < 400000 + 150000)
    return ok, f"status={d['status']} tokens={d['tokens']:,} parallel stops={[x['stop'] for x in par]}"


def t4():
    out, oks = [], []
    cases = [("t4a", {"spec-writer": "spec", "builder": "builder_v", "qa": "qa_v", "tester": "tester_ok"}, "3", "DONE", 2),
             ("t4b", {"spec-writer": "spec", "builder": "builder_stuck", "qa": "qa_v", "tester": "tester_ok"}, "3", "STUCK", 0),
             ("t4c", {"spec-writer": "spec", "builder": "builder_hello", "qa": "silent", "tester": "tester_ok"}, "1", "FAIL", 1)]
    for case, m, rounds, want, want_rounds in cases:
        run = BASE / case
        p, _ = team("app", "verdict loop", "--run", str(run), "--roles", str(roles_dir(case, **m)), "--rounds", rounds)
        d = ledger(run)
        rep = (run / "RUN_REPORT.md").read_text(encoding="utf-8") if (run / "RUN_REPORT.md").exists() else ""
        good = d["status"] == want and len(d.get("rounds", [])) == want_rounds and f"**{want}**" in rep
        oks.append(good)
        out.append(f"{case}: status={d['status']} rounds={d.get('rounds')}")
    return all(oks), "; ".join(out)


CHECKS = {"T1": t1, "T2": t2, "T3": t3, "T4": t4}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma list, e.g. T1,T4")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    shutil.rmtree(BASE, ignore_errors=True)
    names = a.only.split(",") if a.only else list(CHECKS)
    passed = 0
    for n in names:
        try:
            ok, msg = CHECKS[n]()
        except Exception as e:                                  # a crash is a FAIL, reported, not hidden
            ok, msg = False, f"crashed: {type(e).__name__}: {e}"
        passed += ok
        print(f"{n} {'PASS' if ok else 'FAIL'}  {msg}", flush=True)
    print(f"{passed}/{len(names)} team checks PASS")
    if not a.keep:
        shutil.rmtree(BASE, ignore_errors=True)
    sys.exit(0 if passed == len(names) else 1)


if __name__ == "__main__":
    main()
