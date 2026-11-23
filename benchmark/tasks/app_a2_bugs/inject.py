"""Plant 20 bugs in the Split reference build for benchmark task A2 (plan 10, smoke D5 / R8).

Each bug is one small edit to benchmark/tasks/app_a1_build/reference/, in its own area of the spec
(money rules, validation, status codes, ordering, settle-up, storage, the UI). The agent gets the app with
all 20 planted (app_a2_bugs) or with none (app_a2_clean) and reports the bugs it finds; the grader
matches reports to planted bugs by file and line.

  python benchmark/tasks/app_a2_bugs/inject.py --build      # inputs_local/{bugs,clean}/ + keys/a2.json (local)
  python benchmark/tasks/app_a2_bugs/inject.py --selftest   # 20/20 apply; app starts; each bug trips >= 1 A1 check
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REF = ROOT / "benchmark/tasks/app_a1_build/reference"
A1 = ROOT / "benchmark/tasks/app_a1_build"
OUT = HERE / "inputs_local"
KEY = ROOT / "benchmark/keys/a2.json"
APP_FILES = ("server.py", "index.html", "START.txt")

# (id, area, file, old, new, anchor): `anchor` is a unique substring of the planted file on the bug's
# line (default: the first line of `new`); deletions anchor on a neighbouring line
BUGS = [
    ("B01", "leftover cents go to the last members", "server.py",
     "base + (1 if i < extra else 0)", "base + (1 if i >= len(order) - extra else 0)", None),
    ("B02", "leftover cents follow the request's order, not the group's", "server.py",
     'shares(cents, split, group["members"])', 'shares(cents, split, body.get("split_among", group["members"]))', None),
    ("B03", "negative amounts formatted wrongly", "server.py",
     '    sign = "-" if cents < 0 else ""\n    return f"{sign}{abs(cents) // 100}.{abs(cents) % 100:02d}"',
     '    return f"{cents // 100}.{cents % 100:02d}"', None),
    ("B04", "whole-dollar amounts rejected", "server.py",
     r'AMOUNT = re.compile(r"^\d+(\.\d{1,2})?$")', r'AMOUNT = re.compile(r"^\d+\.\d{1,2}$")', None),
    ("B05", "an empty split list is treated as everyone", "server.py",
     '    if not isinstance(split, list) or not split:\n        raise Bad(400, "split_among must list at least one member")\n',
     '    split = split or group["members"]\n    if not isinstance(split, list):\n        raise Bad(400, "split_among must be a list")\n',
     None),
    ("B06", "zero amount accepted", "server.py",
     '    if cents <= 0:\n        raise Bad(400, "amount must be positive")\n', "",
     "    cents = int(whole) * 100 + int((frac + \"00\")[:2])"),
    ("B07", "numeric amounts truncated to whole dollars", "server.py",
     '        s = f"{value:.10f}".rstrip("0").rstrip(".")', "        s = str(int(value))", None),
    ("B08", "payer not checked against the members", "server.py",
     '    if paid_by not in group["members"]:\n        raise Bad(400, "paid_by must be a member")\n', "",
     '    paid_by = body.get("paid_by")'),
    ("B09", "duplicate names allowed when the case differs", "server.py",
     "    if len({m.lower() for m in members}) != len(members):",
     "    if len(set(members)) != len(members):", None),
    ("B10", "delete answers 200 with a body instead of 204", "server.py",
     "                return self.send(204)", '                return self.send(200, {"deleted": rest[1]})', None),
    ("B11", "deleting an unknown expense succeeds", "server.py",
     '                if len(keep) == len(g["expenses"]):\n                    raise Bad(404, "expense not found")\n', "",
     '                keep = [e for e in g["expenses"] if e["id"] != rest[1]]'),
    ("B12", "expenses listed newest first", "server.py",
     '                return self.send(200, [expense_out(e) for e in g["expenses"]])',
     '                return self.send(200, [expense_out(e) for e in reversed(g["expenses"])])', None),
    ("B13", "settle-up ties broken in reverse member order", "server.py",
     "        debtor = min(order, key=lambda m: (bal[m], order.index(m)))",
     "        debtor = min(order, key=lambda m: (bal[m], -order.index(m)))", None),
    ("B14", "balances have the wrong sign", "server.py",
     '        bal[e["paid_by"]] += e["cents"]\n        for m, c in e["shares"].items():\n            bal[m] -= c',
     '        bal[e["paid_by"]] -= e["cents"]\n        for m, c in e["shares"].items():\n            bal[m] += c', None),
    ("B15", "data never reaches the file", "server.py",
     "    os.replace(tmp, DATA)\n", "", '    tmp.write_text(json.dumps(db, indent=1), encoding="utf-8")'),
    ("B16", "empty description accepted", "server.py",
     '    if not desc:\n        raise Bad(400, "description is required")\n', "",
     '    desc = str(body.get("description") or "").strip()'),
    ("B17", "UI ignores unchecked members", "index.html",
     "amount: $(\"expense-amount\").value, paid_by: $(\"expense-paid-by\").value, split_among: split });",
     "amount: $(\"expense-amount\").value, paid_by: $(\"expense-paid-by\").value, split_among: members });", None),
    ("B18", "UI hides the error message", "index.html",
     "  } catch (e) { showError(e.message); }", '  } catch (e) { showError(""); }', None),
    ("B19", "UI does not refresh after a delete", "index.html",
     "    del.onclick = async () => { await api(\"DELETE\", `/api/groups/${gid}/expenses/${x.id}`); await refresh(); };",
     "    del.onclick = async () => { await api(\"DELETE\", `/api/groups/${gid}/expenses/${x.id}`); };", None),
    ("B20", "UI always records the first member as payer", "index.html",
     '      sel.appendChild(el("option", { value: m }, m));', '      sel.appendChild(el("option", { value: members[0] }, m));',
     None),
]


def plant(dest, bugs):
    """Copy the reference to dest and apply `bugs`; return {bug id: (file, line)} in the planted files."""
    shutil.copytree(REF, dest, ignore=shutil.ignore_patterns("data.json", "__pycache__"), dirs_exist_ok=True)
    text = {f: (dest / f).read_text(encoding="utf-8") for f in ("server.py", "index.html")}
    for bid, _, f, old, new, _ in bugs:
        if text[f].count(old) != 1:
            raise SystemExit(f"{bid}: target found {text[f].count(old)} times in {f} (want 1)")
        text[f] = text[f].replace(old, new)
    where = {}
    for bid, _, f, old, new, anchor in bugs:
        a = anchor or new.strip("\n").splitlines()[0]
        if text[f].count(a) != 1:
            raise SystemExit(f"{bid}: anchor found {text[f].count(a)} times in {f} (want 1): {a!r}")
        where[bid] = (f, text[f][:text[f].index(a)].count("\n") + 1)
    for f, t in text.items():
        (dest / f).write_text(t, encoding="utf-8", newline="\n")
    return where


def spec():
    """A1's spec without its build instructions: the money rules, API, start contract and UI."""
    t = (A1 / "task.md").read_text(encoding="utf-8")
    return "# Split: the specification\n\n" + t[t.index("## Money rules"):t.index("## How your work will be checked")].rstrip() + "\n"


def build():
    shutil.rmtree(OUT, ignore_errors=True)
    where = plant(OUT / "bugs", BUGS)
    plant(OUT / "clean", [])
    for d in ("bugs", "clean"):
        (OUT / d / "spec.md").write_text(spec(), encoding="utf-8", newline="\n")
    KEY.write_text(json.dumps({"bugs": [{"id": b[0], "area": b[1], "file": where[b[0]][0], "line": where[b[0]][1]}
                                        for b in BUGS]}, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}/bugs (20 planted) and /clean, and {KEY.relative_to(ROOT)} (local only)")


def grade_a1(folder):
    p = subprocess.run([sys.executable, str(ROOT / "benchmark/grade/walk.py"), str(A1), str(folder)],
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    return json.loads(p.stdout)


def selftest():
    tmp = Path(tempfile.mkdtemp(prefix="a2_selftest_"))
    try:
        plant(tmp / "all", BUGS)                                    # all 20 apply together, anchors unique
        print(f"all {len(BUGS)} bugs apply together; anchors unique")
        bad = 0
        for b in BUGS:
            d = tmp / b[0]
            plant(d, [b])
            g = grade_a1(d)
            fails = [k for k, v in g["details"].get("checks", {}).items() if v != "ok"]
            started = "checks" in g["details"]
            ok = started and len(fails) >= 1
            bad += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {b[0]} {b[1]}: {len(fails)} A1 check(s) fail"
                  + ("" if started else f" (app did not start: {g['details'].get('summary')})"))
        print(f"{len(BUGS) - bad}/{len(BUGS)} bugs trip at least one hidden check")
        return 1 if bad else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    build()
