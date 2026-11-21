# QA A: Sections 1 to 5 (Introduction, Scope, Concepts, Architecture, Harness)

Phase 7.5 pre-release QA, 2026-11-21. Scope: `literature/review/sections/01_introduction.tex` to
`05_harness.tex`, ledgers `literature/review/ledger/01_03.tsv` and `04_05.tsv`.

**Method.** Every PDF-quoted claim was read in context in the PDF (pymupdf page text), not only matched
by the script. Every web row was re-fetched raw (curl, tags stripped) and the quote matched verbatim.
Every GitHub row was re-read with `gh api` (issue body, title, state; file contents at HEAD). Corpus
counts were recomputed from `literature/papers.tsv`, `public/_candidates/*.tsv`,
`public/candidates.tsv`, `public/manifest.tsv`, `public/_README.md`, `PUBLIC_REPOS.md` and `ROADMAP.md`.

**Rows checked:** 261 ledger rows (01_03: 113, 04_05: 148, including 15 rows added by QA); 115 citation
instances across §§1 to 5 (23 + 3 + 27 + 32 + 30), all with a ledger row in their own section.

**Result:** 33 findings: 2 blocker, 19 major, 12 minor. All fixed.

| # | section | severity | finding | source checked (ID, page) | fix made | status |
|---|---|---|---|---|---|---|
| 1 | 4.3 | blocker | "only 0.24 of the planner's spec-critical tokens reached the executor's tool calls" misattributes the number: 0.24 is mean recall of spec-critical tokens in the executor channel (0.79 in the planner channel); the share of the planner's tokens retained is 0.21, and it is a lower bound | T18, p. 6, §3.4 | Text now says recall fell from 0.79 in the planner's channel to 0.24 in the executor's tool inputs and outputs; ledger claim and number updated | fixed |
| 2 | 5.2 | blocker | The 81.0% false-negative rate was attributed to the in-project-edit gap ("because 36.8% ... never reached the classifier"). The paper says the gap is "contributing to" the rate, and on the actions the classifier did evaluate the rate was still 70.3% | H17, p. 1, Abstract | Causal "because" removed; added the 70.3% figure; "deliberately ambiguous" from source; two ledger rows added | fixed |
| 3 | 1.2 | major | Ledger quote NOT FOUND (9.33%): line-break hyphen ("oc- curs") copied into the quote | T23, p. 2 | Quote de-hyphenated; now VERIFIED | fixed |
| 4 | 1.2 | major | "reached a visible resolution in only 9.33%" can read as 90% unresolved; the paper says the rest have unknown status and these "reflect observable within-session outcomes rather than true resolution rates" | T23, p. 7, RQ2 | Added "(for the rest, the logs show no outcome)"; ledger row added | fixed |
| 5 | 1.2 | major | Ledger quote NOT FOUND (61.8%): hyphen break inside "GPT- 5.3-Codex" | C19, p. 1, §1 | Quote split with "..." around the model name; now VERIFIED | fixed |
| 6 | 3.1 | major | Ledger quote NOT FOUND: hyphen break "mech- anisms" | H2, p. 1, Abstract | Quote de-hyphenated; now VERIFIED | fixed |
| 7 | 3.4 (Table 2) | major | Ledger quote NOT FOUND: hyphen break "auto- mated" | S10, p. 1, Abstract | Quote de-hyphenated; now VERIFIED | fixed |
| 8 | 1.3 | major | Thesis sentence: "the same agents appear on both sides of it: Claude Code produced the placeholder results ... and, running Claude Opus 5, the 99.4%". MLR-Bench ran Claude Code with Claude 3.7 Sonnet; C12 ran it with Claude Opus 5. Same harness, models a generation apart, so "same agents" overstates and hides a capability difference | S16, p. 5 (evaluated models); C12, p. 2 | Rewritten: "The same agent harness appears on both sides ... while running Claude 3.7 Sonnet ... The models are a generation apart, so capability explains part of the difference, but not its pattern." Ledger row added | fixed |
| 9 | 2.3 | major | OpenAI "stopped reporting" SWE-bench Verified "after frontier models proved able to reproduce the original human-written fixes": the post says models reproduced the gold patch "or verbatim problem statement specifics for certain tasks"; title is "no longer evaluate" | C15 (web, re-fetched) | Now "stopped evaluating on ... every frontier model it tested proved able to reproduce the original human-written fix, or verbatim details of the problem statement, for certain tasks" | fixed |
| 10 | 2.3 | major | "weaknesses in SWE-bench's patch validation inflated reported resolution rates by 6.4 percentage points" generalizes: it is an extrapolated estimate, averaged over three tools on SWE-bench Verified | V12, p. 1 Abstract; p. 2 §1 | Scoped to three tools on SWE-bench Verified, "estimated", "on average"; two ledger rows added | fixed |
| 11 | 4.1 | major | "An annotation study of 1,642 execution traces found failure rates of 41% to 86.7%" stitches two parts of the paper: the rates come from Figure 5, per-system benchmark runs that "are not directly comparable", not from the 1,642 annotated traces | T7, p. 2 §1; p. 19 Fig. 5 caption | Reworded to the authors' report of failure rates "on benchmarks that differ by system"; ledger row added | fixed |
| 12 | 4.2 | major | Selective: "six multi-agent workflows ... found five trailing by 1.71–8.76 points" omits that the sixth (EvoAgent) beat the single-agent controller in all three runs (79.70% vs 76.65%) | T25, p. 1, Abstract | Added "one ahead by about three points and the other five trailing"; ledger row added | fixed |
| 13 | 4.2 | major | "the Terminal-Bench consortium, which includes Anthropic" misstates the authorship: a Stanford and Laude Institute-led author list with one Anthropic author | C18, p. 1, author block | Now "the Terminal-Bench authors, led from Stanford and the Laude Institute, conclude"; ledger quote extended | fixed |
| 14 | 4.3 | major | "because tests written alongside the code 'can be biased by the code'" states as cause what the authors offer as one of "two possible reasons" | T4, p. 9, §4.5 | Now "which its authors attribute in part to tests ... that 'can be biased by the code'"; ledger quote extended | fixed |
| 15 | 4.3 | major | "isolation without worktrees scored 55.5" mislabels the condition: soft isolation is engineers sharing one workspace, separated only by instructions | T20, p. 6, §4.1 | Now "engineers sharing one workspace, kept apart only by instructions, scored 55.5"; ledger row added | fixed |
| 16 | 4.3 | major | Absolute "Parallel builders help only when isolation and executed tests discipline the merge" goes beyond three studies (T20's own Commit0-Lite shared-workspace run beat the single agent) | T19, T22, T20 | Hedged: "In these studies, parallel builders helped only when ..." | fixed |
| 17 | 4.4 | major | Fairness: "none of the four repositories reports a measured success rate" without noting that MetaGPT's results are published in its papers (our own `public/_README.md` says so) | `public/_README.md` line 578; T2 | Added "(MetaGPT's results are in its papers)"; ledger quote extended | fixed |
| 18 | 4.4 | major | Fairness: ruflo's audit is quoted only for the fabricated speedup; the same audit, opening "The learning loop is real", confirms the core loop works. The speedup is a Flash Attention multiplier | ruvnet/ruflo `docs/reviews/intelligence-system-audit-2026-05-29.md` lines 12–13 | Now "ruflo's own audit, while confirming that its core learning loop works, found a claimed attention speedup 'fabricated ...'"; ledger row added | fixed |
| 19 | 5.1 | major | "developer-written files ... helped every agent tested except Claude Code" overstates: the gain is 2.4% on average with p = 21% (not significant) | H1, p. 6, §4 | Now "raised success by a non-significant 2.4% on average, helping every agent tested except Claude Code, at up to 19% more cost"; ledger row added | fixed |
| 20 | 5.1 | major | "losing its five-round cap so that one task ran 18 fix rounds" asserts causation; the issue states the evidence "does not establish cause" | obra/superpowers#2481 (closed), body | Causal "so that" removed; reporter's caveat added; ledger row added | fixed |
| 21 | 5.2 | major | Fairness/tense: "one plugin's safety hooks 'appear installed and simply never fire' on Windows" presents a closed issue as a current defect | uditgoenka/autoresearch#115 (state: closed) | Now "a since-closed issue reported that ..."; ledger location records state | fixed |
| 22 | 1.4 | minor | R9 quote attached to the wrong verb ("reach divergent results, 'even by experts ...'"); source: variation "may be difficult to avoid, even by experts with honest intentions" | R9, p. 2, Abstract | Now "a variation that 'may be difficult to avoid, even by experts with honest intentions'" | fixed |
| 23 | 1.5 | minor | UK spelling "programme" | n/a | "program" | fixed |
| 24 | 3.1 | minor | The source's term is "harness engineering", not "harness" | H2, p. 1 | "the emerging term harness engineering broadens attention" | fixed |
| 25 | 3.2 | minor | 99.9th-percentile turn figure lacked its window and population (interactive sessions, Oct 2025 to Jan 2026) | F14 (web, re-fetched) | Window and "interactive Claude Code sessions" added; ledger row added | fixed |
| 26 | 3.2 | minor | OpenAI calls the 13% to 35% figures "estimated success" | F32 (web, re-fetched) | "estimated zero-intervention success"; ledger quote extended to include "estimated success rose" | fixed |
| 27 | 4 intro | minor | Uncited superlative "the most visible design choice" | n/a | "one of the most visible design choices" | fixed |
| 28 | 4.1 | minor | UK spellings "Programme" (subsection title), "modelling" | n/a | "Program", "modeling" | fixed |
| 29 | 4.2 | minor | "helped a weak model": the paper says weaker models (Llama 3.3, Llama 4 Maverick) | A26, p. 15, p. 16 | "helped weaker models"; ledger row added | fixed |
| 30 | 4.3 | minor | "1.18 times the single agent's tokens": source gives 1.17 to 1.18 times the oracle's effective token cost | T22, p. 8, §4.1 | "1.17 to 1.18 times the single agent's token cost"; ledger claim/number updated | fixed |
| 31 | 4.4 | minor | Overfull hbox (19 pt) from the long `\repofile` path in the Practitioner Evidence paragraph | build log | Paragraph wrapped in `sloppypar`; overfull gone | fixed |
| 32 | 5.2 | minor | "0.4% false-positive rate on real traffic": the dataset is internal Anthropic employee traffic (n = 10,000) | H23 (web, re-fetched) | "on internal traffic"; ledger row added | fixed |
| 33 | 5.2 / ledger | minor | Sandbox-disable issue applies "in sandbox auto-allow mode" (scope missing); separately, the superpowers#2481 title quote in `04_05.tsv` carried CSV doubled quote marks (`"""Five ..."" ..."`) that are not in the source | anthropics/sandbox-runtime#97 (open); obra/superpowers#2481 title | "in auto-allow mode" added; ledger quote cleaned to the verbatim title text | fixed |

## Checked, no change needed

- **Table 1 (`tab:corpus`)**: every cell recomputed from `papers.tsv` (folder × year, `file` not `.pdf`):
  all 54 theme cells and the totals row (28 / 41 / 109 / 110 / 288 / 55) match. 288 IDs unique; years
  2013–2026; 219 from 2025–2026; all 288 `verified = yes`. The 55 no-PDF rows are blogs, docs and web
  reports (`_NOTE.md` files), as the text says.
- **Corpus rounds**: 15 + 64 + 62 = 141 (ROADMAP 4.6, 5.1, 5.2; 5.3 records 141); +115 after 12
  duplicates (5.5); +32 lab sweep (5.6) = 288. The 14 labs listed match row 5.6.
- **Repositories**: `_candidates/01–09.tsv` sum to 216; `10_sweep2.tsv` has 34; `candidates.tsv` has 237
  unique; `manifest.tsv` pins 32 repos with commits; `public/_README.md` has 32 write-ups.
- **Web rows** (S20, C15, V31, A15, F14, F32, T16, H23, H24, H13): every quote found verbatim in the raw
  page. (A15's "Agents, on the other hand" only fails an automated match because the page renders
  "Agents" as a link; checked by hand.)
- **GitHub rows**: issue text and state confirmed for ralph-claude-code#91 (closed), BMAD-METHOD#95
  (closed), spec-kit#75 (closed), paperclip#13532 (open, as stated), ruflo#958 (comment by
  mattpainter701, verbatim), wshobson/agents#93, superpowers#2481, sandbox-runtime#97 (open, as
  stated), planning-with-files#240, deer-flow#4651 (RFC, as stated). File quotes confirmed at HEAD:
  gastown README line 15, MetaGPT `software_company.py` lines 19 and 60, planning-with-files
  `docs/attestation-locking.md` line 26, claude-code-action `docs/security.md` line 60, ruflo audit line 13.
- **Lab labels**: Kosmos (Edison Scientific), S20 (Anthropic), F30 (Google DeepMind), TeamBench (MIT,
  Google Research, Google DeepMind), H11 (Google Research, Google DeepMind, MIT), Gaia2 (Meta), H3
  (JetBrains Research), H1 (ETH Zurich), H20 (Meta, Harvard), H17 (HKUST, ZJUT, ETH), T9 (single
  author), T25 (universities): all match the PDFs' author blocks.
- **Build**: `latexmk` compiles (0 undefined citations or references); no overfull boxes left in §§1–5.

## Final script results

- `python scripts/literature/build_evidence.py`: 1041 ledger rows; VERIFIED 752, MANUAL 289; 0 cited
  sources with no ledger row. For §§1–5: 01_03 = 66 VERIFIED, 47 MANUAL; 04_05 = 109 VERIFIED, 39
  MANUAL; no WRONG PAGE, NOT FOUND, NO PDF or UNKNOWN ID.
- `python scripts/literature/check_review.py --cites`: PASS, 162 distinct keys, 0 dangling.
