"""Build literature/review/references.bib from papers.tsv, with full author lists.

Author lists come from the arXiv API (arXiv IDs) and Crossref (DOIs), cached in
literature/review/authors.tsv so re-runs are offline. Sources with neither (blogs, system cards,
docs) use `first_author`; an organisation name is kept as one braced author. To correct any entry by
hand, edit its row in authors.tsv (source column `manual`); manual rows are never overwritten.

Usage:
  python scripts/literature/build_bib.py            # fetch missing authors, write references.bib
  python scripts/literature/build_bib.py --offline  # use the cache only

Exits non-zero if papers.tsv has rows the bib could not include.
"""
import argparse
import csv
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPERS = ROOT / "literature" / "papers.tsv"
OUTDIR = ROOT / "literature" / "review"
CACHE = OUTDIR / "authors.tsv"
BIB = OUTDIR / "references.bib"
UA = {"User-Agent": "autonomous-literature-review (github.com/sharifamlani/autonomous)"}
ATOM = "{http://www.w3.org/2005/Atom}"


def kind(ref):
    if ref.startswith("10."):
        return "doi"
    if re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", ref):
        return "arxiv"
    return "other"


def load_cache():
    if not CACHE.exists():
        return {}
    rows = csv.DictReader(CACHE.open(encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)
    return {r["id"]: r for r in rows}


def save_cache(cache):
    with CACHE.open("w", encoding="utf-8", newline="\n") as f:
        f.write("id\tsource\tauthors\n")
        for k in sorted(cache, key=lambda s: (s[0], int(re.sub(r"\D", "", s) or 0))):
            r = cache[k]
            f.write(f"{k}\t{r['source']}\t{r['authors']}\n")


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def fetch_arxiv(ids):
    out = {}
    for i in range(0, len(ids), 40):
        batch = ids[i:i + 40]
        url = "http://export.arxiv.org/api/query?max_results=100&id_list=" + ",".join(batch)
        root = ET.fromstring(get(url))
        for e in root.findall(f"{ATOM}entry"):
            aid = e.find(f"{ATOM}id").text.rsplit("/", 1)[-1]
            aid = re.sub(r"v\d+$", "", aid)
            names = [a.find(f"{ATOM}name").text.strip() for a in e.findall(f"{ATOM}author")]
            out[aid] = names
        time.sleep(3)  # arXiv API etiquette
    return out


def fetch_crossref(doi):
    d = json.loads(get("https://api.crossref.org/works/" + doi))["message"]
    names = []
    for a in d.get("author", []):
        if "family" in a:
            names.append(f"{a.get('given', '')} {a['family']}".strip())
        elif "name" in a:
            names.append("{" + a["name"] + "}")
    return names


def tex(s):
    s = s.replace("\\", "").replace("{", "").replace("}", "")
    for a, b in (("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(a, b)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    papers = list(csv.DictReader(PAPERS.open(encoding="utf-8"), delimiter="\t"))
    cache = load_cache()
    if not a.offline:
        need_ax = [p for p in papers if kind(p["arxiv_or_doi"]) == "arxiv" and p["id"] not in cache]
        if need_ax:
            got = fetch_arxiv([re.sub(r"v\d+$", "", p["arxiv_or_doi"]) for p in need_ax])
            for p in need_ax:
                names = got.get(re.sub(r"v\d+$", "", p["arxiv_or_doi"]))
                if names:
                    cache[p["id"]] = {"source": "arxiv", "authors": " and ".join(names)}
        for p in papers:
            if kind(p["arxiv_or_doi"]) == "doi" and p["id"] not in cache:
                try:
                    names = fetch_crossref(p["arxiv_or_doi"])
                except Exception as e:  # noqa: BLE001
                    print(f"  crossref failed for {p['id']}: {e}")
                    names = []
                if names:
                    cache[p["id"]] = {"source": "crossref", "authors": " and ".join(names)}
                time.sleep(1)
    for p in papers:
        if p["id"] not in cache:
            fa = p["first_author"].strip()
            org = not re.fullmatch(r"[A-Z][a-zA-Z'\-]+", fa) or fa in ("OpenAI", "Anthropic", "METR", "Cognition")
            cache[p["id"]] = {"source": "first_author", "authors": "{" + fa + "}" if org else fa}
    save_cache(cache)

    out = []
    for p in papers:
        k = kind(p["arxiv_or_doi"])
        fields = {
            "author": cache[p["id"]]["authors"],
            "title": "{" + tex(p["title"]) + "}",
            "year": p["year"],
            "howpublished" if k == "other" else "journal": tex(p["venue"] or ("arXiv preprint" if k == "arxiv" else "")),
            "url": p["url"],
        }
        if k == "doi":
            fields["doi"] = p["arxiv_or_doi"]
        typ = "misc" if k == "other" else "article"
        body = ",\n".join(f"  {f} = {{{v}}}" for f, v in fields.items() if v)
        out.append(f"@{typ}{{{p['id']},\n{body}\n}}")
    BIB.write_text("\n\n".join(out) + "\n", encoding="utf-8", newline="\n")
    src = {}
    for r in cache.values():
        src[r["source"]] = src.get(r["source"], 0) + 1
    print(f"wrote {BIB.relative_to(ROOT)}: {len(out)} entries; author sources {src}")
    sys.exit(0 if len(out) == len(papers) else 1)


if __name__ == "__main__":
    main()
