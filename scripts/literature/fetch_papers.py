"""Re-download the literature PDFs from papers.tsv (PDFs are local only; the catalogue is public).

  python scripts/literature/fetch_papers.py                         # every row -> literature/<folder>/<file>
  python scripts/literature/fetch_papers.py --tsv T.tsv --dest DIR  # another catalogue -> DIR/<folder>/<file>

For each row: resolve the URL (arXiv abs -> pdf), download, keep the file only if it starts with %PDF
(anything else is deleted and reported). A row whose PDF already exists and is valid is skipped, so
the script is safe to re-run. Rows whose file is a _NOTE.md have no PDF and are skipped.
Polite: a User-Agent on every request and a 3-second gap between arXiv requests.

Prints one line per row, then `fetched N, skipped N, failed N`. Exit 0 only when nothing failed.
"""
import argparse
import csv
import re
import sys
import time
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[2]
LIT = REPO / "literature"
USER_AGENT = "autonomous-literature-fetcher/0.1 (+https://github.com/sharifamlani/autonomous)"
ARXIV_GAP_S = 3.0
TIMEOUT_S = 60
ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+(?:\.[A-Z]{2})?/\d{7}(?:v\d+)?)")
_last_arxiv = 0.0


def resolve_url(url, arxiv_or_doi=""):
    """The URL to download: arXiv abs/html links become pdf links; a bare arXiv id with no URL builds one."""
    url = (url or "").strip()
    m = re.match(r"https?://(?:www\.|export\.)?arxiv\.org/(?:abs|pdf|html)/(.+?)(?:\.pdf)?/?$", url)
    if m:
        return f"https://arxiv.org/pdf/{m.group(1)}"
    if not url and ARXIV_ID.fullmatch((arxiv_or_doi or "").strip()):
        return f"https://arxiv.org/pdf/{arxiv_or_doi.strip()}"
    return url


def is_pdf(path):
    with open(path, "rb") as fh:
        return fh.read(4) == b"%PDF"


def polite_wait(url):
    """Keep at least ARXIV_GAP_S seconds between requests to arxiv.org."""
    global _last_arxiv
    if "arxiv.org" not in url:
        return
    wait = ARXIV_GAP_S - (time.monotonic() - _last_arxiv)
    if wait > 0:
        time.sleep(wait)
    _last_arxiv = time.monotonic()


def download_pdf(url, out, session=None):
    """Download url to out. Returns None on success, or the reason it failed (non-PDFs are deleted)."""
    session = session or requests.Session()
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    part = out.with_name(out.name + ".part")
    polite_wait(url)
    try:
        with session.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_S, stream=True,
                         allow_redirects=True) as r:
            if r.status_code != 200:
                return f"HTTP {r.status_code}"
            with open(part, "wb") as fh:
                for chunk in r.iter_content(64 * 1024):
                    fh.write(chunk)
            ctype = r.headers.get("Content-Type", "?")
    except requests.RequestException as e:
        part.unlink(missing_ok=True)
        return f"request failed: {type(e).__name__}"
    if not is_pdf(part):
        part.unlink(missing_ok=True)
        return f"not a PDF (Content-Type {ctype}); deleted"
    part.replace(out)
    return None


def folder_name(folder, lit=LIT):
    """papers.tsv folder value (NN or NN_<Name>) -> the folder's directory name."""
    if "_" in folder:
        return folder
    hits = sorted(d.name for d in lit.glob(f"{folder[:2]}_*") if d.is_dir()) if lit.exists() else []
    return hits[0] if hits else folder


def fetch(tsv, dest, session=None):
    session = session or requests.Session()
    counts = {"fetched": 0, "skipped": 0, "failed": 0}
    with open(tsv, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    for r in rows:
        rid, name = (r.get("id") or "?").strip(), (r.get("file") or "").strip()
        if not name:
            print(f"  failed  {rid}: no file name in papers.tsv")
            counts["failed"] += 1
            continue
        if name.endswith("_NOTE.md"):
            print(f"  skipped {rid}: note, no PDF to fetch")
            counts["skipped"] += 1
            continue
        out = dest / name if "/" in name else dest / folder_name((r.get("folder") or "").strip()) / name
        if out.exists():
            if is_pdf(out):
                print(f"  skipped {rid}: {out.name} already present")
                counts["skipped"] += 1
                continue
            out.unlink()
            print(f"  deleted {rid}: existing {out.name} was not a PDF; re-fetching")
        url = resolve_url(r.get("url"), r.get("arxiv_or_doi"))
        if not url:
            print(f"  failed  {rid}: no url")
            counts["failed"] += 1
            continue
        err = download_pdf(url, out, session)
        if err:
            print(f"  failed  {rid}: {url}: {err}")
            counts["failed"] += 1
        else:
            print(f"  fetched {rid}: {url} -> {out}")
            counts["fetched"] += 1
    print(f"fetched {counts['fetched']}, skipped {counts['skipped']}, failed {counts['failed']}")
    return counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tsv", default=str(LIT / "papers.tsv"), help="catalogue to read (default literature/papers.tsv)")
    ap.add_argument("--dest", default=str(LIT), help="root to write <folder>/<file> under (default literature/)")
    a = ap.parse_args()
    sys.stdout.reconfigure(errors="replace")
    counts = fetch(Path(a.tsv), Path(a.dest))
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
