"""Verify the literature/ library: inventory, relative links, and stale folder references.

  --inventory OUT.json   write {md5: relative path} for every PDF (run before and after a reorg)
  --compare A.json B.json  same md5 set and count in both inventories?
  --links                every relative markdown link / ../ path in literature/ resolves
  --stale                no reference to a pre-reorg folder name or to 000_Foundations remains
  --titles               each NN_<name>/README.md H1 starts with "# NN " (catches stale folder numbers)
  --readmes              each NN_<name>/README.md: H1 is "# NN <Title>" matching the folder; has the four
                         sections Role, Contents, What it establishes, The catch
  --papers               papers.tsv: exact header, 10 fields per row, unique IDs, ID prefix matches folder,
                         4-digit year, verified is yes/no
  --files                each row's file: <ID>_<FirstAuthor>_<Year>_<Short_Title>.pdf (or _NOTE.md); a local
                         .pdf must start with %PDF; a missing PDF is only a warning (PDFs are local only)
  --candidates           public/_candidates/*.tsv: exact 8-column header, no short or empty fields
  --agent PATH           a scout agent prompt carries the whole output contract
  --root DIR             repo root to check (default: this repo); tests point it at fixture trees
  --all                  links + stale + titles + readmes + papers + files + candidates

Exit code 0 when every requested check passes, 1 otherwise.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
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
    if not MAP.exists():
        print(f"stale: skipped ({MAP.name} not found; this repo has had no folder reorg)")
        return True
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


# ---- Conventions from literature/README.md (the spec) ----------------------------------------------

SECTIONS = ["Role", "Contents", "What it establishes", "The catch"]
PAPER_COLS = ["id", "folder", "first_author", "year", "title", "venue", "url", "arxiv_or_doi", "file", "verified"]
PAPER_REQUIRED = ["id", "folder", "first_author", "year", "title", "url", "file", "verified"]
CAND_COLS = ["name", "url", "stars", "last_push", "license", "archived", "theme", "why"]
FILE_PATTERN = "<ID>_<FirstAuthor>_<Year>_<Short_Title>.pdf"
DEFAULT_PREFIX = {"01": "A", "02": "H", "03": "C", "04": "T", "05": "V", "06": "S", "07": "D", "08": "R", "09": "F"}
TREE_RE = re.compile(r"(\d\d)_[A-Za-z0-9_]+/\s+#\s+([A-Z])\s")
FILE_RE = re.compile(r"([A-Z]\d+)_([A-Za-z][A-Za-z-]*)_(\d{4})_([A-Za-z0-9][A-Za-z0-9_-]*?)(\.pdf|_NOTE\.md)")


def set_root(root):
    """Point every check at another repo root (the tests use fixture trees)."""
    global REPO, LIT, SCAN, EXTRA
    REPO = Path(root).resolve()
    LIT = REPO / "literature"
    SCAN = [LIT]
    EXTRA = [REPO / "public" / "_README.md"]


def report(tag, problems, warnings=()):
    for w in warnings:
        print("  WARN", w)
    for p in problems:
        print(f"  {tag}", p)
    return not problems


def prefix_map():
    """Folder number -> ID prefix, read from the literature/README.md tree; the documented default if absent."""
    idx = LIT / "README.md"
    found = dict(TREE_RE.findall(idx.read_text(encoding="utf-8", errors="replace"))) if idx.exists() else {}
    return found or dict(DEFAULT_PREFIX)


def theme_dirs():
    return sorted(p for p in LIT.iterdir() if p.is_dir() and p.name[:2].isdigit()) if LIT.exists() else []


def norm(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def ascii_fold(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()


def readmes():
    bad, dirs = [], theme_dirs()
    for d in dirs:
        readme = d / "README.md"
        if not readme.exists():
            bad.append(f"{d.name}: no README.md")
            continue
        lines = readme.read_text(encoding="utf-8", errors="replace").splitlines()
        first = lines[0].strip() if lines else ""
        nn, title = d.name[:2], d.name[3:].replace("_", " ")
        m = re.match(r"# (\d\d) (.+)$", first)
        if not m or m.group(1) != nn or norm(m.group(2)) != norm(title):
            bad.append(f"{d.name}/README.md: first line is {first!r}, expected '# {nn} {title}'")
        heads = {norm(re.sub(r"^#+\s*", "", ln)) for ln in lines if re.match(r"#{2,4}\s", ln)}
        for sec in SECTIONS:
            if norm(sec) not in heads:
                bad.append(f"{d.name}/README.md: missing section '{sec}'")
    ok = report("README", bad)
    print(f"readmes: {len(dirs)} folders, {len(bad)} problems")
    return ok


def read_papers():
    """(header, [(line_no, fields)]) from papers.tsv, or None when the file is absent."""
    path = LIT / "papers.tsv"
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t") if lines else []
    rows = [(i, ln.split("\t")) for i, ln in enumerate(lines[1:], 2) if ln.strip()]
    # Parallel scouts stage rows in literature/_incoming/NN_papers.tsv (merge_incoming.py folds them
    # in); check them as if they were already in papers.tsv, so duplicates across scouts show up.
    for inc in sorted((LIT / "_incoming").glob("*.tsv")):
        inc_lines = inc.read_text(encoding="utf-8").splitlines()
        tag = f"_incoming/{inc.name}"
        if not inc_lines or inc_lines[0].split("\t") != PAPER_COLS:
            rows.append((f"{tag}:1", ["(header is not the 10 papers.tsv columns)"]))
            continue
        rows += [(f"{tag}:{i}", ln.split("\t")) for i, ln in enumerate(inc_lines[1:], 2) if ln.strip()]
    return header, rows


def paper_rows():
    """Well-formed papers.tsv rows as (line_no, dict); malformed rows are papers()'s to report."""
    got = read_papers()
    return [(i, dict(zip(PAPER_COLS, (x.strip() for x in f)))) for i, f in (got[1] if got else [])
            if len(f) == len(PAPER_COLS)]


def papers():
    got = read_papers()
    if got is None:
        return report("PAPERS", ["literature/papers.tsv: file not found"])
    header, rows = got
    bad = []
    if header != PAPER_COLS:
        bad.append(f"papers.tsv:1: header is {header!r}, expected the 10 tab-separated columns {PAPER_COLS!r}")
    prefixes, seen = prefix_map(), {}
    for i, f in rows:
        if len(f) != len(PAPER_COLS):
            bad.append(f"papers.tsv:{i}: short row: {len(f)} fields, expected 10 (row starts {f[0]!r})")
            continue
        r = dict(zip(PAPER_COLS, (x.strip() for x in f)))
        for col in PAPER_REQUIRED:
            if not r[col]:
                bad.append(f"papers.tsv:{i}: {r['id'] or '(no id)'} has an empty '{col}'")
        if r["id"] in seen:
            bad.append(f"papers.tsv:{i}: duplicate id {r['id']} (first on line {seen[r['id']]})")
        seen.setdefault(r["id"], i)
        m = re.fullmatch(r"([A-Z])(\d+)", r["id"])
        want = prefixes.get(r["folder"][:2])
        if not m:
            bad.append(f"papers.tsv:{i}: id {r['id']!r} is not <prefix letter><number>")
        elif want is None:
            bad.append(f"papers.tsv:{i}: {r['id']} folder {r['folder']!r} is not a numbered folder in literature/README.md")
        elif m.group(1) != want:
            bad.append(f"papers.tsv:{i}: {r['id']} prefix {m.group(1)} does not match folder {r['folder'][:2]} (prefix {want})")
        if not re.fullmatch(r"\d{4}", r["year"]):
            bad.append(f"papers.tsv:{i}: {r['id']} year {r['year']!r} is not 4 digits")
        if r["verified"] not in ("yes", "no"):
            bad.append(f"papers.tsv:{i}: {r['id']} verified {r['verified']!r} is not yes/no")
    ok = report("PAPERS", bad)
    print(f"papers: {len(rows)} rows, {len(bad)} problems")
    return ok


def folder_dir(folder):
    """papers.tsv folder value (NN or NN_<Name>) -> its directory under literature/."""
    if (LIT / folder).is_dir():
        return LIT / folder
    hits = [d for d in theme_dirs() if d.name[:2] == folder[:2]]
    return hits[0] if hits else LIT / folder


def files():
    bad, warn, listed, checked = [], [], set(), 0
    for i, r in paper_rows():
        if not r["file"]:
            continue   # papers() reports the empty field
        checked += 1
        name = Path(r["file"]).name
        path = LIT / r["file"] if "/" in r["file"] else folder_dir(r["folder"]) / name
        listed.add(path.resolve())
        m = FILE_RE.fullmatch(name)
        if not m:
            bad.append(f"papers.tsv:{i}: file {name!r} does not follow {FILE_PATTERN} (or _NOTE.md)")
        else:
            if m.group(1) != r["id"] or m.group(3) != r["year"]:
                bad.append(f"papers.tsv:{i}: file {name!r} does not start with this row's id and year ({r['id']}, {r['year']})")
            if norm(m.group(2)) not in norm(ascii_fold(r["first_author"])):
                bad.append(f"papers.tsv:{i}: file {name!r} author {m.group(2)!r} is not in first_author {r['first_author']!r}")
        rel = path.relative_to(REPO).as_posix() if path.is_relative_to(REPO) else str(path)
        if not path.exists():
            if name.endswith("_NOTE.md"):
                bad.append(f"papers.tsv:{i}: {r['id']} note {rel} is missing (notes are committed, unlike PDFs)")
            else:
                warn.append(f"{r['id']}: {rel} not downloaded (PDFs are local only; run scripts/literature/fetch_papers.py)")
        elif name.lower().endswith(".pdf") and path.read_bytes()[:4] != b"%PDF":
            bad.append(f"{rel}: not a PDF (does not start with %PDF)")
    for p in sorted(LIT.rglob("*.pdf")) if LIT.exists() else []:
        if p.resolve() in listed:
            continue
        rel = p.relative_to(REPO).as_posix()
        if p.read_bytes()[:4] != b"%PDF":
            bad.append(f"{rel}: not a PDF (does not start with %PDF)")
        else:
            warn.append(f"{rel}: PDF not listed in papers.tsv")
    ok = report("FILE", bad, warn)
    print(f"files: {checked} rows checked, {len(bad)} problems, {len(warn)} warnings")
    return ok


def candidates():
    folder = REPO / "public" / "_candidates"
    tsvs = sorted(folder.glob("*.tsv")) if folder.exists() else []
    bad, n = [], 0
    for t in tsvs:
        rel = t.relative_to(REPO).as_posix()
        lines = t.read_text(encoding="utf-8").splitlines()
        header = lines[0].split("\t") if lines else []
        if header != CAND_COLS:
            bad.append(f"{rel}:1: header is {header!r}, expected the 8 tab-separated columns {CAND_COLS!r}")
        for i, ln in enumerate(lines[1:], 2):
            if not ln.strip():
                continue
            n += 1
            f = [x.strip() for x in ln.split("\t")]
            if len(f) != len(CAND_COLS):
                bad.append(f"{rel}:{i}: short candidates row: {len(f)} fields, expected 8 (row starts {f[0]!r})")
                continue
            r = dict(zip(CAND_COLS, f))
            empty = [c for c in CAND_COLS if not r[c]]
            if empty:
                bad.append(f"{rel}:{i}: {r['name'] or '(no name)'} has empty field(s): {', '.join(empty)}")
            if r["url"] and not r["url"].startswith("https://github.com/"):
                bad.append(f"{rel}:{i}: url {r['url']!r} is not a https://github.com/ link")
            if r["stars"] and not r["stars"].isdigit():
                bad.append(f"{rel}:{i}: stars {r['stars']!r} is not a whole number")
            if r["archived"] and r["archived"].lower() not in ("true", "false"):
                bad.append(f"{rel}:{i}: archived {r['archived']!r} is not true/false")
            if r["last_push"] and not re.match(r"\d{4}-\d{2}-\d{2}", r["last_push"]):
                bad.append(f"{rel}:{i}: last_push {r['last_push']!r} is not an ISO date")
    ok = report("CANDIDATES", bad)
    print(f"candidates: {len(tsvs)} files, {n} rows, {len(bad)} problems")
    return ok


def agent(path):
    """A scout prompt must carry the whole output contract, or its output cannot pass the checks above."""
    p = Path(path)
    if not p.exists():
        print(f"  MISSING {path}: file not found")
        print("agent contract: FAIL")
        return False
    s = p.read_text(encoding="utf-8", errors="replace")
    low = s.lower()

    def has(word):
        return re.search(r"(?<![a-z0-9_])" + re.escape(word.lower()) + r"(?![a-z0-9_])", low)

    missing = [f"README section '{x}'" for x in SECTIONS if not has(x)]
    missing += [f"papers.tsv column '{x}'" for x in PAPER_COLS if not has(x)]
    missing += [f"candidates column '{x}'" for x in CAND_COLS if not has(x)]
    if FILE_PATTERN not in s:
        missing.append(f"file-name pattern '{FILE_PATTERN}'")
    if "fetched source" not in low:
        missing.append("phrase 'fetched source'")
    for m in missing:
        print("  MISSING", m)
    print("agent contract: " + ("PASS" if not missing else f"FAIL ({len(missing)} missing)"))
    return not missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory")
    ap.add_argument("--compare", nargs=2)
    ap.add_argument("--links", action="store_true")
    ap.add_argument("--stale", action="store_true")
    ap.add_argument("--titles", action="store_true")
    ap.add_argument("--readmes", action="store_true")
    ap.add_argument("--papers", action="store_true")
    ap.add_argument("--files", action="store_true")
    ap.add_argument("--candidates", action="store_true")
    ap.add_argument("--agent", metavar="PATH")
    ap.add_argument("--root", metavar="DIR")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(errors="replace")
    if a.root:
        set_root(a.root)
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
    if a.readmes or a.all:
        ok &= readmes()
    if a.papers or a.all:
        ok &= papers()
    if a.files or a.all:
        ok &= files()
    if a.candidates or a.all:
        ok &= candidates()
    if a.agent:
        ok &= agent(a.agent)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
