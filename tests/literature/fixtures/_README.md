# tests/literature/fixtures

Inputs for `tests/literature/` (the literature checker and the paper fetcher). Nothing here is read by
the real library checks.

| Path | What it is |
|---|---|
| `clean/` | A complete, valid repo root (`literature/` + `public/_candidates/`): the checker must exit 0 on it |
| `missing_section/` | Overlay: folder 02 README without "The catch" |
| `duplicate_id/` | Overlay: `papers.tsv` with ID A1 twice |
| `short_row/` | Overlay: `papers.tsv` with a 9-field row |
| `fake_pdf/` | Overlay: an HTML page saved under a paper's `.pdf` name |
| `short_candidate/` | Overlay: `public/_candidates/02.tsv` with a 3-field row |
| `one_paper.tsv` | One real arXiv paper (ReAct, 2210.03629) for `fetch_papers.py` |
| `bad_url.tsv` | Two rows that must fail: an HTML page and an unresolvable host |
| `scout_prompt_full.md` / `scout_prompt_partial.md` | Agent prompts with the whole contract / part of it |

**Overlays:** the tests copy `clean/` into a temp dir, then copy the defect folder over it. A file
ending in `.pdf.txt` lands with the `.txt` dropped, so no `*.pdf` is ever committed (the repo publishes
no PDFs; criterion C7 checks `git ls-files '*.pdf'` is 0).
