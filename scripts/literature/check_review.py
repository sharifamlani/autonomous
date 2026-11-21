"""Check the LaTeX literature review against its criteria (ROADMAP 7.2, docs/plans/07_literature_review.md).

Checks, from the section sources in literature/review/sections/:
  - every \\cite key is a paper ID in literature/papers.tsv        (0 dangling: hard fail)
  - body word count 9,000-15,500 (Sharif 2026-11-21); abstract <= 150 words
  - >= 150 distinct works cited; each of the 9 themes cited >= 8 distinct times; >= 15 repo citations
  - Summary Points and Future Issues present
  - after a build: no undefined citations or references in build/main.log

Usage:
  python scripts/literature/check_review.py            # all checks; exit 1 on any FAIL
  python scripts/literature/check_review.py --cites    # citation resolution only (fast)
"""
import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REV = ROOT / "literature" / "review"
SEC = REV / "sections"
LOG = REV / "build" / "main.log"
CITE = re.compile(r"\\cite[tp]?\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
REPO = re.compile(r"\\repo(?:file)?\{([^}]*)\}\{([^}]*)\}")
PREFIX_THEME = {"A": "01", "H": "02", "C": "03", "T": "04", "V": "05", "S": "06", "D": "07", "R": "08", "F": "09"}


def words(tex):
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    tex = re.sub(r"\\begin\{(table|figure)\*?\}.*?\\end\{\1\*?\}", " ", tex, flags=re.S)
    tex = CITE.sub(" Author 2026 ", tex)
    tex = REPO.sub(lambda m: " " + m.group(1) + " ", tex)
    tex = re.sub(r"\\(defn|marginnote)\{[^}]*\}\{[^}]*\}", " ", tex)
    tex = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", tex)
    tex = re.sub(r"[{}$\\~]", " ", tex)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-.,%]*", tex))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cites", action="store_true")
    a = ap.parse_args()
    ids = {r["id"] for r in csv.DictReader((ROOT / "literature" / "papers.tsv").open(encoding="utf-8"), delimiter="\t")}
    files = sorted(SEC.glob("*.tex"))
    keys, repos, body_words, per_file = Counter(), [], 0, {}
    dangling = []
    for f in files:
        t = f.read_text(encoding="utf-8")
        for m in CITE.finditer(t):
            for k in (x.strip() for x in m.group(1).split(",")):
                if k:
                    keys[k] += 1
                    if k not in ids:
                        dangling.append(f"{f.name}: {k}")
        repos += [m.group(1) for m in REPO.finditer(t)]
        if f.stem not in ("00_abstract", "contents", "17_endmatter"):
            per_file[f.stem] = words(t)
            body_words += per_file[f.stem]
    results = []

    def check(name, ok, detail):
        results.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")

    check("citations resolve", not dangling, f"{len(keys)} distinct keys, {len(dangling)} dangling" +
          ("".join(f"\n        dangling {d}" for d in dangling)))
    if a.cites:
        sys.exit(0 if all(results) else 1)

    abstract = SEC / "00_abstract.tex"
    aw = words(abstract.read_text(encoding="utf-8")) if abstract.exists() else 0
    check("abstract <= 150 words", 0 < aw <= 150, f"{aw} words")
    # Sharif 2026-11-21: "length is acceptable" (criterion raised from 9,000-11,000 after the Phase 8 grade)
    check("body 9,000-15,500 words", 9000 <= body_words <= 15500, f"{body_words} words")
    for stem, n in per_file.items():
        print(f"        {stem}: {n}")
    valid = [k for k in keys if k in ids]
    check(">= 150 works cited", len(valid) >= 150, f"{len(valid)} distinct papers")
    theme = Counter(PREFIX_THEME[k[0]] for k in valid)
    low = {t: theme.get(t, 0) for t in sorted(PREFIX_THEME.values()) if theme.get(t, 0) < 8}
    check("each theme cited >= 8 distinct", not low, f"{dict(sorted(theme.items()))}" + (f" low: {low}" if low else ""))
    check(">= 15 repo citations", len(repos) >= 15, f"{len(repos)} citations, {len(set(repos))} repos")
    end = (SEC / "17_endmatter.tex").read_text(encoding="utf-8") if (SEC / "17_endmatter.tex").exists() else ""
    check("Summary Points + Future Issues", "SUMMARY POINTS" in end.upper() and "FUTURE ISSUES" in end.upper(), "boxes present" if end else "endmatter missing")
    if LOG.exists():
        log = LOG.read_text(encoding="latin-1")
        undef = re.findall(r"(?:Citation|Reference) `([^']+)' .*undefined", log)
        check("build: no undefined refs", not undef, f"{len(undef)} undefined" + (f": {sorted(set(undef))[:10]}" if undef else ""))
    else:
        check("build: no undefined refs", False, "no build log; run scripts/literature/build_review.sh")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
