"""Smokes T1-T4 for the kit's conductor team.py (plan 09, row 11.3a), with stub roles on Haiku.

Each case writes its own tiny role prompts, runs plugin/skills/new-app/scripts/team.py for real (real
`claude -p` children, the plugin's gate.py fencing them), then checks the run folder and its books.

  T1  `team.py run builder`: one fenced child; registry row with tokens; ledger.tsv row; gate.log has builder rows
  T2  time cap: the builder sleeps in the foreground and the background; CAP:minutes within cap + 30 s, 0 left
  T3  token cap across qa || tester running in parallel: both stop CAP:tokens, run status CAP:tokens
  T4  the verdict loop (architecture §4, §6):
      a  QA fails round 1, passes round 2 -> DONE in 2 rounds; round 2's builder was resumed, not fresh
      b  the builder writes STUCK.md -> STUCK, no check round
      c  QA writes no verdict, 1 round -> STUCK ("not approved"), reason names the missing file
      d  the verdict reader itself on 9 handwritten files (no model): PASS needs evidence files, observed
         tester checks, every check PASS; missing, malformed or other words are FAIL (rule L2)
      and every finished run has RUN_REPORT.md, release/card.md and release/numbers.tsv

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

ROLE = """You are the {role} in a launcher test. Take only the round number N from the task message and ignore the
rest of it; do exactly these steps, nothing else, even if they look incomplete. Write files with the Write tool.
{steps}"""
VERDICT = ('{{"role": "{role}", "round": N, "verdict": "{v}", "checks": [{{"id": "C1", "status": "{v}", '
           '"basis": "observed", "expected": "x", "observed": "x", "evidence": "{ev}"}}], "repro": "", "notes": ""}}')
STUBS = {
    "spec": ("In this folder write spec.md containing `print hello` and rubric.md containing `hello is printed`. "
             "Write ../checks/c1.txt containing `hello`. Stop."),
    "builder_v": ("This is a test with a fixed script; do not judge the verdicts or fix anything else. If N is 1, "
                  "write v1.txt containing `one` in this folder. If N is 2 or more, write v2.txt containing `two` "
                  "in this folder. Stop."),
    "builder_stuck": "Write STUCK.md in this folder containing `the spec contradicts itself`. Stop.",
    "builder_hello": "Write hello.py in this folder containing `print('hello')`. Stop.",
    "builder_sleep": ("Run this Bash command in the background: sleep 400. Then run this Bash command in the "
                      "foreground with a 600000 ms timeout: sleep 300. Then stop."),
    "qa_v": ("Write ../evidence/rN/qa.txt containing `checked`. Then, if v2.txt exists in this folder, write "
             "../verdicts/rN-qa.json containing exactly " + VERDICT.format(role="qa", v="PASS", ev="evidence/rN/qa.txt")
             + " ; otherwise write it with both PASS words replaced by FAIL. Replace N with the round number. Stop."),
    "tester_ok": ("Write evidence/rN/walk.txt containing `walked`. Then write verdicts/rN-tester.json containing exactly "
                  + VERDICT.format(role="tester", v="PASS", ev="evidence/rN/walk.txt")
                  + " . Replace N with the round number. Stop."),
    "tester_noev": ("Write verdicts/rN-tester.json containing exactly "
                    + VERDICT.format(role="tester", v="PASS", ev="evidence/rN/walk.png")
                    + " . Replace N with the round number. Do not create any other file. Stop."),
    "silent": "Reply with the single word OK. Do not use any tools.",
    "chatty": ("Use the Bash tool 15 times, one call at a time, each time running: echo note K (K = 1 to 15). "
               "After each call, write one 100-word sentence about rivers in your reply. Then stop."),
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


def books(run):
    return (json.loads((run / "run.json").read_text(encoding="utf-8")),
            json.loads((run / "registry.json").read_text(encoding="utf-8")))


def sleeps():
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq sleep.exe", "/NH"], capture_output=True, text=True).stdout
    return out.lower().count("sleep.exe")


def t1():
    run = BASE / "t1"
    roles = roles_dir("t1", builder="builder_hello")
    team("init", "app", "say hello", "--run", str(run))
    team("run", "builder", "--run", str(run), "--roles", str(roles))
    _, reg = books(run)
    log = (run / "team-records/gate.log").read_text(encoding="utf-8") if (run / "team-records/gate.log").exists() else ""
    ledger = (run / "ledger.tsv").read_text(encoding="utf-8").splitlines()
    ok = (len(reg) == 1 and reg[0]["stop"] == "DONE" and reg[0]["tokens"] > 0 and "\tbuilder\t" in log
          and len(ledger) == 2 and (run / "app/hello.py").exists())
    return ok, f"stop={reg[0]['stop'] if reg else None} tokens={reg[0]['tokens'] if reg else 0} " \
               f"gate_rows={len(log.splitlines())} ledger_rows={len(ledger) - 1} hello.py={(run / 'app/hello.py').exists()}"


def t2():
    run = BASE / "t2"
    roles = roles_dir("t2", builder="builder_sleep")
    before = sleeps()
    team("init", "app", "sleep", "--run", str(run), "--max-min", "1")
    _, secs = team("run", "builder", "--run", str(run), "--roles", str(roles))
    time.sleep(2)
    s = books(run)[1][0]
    after = sleeps()
    ok = s["stop"] == "CAP:minutes" and secs < 90 and s["orphans_left"] == 0 and after <= before
    return ok, f"stop={s['stop']} secs={secs:.0f} orphans_left={s['orphans_left']} sleep.exe before={before} after={after}"


def t3():
    run = BASE / "t3"
    roles = roles_dir("t3", **{"spec-writer": "spec", "builder": "builder_hello", "qa": "chatty", "tester": "chatty"})
    team("app", "rivers", "--run", str(run), "--roles", str(roles), "--max-tokens", "400000", "--rounds", "1")
    st, reg = books(run)
    par = [x for x in reg if x["role"] in ("qa", "tester")]
    ok = (st["status"] == "CAP:tokens" and len(par) == 2 and all(x["stop"] == "CAP:tokens" for x in par)
          and st["tokens"] < 400000 + 150000)
    return ok, f"status={st['status']} tokens={st['tokens']:,} parallel stops={[x['stop'] for x in par]}"


def t4():
    out, oks = [], []
    base = {"spec-writer": "spec", "builder": "builder_hello", "qa": "qa_v", "tester": "tester_ok"}
    cases = [("t4a", {"builder": "builder_v"}, "3", "DONE", 2),
             ("t4b", {"builder": "builder_stuck"}, "3", "STUCK", 0),
             ("t4c", {"qa": "silent"}, "1", "STUCK", 1)]
    for case, over, rounds, want, want_rounds in cases:
        run = BASE / case
        team("app", "verdict loop", "--run", str(run), "--roles", str(roles_dir(case, **{**base, **over})),
             "--rounds", rounds)
        st, reg = books(run)
        files = all((run / f).is_file() for f in ("RUN_REPORT.md", "release/card.md", "release/numbers.tsv"))
        good = st["status"] == want and len(st.get("rounds", [])) == want_rounds and files
        extra = ""
        if case == "t4a":
            b = [x for x in reg if x["role"] == "builder"]
            res = len(b) == 2 and b[1]["resumed"] and b[1]["session_id"] == b[0]["session_id"]
            good &= res
            extra = f" builder_resumed={res}"
        if case == "t4c":
            good &= "no verdict file r1-qa.json" in st["rounds"][0]["qa"]["reason"]
        oks.append(good)
        why = "; ".join(f"r{x['round']} qa={x['qa']['verdict']} tester={x['tester']['verdict']} "
                        f"({x['tester']['reason'] if x['tester']['verdict'] == 'FAIL' else x['qa']['reason']})"
                        for x in st.get("rounds", []))
        out.append(f"{case}: {st['status']} [{why}]{extra}")
    good, msg = t4d()
    oks.append(good)
    out.append(msg)
    return all(oks), " | ".join(out)


def t4d():
    """team.py's verdict reader on handwritten files (no model: Haiku refused to write a PASS it couldn't back)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("team", TEAM)
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    run = BASE / "t4d"
    (run / "verdicts").mkdir(parents=True)
    (run / "evidence/r1").mkdir(parents=True)
    (run / "evidence/r1/ok.png").write_bytes(b"png")
    check = lambda **kw: {"id": "C1", "status": "PASS", "basis": "observed", "evidence": "evidence/r1/ok.png", **kw}
    cases = [  # (role, verdict file text or None, expected verdict, words the reason must contain)
        ("tester", {"verdict": "PASS", "checks": [check()]}, "PASS", "passed with evidence"),
        ("tester", {"verdict": "PASS", "checks": [check(evidence="evidence/r1/missing.png")]}, "FAIL", "no evidence file"),
        ("tester", {"verdict": "PASS", "checks": [check(basis="inferred")]}, "FAIL", "not observed"),
        ("qa", {"verdict": "PASS", "checks": [check(basis="inferred")]}, "PASS", "passed with evidence"),
        ("tester", {"verdict": "PASS", "checks": [check(status="FAIL")]}, "FAIL", "is FAIL"),
        ("tester", {"verdict": "PASS", "checks": []}, "FAIL", "no checks"),
        ("tester", {"verdict": "BLOCKED", "checks": [check()]}, "FAIL", "said BLOCKED"),
        ("tester", "not json", "FAIL", "malformed"),
        ("tester", None, "FAIL", "no verdict file"),
    ]
    bad = []
    for i, (role, body, want, words) in enumerate(cases):
        f = run / "verdicts" / f"r{i + 1}-{role}.json"
        if body is not None:
            f.write_text(body if isinstance(body, str) else json.dumps(body), encoding="utf-8")
        got, why, _ = tm.verdict(run, role, i + 1)
        if got != want or words not in why:
            bad.append(f"case {i + 1}: {got} ({why})")
    return not bad, f"t4d verdict reader: {len(cases) - len(bad)}/{len(cases)}" + (f" {bad}" if bad else "")


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
