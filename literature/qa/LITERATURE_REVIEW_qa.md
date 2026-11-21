# QA re-check: Literature review (Phase 7.5)

Independent re-check, 2026-11-21. I did not write or fix the paper. Scope: every row marked fixed in
`qa_A.md` to `qa_E.md` (135 findings), the whole-paper gates, and one full read of the rendered PDF.
Baseline `ff08499`. Round 1 checked `1107c3d` plus the minor edits listed in §2. Round 2 (§6) checked the lead's fixes at `23a5ad3`.

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
| qa_B | §§6–8 | 28 | 2 | 13 | 13 | 28 | 28 (B1 confirmed in round 2 after N1; B28 confirmed with a cosmetic residual, see N10) |
| qa_C | §§9–12 | 24 | 3 | 9 | 12 | 24 | 24 |
| qa_D | abstract, §§13–17 | 27 | 2 | 14 | 11 | 25 (+2 routed) | 27 (D26 is resolved by B12; D27 is resolved by C2/C3) |
| qa_E | bibliography, consistency, PDF | 23 | 0 | 6 | 17 | 22 | 23 (E21 resolved for QA: evidence file committed; PDF held back as a release step) |
| **Total** | | **135** | **9** | **61** | **65** | **132 (+2 routed)** | **135** |

Three earlier fixes were made in one place only, and the same wording survives elsewhere: A8 in §16 and
Summary Point 1, D7 in §8.3, and C20 in §13 P5. I log these as new findings N2, N3 and N5 below rather than as
unconfirmed fixes, because the fix itself is correct where it was made.

## 2. Unconfirmed and new findings

| # | Section | Severity | Problem | Source checked | Recommended fix | Status |
|---|---|---|---|---|---|---|
| N1 (B1) | §6.6 Silent Failure | **major** | The B1 fix says PR #302 "was closed unmerged after review found **unrelated** blockers". The source does not say "unrelated", and it is wrong. The maintainer's blockers include the PR's own change that made CLI cost budgets fail fast (PR body, "Highlights") and a result gate the PR depends on. The maintainer asked for a focused PR "decoupled from the result gate". The ledger row (06.tsv l.160) says only "after review found blockers", so the sentence and its ledger row disagree. | aiming-lab/AutoResearchClaw#302: body; comments by Jiaaqiliu, 2026-07-13; state closed, merged = false | Delete "unrelated": "...was closed unmerged after review found blockers (\repo{...}{302}), and a narrower version remains open (\repo{...}{323})." | fixed by lead in `23a5ad3`; confirmed in round 2 |
| N2 | §16 Conclusion ¶1; Summary Point 1 (17_endmatter) | **major** | "The same agents appear among the successes and the failures." This is the overstatement A8 fixed in §1: MLR-Bench ran Claude Code with Claude 3.7 Sonnet, and C12 ran it with Claude Opus 5. Only the harness is the same. §1 now says so, so the conclusion and the summary box contradict §1. | S16 p.5 (Coding: "Claude Code (Claude-3.7-Sonnet)"); C12 p.2 ("Claude Opus 5 (run in Claude Code)") | §16: "The same agent harness appears among the successes and the failures." SP1: "The same agent harness, with models of different generations, appears among the successes and the failures; what differs is ...". Update the matching 13_17 ledger sentence starts. | fixed by lead in `23a5ad3` (plus my minor follow-up, §6); confirmed in round 2 |
| N3 | §8.3 Where It Works, first sentence | **major** | "The positive evidence comes almost entirely from tasks with a computable metric and a held-out set." D7 corrected this exact claim in §13 P1, Figure 2 and SP7, because AlphaEvolve (A25, cited in the same paragraph) uses an automated evaluator, not a held-out set. §8.3 kept the old wording. | A25 p.1, p.21 (evaluator); S31 p.5 (holdout) | "The positive evidence comes almost entirely from tasks with a computable metric, often scored on held-out data." | fixed by lead in `23a5ad3`; confirmed in round 2 |
| N4 | §1.3 | minor | "The models are a generation apart." Claude 3.7 Sonnet and Claude Opus 5 are more than one generation apart: the corpus itself cites Claude 4, 4.5, 4.6 and 4.8 models in between. | S16 p.5; C12 p.2; T22 (Claude Opus 4.8) | Changed to "The models are generations apart." | fixed (by me) |
| N5 (C20 residual) | §13 P5 | minor | "a watchdog in one orchestrator killed healthy sessions". C20 corrected this in §11: the gastown issue describes a session-hygiene (cleanup) plugin, not a watchdog. | gastownhall/gastown#2707 (title and body) | Changed to "a session-cleanup plugin"; 13_17.tsv l.38 sentence_start and claim updated to match. | fixed (by me) |
| N6 (D13 residual) | §12 Table 3, k-runs row | minor | "identical runs varied more than agents differed" is unscoped. D13 scoped the same F24 claim in §13 P6 to one task and to agent–model pairings. | F24 p.1 ("Identical runs of one pairing varied more than the pairings differed"; "one machine-learning task") | Changed to "on one task, identical runs varied more than agent--model pairings differed"; 11_12.tsv l.101 claim updated. | fixed (by me) |
| N7 | Ledger 01_03.tsv l.47, 13_17.tsv l.186 | minor | Both rows quote `docs/plans/07_literature_review.md` line 14 as "288 verified papers ... 219 of them". Commit 1107c3d rewrote that line, so the quote was no longer verbatim. | docs/plans/07_literature_review.md l.14 at HEAD | Quote replaced with the current verbatim line ("286 distinct verified papers ... 218 of them ...; 288 entries before two duplicates were removed in QA"). | fixed (by me) |
| N8 | Ledger 01_03.tsv l.70–73 | minor | sentence_start still read "OpenAI stopped reporting SWE-bench Verified"; after A9 the §2 text reads "stopped evaluating on". (§7 keeps "stopped reporting", which is OpenAI's own wording: "we have stopped reporting SWE-bench Verified scores".) | C15 (raw page) | sentence_start updated on 4 rows. | fixed (by me) |
| N9 | Disclosure (17_endmatter) | minor | `\url{literature/LITERATURE_REVIEW_EVIDENCE.md}` produced a relative link that is broken when the PDF is read outside the repo (LinkedIn, X, a download). | rendered PDF p.28 link annotations | Now `\href{https://github.com/sharifamlani/autonomous/blob/main/literature/LITERATURE_REVIEW_EVIDENCE.md}{...}`. The default branch `main` was checked with `gh api`, and the rebuilt PDF carries the absolute link. | fixed (by me) |
| N10 (B28 residual) | §6 Figure 1 | minor | B28 reports "no overfull boxes in §§6–8", but the log still shows `Overfull \hbox (21.38pt)` at 06_verification lines 21–23, from the unbreakable `K-Dense-AI/scientific-agent-skills #152` in the Internal/editable cell. QA-E also noted it. Not visible in the rendered page, because the table is narrower than the text block. | build/main.log; rendered p.9 | Optional: shorten to `\repo{K-Dense-AI/scientific-agent-skills}{152}` on its own line, or accept. | open (cosmetic; accepted) |
| E21 | Release | minor | `literature/LITERATURE_REVIEW_EVIDENCE.md` is now tracked (dbdf44a). `literature/LITERATURE_REVIEW.pdf` is still untracked, although `build_review.sh` says "(committed)". | `git status` | The lead commits the rebuilt PDF and evidence file (QA does not commit). | resolved for QA (evidence file committed; the PDF is held until the independent grade passes, a release step) |

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

## 5. Round-1 verdict (superseded by §6)

Round 1 was **QA FAIL** on three open majors: N1, N2 and N3. B1 was unconfirmed pending N1, and E21 was
pending a commit. §6 records how each was closed.

## 6. Round 2: re-check of the lead's fixes (`23a5ad3`)

| Item | Text now | Source check | Ledger | Result |
|---|---|---|---|---|
| N1 / B1 (§6.6) | "...was closed unmerged after review found blockers (#302), and a narrower version remains open (#323)." | #302: maintainer comment "Closing for now given the blockers above"; `state=closed`, `merged=false`. #323: `state=open`, `merged=false` (`gh api`, re-pulled). | 06.tsv l.160 claim "PR #302 closed unmerged after review found blockers" matches the sentence; l.161 (#323 open) matches. | **confirmed** |
| N2 (§16 ¶1, SP1) | §16: "The same agent harness appears among the successes and the failures, running models a generation apart." SP1: "The same agent harness appears among the successes and the failures; what differs ..." | S16 p.5: "Claude Code (Claude-3.7-Sonnet)". C12 p.2: "Claude Opus 5 (run in Claude Code)". Both match "same agent harness". **New minor (N11):** "a generation apart" contradicts §1, which says "generations apart" after N4, and it understates the gap: the corpus cites Claude 4.x models (Opus 4.1, 4.6, 4.8) between 3.7 Sonnet and Opus 5. I changed §16 to "running models generations apart" (`sections/16_conclusion.tex`, not committed). | Neither sentence carries a citation, so neither has a ledger row. The supporting S16 and C12 rows (01_03, §1) are unchanged and still match. No row in any ledger still says "same agents" or "a generation apart". | **confirmed** (after the N11 minor edit) |
| N3 (§8.3) | "The positive evidence comes almost entirely from tasks with a computable metric scored by an automated evaluator, in some cases on held-out data." | S31: selects on training data and reports on holdout datasets (ledger 07_08 l.113, VERIFIED). A25: automated evaluator, named as its main limitation (l.125–127, VERIFIED). S20: one objective metric (§8.3 rows). "In some cases on held-out data" fits S31 and is not claimed for A25. | The sentence is uncited, so it has no ledger row. The rows for the paragraph's examples (l.113, 125–127) still match their sentences. | **confirmed** |
| E21 | The evidence file is committed. The PDF is held back on purpose until the independent grade. | `git status`: only `literature/LITERATURE_REVIEW.pdf` is untracked. | n/a | **resolved for QA** (a release step, per the coordinator) |

Round-2 gates (after the N11 edit, rebuilt):

```
$ bash scripts/literature/build_review.sh
built literature/LITERATURE_REVIEW.pdf (460 KB)   overfull: 0.56pt (13 Fig. 2), 21.38pt (06 Fig. 1, N10, cosmetic) + intentional wide boxes
$ python scripts/literature/check_review.py
PASS  citations resolve: 162 distinct keys, 0 dangling
PASS  abstract <= 150 words: 150 words
FAIL  body 9,000-11,000 words: 14929 words        <- known open decision for the author; ignored per brief
PASS  >= 150 works cited: 162 distinct papers
PASS  each theme cited >= 8 distinct: {'01': 10, '02': 20, '03': 12, '04': 19, '05': 20, '06': 20, '07': 16, '08': 23, '09': 22}
PASS  >= 15 repo citations: 70 citations, 28 repos
PASS  Summary Points + Future Issues: boxes present
PASS  build: no undefined refs: 0 undefined
$ python scripts/literature/build_evidence.py
1043 ledger rows; VERIFIED 753, MANUAL 290
0 cited sources with no ledger row          (0 NOT FOUND, 0 WRONG PAGE, 0 NO PDF, 0 UNKNOWN ID)
$ python scripts/literature/verify_literature.py --all
PASS   (papers: 286 rows, 0 problems; files: 0 problems, 2 expected warnings)
```

## 7. Final verdict

**QA PASS.**
- **Blockers and majors.** 0 open blockers and 0 open majors.
- **The 135 logged findings.** All are confirmed against their sources, or resolved by a later fix (D26 by B12,
  D27 by C2/C3). E21 is resolved for QA as a release step.
- **New findings N1–N11.** All are fixed, except N10: the 21 pt overfull box in Figure 1, which is not
  visible on the page. I accept it as cosmetic.
- **Gates.** All green apart from the author's open word-count decision.

**Uncommitted edit from round 2:** `literature/review/sections/16_conclusion.tex` (N11: "a generation apart"
changed to "generations apart").

## 8. Phase 8 fixes

Fixes for the expert-reader findings in `literature/qa/PHASE8_SCORECARD.md`. Word-count cuts (m7) are not
done: that decision is waiting on the author. Not committed.

| # | section | severity | finding | source checked (ID, page) | fix made | status |
|---|---|---|---|---|---|---|
| M1 | §4.4 | major | ruflo's audit records that the fabricated attention metric was removed; the review omitted the fix | ruvnet/ruflo `docs/reviews/intelligence-system-audit-2026-05-29.md` l. 97: "randomized telemetry removed from both `attention-coordinator` copies" | Added "(the same audit records that the ``randomized telemetry'' has since been ``removed'')"; ledger row added (`04_05.tsv`, line 97) | fixed |
| m1 | Summary Point 1 | minor | Hedge on different models missing | §1.3 (S16, C12) | "The same agent harness, running different models, appears among the successes and the failures" (`17_endmatter.tex`) | fixed |
| m2 | §6.2 | minor | 49.4% is conditional on a verdict; 22.3% counts missing verdicts | T18 p. 7 ("Counting the 942 missing verdicts as failures lowers the effective false-accept rate from 49.4% to 22.3%"), p. 8 ("should be read as a verdict-quality estimate conditional on a verdict") | Added both, cited `\citep[pp.~7--8]{T18}`; two ledger rows (`06.tsv`), both VERIFIED | fixed |
| m3 | §7 | minor | 61.8% is on the held-out test split | C19 p. 1 Abstract ("the best achieves 61.8% accuracy on the test split"; "50 held-out test") | "the best of 16 models achieves 61.8% accuracy on the held-out test split of 50 applications"; ledger row updated, one added (`07_08.tsv`) | fixed |
| m4 | §8.3 | minor | AlphaEvolve 0.7% is Google's own measurement | A25 p. 14 ("Post-deployment measurements across Google's fleet confirmed the simulator results") | Added "by Google's own post-deployment measurement"; ledger row added | fixed |
| m5 | §15 / Future Issue 8 | minor | Issue 8 had no study in §15 | §11.3 (F14, F30, F32) | Added one sentence to §15 framing an independent third-party measurement of interventions per task and hours unattended; no new citations | fixed |
| m6a | Table 2 | minor | `frankbria/ralph-claude-code #91` shrunk to ~4.5 pt by `\resizebox` | rendered p. 5 (pymupdf, 200 dpi) | Removed `\resizebox`; new `\repobreak` macro in `main.tex` (breaks after `/` and `-`, current font size) applied locally with `\let\repo\repobreak`; span now 7.97 pt (footnotesize) on two lines | fixed |
| m6b | Figure 1 | minor | `K-Dense-AI/scientific-agent-skills #152,` overran by 21 pt (also N10) | rendered p. 9 | Same local `\repobreak`; the Figure 1 overfull box is gone from the build log; text stays inside the column | fixed |
| m8 | §1.2, §11.3 | minor | F30 cited as "p. 77" and "sec. 3.4.2" | F30 PDF p. 78 (quote VERIFIED there) | Both now `\citep[p.~78]{F30}`; all five F30 ledger locations set to "p. 78, §3.4.2 ..." | fixed |
| m7 | body | minor | Redundancy / word count | | Not done: waiting on the author's word-count decision | open (author decision) |

**Gates after the fixes:** `build_review.sh` builds (only remaining overfull boxes: the intentional full-width
title and boxes, plus a 0.56 pt one in §13 that predates these fixes); `check_review.py` passes everything except
the body word count (15,043); `build_evidence.py`: 1,048 rows, VERIFIED 757, MANUAL 291, 0 NOT FOUND, 0 WRONG
PAGE, 0 cited sources with no ledger row.
