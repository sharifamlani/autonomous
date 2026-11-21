"""Fold parallel scouts' staged rows into literature/papers.tsv.

When several research scouts run at once, each writes its rows to
literature/_incoming/NN_papers.tsv (same header as papers.tsv) instead of editing
papers.tsv directly. This script appends those rows to papers.tsv in theme order,
refuses on a bad header or an ID already present, and deletes each staged file once
merged.

Usage:
  python scripts/literature/merge_incoming.py            # merge every staged file
  python scripts/literature/merge_incoming.py --dry-run  # show what would merge

Exit 1 if any staged file is refused (nothing from that file is merged).
Then run: python scripts/literature/verify_literature.py --all
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LIT = REPO / "literature"
PAPER_COLS = ["id", "folder", "first_author", "year", "title", "venue", "url", "arxiv_or_doi", "file", "verified"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=LIT, help="literature folder (tests)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    papers = args.root / "papers.tsv"
    lines = papers.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].split("\t") != PAPER_COLS:
        print(f"refused: {papers} header is not the 10 papers.tsv columns")
        return 1
    have = {ln.split("\t")[0] for ln in lines[1:] if ln.strip()}

    failed, merged = 0, 0
    for inc in sorted((args.root / "_incoming").glob("*.tsv")):
        inc_lines = [ln for ln in inc.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if not inc_lines or inc_lines[0].split("\t") != PAPER_COLS:
            print(f"refused: {inc.name}: header is not the 10 papers.tsv columns")
            failed += 1
            continue
        rows = inc_lines[1:]
        ids = [r.split("\t")[0] for r in rows]
        clash = sorted((set(ids) & have) | {i for i in ids if ids.count(i) > 1})
        short = [r.split("\t")[0] for r in rows if len(r.split("\t")) != len(PAPER_COLS)]
        if clash or short:
            print(f"refused: {inc.name}: duplicate ids {clash} short rows {short}")
            failed += 1
            continue
        print(f"{'would merge' if args.dry_run else 'merged'} {len(rows)} rows from {inc.name}")
        if not args.dry_run:
            lines += rows
            have |= set(ids)
            inc.unlink()
        merged += len(rows)

    if not args.dry_run and merged:
        papers.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"merged {merged} rows, refused {failed} files{' (dry run)' if args.dry_run else ''}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
