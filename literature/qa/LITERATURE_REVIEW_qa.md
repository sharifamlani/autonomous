# QA re-check: Literature review (Phase 7.5)

Independent re-check, 2026-11-21. I did not write or fix the paper. Scope: every row marked fixed in
`qa_A.md` to `qa_E.md` (135 findings), the whole-paper gates, and one full read of the rendered PDF.
Baseline `ff08499`, checked at `1107c3d` plus the minor edits listed in §2.

**Method.**
- **Text.** I diffed every section word by word against `ff08499` and read each fix in its paragraph.
- **PDF sources.** Each claim was read in context on the cited page (pymupdf page text), not just matched to a quote.
- **Web sources.** I re-fetched all 20 cited web pages raw (curl, tags stripped) and ran a script that matches all
  123 web ledger quotes verbatim. All 123 matched. The S21 quote is image alt text in the raw HTML.
- **GitHub issues and PRs.** I re-pulled all 24 cited issues and PRs with `gh api` (title, body, comments,
  state, and `merged` for the PRs). All 61 issue/PR ledger quotes matched verbatim.
- **Repository files.** All 106 repo-file and local-file ledger rows were checked against the pinned clones in
  `public/`, this repo's own files, and the DataAgentBench README via `gh api`.
- **Counts.** Table 1 was recomputed from `papers.tsv`, and it matches cell for cell: 286 rows, years 2013–2026,
  218 from 2025–2026, 55 with no PDF, no duplicate IDs, arXiv IDs, URLs or titles.

## 1. Summary of the five QA files

| File | Scope | Findings | Blocker | Major | Minor | Marked fixed | Confirmed by re-check |
|---|---|---|---|---|---|---|---|
| qa_A | §§1–5 | 33 | 2 | 19 | 12 | 33 | 33 |
| qa_B | §§6–8 | 28 | 2 | 13 | 13 | 28 | 27 (B1 not confirmed; B28 confirmed with a cosmetic residual, see N10) |
| qa_C | §§9–12 | 24 | 3 | 9 | 12 | 24 | 24 |
| qa_D | abstract, §§13–17 | 27 | 2 | 14 | 11 | 25 (+2 routed) | 27 (D26 is resolved by B12; D27 is resolved by C2/C3) |
| qa_E | bibliography, consistency, PDF | 23 | 0 | 6 | 17 | 22 | 22 (E21 still open: PDF not committed) |
| **Total** | | **135** | **9** | **61** | **65** | **132 (+2 routed)** | **133** |

Three earlier fixes were made in one place only, and the same wording survives elsewhere: A8 in §16 and
Summary Point 1, D7 in §8.3, and C20 in §13 P5. I log these as new findings N2, N3 and N5 below rather than as
unconfirmed fixes, because the fix itself is correct where it was made.

## 2. Unconfirmed and new findings

| # | Section | Severity | Problem | Source checked | Recommended fix | Status |
|---|---|---|---|---|---|---|
| N1 (B1) | §6.6 Silent Failure | **major** | The B1 fix says PR #302 "was closed unmerged after review found **unrelated** blockers". The source does not say "unrelated", and it is wrong. The maintainer's blockers include the PR's own change that made CLI cost budgets fail fast (PR body, "Highlights") and a result gate the PR depends on. The maintainer asked for a focused PR "decoupled from the result gate". The ledger row (06.tsv l.160) says only "after review found blockers", so the sentence and its ledger row disagree. | aiming-lab/AutoResearchClaw#302: body; comments by Jiaaqiliu, 2026-07-13; state closed, merged = false | Delete "unrelated": "...was closed unmerged after review found blockers (\repo{...}{302}), and a narrower version remains open (\repo{...}{323})." | open (major: for a fixer) |
| N2 | §16 Conclusion ¶1; Summary Point 1 (17_endmatter) | **major** | "The same agents appear among the successes and the failures." This is the overstatement A8 fixed in §1: MLR-Bench ran Claude Code with Claude 3.7 Sonnet, and C12 ran it with Claude Opus 5. Only the harness is the same. §1 now says so, so the conclusion and the summary box contradict §1. | S16 p.5 (Coding: "Claude Code (Claude-3.7-Sonnet)"); C12 p.2 ("Claude Opus 5 (run in Claude Code)") | §16: "The same agent harness appears among the successes and the failures." SP1: "The same agent harness, with models of different generations, appears among the successes and the failures; what differs is ...". Update the matching 13_17 ledger sentence starts. | open (major: for a fixer) |
| N3 | §8.3 Where It Works, first sentence | **major** | "The positive evidence comes almost entirely from tasks with a computable metric and a held-out set." D7 corrected this exact claim in §13 P1, Figure 2 and SP7, because AlphaEvolve (A25, cited in the same paragraph) uses an automated evaluator, not a held-out set. §8.3 kept the old wording. | A25 p.1, p.21 (evaluator); S31 p.5 (holdout) | "The positive evidence comes almost entirely from tasks with a computable metric, often scored on held-out data." | open (major: for a fixer) |
| N4 | §1.3 | minor | "The models are a generation apart." Claude 3.7 Sonnet and Claude Opus 5 are more than one generation apart: the corpus itself cites Claude 4, 4.5, 4.6 and 4.8 models in between. | S16 p.5; C12 p.2; T22 (Claude Opus 4.8) | Changed to "The models are generations apart." | fixed (by me) |
| N5 (C20 residual) | §13 P5 | minor | "a watchdog in one orchestrator killed healthy sessions". C20 corrected this in §11: the gastown issue describes a session-hygiene (cleanup) plugin, not a watchdog. | gastownhall/gastown#2707 (title and body) | Changed to "a session-cleanup plugin"; 13_17.tsv l.38 sentence_start and claim updated to match. | fixed (by me) |
| N6 (D13 residual) | §12 Table 3, k-runs row | minor | "identical runs varied more than agents differed" is unscoped. D13 scoped the same F24 claim in §13 P6 to one task and to agent–model pairings. | F24 p.1 ("Identical runs of one pairing varied more than the pairings differed"; "one machine-learning task") | Changed to "on one task, identical runs varied more than agent--model pairings differed"; 11_12.tsv l.101 claim updated. | fixed (by me) |
| N7 | Ledger 01_03.tsv l.47, 13_17.tsv l.186 | minor | Both rows quote `docs/plans/07_literature_review.md` line 14 as "288 verified papers ... 219 of them". Commit 1107c3d rewrote that line, so the quote was no longer verbatim. | docs/plans/07_literature_review.md l.14 at HEAD | Quote replaced with the current verbatim line ("286 distinct verified papers ... 218 of them ...; 288 entries before two duplicates were removed in QA"). | fixed (by me) |
| N8 | Ledger 01_03.tsv l.70–73 | minor | sentence_start still read "OpenAI stopped reporting SWE-bench Verified"; after A9 the §2 text reads "stopped evaluating on". (§7 keeps "stopped reporting", which is OpenAI's own wording: "we have stopped reporting SWE-bench Verified scores".) | C15 (raw page) | sentence_start updated on 4 rows. | fixed (by me) |
| N9 | Disclosure (17_endmatter) | minor | `\url{literature/LITERATURE_REVIEW_EVIDENCE.md}` produced a relative link that is broken when the PDF is read outside the repo (LinkedIn, X, a download). | rendered PDF p.28 link annotations | Now `\href{https://github.com/sharifamlani/autonomous/blob/main/literature/LITERATURE_REVIEW_EVIDENCE.md}{...}`. The default branch `main` was checked with `gh api`, and the rebuilt PDF carries the absolute link. | fixed (by me) |
| N10 (B28 residual) | §6 Figure 1 | minor | B28 reports "no overfull boxes in §§6–8", but the log still shows `Overfull \hbox (21.38pt)` at 06_verification lines 21–23, from the unbreakable `K-Dense-AI/scientific-agent-skills #152` in the Internal/editable cell. QA-E also noted it. Not visible in the rendered page, because the table is narrower than the text block. | build/main.log; rendered p.9 | Optional: shorten to `\repo{K-Dense-AI/scientific-agent-skills}{152}` on its own line, or accept. | open (cosmetic; accepted) |
| E21 | Release | minor | `literature/LITERATURE_REVIEW_EVIDENCE.md` is now tracked (dbdf44a). `literature/LITERATURE_REVIEW.pdf` is still untracked, although `build_review.sh` says "(committed)". | `git status` | The lead commits the rebuilt PDF and evidence file (QA does not commit). | open (needs lead commit) |

**Checked and confirmed, no change** (beyond what the five QA files list):
- **AutoResearchClaw and commit0.** #302 and #100 are closed and unmerged (`merged=false`); #323 is open.
- **commit0 #100.** The maintainer's comment reads "This PR isn't correct yet".
- **karpathy/autoresearch #599.** It is open, and it offers a "Minimal reproducer (stdlib only)".
- **Issue states quoted in the text.** All 24 match: K-Dense #152, AI-Scientist-v3 #5, commit0 #113,
  uditgoenka/autoresearch #115, gastown #2707 and planning-with-files #240 are closed; sandbox-runtime #97,
  paperclip #13532, InfiAgent #28 and #29, and AI-Scientist-v2 #133 are open.
- **Rechecked numbers.** C29 (22.7%→84.0% is claude-fable-5-1; multipliers 2.6×–6.7× across six agents), V12
  (6.4 points combined; three tools on Verified), T18 (0.79/0.24; "not significantly better", +0.5, p = 0.20;
  verifier read-only), T25 (79.70 vs 76.65), T20 (57.2/63.3/55.5; cost 3.3→6.5), T22 (1.17–1.18× the oracle),
  H17 (81.0%, 70.3%, "contributing to"), H1 (2.4%, p = 21%, at most 19%), H23 (n = 10,000 internal employee
  traffic), F14 (internal users, Aug–Dec, 5.4→3.3), F32 (Mar–Oct; 23→46%, 13→35%; "humans are still
  central"), F3 (Qwen3-32B; GPT-5 over 2,100 steps), D23 (Qwen 4B/27B on commodity hardware plus Gemini 3.7
  Flash; LLM judge; "All data leakage modes lead to improved rankings"), D26, D14, D21, C5, C16, S3, S28,
  V3, V17, V19, V24, V31, C15 and R3.
- **Harbor parity summary.** 14 merged single-run rows; line 3 is claude-haiku-4-5 with 43.7 / 62.6.
- **Bibliography spot checks.** Bylines for A15, V16, V17 and F35, and the corrected names in S31, D15 and A11,
  match the sources.

## 3. Gate results (after the minor edits above, rebuilt)

```
$ bash scripts/literature/build_review.sh
wrote literature\review\references.bib: 286 entries; author sources {'arxiv': 175, 'manual': 72, 'first_author': 37, 'crossref': 4}
built literature/LITERATURE_REVIEW.pdf (460 KB)
      1 Overfull \hbox (0.55539pt too wide) in paragraph at lines 32--54     (13 Figure 2, invisible)
      1 Overfull \hbox (21.38405pt too wide) in paragraph at lines 21--23    (06 Figure 1, see N10)
      (remaining 112pt / 224pt boxes are the intentional wide title/abstract/box layout)

$ python scripts/literature/check_review.py
PASS  citations resolve: 162 distinct keys, 0 dangling
PASS  abstract <= 150 words: 150 words
FAIL  body 9,000-11,000 words: 14918 words        <- known open decision for the author; ignored per brief
PASS  >= 150 works cited: 162 distinct papers
PASS  each theme cited >= 8 distinct: {'01': 10, '02': 20, '03': 12, '04': 19, '05': 20, '06': 20, '07': 16, '08': 23, '09': 22}
PASS  >= 15 repo citations: 70 citations, 28 repos
PASS  Summary Points + Future Issues: boxes present
PASS  build: no undefined refs: 0 undefined

$ python scripts/literature/build_evidence.py
1043 ledger rows; VERIFIED 753, MANUAL 290
0 cited sources with no ledger row
wrote literature\LITERATURE_REVIEW_EVIDENCE.md
   -> 0 NOT FOUND, 0 WRONG PAGE, 0 NO PDF, 0 UNKNOWN ID (no row carries those statuses)

$ python scripts/literature/verify_literature.py --all
links: 0 broken relative links
readmes: 9 folders, 0 problems
papers: 286 rows, 0 problems
files: 286 rows checked, 0 problems, 2 warnings   (the review PDF and build/main.pdf are not in papers.tsv; expected)
candidates: 10 files, 250 rows, 0 problems
PASS
```

Independent ledger checks (my scripts, scratchpad):
- Web quotes: 123 of 123 verbatim.
- Issue/PR quotes: 61 of 61 verbatim.
- File quotes: 106 rows. The stale plan-doc quote (N7) is now fixed. The two mini-swe-agent rows flagged by my
  checker are a CSV-quoting artifact in my reader; the raw TSV quote is verbatim.

## 4. Rendered PDF read (35 pages)

I read every page as extracted text and looked at renders of the pages with tables, figures and the cover
(pp.1, 4, 5, 9, 21, 23, 24).
- **Layout.** The cover has a clear gap between Contents and Abstract (E16 fix holds). No headings are
  hyphenated, and no backslash shows in any repo path. The tables fit their pages.
- **Text and links.** There is no garbled text, no "??", and no broken reference or citation.
- **Bibliography.** The 162 entries render cleanly. Long author lists are truncated after seven names
  with "et al.", and the R19 and C29 entries match their fixes.

Overclaims and contradictions found in this read are N2 and N3 above, plus the minor items N4–N6. I found
nothing unfair to a named project or lab beyond N1.

## 5. Verdict

**QA FAIL.** All gates are green apart from the known word-count decision, but these items are open:
1. **N1 (major).** §6.6: remove "unrelated" from the PR #302 sentence, so it matches the source and ledger row 160.
2. **N2 (major).** §16 ¶1 and Summary Point 1: "The same agents" should become "the same agent harness"
   (A8 residual; it now contradicts §1).
3. **N3 (major).** §8.3, first sentence: "a computable metric and a held-out set" should become "a computable
   metric, often scored on held-out data" (D7 residual).
4. **B1** is not confirmed until N1 is fixed.
5. **E21 (minor, release step).** Commit `literature/LITERATURE_REVIEW.pdf` (and the regenerated evidence file).
6. **N10 (minor, cosmetic).** The Figure 1 overfull box. It is acceptable as is, and listed only for completeness.

There are 0 open blockers. All three majors are one-phrase text edits with no effect on numbers or ledger
quotes, except the 13_17 sentence starts for N2. After the fixer applies them, I re-check only those three
sentences plus the gates.

**Minor edits I made (not committed):**
- `sections/01_introduction.tex` (N4), `sections/13_synthesis.tex` (N5), `sections/12_measurement.tex` (N6)
  and `sections/17_endmatter.tex` (N9).
- `ledger/01_03.tsv` (N7, N8), `ledger/11_12.tsv` (N6) and `ledger/13_17.tsv` (N5, N7).
- Rebuilt PDF and evidence file.
