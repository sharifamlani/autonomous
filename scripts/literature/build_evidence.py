"""Build literature/LITERATURE_REVIEW_EVIDENCE.md: every claim in the review, with its verbatim source quote.

Sharif 2026-11-21: every claim, item or citation in the review gets a row with the verbatim quote,
the page number and exactly where in the source it is. This script:

  1. reads the claims ledgers in literature/review/ledger/*.tsv (columns: section, sentence_start,
     claim, number, source_id, exact_quote, location),
  2. checks completeness: every \\cite key and \\repo used in a section file has >= 1 ledger row,
  3. checks each quote mechanically where it can: for papers with a local PDF it extracts the text of
     the stated page (pymupdf) and confirms the quote is there verbatim (whitespace, hyphenation,
     ligatures and quote marks normalised; "..." splits a quote into pieces that must all appear, in
     order). Quotes from web pages and repos are marked for QA's manual check.
  4. writes the evidence file, grouped by section, one entry per claim.

Status per row: VERIFIED (found on the stated page), WRONG PAGE (found, on another page; the true
page is shown), NOT FOUND (not in the PDF), MANUAL (web or repo source: QA checks by hand),
NO PDF (paper with no local file).

Usage:
  python scripts/literature/build_evidence.py           # write the evidence file; exit 1 on gaps or failures
  python scripts/literature/build_evidence.py --summary # counts only
"""
import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parents[2]
LIT = ROOT / "literature"
LEDGER = LIT / "review" / "ledger"
SEC = LIT / "review" / "sections"
OUT = LIT / "LITERATURE_REVIEW_EVIDENCE.md"
COLS = ["section", "sentence_start", "claim", "number", "source_id", "exact_quote", "location"]
CITE = re.compile(r"\\cite[tp]?\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
REPO = re.compile(r"\\repo(?:file)?\{([^}]*)\}\{([^}]*)\}")
PAGE = re.compile(r"\bp(?:p)?\.\s*(\d+)")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("\u2018", "'"), ("\u2019", "'"), ("\u201c", '"'), ("\u201d", '"'), ("\u2013", "-"),
                 ("\u2014", "-"), ("\u2212", "-"), ("\u00a0", " "), ("\u00ad", "")):
        s = s.replace(a, b)
    s = re.sub(r"-\s*\n\s*", "", s)  # hyphenated line breaks
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def pieces(quote):
    return [norm(p) for p in re.split(r"\.\.\.|\u2026|\[\.\.\.\]", quote) if norm(p)]


def found(text, quote):
    pos = 0
    for p in pieces(quote):
        i = text.find(p, pos)
        if i < 0:
            return False
        pos = i + len(p)
    return True


class Pdfs:
    def __init__(self):
        self.papers = {r["id"]: r for r in csv.DictReader((LIT / "papers.tsv").open(encoding="utf-8"), delimiter="\t")}
        self.cache = {}

    def pages(self, pid):
        if pid not in self.cache:
            r = self.papers.get(pid)
            path = (LIT / r["folder"] / r["file"]) if r and r.get("file") else None
            if not path or not path.exists() or path.suffix.lower() != ".pdf":
                self.cache[pid] = None
            else:
                with fitz.open(path) as doc:
                    self.cache[pid] = [norm(pg.get_text()) for pg in doc]
        return self.cache[pid]


def check(row, pdfs):
    sid = row["source_id"].strip()
    if "/" in sid or "#" in sid:
        return "MANUAL", ""
    pages = pdfs.pages(sid)
    if sid not in pdfs.papers:
        return "UNKNOWN ID", ""
    if pages is None:
        return ("MANUAL", "") if not pdfs.papers[sid].get("file", "").lower().endswith(".pdf") else ("NO PDF", "")
    m = PAGE.search(row["location"])
    want = int(m.group(1)) if m else None
    if want and 1 <= want <= len(pages) and found(pages[want - 1], row["exact_quote"]):
        return "VERIFIED", ""
    hits = [i + 1 for i, t in enumerate(pages) if found(t, row["exact_quote"])]
    if not hits:  # quote may run across a page break
        joined = " ".join(pages)
        if found(joined, row["exact_quote"]):
            return ("VERIFIED" if want else "WRONG PAGE"), "spans a page break"
        return "NOT FOUND", ""
    return "WRONG PAGE", f"found on p. {', '.join(map(str, hits))}"


def ledger_rows():
    rows = []
    for f in sorted(LEDGER.glob("*.tsv")):
        lines = f.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines[1:], 2):
            if not line.strip():
                continue
            c = line.split("\t")
            c += [""] * (len(COLS) - len(c))
            r = dict(zip(COLS, c[:len(COLS)]))
            r["_file"], r["_line"] = f.name, n
            rows.append(r)
    return rows


def used_sources():
    """(section file prefix, source) pairs used in the LaTeX."""
    used = defaultdict(set)
    for f in sorted(SEC.glob("[0-9][0-9]_*.tex")):
        t = f.read_text(encoding="utf-8")
        for m in CITE.finditer(t):
            for k in (x.strip() for x in m.group(1).split(",")):
                if k:
                    used[f.name[:2]].add(k)
        for m in REPO.finditer(t):
            used[f.name[:2]].add(m.group(1).lower())
    return used


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    pdfs = Pdfs()
    rows = ledger_rows()
    for r in rows:
        r["_status"], r["_note"] = check(r, pdfs)
    # completeness: every source used in a section file appears in a ledger row covering that section
    have = defaultdict(set)
    for r in rows:
        for pre in re.findall(r"\d\d", r["_file"]):
            sid = r["source_id"].strip()
            have[pre].add(sid.split("#")[0].lower() if "/" in sid else sid)
    used = used_sources()
    missing = sorted(f"{pre}: {s}" for pre, ss in used.items() for s in ss if s not in have.get(pre, set()))
    st = Counter(r["_status"] for r in rows)
    print(f"{len(rows)} ledger rows; " + ", ".join(f"{k} {v}" for k, v in st.most_common()))
    print(f"{len(missing)} cited sources with no ledger row" + "".join(f"\n  missing {m}" for m in missing[:40]))
    if a.summary:
        sys.exit(0)

    names = {}
    bib = (LIT / "review" / "authors.tsv")
    if bib.exists():
        for r in csv.DictReader(bib.open(encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE):
            first = r["authors"].split(" and ")[0].strip("{}").split()[-1]
            n = len(r["authors"].split(" and "))
            names[r["id"]] = first + (" et al." if n >= 3 else (" & " + r["authors"].split(" and ")[1].strip("{}").split()[-1] if n == 2 else ""))
    out = ["# Literature review: evidence for every claim", "",
           "Every claim, number and citation in *Verification, Not Capability* (`literature/LITERATURE_REVIEW.pdf`),",
           "with the verbatim quote from the source that supports it and exactly where that quote is.",
           "Generated by `scripts/literature/build_evidence.py` from the writers' claims ledgers; QA checks every row.", "",
           "**Status key:** VERIFIED = the quote was found verbatim on the stated PDF page by script ·",
           "MANUAL = web page or GitHub source, checked by hand in QA (`literature/qa/`) · WRONG PAGE /",
           "NOT FOUND / NO PDF = open QA finding.", "",
           f"**Rows:** {len(rows)} · " + " · ".join(f"{k} {v}" for k, v in st.most_common()), ""]
    by_sec = defaultdict(list)
    for r in rows:
        by_sec[r["section"].strip() or r["_file"]].append(r)

    def seckey(s):
        nums = re.findall(r"\d+", s)
        return [int(x) for x in nums] or [999]

    for sec in sorted(by_sec, key=seckey):
        out += [f"## §{sec}", ""]
        for i, r in enumerate(by_sec[sec], 1):
            sid = r["source_id"].strip()
            src = f"{names.get(sid, '')} {pdfs.papers[sid]['year']} [{sid}]".strip() if sid in pdfs.papers else f"`{sid}`"
            title = pdfs.papers[sid]["title"] if sid in pdfs.papers else ""
            out += [f"### {sec}.{i} {r['claim'].strip()}", "",
                    f"- **In the paper:** \"{r['sentence_start'].strip()}...\"" + (f" (number: {r['number'].strip()})" if r["number"].strip() else ""),
                    f"- **Source:** {src}" + (f", *{title}*" if title else ""),
                    f"- **Where:** {r['location'].strip()}",
                    f"- **Verbatim quote:**", "",
                    "  > " + r["exact_quote"].strip().replace("\n", " "), "",
                    f"- **Check:** {r['_status']}" + (f" ({r['_note']})" if r["_note"] else ""), ""]
    if missing:
        out += ["## Cited in the paper with no evidence row yet (open QA findings)", ""] + [f"- {m}" for m in missing] + [""]
    OUT.write_text("\n".join(out), encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)}")
    bad = st.get("NOT FOUND", 0) + st.get("WRONG PAGE", 0) + st.get("NO PDF", 0) + st.get("UNKNOWN ID", 0)
    sys.exit(1 if bad or missing else 0)


if __name__ == "__main__":
    main()
