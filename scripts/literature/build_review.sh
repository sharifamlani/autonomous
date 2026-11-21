#!/usr/bin/env bash
#
# Build the literature review PDF from literature/review/main.tex.
#
#   bash scripts/literature/build_review.sh          rebuild references.bib from cache, compile, copy PDF
#
# Output: literature/LITERATURE_REVIEW.pdf (committed); build files in literature/review/build/ (ignored).
# Exits non-zero if LaTeX fails or the PDF is missing.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REV="$ROOT/literature/review"

python "$ROOT/scripts/literature/build_bib.py" --offline
cd "$REV"
# BIBINPUTS lets bibtex, running in build/, find references.bib one level up
BIBINPUTS="$REV:" latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex > build.out 2>&1 || {
  echo "LaTeX failed; last lines of the log:" >&2; tail -30 build.out >&2; exit 1; }
cp build/main.pdf "$ROOT/literature/LITERATURE_REVIEW.pdf"
pages=$(grep -a -c "/Type /Page\b" build/main.pdf || true)
echo "built literature/LITERATURE_REVIEW.pdf ($(du -k build/main.pdf | cut -f1) KB)"
grep -E "Overfull|undefined" build/main.log | sort | uniq -c | head -20 || true
