"""Tests for Split, written from the spec. Run them with pytest while the app is running (they read PORT)."""
import json
import os
import urllib.error
import urllib.request

BASE = f"http://127.0.0.1:{os.environ.get('PORT', '8000')}"


def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            return r.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, json.loads(raw) if raw else None


def group(members=("Ana", "Ben", "Cy")):
    s, g = call("POST", "/api/groups", {"name": "Trip", "members": list(members)})
    assert s == 201
    return g["id"]


def test_create_group_keeps_member_order():
    gid = group(("Cy", "Ana", "Ben"))
    s, g = call("GET", f"/api/groups/{gid}")
    assert s == 200 and g["members"] == ["Cy", "Ana", "Ben"]


def test_leftover_cent():
    gid = group()
    s, e = call("POST", f"/api/groups/{gid}/expenses", {"description": "Dinner", "amount": "100.00", "paid_by": "Ana"})
    assert s == 201
    assert e["shares"] == {"Ana": "33.33", "Ben": "33.33", "Cy": "33.34"}


def test_balances_sum_to_zero():
    gid = group()
    call("POST", f"/api/groups/{gid}/expenses", {"description": "Taxi", "amount": "20.01", "paid_by": "Ben"})
    s, b = call("GET", f"/api/groups/{gid}/balances")
    assert s == 200 and sum(round(float(v) * 100) for v in b.values()) == 0


def test_invalid_amount_is_400():
    gid = group()
    s, e = call("POST", f"/api/groups/{gid}/expenses", {"description": "Gum", "amount": "abc", "paid_by": "Ana"})
    assert s == 400 and "error" in e
