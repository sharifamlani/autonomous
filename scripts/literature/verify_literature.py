"""Verify the literature/ library: inventory, relative links, and stale folder references.

  --inventory OUT.json   write {md5: relative path} for every PDF (run before and after a reorg)
  --compare A.json B.json  same md5 set and count in both inventories?
  --links                every relative markdown link / ../ path in literature/ resolves
  --stale                no reference to a pre-reorg folder name or to 000_Foundations remains
  --titles               each NN_<name>/README.md H1 starts with "# NN " (catches stale folder numbers)
  --all                  links + stale + titles

Exit code 0 when every requested check passes, 1 otherwise.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LIT = REPO / "literature"
MAP = Path(__file__).with_name("reorg_map.tsv")
SCAN = [LIT]
EXTRA = [REPO / "public" / "_README.md"]


def text_files():
    for root in SCAN:
        for f in root.rglob("*"):
            if f.is_file() and f.suffix.lower() in {".md", ".csv", ".tsv", ".py"} and "_tools" not in f.parts:
                yield f
    yield from (f for f in EXTRA if f.exists())


def inventory(out):
    inv = {}
    for f in LIT.rglob("*.pdf"):
        inv.setdefault(hashlib.md5(f.read_bytes()).hexdigest(), []).append(str(f.relative_to(LIT)))
    Path(out).write_text(json.dumps(inv, indent=0), encoding="utf-8")
    n = sum(len(v) for v in inv.values())
    print(f"inventory: {n} PDFs, {len(inv)} unique md5 -> {out}")
    return True


def compare(a, b):
    A, B = (json.loads(Path(x).read_text(encoding="utf-8")) for x in (a, b))
    na, nb = sum(map(len, A.values())), sum(map(len, B.values()))
    ok = set(A) == set(B) and na == nb
    print(f"compare: {na} vs {nb} PDFs, md5 sets {'identical' if set(A) == set(B) else 'DIFFER'}")
    return ok


LINK_RE = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
REL_RE = re.compile(r"(?<![\w/:.])((?:\.\./)+[^\s`)\]\"'|<>,;]+)")


def links():
    broken = []
    for f in text_files():
        if f.suffix != ".md":
            continue
        s = f.read_text(encoding="utf-8", errors="replace")
        targets = {t for t in LINK_RE.findall(s) if not re.match(r"[a-z]+:", t)} | set(REL_RE.findall(s))
        for t in targets:
            t = t.rstrip(".")
            if any(ch in t for ch in "*<{"):
                continue
            if not (f.parent / t).exists():
                broken.append(f"{f.relative_to(REPO)} -> {t}")
    for b in broken:
        print("  BROKEN", b)
    print(f"links: {len(broken)} broken relative links")
    return not broken


def stale():
    rows = list(csv.DictReader(open(MAP, encoding="utf-8"), delimiter="\t"))
    old_names = {r["old_path"].split("/")[-1] for r in rows} - {r["new_path"] for r in rows}
    pat = re.compile(r"000_Foundations|(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, old_names)) + r")(?![A-Za-z0-9_])")
    hits = []
    for f in text_files():
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if pat.search(line) and "the former `" not in line:   # provenance notes name old folders on purpose
                hits.append(f"{f.relative_to(REPO)}:{i}: {line.strip()[:140]}")
    for h in hits:
        print("  STALE", h)
    print(f"stale: {len(hits)} lines reference pre-reorg folders")
    return not hits


def titles():
    bad = []
    for d in sorted(p for p in LIT.iterdir() if p.is_dir() and p.name[:2].isdigit()):
        readme = d / "README.md"
        first = readme.read_text(encoding="utf-8").splitlines()[0] if readme.exists() else ""
        if not first.startswith(f"# {d.name[:2]}"):
            bad.append(f"{d.name}: {first or '(no README)'}")
    for b in bad:
        print("  TITLE", b)
    print(f"titles: {len(bad)} README titles do not match their folder number")
    return not bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory")
    ap.add_argument("--compare", nargs=2)
    ap.add_argument("--links", action="store_true")
    ap.add_argument("--stale", action="store_true")
    ap.add_argument("--titles", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    ok = True
    if a.inventory:
        ok &= inventory(a.inventory)
    if a.compare:
        ok &= compare(*a.compare)
    if a.links or a.all:
        ok &= links()
    if a.stale or a.all:
        ok &= stale()
    if a.titles or a.all:
        ok &= titles()
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
