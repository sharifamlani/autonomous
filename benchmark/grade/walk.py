"""Grader `walk` (A1): start the app the agent built and run the hidden acceptance checks.

Config ([grade] in task.toml):  threshold = 0.9   start_timeout = 90
  1. API checks against the money rules, validation and 404s in task.md;
  2. restart: stop the server, start it again, the data must still be there;
  3. UI walk in headless Chromium (Playwright), finding elements by the data-testid names task.md lists.
Expected values are worked out by hand from task.md's rules, not taken from the reference build, so a
bug in the reference cannot hide a bug in the checks. Passing = at least `threshold` of the checks.

The app is started from START.txt with Git Bash, in a Windows job object, on a free port, and every
process it started is killed at the end.
Usage: python benchmark/grade/walk.py <task_dir> <outputs_dir>
"""
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from _common import args, emit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runner"))
import launch  # noqa: E402  (the Job object)

BASH = r"C:\Program Files\Git\bin\bash.exe"
MONEY = re.compile(r"^-?\d+\.\d{2}$")
UI_CHECKS = 7                                                # ui_checks() runs this many checks


class App:
    def __init__(self, folder, cmd, timeout):
        self.folder, self.cmd, self.timeout = folder, cmd, timeout
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        self.port = s.getsockname()[1]
        s.close()
        self.base = f"http://127.0.0.1:{self.port}"
        self.log = tempfile.NamedTemporaryFile(prefix="walk_app_", suffix=".log", delete=False)
        self.job = None

    def start(self):
        env = os.environ.copy() | {"PORT": str(self.port)}
        shell = [BASH, "-c", self.cmd] if os.path.exists(BASH) else self.cmd
        self.proc = subprocess.Popen(shell, cwd=self.folder, env=env, stdout=self.log, stderr=subprocess.STDOUT,
                                     shell=not os.path.exists(BASH))
        self.job = launch.Job()
        self.job.add(self.proc.pid)
        t0 = time.time()
        while time.time() - t0 < self.timeout:
            if self.proc.poll() is not None and self.job.counts()[1] == 0:
                return False
            try:
                urllib.request.urlopen(self.base + "/", timeout=2).read()
                return True
            except (urllib.error.URLError, ConnectionError, OSError):
                time.sleep(0.5)
        return False

    def stop(self):
        if self.job:
            self.job.kill()
            self.job.close()
            self.job = None
        time.sleep(0.5)

    def tail(self):
        try:
            return Path(self.log.name).read_text(encoding="utf-8", errors="replace")[-400:]
        except OSError:
            return ""


def call(base, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            status = r.status
    except urllib.error.HTTPError as e:
        raw, status = e.read(), e.code
    try:
        return status, json.loads(raw) if raw else None
    except json.JSONDecodeError:
        return status, raw.decode("utf-8", "replace")[:200]


class Checks:
    def __init__(self):
        self.results = {}

    def run(self, name, fn):
        try:
            ok = bool(fn())
            why = "" if ok else "condition false"
        except Exception as e:                               # a crash in one check fails only that check
            ok, why = False, f"{type(e).__name__}: {str(e)[:120]}"
        self.results[name] = "ok" if ok else f"FAIL ({why})"
        return ok


def api_checks(c, base, st):
    def post(path, body):
        return call(base, "POST", path, body)

    def err(resp, code):
        return resp[0] == code and isinstance(resp[1], dict) and "error" in resp[1]

    def create():
        s, g = post("/api/groups", {"name": "Trip", "members": ["Ana", "Ben", "Cy"]})
        st["gid"] = g["id"]
        return s == 201 and g["name"] == "Trip" and g["members"] == ["Ana", "Ben", "Cy"]
    c.run("API: create group", create)
    gid = st.get("gid", "missing")
    G = f"/api/groups/{gid}"
    def get():
        s, g = call(base, "GET", G)
        return s == 200 and g["name"] == "Trip" and g["members"] == ["Ana", "Ben", "Cy"]
    c.run("API: get group keeps member order", get)
    c.run("API: group validation (empty name, 1 member, duplicate names) is 400",
          lambda: err(post("/api/groups", {"name": "", "members": ["A", "B"]}), 400)
          and err(post("/api/groups", {"name": "X", "members": ["Ana"]}), 400)
          and err(post("/api/groups", {"name": "X", "members": ["ana", "Ana"]}), 400))

    def e1():
        s, e = post(G + "/expenses", {"description": "Dinner", "amount": "100.00", "paid_by": "Ana"})
        st["e1"] = e["id"]
        return s == 201 and e["amount"] == "100.00" and e["shares"] == {"Ana": "33.34", "Ben": "33.33", "Cy": "33.33"}
    c.run("API: 100.00 split 3 ways, leftover cent to the first member", e1)

    def e2():
        s, e = post(G + "/expenses", {"description": "Taxi", "amount": 20.01, "paid_by": "Ben", "split_among": ["Cy", "Ben"]})
        return s == 201 and e["shares"] == {"Ben": "10.01", "Cy": "10.00"}
    c.run("API: numeric amount; leftover cent follows group order, not request order", e2)

    def e3():
        s, e = post(G + "/expenses", {"description": "Snacks", "amount": "10", "paid_by": "Cy"})
        st["e3"] = e["id"]
        return s == 201 and e["amount"] == "10.00" and e["shares"] == {"Ana": "3.34", "Ben": "3.33", "Cy": "3.33"}
    c.run("API: amount '10' is accepted and returned as '10.00'", e3)
    c.run("API: balances exact", lambda: call(base, "GET", G + "/balances") == (200, {"Ana": "63.32", "Ben": "-26.66", "Cy": "-36.66"}))

    def sums():
        b = call(base, "GET", G + "/balances")[1]
        return all(MONEY.match(v) for v in b.values()) and sum(round(float(v) * 100) for v in b.values()) == 0
    c.run("API: balances are 2-decimal strings summing to 0.00", sums)

    def listing():
        s, xs = call(base, "GET", G + "/expenses")
        return s == 200 and [x["description"] for x in xs] == ["Dinner", "Taxi", "Snacks"] and [x["amount"] for x in xs] == ["100.00", "20.01", "10.00"]
    c.run("API: expense list oldest first", listing)
    c.run("API: settle up exact", lambda: call(base, "GET", G + "/settle") == (200, [
        {"from": "Cy", "to": "Ana", "amount": "36.66"}, {"from": "Ben", "to": "Ana", "amount": "26.66"}]))
    c.run("API: delete expense is 204 and balances update",
          lambda: call(base, "DELETE", f"{G}/expenses/{st['e3']}")[0] == 204
          and call(base, "GET", G + "/balances") == (200, {"Ana": "66.66", "Ben": "-23.33", "Cy": "-43.33"}))
    c.run("API: settle up after delete", lambda: call(base, "GET", G + "/settle") == (200, [
        {"from": "Cy", "to": "Ana", "amount": "43.33"}, {"from": "Ben", "to": "Ana", "amount": "23.33"}]))

    def ties():
        s, g = post("/api/groups", {"name": "Tie", "members": ["Dee", "Eve", "Fay", "Gus"]})
        T = f"/api/groups/{g['id']}"
        st["tie"] = T
        post(T + "/expenses", {"description": "Hut", "amount": "30.00", "paid_by": "Dee"})
        return call(base, "GET", T + "/settle") == (200, [{"from": "Eve", "to": "Dee", "amount": "7.50"},
                                                          {"from": "Fay", "to": "Dee", "amount": "7.50"},
                                                          {"from": "Gus", "to": "Dee", "amount": "7.50"}])
    c.run("API: settle-up ties broken by member order", ties)

    def small():
        s, e = post(st["tie"] + "/expenses", {"description": "Gum", "amount": "0.05", "paid_by": "Gus"})
        return s == 201 and e["shares"] == {"Dee": "0.02", "Eve": "0.01", "Fay": "0.01", "Gus": "0.01"}
    c.run("API: 0.05 split 4 ways", small)
    c.run("API: invalid amounts ('0', '-5', 'abc', '1.234') are 400",
          lambda: all(err(post(G + "/expenses", {"description": "x", "amount": a, "paid_by": "Ana"}), 400)
                      for a in ("0", "-5", "abc", "1.234")))
    c.run("API: non-member payer, non-member or empty split are 400",
          lambda: err(post(G + "/expenses", {"description": "x", "amount": "1", "paid_by": "Zed"}), 400)
          and err(post(G + "/expenses", {"description": "x", "amount": "1", "paid_by": "Ana", "split_among": ["Zed"]}), 400)
          and err(post(G + "/expenses", {"description": "x", "amount": "1", "paid_by": "Ana", "split_among": []}), 400))
    c.run("API: empty description is 400",
          lambda: err(post(G + "/expenses", {"description": "", "amount": "1", "paid_by": "Ana"}), 400))
    c.run("API: unknown group and unknown expense are 404",
          lambda: err(call(base, "GET", "/api/groups/no-such-group"), 404)
          and err(call(base, "DELETE", f"{G}/expenses/no-such-expense"), 404))

    def empty():
        s, g = post("/api/groups", {"name": "Quiet", "members": ["Hal", "Ivy"]})
        return call(base, "GET", f"/api/groups/{g['id']}/settle") == (200, [])
    c.run("API: settle up with no expenses is []", empty)


def restart_checks(c, app, st):
    G = f"/api/groups/{st.get('gid', 'missing')}"
    app.stop()
    up = app.start()
    c.run("restart: group survives a restart", lambda: up and call(app.base, "GET", G)[1]["members"] == ["Ana", "Ben", "Cy"])
    c.run("restart: balances survive a restart",
          lambda: up and call(app.base, "GET", G + "/balances") == (200, {"Ana": "66.66", "Ben": "-23.33", "Cy": "-43.33"}))


def amounts_in(text):
    t = text.replace("$", "").replace(",", "").replace("\u2212", "-").replace("+", "")
    return set(re.findall(r"(?<![\d.])-?\d+\.\d{2}(?!\d)", t))


def ui_checks(c, base):
    from playwright.sync_api import sync_playwright

    def until(fn, timeout=6.0):
        t0 = time.time()
        while time.time() - t0 < timeout:
            try:
                if fn():
                    return True
            except Exception:
                pass
            time.sleep(0.2)
        return False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        tid = page.get_by_test_id

        def balances_are(want):
            return all(want[m] in amounts_in(tid(f"balance-{m}").inner_text()) for m in want)

        def loaded():
            page.goto(base + "/", wait_until="domcontentloaded")
            return all(tid(t).count() == 1 for t in ("group-name", "group-members", "create-group"))
        c.run("UI: page shows the create-group form", loaded)

        def create():
            tid("group-name").fill("Cabin")
            tid("group-members").fill("Ana, Ben, Cy")
            tid("create-group").click()
            return until(lambda: tid("group-title").is_visible() and "Cabin" in tid("group-title").inner_text()) and \
                until(lambda: all(tid(f"split-{m}").count() == 1 for m in ("Ana", "Ben", "Cy")))
        c.run("UI: create a group", create)

        def add(desc, amount, payer, uncheck=()):
            tid("expense-description").fill(desc)
            tid("expense-amount").fill(amount)
            tid("expense-paid-by").select_option(payer)
            for m in ("Ana", "Ben", "Cy"):
                box = tid(f"split-{m}")
                if (m in uncheck) == box.is_checked():
                    box.click()
            tid("add-expense").click()

        def first():
            add("Dinner", "100.00", "Ana")
            return until(lambda: tid("expense-row").count() == 1 and balances_are({"Ana": "66.66", "Ben": "-33.33", "Cy": "-33.33"}))
        c.run("UI: add an expense; rows and balances update", first)

        def second():
            add("Taxi", "30.00", "Ben", uncheck=("Cy",))
            return until(lambda: tid("expense-row").count() == 2 and balances_are({"Ana": "51.66", "Ben": "-18.33", "Cy": "-33.33"}))
        c.run("UI: unchecked member is left out of the split", second)

        def invalid():
            add("Bad", "abc", "Ana")
            return until(lambda: tid("error").is_visible() and tid("error").inner_text().strip() != "") and \
                tid("expense-row").count() == 2
        c.run("UI: invalid amount shows an error and adds nothing", invalid)

        def settle():
            def rows_ok():
                rows = [r.inner_text() for r in tid("settle-row").all()]
                return len(rows) == 2 and all(n in rows[0] for n in ("Cy", "Ana")) and "33.33" in amounts_in(rows[0]) \
                    and all(n in rows[1] for n in ("Ben", "Ana")) and "18.33" in amounts_in(rows[1])
            return until(rows_ok)
        c.run("UI: settle-up rows", settle)

        def delete():
            tid("expense-row").first.get_by_test_id("delete-expense").click()
            return until(lambda: tid("expense-row").count() == 1 and balances_are({"Ana": "-15.00", "Ben": "15.00", "Cy": "0.00"}))
        c.run("UI: delete an expense; balances update", delete)
        browser.close()


def main():
    cfg, g, out = args()
    start = out / "START.txt"
    if not start.exists():
        emit(False, 0, {"summary": "no START.txt: the app cannot be started"})
        return
    cmd = next((l.strip() for l in start.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()), "")
    app = App(out, cmd, g.get("start_timeout", 90))
    c, st = Checks(), {}
    try:
        if not app.start():
            emit(False, 0, {"summary": f"app did not start with `{cmd[:80]}`", "log_tail": app.tail()})
            return
        api_checks(c, app.base, st)
        restart_checks(c, app, st)
        try:
            ui_checks(c, app.base)
        except Exception as e:                               # the walk itself crashed: unreached checks fail
            done = sum(k.startswith("UI:") for k in c.results)
            for i in range(done, UI_CHECKS):
                c.results[f"UI: check {i + 1} not reached"] = f"FAIL (walk crashed: {type(e).__name__}: {str(e)[:100]})"
    finally:
        app.stop()
    n = len(c.results)
    passed = sum(v == "ok" for v in c.results.values())
    failed = [k for k, v in c.results.items() if v != "ok"]
    ok = n > 0 and passed / n >= g.get("threshold", 0.9)
    emit(ok, round(passed / n, 3) if n else 0,
         {"summary": f"{passed} of {n} checks ok" + (f"; failed: {', '.join(failed)}" if failed else ""),
          "checks": c.results})


if __name__ == "__main__":
    main()
