"""Rota: the reference build of benchmark task A4 (Python standard library only).

The known-good answer for the A4 grader's calibration (L11). Every rule is task.md's, in its order.
Run: PORT=8000 python server.py   (data in rota.json beside this file)
"""
import copy
import csv
import datetime as dt
import io
import json
import os
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
DATA = HERE / "rota.json"
LOCK = threading.Lock()
ROLES = ("nurse", "doctor", "porter")
DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
UNDO_LIMIT = 20
REST_MIN = 10 * 60
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME = re.compile(r"^(\d{2}):(\d{2})$")


class Bad(Exception):
    def __init__(self, status, msg, rule=None):
        super().__init__(msg)
        self.status, self.rule = status, rule


# ---------------------------------------------------------------- storage
def fresh():
    return {"people": [], "shifts": [], "next_person": 1, "next_shift": 1, "audit": [], "undo": []}


def load():
    return json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else fresh()


def save():
    tmp = DATA.with_suffix(".tmp")
    tmp.write_text(json.dumps(DB), encoding="utf-8")
    os.replace(tmp, DATA)


DB = load()


def record(kind, detail, before, person_id=None):
    """One action: an audit entry plus an undo entry holding the state before it (last 20 kept)."""
    DB["audit"].append({"seq": len(DB["audit"]) + 1, "action": kind, "detail": detail})
    DB["undo"].append({"action": kind, "people": before[0], "shifts": before[1], "person_id": person_id})
    DB["undo"] = DB["undo"][-UNDO_LIMIT:]
    save()


def snapshot():
    return copy.deepcopy(DB["people"]), copy.deepcopy(DB["shifts"])


def undo():
    if not DB["undo"]:
        raise Bad(409, "nothing to undo", "nothing_to_undo")
    u = DB["undo"].pop()
    if u["action"] == "person.update":                      # old fields come back, the version moves on
        now = next(p["version"] for p in DB["people"] if p["id"] == u["person_id"])
        for p in u["people"]:
            if p["id"] == u["person_id"]:
                p["version"] = now + 1
    DB["people"], DB["shifts"] = u["people"], u["shifts"]
    DB["audit"].append({"seq": len(DB["audit"]) + 1, "action": "undo", "detail": f"undid {u['action']}"})
    save()
    return {"undone": u["action"]}


# ---------------------------------------------------------------- people
def whole(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return None


def clean_person(body, exclude=None):
    name = body.get("name")
    if not isinstance(name, str) or not name.strip():
        raise Bad(400, "name is required")
    name = name.strip()
    if any(p["name"].lower() == name.lower() and p["id"] != exclude for p in DB["people"]):
        raise Bad(400, f"name {name} is already used")
    role = body.get("role")
    if role not in ROLES:
        raise Bad(400, "role must be nurse, doctor or porter")
    mh = whole(body.get("max_hours"))
    if mh is None or not 1 <= mh <= 60:
        raise Bad(400, "max_hours must be a whole number from 1 to 60")
    un = body.get("unavailable")
    un = [] if un is None else un
    if not isinstance(un, list) or any(d not in DAYS for d in un):
        raise Bad(400, "unavailable must be a list of day codes mon..sun")
    return {"name": name, "role": role, "max_hours": mh, "unavailable": [d for d in DAYS if d in un]}


def person(pid):
    for p in DB["people"]:
        if str(p["id"]) == str(pid):
            return p
    raise Bad(404, "person not found")


def add_person(fields):
    p = {"id": DB["next_person"], **fields, "version": 1}
    DB["next_person"] += 1
    DB["people"].append(p)
    return p


def import_csv(text):
    rows = csv.reader(io.StringIO(text))
    header = next(rows, None)
    cols = [h.strip().lower() for h in header or []]
    if not {"name", "role", "max_hours"} <= set(cols):
        raise Bad(400, "the CSV header must be name,role,max_hours,unavailable")
    created, errors = 0, []
    for row in rows:
        line = rows.line_num
        if not row or all(not c.strip() for c in row):
            continue
        if len(row) > len(cols):
            errors.append({"line": line, "error": f"expected {len(cols)} columns"})
            continue
        rec = dict(zip(cols, row + [""] * (len(cols) - len(row))))
        mh = rec["max_hours"].strip()
        un = [d.strip() for d in rec.get("unavailable", "").split(";") if d.strip()]
        try:
            fields = clean_person({"name": rec["name"], "role": rec["role"].strip(),
                                   "max_hours": int(mh) if mh.isdigit() else mh, "unavailable": un})
        except Bad as b:
            errors.append({"line": line, "error": str(b)})
            continue
        add_person(fields)
        created += 1
    return {"created": created, "errors": errors}


# ---------------------------------------------------------------- shifts
def minutes(t):
    m = TIME.match(t) if isinstance(t, str) else None
    if not m or int(m[1]) > 23 or m[2] not in ("00", "30"):
        raise Bad(400, "times must be HH:MM on the hour or half hour")
    return int(m[1]) * 60 + int(m[2])


def day(s, what="date"):
    if not isinstance(s, str) or not DATE.match(s):
        raise Bad(400, f"{what} must be YYYY-MM-DD")
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        raise Bad(400, f"{what} is not a real date")


def length(start, end):
    m = minutes(end) - minutes(start)
    return m + 1440 if m <= 0 else m                       # end not after start: ends the next day


def span(s):
    """(start, end) in minutes on one absolute clock."""
    a = dt.date.fromisoformat(s["date"]).toordinal() * 1440 + minutes(s["start"])
    return a, a + length(s["start"], s["end"])


def week(s):
    d = dt.date.fromisoformat(s["date"])
    return d - dt.timedelta(days=d.weekday())


def num(mins):
    h = mins / 60
    return int(h) if h.is_integer() else h


def shift_out(s):
    return {"id": s["id"], "date": s["date"], "start": s["start"], "end": s["end"], "role": s["role"],
            "slots": s["slots"], "hours": num(length(s["start"], s["end"])), "assigned": list(s["assigned"])}


def add_shift(body):
    day(body.get("date"))
    mins = length(body.get("start"), body.get("end"))
    if not 60 <= mins <= 720:
        raise Bad(400, "a shift lasts from 1 to 12 hours")
    if body.get("role") not in ROLES:
        raise Bad(400, "role must be nurse, doctor or porter")
    slots = whole(body.get("slots"))
    if slots is None or not 1 <= slots <= 5:
        raise Bad(400, "slots must be a whole number from 1 to 5")
    s = {"id": DB["next_shift"], "date": body["date"], "start": body["start"], "end": body["end"],
         "role": body["role"], "slots": slots, "assigned": []}
    DB["next_shift"] += 1
    DB["shifts"].append(s)
    return s


def shift(sid):
    for s in DB["shifts"]:
        if str(s["id"]) == str(sid):
            return s
    raise Bad(404, "shift not found")


def ordered(shifts):
    return sorted(shifts, key=lambda s: (s["date"], s["start"], s["id"]))


def in_range(q):
    lo = day(q["from"], "from") if q.get("from") else None
    hi = day(q["to"], "to") if q.get("to") else None
    role = q.get("role")
    if role and role not in ROLES:
        raise Bad(400, "role must be nurse, doctor or porter")
    out = []
    for s in DB["shifts"]:
        d = dt.date.fromisoformat(s["date"])
        if (lo is None or d >= lo) and (hi is None or d <= hi) and (not role or s["role"] == role):
            out.append(s)
    return ordered(out)


def week_minutes(p, wk):
    return sum(length(o["start"], o["end"]) for o in DB["shifts"] if p["id"] in o["assigned"] and week(o) == wk)


def broken(s, p):
    """The first of the 7 rules this assignment breaks, as (code, message), or None."""
    if p["role"] != s["role"]:
        return "role", f"{p['name']} is a {p['role']}, this shift needs a {s['role']}"
    if len(s["assigned"]) >= s["slots"]:
        return "full", "every slot is already taken"
    if p["id"] in s["assigned"]:
        return "duplicate", f"{p['name']} is already on this shift"
    if DAYS[dt.date.fromisoformat(s["date"]).weekday()] in p["unavailable"]:
        return "unavailable", f"{p['name']} is unavailable on that day"
    a, b = span(s)
    mine = [o for o in DB["shifts"] if p["id"] in o["assigned"] and o["id"] != s["id"]]
    for o in mine:
        c, d = span(o)
        if a < d and c < b:
            return "overlap", f"{p['name']} is on an overlapping shift"
    for o in mine:                                          # an overlap also leaves under 10h (rule order decides)
        c, d = span(o)
        gap = a - d if c <= a else c - b                    # end of the earlier shift to start of the later one
        if gap < REST_MIN:
            return "rest", f"{p['name']} would have under 10 hours of rest"
    if week_minutes(p, week(s)) + (b - a) > p["max_hours"] * 60:
        return "hours", f"{p['name']} would exceed {p['max_hours']} hours that week"
    return None


def autofill(body):
    lo, hi = day(body.get("from"), "from"), day(body.get("to"), "to")
    assigned, unfilled = [], []
    for s in ordered(DB["shifts"]):
        if not lo <= dt.date.fromisoformat(s["date"]) <= hi:
            continue
        while len(s["assigned"]) < s["slots"]:
            ok = [p for p in DB["people"] if broken(s, p) is None]
            if not ok:
                unfilled.append({"shift_id": s["id"], "open": s["slots"] - len(s["assigned"])})
                break
            pick = min(ok, key=lambda p: (week_minutes(p, week(s)), p["name"].lower()))
            s["assigned"].append(pick["id"])
            assigned.append({"shift_id": s["id"], "person_id": pick["id"]})
    return {"assigned": assigned, "unfilled": unfilled}


def export(q):
    names = {p["id"]: p["name"] for p in DB["people"]}
    lines = ["date,start,end,role,person"]
    for s in in_range(q):
        row = f"{s['date']},{s['start']},{s['end']},{s['role']},"
        for n in sorted((names[i] for i in s["assigned"]), key=str.lower):
            lines.append(row + n)
        lines += [row + "OPEN"] * (s["slots"] - len(s["assigned"]))
    return "".join(l + "\n" for l in lines)


# ---------------------------------------------------------------- HTTP
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, status, body=None, ctype="application/json"):
        data = b"" if body is None else (body if isinstance(body, bytes) else json.dumps(body).encode())
        self.send_response(status)
        if body is not None:
            self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def raw(self):
        return self.rfile.read(int(self.headers.get("Content-Length") or 0))

    def body(self):
        try:
            b = json.loads(self.raw() or b"{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise Bad(400, "body must be JSON")
        if not isinstance(b, dict):
            raise Bad(400, "body must be a JSON object")
        return b

    def route(self, method):
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        q = {k: v[-1] for k, v in parse_qs(url.query).items()}
        if method == "GET" and not parts:
            return self.send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        if parts[:1] != ["api"]:
            raise Bad(404, "not found")
        r = parts[1:]
        if r == ["people"] and method == "GET":
            return self.send(200, sorted(DB["people"], key=lambda p: (p["name"].lower(), p["id"])))
        if r == ["people"] and method == "POST":
            fields = clean_person(self.body())
            before = snapshot()
            p = add_person(fields)
            record("person.create", f"created {p['name']} (id {p['id']})", before)
            return self.send(201, p)
        if r == ["people", "import"] and method == "POST":
            before = snapshot()
            out = import_csv(self.raw().decode("utf-8-sig", "replace"))
            record("person.import", f"imported {out['created']} people, {len(out['errors'])} rows refused", before)
            return self.send(200, out)
        if len(r) == 2 and r[0] == "people" and method == "PUT":
            p = person(r[1])
            tag = self.headers.get("If-Match")
            if tag is None or not tag.strip():
                raise Bad(428, "If-Match: <version> is required")
            tag = tag.strip().removeprefix("W/").strip('"')
            if tag != str(p["version"]):
                raise Bad(409, f"version {tag} is not the current version {p['version']}")
            fields = clean_person(self.body(), exclude=p["id"])
            before = snapshot()
            p.update(fields, version=p["version"] + 1)
            record("person.update", f"updated {p['name']} (id {p['id']}) to version {p['version']}", before, p["id"])
            return self.send(200, p)
        if len(r) == 2 and r[0] == "people" and method == "DELETE":
            p = person(r[1])
            before = snapshot()
            DB["people"].remove(p)
            for s in DB["shifts"]:
                s["assigned"] = [i for i in s["assigned"] if i != p["id"]]
            record("person.delete", f"deleted {p['name']} (id {p['id']})", before)
            return self.send(204)
        if r == ["shifts"] and method == "POST":
            body = self.body()
            before = snapshot()
            s = add_shift(body)
            record("shift.create", f"created shift {s['id']} {s['date']} {s['start']}-{s['end']} {s['role']}", before)
            return self.send(201, shift_out(s))
        if r == ["shifts"] and method == "GET":
            items = in_range(q)
            try:
                page, per = int(q.get("page", 1)), int(q.get("per_page", 20))
            except ValueError:
                raise Bad(400, "page and per_page must be whole numbers")
            if page < 1 or per < 1:
                raise Bad(400, "page and per_page start at 1")
            per = min(per, 100)
            chunk = items[(page - 1) * per: page * per]
            return self.send(200, {"items": [shift_out(s) for s in chunk], "page": page, "per_page": per,
                                   "total": len(items)})
        if len(r) == 3 and r[0] == "shifts" and r[2] == "assign" and method == "POST":
            s = shift(r[1])
            body = self.body()
            if body.get("person_id") is None:
                raise Bad(400, "person_id is required")
            p = person(body["person_id"])
            why = broken(s, p)
            if why:
                raise Bad(409, why[1], why[0])
            before = snapshot()
            s["assigned"].append(p["id"])
            record("assign", f"assigned {p['name']} to shift {s['id']}", before)
            return self.send(200, shift_out(s))
        if len(r) == 4 and r[0] == "shifts" and r[2] == "assign" and method == "DELETE":
            s = shift(r[1])
            p = person(r[3])
            if p["id"] not in s["assigned"]:
                raise Bad(404, f"{p['name']} is not on shift {s['id']}")
            before = snapshot()
            s["assigned"].remove(p["id"])
            record("unassign", f"removed {p['name']} from shift {s['id']}", before)
            return self.send(204)
        if r == ["autofill"] and method == "POST":
            body = self.body()
            before = snapshot()
            out = autofill(body)
            record("autofill", f"filled {len(out['assigned'])} slots, {len(out['unfilled'])} shifts left open", before)
            return self.send(200, out)
        if r == ["undo"] and method == "POST":
            return self.send(200, undo())
        if r == ["audit"] and method == "GET":
            return self.send(200, DB["audit"])
        if r == ["export.csv"] and method == "GET":
            return self.send(200, export(q).encode(), "text/csv; charset=utf-8")
        raise Bad(404, "not found")

    def handle_any(self, method):
        try:
            with LOCK:
                self.route(method)
        except Bad as b:
            self.send(b.status, {"error": str(b)} | ({"rule": b.rule} if b.rule else {}))

    def do_GET(self):
        self.handle_any("GET")

    def do_POST(self):
        self.handle_any("POST")

    def do_PUT(self):
        self.handle_any("PUT")

    def do_DELETE(self):
        self.handle_any("DELETE")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
