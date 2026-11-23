"""Grader `rota` (A4): start the app the agent built and run the hidden acceptance checks.

Config ([grade] in task.toml):  threshold = 0.9   start_timeout = 90
  1. API checks, one rule of task.md each (people + If-Match, CSV import, shifts + overnight hours,
     pagination, the 7 assignment rules alone and in order, auto-fill, undo, audit, export, errors);
  2. restart: stop the server, start it again: data, versions, audit log and undo history must survive;
     then the 20-action undo limit, after the restart;
  3. the folder is put back as handed in (files the run created are deleted, files it changed are
     restored), the app is started on that fresh store, and the UI is walked in headless Chromium
     (Playwright), finding elements by the data-testid names task.md lists.
Expected values are worked out by hand from task.md's rules (dates in March 2026; 2026-03-02 is a
Monday), not taken from the reference build. Passing = at least `threshold` of the checks.

The app is graded in place (like walk.py), started from START.txt with Git Bash in a Windows job
object on a free port; every process it started is killed and the folder is restored at the end.
Usage: python benchmark/grade/rota.py <task_dir> <outputs_dir>
"""
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

from _common import args, emit
from walk import App, Checks, call

UI_CHECKS = 10                                               # ui_checks() runs this many checks
DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
SKIP = {"node_modules", ".git", ".venv", "venv", "env", "__pycache__", ".next", ".cache", "site-packages",
        ".pytest_cache", ".mypy_cache"}
BIG = 50 * 2 ** 20


class Folder:
    """The outputs folder as handed in, so a run can put it back (the store starts empty each time)."""

    def __init__(self, root):
        self.root = Path(root)
        self.files, self.dirs = {}, set()
        for f in self.walk():
            if f.stat().st_size <= BIG:
                self.files[f.relative_to(self.root)] = f.read_bytes()
        self.dirs = {d.relative_to(self.root) for d in self.walk(dirs=True)}

    def walk(self, dirs=False):
        for top, ds, fs in os.walk(self.root):
            ds[:] = [d for d in ds if d not in SKIP]
            for n in (ds if dirs else fs):
                yield Path(top) / n

    def restore(self):
        for f in list(self.walk()):
            rel = f.relative_to(self.root)
            if rel not in self.files:
                if f.stat().st_size <= BIG:
                    retry(f.unlink)
            elif f.read_bytes() != self.files[rel]:
                retry(lambda: f.write_bytes(self.files[rel]))
        for rel, data in self.files.items():
            f = self.root / rel
            if not f.exists():
                f.parent.mkdir(parents=True, exist_ok=True)
                retry(lambda: f.write_bytes(data))
        for d in sorted(self.walk(dirs=True), key=lambda p: -len(p.parts)):
            if d.relative_to(self.root) not in self.dirs and not any(d.iterdir()):
                retry(d.rmdir)


def retry(fn, tries=20):
    for i in range(tries):
        try:
            return fn()
        except OSError:
            if i == tries - 1:
                raise
            time.sleep(0.3)


def send(base, method, path, body=None, headers=None, raw=None, ctype="application/json"):
    """Like walk.call, plus custom headers and a raw (CSV) body; returns (status, parsed, content-type, bytes)."""
    data = raw.encode() if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(base + path, data=data, method=method,
                                 headers={"Content-Type": ctype} | (headers or {}))
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            got, status, ct = r.read(), r.status, r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        got, status, ct = e.read(), e.code, e.headers.get("Content-Type", "")
    try:
        parsed = json.loads(got) if got else None
    except (json.JSONDecodeError, UnicodeDecodeError):
        parsed = got.decode("utf-8", "replace")[:300]
    return status, parsed, ct, got


def idkey(x):
    return (0, int(x), "") if str(x).isdigit() else (1, 0, str(x))


def err(resp, code):
    return resp[0] == code and isinstance(resp[1], dict) and "error" in resp[1]


def refused(resp, rule):
    return resp[0] == 409 and isinstance(resp[1], dict) and resp[1].get("rule") == rule and "error" in resp[1]


class Api:
    """Calls that change data go through here, so the expected audit log follows what the app accepted."""

    def __init__(self, base, st):
        self.base, self.st = base, st
        st.setdefault("acts", [])
        st.setdefault("P", {})
        st.setdefault("S", {})

    def did(self, kind, resp, ok):
        if resp[0] == ok:
            self.st["acts"].append(kind)
        return resp

    def post(self, path, body):
        return call(self.base, "POST", path, body)

    def get(self, path):
        return call(self.base, "GET", path)

    def person(self, name, role, mx, off=None, keep=True):
        body = {"name": name, "role": role, "max_hours": mx} | ({} if off is None else {"unavailable": off})
        try:
            r = self.did("person.create", self.post("/api/people", body), 201)
        except Exception:
            r = (None, None)
        if keep:
            self.st["P"][name] = r[1]["id"] if r[0] == 201 and isinstance(r[1], dict) else f"missing-{name}"
        return r

    def shift(self, label, date, start, end, role, slots=1):
        body = {"date": date, "start": start, "end": end, "role": role, "slots": slots}
        try:
            r = self.did("shift.create", self.post("/api/shifts", body), 201)
        except Exception:
            r = (None, None)
        if label:
            self.st["S"][label] = r[1]["id"] if r[0] == 201 and isinstance(r[1], dict) else f"missing-{label}"
        return r

    def bad_shift(self, date, start, end, role="porter", slots=1):
        return err(self.shift(None, date, start, end, role, slots), 400)

    def assign(self, label, name):
        sid, pid = self.st["S"].get(label, "missing"), self.st["P"].get(name, "missing")
        return self.did("assign", self.post(f"/api/shifts/{sid}/assign", {"person_id": pid}), 200)

    def unassign(self, label, name):
        sid, pid = self.st["S"].get(label, "missing"), self.st["P"].get(name, "missing")
        return self.did("unassign", call(self.base, "DELETE", f"/api/shifts/{sid}/assign/{pid}"), 204)

    def put(self, name, body, version=None):
        h = {} if version is None else {"If-Match": str(version)}
        r = send(self.base, "PUT", f"/api/people/{self.st['P'].get(name, 'missing')}", body, headers=h)
        return self.did("person.update", r, 200)

    def undo(self):
        return self.did("undo", self.post("/api/undo", {}), 200)

    def import_csv(self, text):
        return self.did("person.import", send(self.base, "POST", "/api/people/import", raw=text, ctype="text/csv"), 200)

    def people(self):
        return {p["name"]: p for p in self.get("/api/people")[1]}

    def shifts(self):
        return {s["id"]: s for s in self.get("/api/shifts?per_page=100")[1]["items"]}

    def on(self, label):
        """The assigned person ids of one shift."""
        return self.shifts()[self.st["S"][label]]["assigned"]

    def ids(self, *names):
        return [self.st["P"].get(n) for n in names]


def safely(fn):
    try:
        fn()
    except Exception:
        pass


def api_checks(c, base, st):
    a = Api(base, st)
    P, S = st["P"], st["S"]

    c.run("API: POST /api/undo with nothing to undo is 409 rule nothing_to_undo", lambda: refused(a.undo(), "nothing_to_undo"))

    # ---- people
    def ana():
        s, p = a.person("Ana", "nurse", 40, ["sun", "sat", "sun"])
        return s == 201 and p["name"] == "Ana" and p["role"] == "nurse" and p["max_hours"] == 40 \
            and p["unavailable"] == ["sat", "sun"] and p["version"] == 1 and "id" in p
    c.run("API: create person is 201 with version 1; unavailable returned in day order, no duplicates", ana)

    def empty_off():
        (s1, b), (s2, k) = a.person("Bob", "doctor", 40, []), a.person("Cat", "nurse", 40)
        return s1 == 201 and b["unavailable"] == [] and s2 == 201 and k["unavailable"] == []
    c.run("API: unavailable may be empty or omitted (returned as [])", empty_off)
    safely(lambda: a.person("bea", "porter", 40, []))

    c.run("API: person name empty or already used (ignoring case: 'ana', 'ANA') is 400",
          lambda: all([err(a.person(n, "nurse", 40, keep=False), 400) for n in ("", "ana", "ANA")]))
    c.run("API: person role not nurse/doctor/porter is 400",
          lambda: all([err(a.person("Rex", r, 40, keep=False), 400) for r in ("surgeon", "")]))

    def max_hours():
        bad = all([err(a.person("Rex", "porter", m, keep=False), 400) for m in (0, 61, 7.5)])
        return bad and a.person("Pam", "porter", 1)[0] == 201 and a.person("Quin", "porter", 60)[0] == 201
    c.run("API: max_hours is a whole number from 1 to 60 (0, 61, 7.5 are 400; 1 and 60 accepted)", max_hours)
    c.run("API: unavailable with a code outside mon..sun is 400",
          lambda: all([err(a.person("Rex", "porter", 40, off, keep=False), 400) for off in (["funday"], ["mon", "xyz"])]))
    c.run("API: GET /api/people sorted by name ignoring case",
          lambda: [p["name"] for p in a.get("/api/people")[1]] == ["Ana", "bea", "Bob", "Cat", "Pam", "Quin"])

    # ---- PUT with If-Match
    bob = {"name": "Bob", "role": "doctor", "max_hours": 30, "unavailable": ["mon"]}
    c.run("API: PUT /api/people/{id} without If-Match is 428", lambda: a.put("Bob", bob)[0] == 428)
    c.run("API: PUT with an If-Match that is not the current version is 409", lambda: a.put("Bob", bob, 7)[0] == 409)

    def put_ok():
        s, p = a.put("Bob", bob, 1)[:2]
        return s == 200 and p["version"] == 2 and p["max_hours"] == 30 and p["unavailable"] == ["mon"] and p["name"] == "Bob"
    c.run("API: PUT with the current If-Match is 200 and version increases by 1", put_ok)
    c.run("API: PUT applies the same validation as create (bad role, name used by another person) is 400",
          lambda: err(a.put("Bob", bob | {"role": "surgeon"}, 2), 400) and err(a.put("Bob", bob | {"name": "cat"}, 2), 400))

    def undo_update():
        r = a.undo()
        b = a.people()["Bob"]
        return r[0] == 200 and r[1] == {"undone": "person.update"} and b["max_hours"] == 40 and b["unavailable"] == [] \
            and b["role"] == "doctor" and b["version"] == 3
    c.run("API: undo of person.update restores the old fields and the version advances by 1 (to 3)", undo_update)

    # ---- CSV import
    csv_text = ("name,role,max_hours,unavailable\n"
                "Dan,porter,30,sun;sat\n"      # 2 ok
                "Eve,surgeon,30,\n"            # 3 bad role
                "Fay,porter,0,\n"              # 4 bad max_hours
                "dan,porter,20,\n"             # 5 name used by an earlier row (ignoring case)
                "Gus,nurse,40,sun\n"           # 6 ok
                "ana,nurse,40,\n"              # 7 name used by an existing person
                "Hal,porter,30,mon;xyz\n")     # 8 bad day code

    def imported():
        s, r = a.import_csv(csv_text)[:2]
        return s == 200 and r["created"] == 2 and [e["line"] for e in r["errors"]] == [3, 4, 5, 7, 8] \
            and all(isinstance(e["error"], str) and e["error"] for e in r["errors"])
    c.run("API: CSV import creates valid rows; errors carry line numbers (header = line 1), incl. a name repeated in the file", imported)

    def import_fields():
        ppl = a.people()
        P["Dan"], P["Gus"] = ppl["Dan"]["id"], ppl["Gus"]["id"]
        d, g = ppl["Dan"], ppl["Gus"]
        return d["role"] == "porter" and d["max_hours"] == 30 and d["unavailable"] == ["sat", "sun"] and d["version"] == 1 \
            and g["role"] == "nurse" and g["unavailable"] == ["sun"] and not ({"Eve", "Fay", "Hal", "dan"} & set(ppl))
    c.run("API: imported people have their fields; invalid rows were skipped", import_fields)

    # ---- shifts
    def overnight():
        s, b = a.shift("N1", "2026-03-02", "22:00", "06:00", "nurse", 2)
        return s == 201 and b["hours"] == 8 and b["assigned"] == [] and b["slots"] == 2 and b["date"] == "2026-03-02" \
            and b["start"] == "22:00" and b["end"] == "06:00" and b["role"] == "nurse"
    c.run("API: create shift 22:00-06:00 is 201, ends the next day: hours 8, assigned []", overnight)
    c.run("API: shift 07:00-14:30 has hours 7.5", lambda: a.shift("half", "2026-04-06", "07:00", "14:30", "porter")[1]["hours"] == 7.5)

    def bounds():
        ok = a.shift("h1", "2026-04-07", "10:00", "11:00", "porter")[1]["hours"] == 1 \
            and a.shift("h12", "2026-04-08", "08:00", "20:00", "porter")[1]["hours"] == 12 \
            and a.shift("h12n", "2026-04-09", "20:00", "08:00", "porter")[1]["hours"] == 12
        return ok and all([a.bad_shift("2026-04-10", s, e) for s, e in
                           (("10:00", "10:30"), ("08:00", "20:30"), ("20:00", "09:00"), ("09:00", "09:00"))])
    c.run("API: a shift lasts 1 to 12 hours (1h, 12h, overnight 12h ok; 0.5h, 12.5h, overnight 13h, start=end are 400)", bounds)
    c.run("API: times must be HH:MM on the hour or half hour (07:15, 15:45, 7:00, 24:00 are 400)",
          lambda: all([a.bad_shift("2026-04-10", s, e) for s, e in
                       (("07:15", "15:00"), ("07:00", "15:45"), ("7:00", "15:00"), ("24:00", "06:00"))]))
    c.run("API: shift date, slots (1-5 whole) and role are validated (400)",
          lambda: all([a.bad_shift("2026-02-30", "08:00", "16:00"), a.bad_shift("2026-3-2", "08:00", "16:00"),
                       a.bad_shift("2026-04-10", "08:00", "16:00", slots=0), a.bad_shift("2026-04-10", "08:00", "16:00", slots=6),
                       a.bad_shift("2026-04-10", "08:00", "16:00", slots=2.5),
                       a.bad_shift("2026-04-10", "08:00", "16:00", role="chef")]))

    # ---- pagination (week of Monday 2026-03-16), created out of order
    week3 = {"P1": ("2026-03-18", "09:00", "17:00", "porter", 1), "P2": ("2026-03-16", "12:00", "20:00", "porter", 3),
             "P3": ("2026-03-16", "08:00", "16:00", "nurse", 2), "P4": ("2026-03-18", "09:00", "17:00", "doctor", 1),
             "P5": ("2026-03-17", "23:00", "07:00", "porter", 1)}
    for k, v in week3.items():
        a.shift(k, *v)
    order = sorted(week3, key=lambda k: (week3[k][0], week3[k][1], idkey(S[k])))      # date, start, id
    st["week3"], st["week3_order"] = week3, order
    ids = lambda keys: [S[k] for k in keys]
    W3 = "/api/shifts?from=2026-03-16&to=2026-03-22"

    def page1():
        s, r = a.get(W3)
        return s == 200 and [x["id"] for x in r["items"]] == ids(order) and r["total"] == 5 and r["page"] == 1 and r["per_page"] == 20
    c.run("API: GET /api/shifts filters from..to and orders by date, then start, then id (per_page defaults to 20)", page1)

    def page2():
        r = a.get(W3 + "&page=2&per_page=2")[1]
        return [x["id"] for x in r["items"]] == ids(order[2:4]) and r["total"] == 5 and r["page"] == 2 and r["per_page"] == 2
    c.run("API: pagination: page 2 of per_page 2, total counts all matches", page2)

    def filters():
        r1 = a.get("/api/shifts?from=2026-03-16&to=2026-03-18&role=porter")[1]
        r2 = a.get("/api/shifts?from=2026-03-17&to=2026-03-18")[1]
        return [x["id"] for x in r1["items"]] == ids([k for k in order if week3[k][3] == "porter"]) and r1["total"] == 3 \
            and [x["id"] for x in r2["items"]] == ids([k for k in order if week3[k][0] >= "2026-03-17"]) and r2["total"] == 3
    c.run("API: role filter, and from/to are inclusive", filters)
    c.run("API: per_page is at most 100", lambda: a.get(W3 + "&per_page=500")[1]["per_page"] == 100)

    # ---- 404s
    c.run("API: unknown person is 404 with an error (PUT, DELETE, assign person_id)",
          lambda: err(a.did("person.update", send(base, "PUT", "/api/people/999999", bob, headers={"If-Match": "1"}), 200), 404)
          and err(a.did("person.delete", call(base, "DELETE", "/api/people/999999"), 204), 404)
          and err(a.did("assign", a.post(f"/api/shifts/{S['N1']}/assign", {"person_id": 999999}), 200), 404))
    c.run("API: unknown shift is 404 with an error (assign, unassign)",
          lambda: err(a.did("assign", a.post("/api/shifts/999999/assign", {"person_id": P["Ana"]}), 200), 404)
          and err(a.did("unassign", call(base, "DELETE", f"/api/shifts/999999/assign/{P['Ana']}"), 204), 404))

    # ---- the 7 rules (week of Monday 2026-03-02)
    for k, v in {"N2": ("2026-03-04", "07:00", "15:00", "nurse", 1), "N3": ("2026-03-07", "08:00", "16:00", "nurse", 2),
                 "N4": ("2026-03-03", "05:00", "09:00", "nurse", 1), "N5": ("2026-03-03", "06:00", "10:00", "nurse", 1),
                 "N6": ("2026-03-02", "08:00", "14:00", "nurse", 1), "N7": ("2026-03-03", "16:00", "20:00", "nurse", 1),
                 "N8": ("2026-03-06", "22:00", "06:00", "nurse", 2), "N9": ("2026-03-07", "05:00", "09:00", "nurse", 1),
                 "H1": ("2026-03-05", "08:00", "16:00", "nurse", 1), "H2": ("2026-03-06", "08:00", "10:00", "nurse", 1),
                 "H3": ("2026-03-07", "18:00", "21:00", "nurse", 1), "RH": ("2026-03-05", "18:00", "21:00", "nurse", 1),
                 "J1": ("2026-03-08", "22:00", "06:00", "nurse", 1), "J2": ("2026-03-09", "16:00", "23:00", "nurse", 1),
                 "J3": ("2026-03-05", "08:00", "12:00", "nurse", 1)}.items():
        a.shift(k, *v)
    safely(lambda: a.person("Ivy", "nurse", 10, []))
    safely(lambda: a.person("Jo", "nurse", 10, []))

    c.run("API: rule role alone: a doctor on a nurse shift is 409 rule role", lambda: refused(a.assign("N1", "Bob"), "role"))

    def assign_ok():
        s, b = a.assign("N1", "Ana")
        return s == 200 and b["id"] == S["N1"] and b["assigned"] == [P["Ana"]]
    c.run("API: assign is 200 and returns the updated shift (assigned in order)", assign_ok)
    c.run("API: rule duplicate alone: already on this shift (1 of 2 slots taken) is 409 rule duplicate",
          lambda: refused(a.assign("N1", "Ana"), "duplicate"))
    c.run("API: rule full alone: every slot taken is 409 rule full",
          lambda: a.assign("N2", "Cat")[0] == 200 and refused(a.assign("N2", "Gus"), "full"))
    c.run("API: rule order: role is checked before full", lambda: refused(a.assign("N2", "Bob"), "role"))
    c.run("API: rule order: full is checked before duplicate", lambda: refused(a.assign("N2", "Cat"), "full"))
    c.run("API: rule unavailable alone: a Saturday shift for a sat-unavailable person is 409 rule unavailable",
          lambda: refused(a.assign("N3", "Ana"), "unavailable"))
    c.run("API: rule overlap: overlapping an overnight shift (Tue 05:00 vs Mon 22:00-06:00) is overlap, checked before rest",
          lambda: refused(a.assign("N4", "Ana"), "overlap"))
    c.run("API: touching end-to-start (06:00 after a shift ending 06:00) is not an overlap but breaks rest",
          lambda: refused(a.assign("N5", "Ana"), "rest"))
    c.run("API: rule rest the other way: this shift ends 8h before another of theirs starts is rest",
          lambda: refused(a.assign("N6", "Ana"), "rest"))
    c.run("API: exactly 10 hours of rest is allowed", lambda: a.assign("N7", "Ana")[0] == 200)
    c.run("API: unavailable uses the start date: Fri 22:00-06:00 is allowed for a sat-unavailable person",
          lambda: a.assign("N8", "Ana")[0] == 200)
    c.run("API: rule order: unavailable is checked before overlap (Sat 05:00 overlapping Fri 22:00-06:00)",
          lambda: refused(a.assign("N9", "Ana"), "unavailable"))
    c.run("API: rule hours: reaching max_hours exactly (8h + 2h = 10) is allowed",
          lambda: a.assign("H1", "Ivy")[0] == 200 and a.assign("H2", "Ivy")[0] == 200)
    c.run("API: rule hours alone: exceeding max_hours in the Mon-Sun week (10h + 3h > 10) is 409 rule hours",
          lambda: refused(a.assign("H3", "Ivy"), "hours"))
    c.run("API: rule order: rest is checked before hours", lambda: refused(a.assign("RH", "Ivy"), "rest"))
    c.run("API: hours: an overnight Sunday shift counts in its start week, so a 7h Monday shift after it fits a 10h max",
          lambda: a.assign("J1", "Jo")[0] == 200 and a.assign("J2", "Jo")[0] == 200)
    c.run("API: hours: the Sunday overnight's 8h count in that Mon-Sun week (a 4h Thursday shift is rule hours)",
          lambda: refused(a.assign("J3", "Jo"), "hours"))

    def unassign():
        return a.unassign("N7", "Ana")[0] == 204 and a.on("N7") == []
    c.run("API: DELETE /api/shifts/{id}/assign/{person_id} is 204 and removes the assignment", unassign)

    def update_keeps():
        s, p = a.put("Ana", {"name": "Ana", "role": "nurse", "max_hours": 10, "unavailable": ["sat", "sun"]}, 1)[:2]
        return s == 200 and p["version"] == 2 and P["Ana"] in a.on("N1") and P["Ana"] in a.on("N8")
    c.run("API: changing a person does not touch their existing assignments", update_keeps)

    # ---- auto-fill (week of Monday 2026-03-23, doctors), plus the week-3 assignments the export reads
    for n, mx, off in (("Kim", 40, []), ("jon", 40, ["wed"]), ("Max", 12, [])):
        safely(lambda: a.person(n, "doctor", mx, off))
    for label, name in (("P3", "Gus"), ("P3", "Cat"), ("P2", "Dan"), ("P2", "bea"), ("P4", "Kim")):
        safely(lambda: a.assign(label, name))
    safely(lambda: a.shift("A0", "2026-03-23", "08:00", "16:00", "doctor", 1))
    safely(lambda: a.assign("A0", "Bob"))
    for k, v in {"F1": ("2026-03-25", "08:00", "16:00", "doctor", 2), "F2": ("2026-03-24", "08:00", "18:00", "doctor", 1),
                 "F3": ("2026-03-24", "09:00", "13:00", "doctor", 1), "F4": ("2026-03-28", "09:00", "17:00", "doctor", 5)}.items():
        a.shift(k, *v)
    # by hand: F2 (Tue 08-18) -> jon (0h; jon<Kim<Max ignoring case), F3 -> Kim (0h this week; jon overlaps),
    # F1 (Wed) -> Max (0h), Kim (4h < Bob 8h; jon off wed), F4 (Sat) -> Bob 8h, jon 10h, Kim 12h; Max would pass 12h
    want_assigned = [("F2", "jon"), ("F3", "Kim"), ("F1", "Max"), ("F1", "Kim"), ("F4", "Bob"), ("F4", "jon"), ("F4", "Kim")]
    want = {"assigned": [{"shift_id": S.get(f), "person_id": P.get(n)} for f, n in want_assigned],
            "unfilled": [{"shift_id": S.get("F4"), "open": 2}]}
    W4 = {"from": "2026-03-23", "to": "2026-03-29"}

    def picked(r):
        s, b = r[:2]
        got = {"assigned": [{"shift_id": x["shift_id"], "person_id": x["person_id"]} for x in b["assigned"]],
               "unfilled": [{"shift_id": x["shift_id"], "open": x["open"]} for x in b["unfilled"]]}
        return s == 200 and got == want

    def autofill():
        ok = picked(a.did("autofill", a.post("/api/autofill", W4), 200))
        sh = a.shifts()
        return ok and sh[S["F1"]]["assigned"] == a.ids("Max", "Kim") and sh[S["F4"]]["assigned"] == a.ids("Bob", "jon", "Kim") \
            and sh[S["A0"]]["assigned"] == a.ids("Bob")
    c.run("API: auto-fill picks fewest hours in the shift's week, ties by name ignoring case; reports unfilled; shift order", autofill)

    def undo_autofill():
        r = a.undo()
        sh = a.shifts()
        return r[1] == {"undone": "autofill"} and all(sh[S[f]]["assigned"] == [] for f in ("F1", "F2", "F3", "F4")) \
            and sh[S["A0"]]["assigned"] == a.ids("Bob") and sh[S["P4"]]["assigned"] == a.ids("Kim")
    c.run("API: undo of autofill reverts every slot it filled as one action", undo_autofill)
    c.run("API: auto-fill is deterministic (the same choices again after the undo)",
          lambda: picked(a.did("autofill", a.post("/api/autofill", W4), 200)))

    # ---- export (week 3)
    def export():
        names = {"P3": ["Cat", "Gus"], "P2": ["bea", "Dan"], "P4": ["Kim"]}
        lines = ["date,start,end,role,person"]
        for k in order:
            d, s, e, role, slots = week3[k]
            got = names.get(k, [])
            lines += [f"{d},{s},{e},{role},{n}" for n in got] + [f"{d},{s},{e},{role},OPEN"] * (slots - len(got))
        status, _, ct, raw = send(base, "GET", "/api/export.csv?from=2026-03-16&to=2026-03-22")
        return status == 200 and ct.startswith("text/csv") and raw.decode("utf-8") == "".join(l + "\n" for l in lines)
    c.run("API: export.csv is text/csv, exact rows: by date, start, id; names ignoring case, then OPEN; lines end \\n", export)

    # ---- delete + undo
    def delete():
        r = a.did("person.delete", call(base, "DELETE", f"/api/people/{P['Kim']}"), 204)
        return r[0] == 204 and "Kim" not in a.people() and all(P["Kim"] not in s["assigned"] for s in a.shifts().values())
    c.run("API: DELETE /api/people/{id} is 204 and removes that person's assignments", delete)

    def undo_delete():
        r = a.undo()
        sh = a.shifts()
        return r[1] == {"undone": "person.delete"} and a.people()["Kim"]["id"] == P["Kim"] \
            and all(P["Kim"] in sh[S[k]]["assigned"] for k in ("P4", "F1", "F3", "F4"))
    c.run("API: undo of person.delete brings the person and their assignments back", undo_delete)

    # ---- audit
    def audit():
        s, log = a.get("/api/audit")
        return s == 200 and [e["action"] for e in log] == st["acts"] and [e["seq"] for e in log] == list(range(1, len(log) + 1)) \
            and all("detail" in e for e in log)
    c.run("API: audit has one entry per action and per undo, oldest first, seq from 1", audit)

    # last action before the restart: its undo must still work afterwards
    safely(lambda: a.unassign("A0", "Bob"))
    st["before"] = {}
    safely(lambda: st["before"].update(people=a.get("/api/people")[1], shifts=a.get("/api/shifts?per_page=100")[1],
                                       audit=a.get("/api/audit")[1]))


def restart_checks(c, app, st):
    a = Api(app.base, st)
    before = st.get("before", {})
    app.stop()
    up = app.start()
    c.run("restart: people, shifts and assignments survive a restart",
          lambda: up and a.get("/api/people")[1] == before["people"] and a.get("/api/shifts?per_page=100")[1] == before["shifts"])

    def versions_audit():
        ppl = a.people()
        return up and ppl["Bob"]["version"] == 3 and ppl["Ana"]["version"] == 2 and a.get("/api/audit")[1] == before["audit"]
    c.run("restart: versions and the audit log survive a restart", versions_audit)

    def undo_history():
        r = a.undo()
        return up and r[1] == {"undone": "unassign"} and a.on("A0") == a.ids("Bob")
    c.run("restart: undo history survives (undo after a restart reverts the last action, an unassign)", undo_history)
    return up


def limit_checks(c, base, st):
    """21 actions of every kind, then 21 undos: the newest 20 come back in reverse, the 21st is out of reach."""
    a = Api(base, st)
    P, S = st["P"], st["S"]
    res = {}

    def run():
        res["people"], res["shifts"] = a.get("/api/people")[1], a.get("/api/shifts?per_page=100")[1]["items"]
        z0 = a.shift("Z0", "2026-03-31", "08:00", "16:00", "porter", 1)[1]
        res["z0"] = z0
        a.person("Zed", "nurse", 40, [])
        a.shift("Z1", "2026-03-30", "08:00", "16:00", "nurse", 2)
        a.assign("Z1", "Zed")
        a.unassign("Z1", "Zed")
        a.assign("Z1", "Zed")
        a.put("Zed", {"name": "Zed", "role": "nurse", "max_hours": 30, "unavailable": []}, 1)
        a.import_csv("name,role,max_hours,unavailable\nYan,porter,20,\n")
        a.did("autofill", a.post("/api/autofill", {"from": "2026-03-30", "to": "2026-03-30"}), 200)
        P["Yan"] = a.people()["Yan"]["id"]
        a.did("person.delete", call(base, "DELETE", f"/api/people/{P['Yan']}"), 204)
        for h in range(11):
            a.shift(f"Z{h + 2}", "2026-04-01", f"{h:02d}:00", f"{h + 2:02d}:00", "porter", 1)
        res["undone"] = [a.undo()[1] for _ in range(20)]
        res["last"] = a.undo()

    safely(run)
    want = ["shift.create"] * 11 + ["person.delete", "autofill", "person.import", "person.update", "assign", "unassign",
                                    "assign", "shift.create", "person.create"]
    c.run("API: undo reverts the newest action first, across all 8 action kinds (20 undos name their actions)",
          lambda: res["undone"] == [{"undone": k} for k in want])
    c.run("API: undo reaches only the last 20 actions (the 21st undo is 409 nothing_to_undo)",
          lambda: refused(res["last"], "nothing_to_undo"))

    def state():
        now, z0 = a.get("/api/shifts?per_page=100")[1]["items"], res["z0"]["id"]
        return a.get("/api/people")[1] == res["people"] and [s for s in now if s["id"] != z0] == res["shifts"] \
            and len(now) == len(res["shifts"]) + 1
    c.run("API: after the undos, people and shifts are as before (only the out-of-reach shift.create stays)", state)


def nums(text):
    return {float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)}


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

    def api_people():
        return {p["name"]: p for p in call(base, "GET", "/api/people")[1]}

    def api_shifts():
        return call(base, "GET", "/api/shifts?per_page=100")[1]

    def shift_at(date, start):
        return next(s for s in api_shifts()["items"] if s["date"] == date and s["start"] == start)

    ids = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        tid = page.get_by_test_id

        def card(date, start, end):
            return tid("shift-card").filter(has_text=date).filter(has_text=start).filter(has_text=end)

        def names(cd):
            return [n.strip() for n in cd.get_by_test_id("assigned-name").all_inner_texts()]

        def hours(name):
            return nums(tid(f"hours-{name}").inner_text())

        def set_week(d):
            w = tid("week-start")
            w.fill(d)
            w.dispatch_event("change")

        def loaded():
            page.goto(base + "/", wait_until="domcontentloaded")
            want = ["person-name", "person-role", "person-max", "add-person", "shift-date", "shift-start", "shift-end",
                    "shift-role", "shift-slots", "add-shift", "week-start", "autofill-button", "undo-button"] + \
                   [f"person-unavailable-{d}" for d in DAYS]
            return until(lambda: all(tid(t).count() == 1 for t in want)) and not any(
                tid(f"person-unavailable-{d}").is_checked() for d in DAYS)
        c.run("UI: page shows the person form (7 unchecked day boxes), shift form and week controls", loaded)

        def add_person(name, role, mx, off=()):
            n = tid("person-row").count()
            tid("person-name").fill(name)
            tid("person-role").select_option(role)
            tid("person-max").fill(str(mx))
            for d in DAYS:
                box = tid(f"person-unavailable-{d}")
                if box.is_checked() != (d in off):
                    box.click()
            tid("add-person").click()
            return until(lambda: tid("person-row").count() == n + 1)

        def people():
            ok = add_person("Uma", "nurse", 40) and add_person("Vic", "nurse", 12, ("sat",)) and add_person("Wes", "doctor", 40)
            rows = tid("person-row").all_inner_texts()
            ppl = api_people()
            ids.update({n: ppl[n]["id"] for n in ("Uma", "Vic", "Wes")})
            return ok and all(any(n in r and role in r for r in rows) for n, role in (("Uma", "nurse"), ("Vic", "nurse"), ("Wes", "doctor"))) \
                and ppl["Vic"]["unavailable"] == ["sat"] and ppl["Vic"]["max_hours"] == 12 and ppl["Uma"]["unavailable"] == [] \
                and ppl["Wes"]["role"] == "doctor"
        c.run("UI: add people through the form (person-row shows name and role; a day box sets unavailable)", people)

        def add_shift(date, start, end, role, slots):
            n = api_shifts()["total"]
            tid("shift-date").fill(date)
            tid("shift-start").fill(start)
            tid("shift-end").fill(end)
            tid("shift-role").select_option(role)
            tid("shift-slots").fill(str(slots))
            tid("add-shift").click()
            return until(lambda: api_shifts()["total"] == n + 1)

        U = [("2026-03-03", "07:00", "15:00", "nurse", 2), ("2026-03-02", "22:00", "06:00", "nurse", 1),
             ("2026-03-10", "08:00", "16:00", "nurse", 1), ("2026-03-03", "10:00", "14:00", "nurse", 1)]

        def shifts():
            ok = all([add_shift(*u) for u in U])
            got = {(s["date"], s["start"], s["end"], s["role"], s["slots"]): s["hours"] for s in api_shifts()["items"]}
            return ok and got == {U[0]: 8, U[1]: 8, U[2]: 8, U[3]: 4}
        c.run("UI: add shifts through the form (incl. an overnight 22:00-06:00)", shifts)

        def week_view():
            set_week("2026-03-04")

            def shown():
                t = tid("shift-card").all_inner_texts()
                return len(t) == 3 and all(x in t[0] for x in ("2026-03-02", "22:00", "06:00")) \
                    and all(x in t[1] for x in ("2026-03-03", "07:00", "15:00")) \
                    and all(x in t[2] for x in ("2026-03-03", "10:00", "14:00"))
            return until(shown)
        c.run("UI: week-start shows the Monday-to-Sunday week containing that date, cards in shift order", week_view)

        def assign():
            cd = card("2026-03-03", "07:00", "15:00")
            cd.get_by_test_id("assign-select").select_option(value=str(ids["Uma"]))
            cd.get_by_test_id("assign-button").click()
            return until(lambda: names(cd) == ["Uma"] and 8 in hours("Uma"))
        c.run("UI: assign through a shift card shows assigned-name and updates hours-<name>", assign)

        def refused_ui():
            cd = card("2026-03-03", "10:00", "14:00")
            cd.get_by_test_id("assign-select").select_option(value=str(ids["Uma"]))
            cd.get_by_test_id("assign-button").click()
            return until(lambda: tid("error").is_visible() and "overlap" in tid("error").inner_text()) \
                and names(cd) == [] and shift_at("2026-03-03", "10:00")["assigned"] == []
        c.run("UI: a refused assignment shows error containing the rule code (overlap)", refused_ui)

        def autofill():
            tid("autofill-button").click()
            # by hand: Mon 22:00-06:00 -> Vic (Uma has under 10h rest before Tue 07:00); the Tue shifts stay open
            ok = until(lambda: names(card("2026-03-02", "22:00", "06:00")) == ["Vic"] and 8 in hours("Vic"))
            return ok and shift_at("2026-03-02", "22:00")["assigned"] == [ids["Vic"]] \
                and shift_at("2026-03-03", "07:00")["assigned"] == [ids["Uma"]] \
                and shift_at("2026-03-03", "10:00")["assigned"] == [] and shift_at("2026-03-10", "08:00")["assigned"] == []
        c.run("UI: autofill-button fills the shown week only", autofill)

        def undo():
            tid("undo-button").click()
            ok = until(lambda: names(card("2026-03-02", "22:00", "06:00")) == [] and 0 in hours("Vic") and 8 not in hours("Vic"))
            return ok and shift_at("2026-03-02", "22:00")["assigned"] == []
        c.run("UI: undo-button reverts the last action (the auto-fill)", undo)

        def next_week():
            set_week("2026-03-10")
            return until(lambda: tid("shift-card").count() == 1 and "2026-03-10" in tid("shift-card").first.inner_text()
                         and 0 in hours("Uma") and 8 not in hours("Uma"))
        c.run("UI: changing week-start shows that week; hours-<name> follow the shown week", next_week)

        def half():
            ok = add_shift("2026-03-11", "08:00", "15:30", "nurse", 1) and until(lambda: tid("shift-card").count() == 2)
            cd = card("2026-03-11", "08:00", "15:30")
            cd.get_by_test_id("assign-select").select_option(value=str(ids["Uma"]))
            cd.get_by_test_id("assign-button").click()
            return ok and until(lambda: names(cd) == ["Uma"] and 7.5 in hours("Uma"))
        c.run("UI: hours-<name> shows half hours (7.5)", half)
        browser.close()


def main():
    cfg, g, out = args()
    start = out / "START.txt"
    if not start.exists():
        emit(False, 0, {"summary": "no START.txt: the app cannot be started"})
        return
    cmd = next((l.strip() for l in start.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()), "")
    folder = Folder(out)
    app = App(out, cmd, g.get("start_timeout", 90))
    c, st = Checks(), {}
    try:
        if not app.start():
            emit(False, 0, {"summary": f"app did not start with `{cmd[:80]}`", "log_tail": app.tail()})
            return
        api_checks(c, app.base, st)
        restart_checks(c, app, st)
        limit_checks(c, app.base, st)
        app.stop()
        folder.restore()                                     # the UI walk starts from the store as handed in
        try:
            if not app.start():
                raise RuntimeError("app did not start again on a fresh store")
            ui_checks(c, app.base)
        except Exception as e:                               # the walk itself crashed: unreached checks fail
            done = sum(k.startswith("UI:") for k in c.results)
            for i in range(done, UI_CHECKS):
                c.results[f"UI: check {i + 1} not reached"] = f"FAIL (walk crashed: {type(e).__name__}: {str(e)[:100]})"
    finally:
        app.stop()
        folder.restore()
    n = len(c.results)
    passed = sum(v == "ok" for v in c.results.values())
    failed = [k for k, v in c.results.items() if v != "ok"]
    ok = n > 0 and passed / n >= g.get("threshold", 0.9)
    emit(ok, round(passed / n, 3) if n else 0,
         {"summary": f"{passed} of {n} checks ok" + (f"; failed: {', '.join(failed)}" if failed else ""),
          "checks": c.results})


if __name__ == "__main__":
    main()
