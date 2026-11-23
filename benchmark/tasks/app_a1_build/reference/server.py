"""Split: the reference build of benchmark task A1 (Python standard library only).

The known-good answer for the A1 grader's calibration (L11) and the clean app A2 plants its bugs into.
Run: PORT=8000 python server.py   (data in data.json beside this file)
"""
import json
import os
import re
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data.json"
LOCK = threading.Lock()
AMOUNT = re.compile(r"^\d+(\.\d{1,2})?$")


class Bad(Exception):
    def __init__(self, status, msg):
        super().__init__(msg)
        self.status = status


def load():
    return json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {"groups": {}}


def save(db):
    tmp = DATA.with_suffix(".tmp")
    tmp.write_text(json.dumps(db, indent=1), encoding="utf-8")
    os.replace(tmp, DATA)


def money(cents):
    sign = "-" if cents < 0 else ""
    return f"{sign}{abs(cents) // 100}.{abs(cents) % 100:02d}"


def to_cents(value):
    s = str(value).strip() if not isinstance(value, bool) else ""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        s = repr(value) if isinstance(value, float) else str(value)   # shortest exact form: 1.230001 stays 1.230001
    if not AMOUNT.match(s):
        raise Bad(400, "amount must be a positive number with at most 2 decimals")
    whole, _, frac = s.partition(".")
    cents = int(whole) * 100 + int((frac + "00")[:2])
    if cents <= 0:
        raise Bad(400, "amount must be positive")
    return cents


def shares(cents, split, members):
    order = [m for m in members if m in split]
    base, extra = divmod(cents, len(order))
    return {m: base + (1 if i < extra else 0) for i, m in enumerate(order)}


def balances(group):
    bal = {m: 0 for m in group["members"]}
    for e in group["expenses"]:
        bal[e["paid_by"]] += e["cents"]
        for m, c in e["shares"].items():
            bal[m] -= c
    return bal


def settle(group):
    bal = balances(group)
    order = group["members"]
    out = []
    while any(bal.values()):
        debtor = min(order, key=lambda m: (bal[m], order.index(m)))
        creditor = max(order, key=lambda m: (bal[m], -order.index(m)))
        pay = min(-bal[debtor], bal[creditor])
        bal[debtor] += pay
        bal[creditor] -= pay
        out.append({"from": debtor, "to": creditor, "amount": money(pay)})
    return out


def expense_out(e):
    return {"id": e["id"], "description": e["description"], "amount": money(e["cents"]), "paid_by": e["paid_by"],
            "split_among": e["split_among"], "shares": {m: money(c) for m, c in e["shares"].items()}}


def group_out(g):
    return {"id": g["id"], "name": g["name"], "members": g["members"]}


def create_group(db, body):
    name = str(body.get("name") or "").strip()
    members = body.get("members")
    if not name:
        raise Bad(400, "group name is required")
    if not isinstance(members, list) or len(members) < 2:
        raise Bad(400, "a group needs at least 2 members")
    members = [str(m).strip() for m in members]
    if any(not m for m in members):
        raise Bad(400, "member names cannot be empty")
    if len({m.lower() for m in members}) != len(members):
        raise Bad(400, "member names must be unique")
    gid = uuid.uuid4().hex[:8]
    db["groups"][gid] = {"id": gid, "name": name, "members": members, "expenses": []}
    return db["groups"][gid]


def add_expense(group, body):
    desc = str(body.get("description") or "").strip()
    if not desc:
        raise Bad(400, "description is required")
    cents = to_cents(body.get("amount", ""))
    paid_by = body.get("paid_by")
    if paid_by not in group["members"]:
        raise Bad(400, "paid_by must be a member")
    split = body.get("split_among", group["members"])
    if not isinstance(split, list) or not split:
        raise Bad(400, "split_among must list at least one member")
    if any(m not in group["members"] for m in split):
        raise Bad(400, "split_among has a name that is not a member")
    split = [m for m in group["members"] if m in split]
    e = {"id": uuid.uuid4().hex[:8], "description": desc, "cents": cents, "paid_by": paid_by,
         "split_among": split, "shares": shares(cents, split, group["members"])}
    group["expenses"].append(e)
    return e


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

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            b = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            raise Bad(400, "body must be JSON")
        if not isinstance(b, dict):
            raise Bad(400, "body must be a JSON object")
        return b

    def route(self, method):
        parts = [p for p in self.path.split("?")[0].split("/") if p]
        if method == "GET" and not parts:
            return self.send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        if parts[:2] != ["api", "groups"]:
            raise Bad(404, "not found")
        with LOCK:
            db = load()
            if len(parts) == 2 and method == "POST":
                g = create_group(db, self.body())
                save(db)
                return self.send(201, group_out(g))
            if len(parts) < 3 or parts[2] not in db["groups"]:
                raise Bad(404, "group not found")
            g = db["groups"][parts[2]]
            rest = parts[3:]
            if not rest and method == "GET":
                return self.send(200, group_out(g))
            if rest == ["expenses"] and method == "GET":
                return self.send(200, [expense_out(e) for e in g["expenses"]])
            if rest == ["expenses"] and method == "POST":
                e = add_expense(g, self.body())
                save(db)
                return self.send(201, expense_out(e))
            if len(rest) == 2 and rest[0] == "expenses" and method == "DELETE":
                keep = [e for e in g["expenses"] if e["id"] != rest[1]]
                if len(keep) == len(g["expenses"]):
                    raise Bad(404, "expense not found")
                g["expenses"] = keep
                save(db)
                return self.send(204)
            if rest == ["balances"] and method == "GET":
                return self.send(200, {m: money(c) for m, c in balances(g).items()})
            if rest == ["settle"] and method == "GET":
                return self.send(200, settle(g))
        raise Bad(404, "not found")

    def handle_any(self, method):
        try:
            self.route(method)
        except Bad as b:
            self.send(b.status, {"error": str(b)})

    def do_GET(self):
        self.handle_any("GET")

    def do_POST(self):
        self.handle_any("POST")

    def do_DELETE(self):
        self.handle_any("DELETE")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
