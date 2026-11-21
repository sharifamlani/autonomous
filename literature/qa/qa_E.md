# QA E: Literature Cited metadata, whole-paper consistency, rendered PDF

QA agent E, 2026-11-21. Scope: (1) bibliography metadata for every cited key (owned; edits to
`papers.tsv`, `review/authors.tsv`, `review/references.bib` via `build_bib.py`); (2) whole-paper
consistency, read-only on sections (findings routed to section owners); (3) the rendered PDF.

## What was checked

- **162 cited keys** (every `\cite*` in `review/sections/*.tex`).
  - **127 arXiv entries:** title, year (first-version date), first author and full author list compared
    against the arXiv API (`export.arxiv.org/api/query`). All titles and years match. The only
    differences are formatting (`tau-bench` for `$\tau$-bench`, kept because the bib builder can't
    carry LaTeX math) and diacritics in first-author names (`Mundler`/`Mündler`, `Lu`/`Lù`,
    `ArinoDeLaRubia`/`Ariño de la Rubia`), which are only in the `first_author` file-name column.
  - **10 Crossref DOIs (R9–R20):** title, year and journal checked against `api.crossref.org/works/<doi>`.
    All match.
  - **25 web, report and PDF sources** (`first_author` placeholders): page or PDF fetched; byline, title
    and date checked.
  - **Claimed venues not stated in the arXiv comment** were checked on the conference pages: D3 (ICLR
    2025 poster), F7 and F8 (ICLR 2026), F19 (ICLR 2026 workshop "Agents in the Wild"), V12 (ICSE 2026
    research track), V4 (FSE 2025 industry papers), T7 (NeurIPS 2025 D&B), C16 (ICML 2025, PMLR 267),
    S15 (ICML 2026, spotlight in the AI for Science workshop). All are correct.
- **Rendered PDF (35 pages):** read page by page as PNG renders.
- **Numbers repeated across sections:** checked against each other, with sources opened where they
  differed.
- **Cross-references:** all `\label`s and `\ref`s, plus a privacy grep.

## Findings

| # | section | severity | finding | source checked (ID, page) | fix made | status |
|---|---|---|---|---|---|---|
| E1 | Literature Cited | major | 25 cited web and report sources rendered with placeholder authors: a lone surname (e.g. "Schluntz" for a two-author post, "Carlini", "Young"), and two broken one-word names, **"GoogleDeepMind"** (F30) and **"VonArx"** (V17). | Bylines fetched for A15, C14, C15, C29, D26, F14, F27, F30, F32, F34, F35, H13, H23, H24, R5, R12, R19, S15, S20, S21, T16, T28, V16, V17, V31 (pages' "Written by", "Contributors" or "Authors" lines; PDF title pages). S20, S21, C15, F32, F34 and V31 name no person, so the organization is kept. | Wrote full bylines to `authors.tsv` (source `manual`), e.g. A15 Erik Schluntz and Barry Zhang; F30 {Google DeepMind}; V17 Sydney {Von Arx}, Lawrence Chan, Beth Barnes; R12 Andrew Gelman and Eric Loken; F35 Ryan Greenblatt, Ajeya Cotra, Hjalmar Wijk. | fixed |
| E2 | Literature Cited | major | The bibliography printed every author of the many-analyst papers. That was about two pages of names: R17 has 343 authors, all in CAPITALS from Crossref; R16 has 310, R10 197, R11 166, plus 39 more entries with more than 10 authors. | Crossref (R17, R16, R10, R11, R9, R18, R20); arXiv API | Applied Chicago Manual of Style 17th ed. §14.76: more than ten authors lists the first seven, then "et al." ("and others"). 43 cited rows set to `manual`. R17 first seven re-cased from the source (Albert J. Menkveld … Sebastian Neusüß). | fixed |
| E3 | Literature Cited | major | arXiv metadata errors put wrong author names in print. S31 printed "Renee Johnston Anton Kast" as one person. A11 split "Erkang (Eric) Zhu" into two authors, "Erkang" and "Zhu". D15 split "Yingzhou (Minta) Lu" into "Yingzhou" and "Lu". | S31 PDF p.1; A11 PDF p.1; D15 PDF p.1 | Corrected in `authors.tsv` from the PDF title pages. | fixed |
| E4 | Literature Cited | minor | BibTeX parsed compound surnames wrongly. F24 "Ariño de la Rubia" sorted under "de la Rubia"; V16 "De Jonghe" became given name "Jiri De", surname "Jonghe". | F24 arXiv; V16 page byline | Braced: `Eduardo {Ariño de la Rubia}`, `Jiri {De Jonghe}`. | fixed |
| E5 | Literature Cited | minor | Initials without periods: "Zachary S Siegel" (F7), "Eliu A Huerta" (F22), "Jonathan K Pritchard" (R3). | arXiv API | Periods added (rows set to `manual`). | fixed |
| E6 | Literature Cited | minor | Straight ASCII quotes printed in titles: R12 `"fishing expedition" or "p-hacking"`, V12 (and its duplicate C6) `"Solved Issues"`. | R12 PDF p.1; V12 arXiv | Changed to curly quotes in `papers.tsv`. Wording unchanged. | fixed |
| E7 | Literature Cited | minor | Inconsistent venue labels. "Anthropic Engineering" sat beside "Anthropic Engineering blog"; "Anthropic research blog" beside "Anthropic Research blog". Accepted arXiv papers used three styles ("ICLR 2024", "ICML 2026 (arXiv)", "arXiv (ICLR 2026)"), so lines like "*ICLR 2026*, 2025" read as wrong years. A1 had "arXiv (ICLR)" with no year. | arXiv comments; conference pages (see above) | 21 venue cells normalized to "arXiv (VENUE)" and "Anthropic Engineering/Research blog": A1 to "arXiv (ICLR 2023)" (arXiv v3 comment: ICLR camera-ready); H3 to "arXiv (DL4C workshop at NeurIPS 2025)" (arXiv comment). No titles or years changed. | fixed |
| E8 | Literature Cited | minor | R19 is dated 2024 and its venue notes the *JPE Micro* 2024 publication (verified: vol. 2(3), doi 10.1086/730455). Its URL and the quoted text, however, are from the August 2022 IZA DP 15476, whose title differs slightly. | R19 PDF p.1; Crossref 10.1086/730455 | None. Lead's choice: cite the journal DOI, or date the DP 2022. | fixed (cited as the version actually quoted: `papers.tsv` year 2022, venue "IZA Discussion Paper 15476 (later published in Journal of Political Economy Microeconomics, 2024)", PDF renamed R19_Brodeur_2022_...; theme 08 README row set to 2022. Text and reference list now both read Brodeur et al. 2022; Table 1 08 row 13/4, totals 28/40) |
| E9 | Literature Cited | minor | C29 venue "Google Research technical report" is inferred from where it is hosted (storage.googleapis.com/gweb-research2023-media/pubtools). The 47-page PDF names no institution. | C29 PDF pp.1–47 (no "Google" string) | None. Acceptable; flagged for awareness. | fixed (C29 venue cell emptied in `papers.tsv`; the reference now gives authors, title, 2026 and URL only, with no institution) |
| E10 | 00_abstract l1; 02_scope l5, l29 (Table 1) | major | `papers.tsv` still holds two duplicate pairs: **A4 = T11** (arXiv 2310.01798) and **C6 = V12** (arXiv 2503.15223). "288 papers and reports" therefore counts 286 distinct works. 02_scope says the cross-theme duplicates "were removed". Neither T11 nor C6 is cited, so the bibliography is unaffected. | papers.tsv (duplicate arxiv_or_doi, url, title) | None: deleting rows changes Table 1, the abstract and the theme READMEs. Lead: drop T11 and C6 (Table 1 cells 01/2023 and 03/2025 each fall by one; totals 286, 2025+2026 = 218), or reword as "288 entries (286 distinct works)". | fixed (deleted uncited T11 and C6 from `papers.tsv` and their identical duplicate PDFs (md5 match); 04 README T11 row and mentions now point to A4, 03 README C6 to V12. Corpus count changed 288 to 286 in the abstract and §2, with 219 to 218 and a sentence on the two round-1 duplicates (141 entries, 139 distinct). Table 1 recomputed from papers.tsv: 03 = 33, 04 = 29, totals 28/40/108/110/286/55. Ledger rows 01_03 l47 and 13_17 l186 restated with quotes unchanged; one ledger row added. `verify_literature.py --all` PASS, 286 rows. §1, §14 and the endmatter do not state the count) |
| E11 | 03_concepts l21 vs 06_verification l35 | major | The same V24 result is stated two incompatible-looking ways. §3.4: "inflated the false positive rates of vision-language judges by up to 90%". §6.2: "by 20–30 points". The source's 90% is a *relative* increase, and its 20–30 is absolute points on two judges. | V24 p.1 Abstract ("up to 90%"); p.6 §5.2 ("20–30 points on GPT-4o and GLM-4.1V (70–100% relative increase)") | None (section file). Suggest §3.4: "by up to 90% in relative terms". | fixed (§3.4 now says "by up to 90% in relative terms, or 20–30 percentage points on two of them (GPT-4o and GLM-4.1V)", which matches §6.2. Ledger row added with V24 p.6 §5.2 quote; the 90% row notes the paper's relative definition) |
| E12 | 04_architecture l24 | major | `\repofile{FoundationAgents/MetaGPT}{metagpt/software\_company.py}`: `\detokenize` prints the backslash ("software\_company.py", PDF p.7), and the link goes to `.../software\_company.py`, which is broken. The same file is cited correctly in 14_implications l42. | Rendered PDF p.7 | None (section file). Use a plain `_`. | fixed (argument changed to `metagpt/software_company.py`; the PDF prints no backslash and the link resolves to .../metagpt/software_company.py) |
| E13 | 01 l5; 06 l49; 07 l9; 12 l7 | minor | SWE-Bench Pro repair is attributed three ways: "audits and contracted engineers" (§1), "Authors at Scale AI" (§6.5), "the owner of SWE-Bench Pro" (§7), "Authors from Scale AI and Reflection AI" (§12.1). The verbs vary too: "repaired or retired" against "repaired or removed". | C12 (Dan et al. 2026) | None. Pick one attribution (C12's author list) and one verb. | fixed (one attribution and one verb, both from C12: "authors from Scale AI and Reflection AI ... repaired or retired" in §1, §6.5, §7 (both places) and §12.1, and "repaired or retired" in Table 3. Ledger claims and sentence starts updated; affiliation quote "Scale AI, 2Reflection AI" (p.1) verified) |
| E14 | several | minor | Inconsistent terms. "SWE-Bench Pro" ×5 vs "SWE-bench Pro" ×3 (01, 06, 07, 12, 13). "gpt-4o" (03 l11, 11 l11) vs "GPT-4o" (06, 12). "AI Scientist v2" (08 l11) vs "AI-Scientist-v2" elsewhere. "rerun" (05 l17, 10 l11) vs "re-run" ×4. UK "modelling" (09 l15), which should be US "modeling". | grep of sections | None (section files). | fixed ("SWE-Bench Pro" throughout the prose (02, 06, 12); OpenAI's verbatim quotes keep its own spelling. Also gpt-4o to GPT-4o (03, 11), "AI Scientist v2" to AI-Scientist-v2 (08), re-run to rerun (08, 10, 14, 15), modelling to modeling (09); ledger sentence starts matched) |
| E15 | 03_concepts l11 vs 11_reliability l11 | minor | τ-bench: "succeed on fewer than half of the tasks" (§3) vs "about 61% at pass^1 … retail" (§11.2). Both are right (overall vs retail domain), but they read as a contradiction. | A9 abstract | None. Add "overall" in §3 or "in retail" in §11. | fixed (§3: "succeed on fewer than half of the tasks overall", following A9's abstract; §11 already says retail) |
| E16 | main.tex / contents.tex (p.1) | minor | On the cover page the Contents column runs into the abstract column. "Audits" (entry 8) ends 0.6 pt and "Evidence" (entry 2) 3.7 pt from the abstract text. | PDF p.1 word boxes (x 189.26 / 186.20 vs 189.90) | None. Shorten entries 2 and 8, or add `\hspace` between the minipages. | fixed (minipages 0.24 and 0.70 with an explicit `\hspace{0.06\dimexpr\linewidth+1.55in}` gap; the rendered p.1 gap from the widest Contents word to the abstract is 30.6 pt, up from 0.6 pt) |
| E17 | main.tex (`\titleformat{\section}`) | minor | Section headings hyphenate mid-word: "MEA-SURED" (§3, p.4) and "STAN-DARDS" (§12, p.19). | PDF pp.4, 19 | None. Add `\raggedright` (or `\hyphenpenalty=10000`) to the section format. | fixed (\section and \subsection formats now `\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000`; no hyphenated heading in the rebuilt PDF, e.g. no "MEA-" or "STAN-") |
| E18 | main.tex l3 | minor | `\documentclass[10.5pt]` is not a valid `article` option. The log reads "Unused global option(s): [10.5pt]" and the paper sets at 10 pt. | build/main.log | None. Use 10pt or 11pt (or the `extsizes` class) on purpose. | fixed (`\documentclass[10pt,letterpaper]{article}`) |
| E19 | main.tex (bibliography) | minor | Fully justified bibliography entries with long unbreakable URLs leave wide gaps, e.g. C14 Whitfill et al. (p.34). | PDF p.34 | None. `\renewcommand{\bibfont}{\footnotesize\raggedright}` or `\usepackage{xurl}`. | fixed (`\renewcommand{\bibfont}{\footnotesize\raggedright}`; xurl is not installed in TinyTeX, so it was not added) |
| E20 | 06 l26; 13 l55 | minor | "Figure 1" and "Figure 2" are text grids built as tables, while the similar grids are labelled Tables 1–4. | PDF pp.9, 23 | None. Style choice: relabel as tables, or keep. | fixed (decision: kept as Figures. They are conceptual diagrams, not data tables; no change) |
| E21 | 17_endmatter l31 | minor | The Disclosure links `literature/LITERATURE_REVIEW_EVIDENCE.md`, which is **untracked** in git. `LITERATURE_REVIEW.pdf` is also untracked, although `build_review.sh` says "(committed)". The public link 404s until both are committed. | `git status` | None (no commits by QA). | open (needs a commit by the lead: `literature/LITERATURE_REVIEW_EVIDENCE.md` and `literature/LITERATURE_REVIEW.pdf`, both regenerated in this pass; the fixer does not commit) |
| E22 | 10_replication l19 | minor | Unbacked absolute: "a polished report hides a process no one checked". | n/a | None. Suggest "a process that was not checked". | fixed (now "hides a process that was not checked") |
| E23 | 14_implications l40 | minor | "the author's design scopes them to the project folder and an allow-list of commands" is present tense. The repo's own CLAUDE.md §1 says the permission hook "must be scoped" before it ships, i.e. not yet. | ROOT/CLAUDE.md §1 | None. Suggest "is designed to scope them". | fixed (now "the author's design is meant to scope them"; ledger 13_17 sentence start updated) |

## Passed checks (no finding)

- **Numbers repeated across sections agree:**
  - 99.4% of 642, 480 of 731; 1.96%; about 88% of PRs; 61.8% (16 models).
  - 70.4% of 54; over 85%; 21.2% of 144; 8 of 10.
  - 9.33% and 91.49%; 49.4% (n = 1,083) and 5.5 points.
  - 0.97 vs 0.23 and $18,000; 79.4%; 12 hours.
  - 59.4% of 138 (both phrasings appear in C15); 6.4 points and 7.8% (V12 PDF p.1 says 6.4).
  - 82.7% of 81 and 22.66% to 32.51%; 22.7% to 84.0%; 41%; 30.5% and 38.5%; 2.2–6.0 points.
  - 3.13× to 1.49×; 9–13 points; GPT-5 54% to 9%; 5.4 to 3.3; 13% to 35%; Rajasekaran's more than 20× cost.
  - "OpenAI models" in §15 is supported by V3 p.8.
- **Table 1 matches `papers.tsv` exactly** (themes × years, 55 without PDF). Repository counts 216 + 34 → 237 and 32 match `PUBLIC_REPOS.md`.
- **Cross-references:** 26 labels, every `\ref` resolves (0 undefined in the log), and each target was spot-checked for the right section, table or figure.
- **Rendered Literature Cited:**
  - 162 entries, with 0 duplicate labels, titles or URLs.
  - No "et al." with one or two authors.
  - No broken glyphs; Ngân Vũ renders correctly at 250 dpi.
  - In-text labels updated by the author fixes: "Schluntz and Zhang", "Gelman and Loken", "Ariño de la Rubia and Pafka", "Von Arx et al.", "Google DeepMind".
- **Privacy:** no personal data, emails, local paths or private details in `main.tex`, the sections or the bib.

## Final script runs

- `python scripts/literature/build_bib.py --offline`: 288 entries; author sources arxiv 175, manual 72,
  first_author 37 (all uncited), crossref 4.
- `bash scripts/literature/build_review.sh`: PDF built, 35 pages; only intentional wide-box overfulls
  plus 21 pt (06 Figure 1) and 0.6 pt (13).
- `python scripts/literature/verify_literature.py --all`: PASS (288 rows, 0 problems).
- `python scripts/literature/build_evidence.py`: 1041 ledger rows; VERIFIED 752, MANUAL 289; 0 cited
  sources with no ledger row.
- `python scripts/literature/check_review.py --cites`: PASS, 162 distinct keys, 0 dangling.
