# Phase 8 scorecard: independent grading of the literature review

**Article:** *Verification, Not Capability: What the Evidence Says About Autonomous Agents That Build
Software and Do Research* (`literature/LITERATURE_REVIEW.pdf`, built 2026-11-21 with
`bash scripts/literature/build_review.sh`, 35 pages, 0 undefined references).
**Criteria:** `docs/plans/07_literature_review.md`, "Evaluation criteria (graded in Phase 8 by an
independent evaluator)". **Evaluator:** an independent sub-agent that did not write or QA the review. It
measured every criterion itself. It did not read the QA files or use the claims ledger to locate sources.
**Date:** 2026-11-21.

## Scorecard

| Criterion | Threshold | Result | Evidence | PASS/FAIL |
|---|---|---|---|---|
| 1. Every citation is real | 0 cite keys missing from `papers.tsv` | 162 distinct keys, 0 dangling. Extra check: all 24 cited GitHub issues/PRs exist, and their open/closed state matches the text | `python scripts/literature/check_review.py --cites`: "PASS citations resolve: 162 distinct keys, 0 dangling"; `gh api repos/<r>/issues/<n>` for all 24 | **PASS** |
| 2. Numbers match their sources | ≥ 20 of 20 randomly drawn numbers match | **20 / 20** match on value, unit, condition and sample | Draw table below. Each number was located in the source PDF page (pymupdf) or the raw web page / GitHub file | **PASS** |
| 3. Every claim has verbatim evidence | 0 cited sources without an entry; 0 NOT FOUND / WRONG PAGE; spot checks hold | 1,043 rows (VERIFIED 753, MANUAL 290); 0 sources without a row; 0 NOT FOUND, 0 WRONG PAGE. Spot checks: 10/10 MANUAL and 10/10 VERIFIED rows support the claim as written | `python scripts/literature/build_evidence.py` exit 0 ("0 cited sources with no ledger row"). The regenerated file has no git diff. Spot-check list below | **PASS** |
| 4a. Abstract | ≤ 150 words | 150 words (script), and 150 whitespace tokens from the PDF | `check_review.py` | PASS |
| 4b. Summary Points + Future Issues | both present | Both boxes present (10 points, 8 issues) | `check_review.py`; PDF pp. 27–28 | PASS |
| 4c. Works cited | ≥ 150 | 162 distinct papers | `check_review.py` | PASS |
| **4d. Word count** | **9,000–11,000** | **14,929 body words** (Sections 1–16, tables and figures excluded): **3,929 over the ceiling (+36%)**. Counting table, figure and margin-note text from the PDF gives about 17,400 | `check_review.py`: "FAIL body 9,000-11,000 words: 14929 words". Largest sections: §6 2,080, §8 1,231, §13 1,082 | **FAIL** |
| 4. Structured as a review article (overall) | all of 4a–4d | 4d fails | as above | **FAIL** |
| 5. Covers the corpus | each of 9 themes ≥ 8 distinct; ≥ 15 repo citations | Themes 01:10, 02:20, 03:12, 04:19, 05:20, 06:20, 07:16, 08:23, 09:22; 70 repo citations of 28 repos | `check_review.py` | **PASS** |
| 6. Source quality is labelled | sample of 20 numbers in §§4–12 each labelled where it matters | 20/20 acceptable (18 clear, 2 borderline: CaMeL 77% and least-privilege 1.0%, flagged only by "on their benchmarks") | Draw table below | **PASS** |
| 7. Kit implications are traceable | every row of Table 4 cites ≥ 1 paper or repo | 10 of 10 rows cite ≥ 2 papers or repos | PDF p. 24, Table 4 | **PASS** |

**Corpus counts (extra check):** Table 1 matches `papers.tsv` exactly in every cell: 286 papers, 2013–2026,
218 from 2025–26, and 55 with no PDF.

## Criterion 2: the random draw

**Method.** I extracted the text of PDF pages 1–26 (Abstract through Section 16) with pymupdf, removed the
running heads, page numbers and the contents block, and collapsed whitespace. I took every numeric token
(regex `[-−]?\$?\d[\d,]*(\.\d+)?(%|×| points| percentage points)?`) and dropped section/table/figure numbers,
citation years, calendar years, section headings, `p.`/`sec.` locators and issue numbers. That left
**724 candidates**. I then drew `random.Random(20261121).sample(range(724), 45)` and took the draws in
sample order. Before looking at any source, I fixed a rule for which draws to skip: a digit inside a model
name (GPT-5), a section heading, a citation year that the filter missed, or a Table 1 cell. Table 1 cells
are counts of this review's own corpus, not numbers quoted from a source; they were checked separately
against `papers.tsv`. **Seed 20261121**. Skipped: draws 6, 8, 22, 25, 27, 30, 44 (Table 1), 11 (GPT-5),
14 (heading), 29 and 38 (citation years). The first 20 eligible draws are below. Script:
`scratchpad/draw.py` (session scratchpad, not committed).

| # | Number in review (context) | Source | Where I found it | Found | Match |
|---|---|---|---|---|---|
| 1 | 29 teams, red cards (§10.1) | Silberzahn 2018 [R9] | PDF p. 2 abstract | "29 different analysis teams… 0.89 to 2.93… Twenty teams (69%)… nine" | ✓ |
| 2 | 22,949 vs 7,183 tokens (§4.1) | Qian 2023 [T1] | p. 6, Tables 1 and 3 | ChatDev 22,949.4450; GPT-Engineer 7,182.5333; quality 0.3953 vs 0.1419 | ✓ |
| 3 | 1,750 trajectories on 50 SWE-bench Verified tasks (§6.1) | Mehta 2026 [F20] | p. 1 abstract | "Across 1,750 trajectories on 50 SWE-bench Verified tasks" | ✓ |
| 4 | inflate resolution rates by 6.4 points (§6.5) | Wang 2025c [V12] | p. 1, p. 2 | "inflation of reported resolution rates by 6.4 absolute percent points… on average" | ✓ |
| 5 | delegated PRs 7.5% → 11.9%, Apr–Sep 2026 (§11.3) | Google DeepMind 2026 [F30] | PDF p. 78 | "increased from 7.5% in April to 11.9% in September 2026" | ✓ |
| 6 | o3 reward-hacked 39 of 128 RE-Bench runs (30.4%) (§6.4) | Von Arx 2025 [V17] | metr.org raw page | table: 39 / 128 / 30.4% | ✓ |
| 7 | best of 16 models (Abstract) | Tran 2026 [C19] | p. 1 | "Across 16 frontier models, the best achieves 61.8%" | ✓ |
| 8 | +0.5 pts, p = 0.20, 68 of 155 tasks, Gemini-3 Flash (§4.2) | Kim 2026 [T18] | p. 6 | "+0.5 points (p = 0.20…), team wins on 68 of 155 tasks"; "155-task reference ablation with Gemini-3 Flash" | ✓ |
| 9 | hackable share near 100% → under 10%, four benchmarks (§6.5) | Wang 2026 [V27] | p. 1 | "from near 100% to under 10% on four benchmarks" | ✓ |
| 10 | at least 59.4% of 138 problems o3 did not consistently solve (§6.5) | OpenAI 2026a [C15] | openai.com raw page | "audit of 138… o3 did not consistently solve"; "at least 59.4%… flawed test cases that reject functionally correct submissions" | ✓ |
| 11 | Pearson r = 0.72 (§3.4) | Tran 2026 [C19] | p. 1, p. 7 | "Pearson r=0.72" | ✓ |
| 12 | SD > 1.5 points even at temperature 0 (§11.2) | Bjarnason 2026 [F19] | p. 1 | "exceeding 1.5 percentage points even at temperature 0" | ✓ |
| 13 | 323 of 1,968 tasks (16%) (§6.5) | Zhong 2026 [T24] | p. 1 | "audit 1,968 tasks… find 323 (16%) hackable… given only the task description" | ✓ |
| 14 | 100 specifications, 964 workflows (§7) | Tran 2026 [C19] | p. 1, Table 3 p. 4 | "100 web application specifications… 964 browser-based workflows" | ✓ (see note a) |
| 15 | about 30% of SWE-Bench Pro tasks broken; recommendation retracted (§6.5) | OpenAI 2026d [V31] | openai.com raw page, July 8, 2026 | "~30% of SWE-bench Pro tasks are broken"; "we retract our earlier recommendation" | ✓ |
| 16 | roughly 1,200 agents on a message board (§6.4) | Greenblatt 2026 [F35] | metr.org raw page | "roughly 1200 agents… participated on this message board" | ✓ |
| 17 | GPT-4o about 61% pass^1 → about 25% pass^8, retail (§11.2) | Yao 2024 [A9] | p. 2 | "∼61% on τ-retail… as low as ∼25% for pass^8 on τ-retail" | ✓ |
| 18 | script-bundling skills 2.12× as likely (§5.1) | Liu 2026b [H22] | p. 1 | "2.12× more likely… (OR=2.12, p<0.001)" | ✓ |
| 19 | 22.7% → 84.0%, 2.6–6.7× across six agents (§7) | Trengrove 2026 [C29] | p. 12 table | claude-fable-5-1 22.7% → 84.0%; multipliers 3.7, 6.7, 5.6, 2.6, 4.5, 3.2 | ✓ |
| 20 | ReplicationBench best model averaged 22% (§8.3) | Ye 2025 [S26] | p. 7 | "Claude 4.5 Sonnet, achieves an average score of 22%" | ✓ |

**Result: 20 / 20.** Note a: 964 is correct. In the same §7 sentence, the 61.8% applies to the 50-app
held-out test split (473 workflows), and "accuracy" is the mean per-application share of passing
workflows (C19 p. 5). The sentence reads as if 61.8% were measured over all 964 workflows; see reader
finding m3.

## Criterion 3: evidence spot checks

The rows were drawn with `random.Random(8)`: 10 from the 290 MANUAL rows and 10 from the 753 VERIFIED rows
of `LITERATURE_REVIEW_EVIDENCE.md`. Each quote was re-fetched myself (WebFetch of the raw page,
`gh api`, local file or PDF page) and checked against the claim as written.

| Row | Source | My check | Supports claim? |
|---|---|---|---|
| M 6.4.28 | METR reward-hacking page [V17] | "appended four different instructions… Optimize LLM Foundry"; "ran the model 20 times for each prompt" | ✓ |
| M 9.11 | ucbepic/DataAgentBench README | row 1, tuned ✓, 0.9917; footnote 9: "tells the agent how to solve that query" | ✓ |
| M 9.14 | same | row 12 is the first untuned row, 0.8858 | ✓ |
| M §4.68 | this repo, `public/_README.md` l. 578 | "No benchmark numbers or results are in the repo" | ✓ (the text frames it as "our reading") |
| M 6.1.16 | Anthropic harness post [H13] | "Claude marks features as done prematurely." | ✓ |
| M 2.5 | `literature/README.md` l. 65 | "verified = the title, first author and year were checked" | ✓ |
| M 2.26 | OpenAI page [C15] | "at least 59.4% of the audited problems have flawed test cases" | ✓ |
| M §4.74 | FoundationAgents/MetaGPT `software_company.py` l. 19 | `run_tests=False,`; `QaEngineer` hire commented out | ✓ |
| M 6.6.2 | SakanaAI/AI-Scientist-v2 #133 | "rejects gemini-2.5-flash… every phase3.log (n=10)… v2 never actually reviews its own figures" | ✓ |
| M 14.18 | this repo, `public/_README.md` l. 417 | "no measured success rates for unattended builds" | ✓ |
| V 6.1.15 | Rahman 2026 [F25] p. 1 | quote present | ✓ |
| V 9.10 | Ma 2026 [D11] p. 1 | "57% pass@1" | ✓ |
| V Table4.19 | Huang 2023a [T4] p. 9 | "can be biased by the code" | ✓ |
| V 1.39 | Novikov 2025 [A25] p. 2 | quote present | ✓ |
| V 10.37 | Bertran 2026 [R1] p. 7 | "Compliance filtering… narrows, but does not eliminate"; pp. 1–2 confirm that the AI auditor does the filtering | ✓ |
| V 11.11 | Sinha 2025 [F3] p. 5 | "without intermediate thinking tokens"; p. 6 lists seven Gemma3/Qwen3 models | ✓ |
| V 10.31 | Xu & Yang 2026 [R8] p. 6 | "LLM-driven sub-agent implemented through Claude Code" | ✓ |
| V 8.4.12 | Bragg 2025 [S19] p. 10 | quote present | ✓ |
| V 11.18 | Bragg 2025 [S19] p. 10 | "scores up to ∼70%… near zero… maximum of 5%" | ✓ |
| V 13.18 | Toledo 2025 [R26] p. 2 | "9 to 13 % (absolute scale)" | ✓ |

## Criterion 6: source-quality sample (§§4–12)

**Method.** The same candidate set, restricted to the text between the "4. ONE AGENT OR MANY" and
"13. SYNTHESIS" headings (513 candidates), drawn with `random.Random(6).sample(…, 30)`. Draws 2, 4, 10
and 20 (model-name digits) and 26 (a duplicate of 13) were skipped by the same pre-fixed rule, and the
first 20 eligible draws were graded.

| # | Number | Labelling in text | OK |
|---|---|---|---|
| 1 | 93% prompts accepted (§5.2) | "Anthropic reports…", set against "An independent stress test" | ✓ |
| 3 | $2.33/paper (§8.1) | "Agent Laboratory reports"; paragraph ends "builders' own reports are more cautious" | ✓ |
| 5 | ChatDev 0.3953 (§4.1) | "These papers reported… against weak comparisons"; no matched budget | ✓ |
| 6 | 0–13 of 500 (§6.3) | academic measurement, "not significant" | ✓ |
| 7 | 480 of 731 (§12.1) | "Authors from Scale AI and Reflection AI" | ✓ |
| 8 | 13 of 21 (62%) (§10.1) | independent high-powered replications | ✓ |
| 9 | 14.55% DABstep (§9) | benchmark measurement (independent of model vendor) | ✓ |
| 11 | 70.4% of 54 (§8.2) | under "Independent audits"; "checks… by execution" | ✓ |
| 12 | 49.4% (§12.2) | "in one controlled study" | ✓ |
| 13 | score 7.5 (§6.6) | practitioner issue; "single reports, not rates" | ✓ |
| 14 | 70%/step (§11.1) | AstaBench, quoted arithmetic with page | ✓ |
| 15 | CaMeL 77% (§5.2) | "on their benchmarks"; does not say the authors evaluated their own method | borderline ✓ |
| 16 | 16% hackable (§6.5) | academic audit, measured | ✓ |
| 17 | Kosmos 57.9% (§8.1) | "Kosmos's developers report" | ✓ |
| 18 | 128 prompts (§5.2) | "An independent stress test", with an extrapolation caveat | ✓ |
| 19 | temperature 0 (§11.2) | large-sample academic measurement | ✓ |
| 21 | AgentDojo 1.0% (§5.2) | "on their benchmarks" | borderline ✓ |
| 22 | 20% differ (§10.1) | many-analysts study | ✓ |
| 23 | 2,100 steps (§11.1) | "the same study reports" | ✓ |
| 24 | 57 libraries (§7) | descriptive count; labelling not material | ✓ |

## Recommendations for each FAIL

**Criterion 4d: word count (14,929 against 9,000–11,000).** Either cut about 3,950 words or have Sharif
change the threshold in the plan. The criterion has been reported here exactly as written. Suggested cuts,
in order of yield:
1. **Remove repeated numbers.** The same figures recur across sections: 49.4% (6×), 99.4% (5×), 59.4% /
   138 problems (4×), 82.7% / 22.66→32.51 (3×), 6.4 points (3×), Toledo 9–13 points (4×), the AlphaEvolve
   and Anthropic 0.97 results (3×). State each fully once and cross-reference afterwards. Estimated saving:
   1,200–1,500 words.
2. **Shorten §6 (2,080 words) to about 1,500.** §6.5 and §12.1 cover the same audits, so merge them into
   one section. Estimated saving: about 600.
3. **Cut §13.1/§13.2 restatement.** P1–P6 repeat the sections' evidence; keep the propositions and the
   confidence lines and drop the re-quoted numbers. Estimated saving: about 400.
4. **Shorten §1.2–1.3 and §16.** They preview and recap numbers that appear in full later. Estimated
   saving: about 500.
5. **Trim §4.4, §5.3, §11.5 and §14 (practitioner-repo detail).** Move issue-level detail to the evidence
   file. Estimated saving: about 700.

## Expert-reader findings

| ID | Severity | Finding | Fix |
|---|---|---|---|
| M1 | **major** | **Unfair to a named project (ruflo, §4.4).** The review says ruflo's own audit "found a claimed attention speedup 'fabricated with Math.random() at runtime'", under "Swarm claims are the least supported". The same audit file (`docs/reviews/intelligence-system-audit-2026-05-29.md`, l. 97) records the fix: "✅ #2 Flash Attention fabrication — randomized telemetry removed". The review notes later fixes for other projects ("since closed as completed") but not this one, so a reader concludes ruflo still ships a fabricated metric. | Add "(since removed, per the same audit)". The point that the claim was unmeasured when made still stands. |
| m1 | minor | **Summary Point 1 and §16 drop a caveat.** "The same agent harness appears among the successes and the failures" omits the hedge given in §1.3: the two cases run models generations apart (Claude 3.7 Sonnet vs Claude Opus 5). §16 keeps the hedge ("running models generations apart"); Summary Point 1 does not. | Add "running different models" to Summary Point 1. |
| m2 | minor | **The 49.4% is conditional.** TeamBench's authors say the 49.4% "should be read as a verdict-quality estimate conditional on a verdict"; counting the 942 missing verdicts gives 22.3% (T18 pp. 7–8). The review uses 49.4% six times and never mentions the 22.3%. Each statement is literally accurate. | Add the conditional and the 22.3% once, in §6.2. |
| m3 | minor | **Vibe Code Bench sample (§7).** "graded… through 964 workflows, the best of 16 models passes 61.8% of workflows". The 61.8% is on the 50-app test split (473 workflows), and accuracy is the mean per-application pass share. | Change to "passes 61.8% of workflows on the held-out test split". |
| m4 | minor | **Vendor claim not flagged as such.** §8.3 gives AlphaEvolve's "recovers on average 0.7% of Google's fleet-wide compute" as a result. It is Google's own post-deployment measurement of its own system, which §2.2's labelling rule says should be flagged. | Add "by Google's own measurement". |
| m5 | minor | **Future Issues and §15 do not line up.** Future Issue 8 (third-party measurement of production autonomy) has no study in §15, which "frames six" studies plus a seventh task. | Add one sentence to §15, or drop Issue 8. |
| m6 | minor | **Layout.** In Table 2 (p. 5), the cell repo `frankbria/ralph-claude-code #91` is squeezed by `\resizebox` to 4.5–5 pt, too small to read in print. In Figure 1 (p. 9), `K-Dense-AI/scientific-agent-skills #152,` overruns the column by 21 pt into the gutter. The other overfull boxes (112 pt and 224 pt) are the intentional full-width title block and boxes, and render correctly. | Allow a line break inside the repo name instead of `\resizebox`; add a break point in the Figure 1 cell. |
| m7 | minor | **Redundancy** (see the word-count recommendation). Repeated headline numbers make the middle sections read as restatements. | Same as the word-count cuts. |
| m8 | minor | **Locator style is inconsistent** for the same Google DeepMind source: "p. 77" in §1.2 and "sec. 3.4.2" in §11.3. The PDF page is 78; the printed page is presumably 77. | Use one locator style. |

**Checked and found clean:** no private or personal information (only the author's name and the public
repo URL); the conflict of interest and AI drafting are disclosed; the affiliations attributed to named
labs (TeamBench: MIT, Google Research, Google DeepMind; SWE-Bench Pro V2: Scale AI and Reflection AI)
match the papers; the MetaGPT, gastown, BMAD and spec-kit statements match their repos and issues; all 24
cited issues/PRs exist and their stated open/closed status is right; no contradictions in numbers between
sections (Tang 9.33% / 91.49%, OpenAI 13→35%, and McCain 5.4→3.3 are consistent everywhere they appear);
Table 1 matches `papers.tsv` in every cell; the §2.1 arithmetic (139 + 115 + 32 = 286; 108 + 110 = 218)
holds.

## Final verdict

**GRADE FAIL.**

To change before publication:
1. **Criterion 4d, word count:** the body has 14,929 words against a 9,000–11,000 threshold (+3,929).
   Either cut about 4,000 words (plan above) or have Sharif decide to change the threshold and record that
   decision in `docs/plans/07_literature_review.md`.
2. **Reader finding M1 (major):** add the fix recorded in ruflo's own audit to §4.4.

Word count is the only failing **criterion**. Criteria 1, 2, 3, 5, 6 and 7 pass, and 2 and 3 pass on
independent re-measurement (20/20 numbers; 20/20 evidence spot checks). The grade would still be FAIL
without the word-count failure, because of the one major reader finding (M1), which is a one-clause fix.
The minor findings m1–m8 are recommended and do not block publication.

---

## Round 2 (re-grade of `git diff 257dd35 HEAD -- literature/review`, HEAD f05f4a1)

Scope: only the diff (16 files, +25/−15) and the criteria it can affect (2, 3, 4, 6, and layout). I rebuilt
with `bash scripts/literature/build_review.sh` (35 pages, 0 undefined references) and re-checked each fix
against its source myself.

### Fixes checked against their sources

| Finding | Fix in text | Source check | Status |
|---|---|---|---|
| M1 ruflo (§4.4) | "(the same audit records that the ``randomized telemetry'' has since been ``removed'')" | `ruvnet/ruflo` `docs/reviews/intelligence-system-audit-2026-05-29.md` l. 97: "✅ **#2 Flash Attention fabrication** — randomized telemetry removed from both `attention-coordinator` copies". The quoted words are verbatim | **Fixed** |
| m1 Summary Point 1 | "The same agent harness, running different models, appears…" | matches §1.3's hedge | **Fixed** |
| m2 49.4% conditional (§6.2) | adds "should be read as a verdict-quality estimate conditional on a verdict" and "counting the 942 missing verdicts as failures lowers it to 22.3%" [T18, pp. 7–8] | T18 p. 8: "the 49.4% rate should be read as a verdict-quality estimate conditional on a verdict"; p. 7: "Counting the 942 missing verdicts as failures lowers the effective false-accept rate from 49.4% to 22.3%" | **Fixed** |
| m3 Vibe Code Bench (§7) | "achieves 61.8% accuracy on the held-out test split of 50 applications" | C19 p. 1 abstract: "(50 private validation, 50 held-out test)… the best achieves 61.8% accuracy on the test split" | **Fixed** |
| m4 AlphaEvolve (§8.3) | "…0.7% of Google's fleet-wide compute, by Google's own post-deployment measurement" | A25 p. 14: "Post-deployment measurements across Google's fleet confirmed the simulator results… recovers on average 0.7% of Google's fleet-wide compute resources" | **Fixed** |
| m5 Future Issue 8 vs §15 | §15 adds an "eighth" task: independent third-party measurement of interventions per task and hours unattended | now matches Future Issue 8; no new numbers or citations | **Fixed** |
| m6 layout | `\repobreak` (breakable repo name) replaces `\resizebox` in Table 2 and is used in Figure 1 | see layout check below | **Fixed** |
| m8 locator style | §1.2 and §11.3 both cite F30 as "p. 78" | consistent now. The passage is on PDF page 78, whose **printed page number is 77**. See nit n1 | **Fixed** (nit n1 remains) |
| m7 redundancy | not changed | waiting on the author's word-count decision | open (minor) |

### Layout check
- **Table 2 (p. 5):** `frankbria/ralph-claude-code #91` now wraps over two lines at body-table size. The
  pymupdf scan finds no text under 6.5 pt on pages 1–26 apart from the superscript footnote markers on
  pp. 23–24. Readable.
- **Figure 1 (p. 9):** `K-Dense-AI/scientific-agent-skills #152` wraps inside its cell. The 21 pt overfull
  box is gone from the log, and the remaining overfull boxes are the intentional full-width title block and
  boxes. Readable. Both pages were inspected as 110 dpi renders.

### Re-run checks

| Criterion | Round-2 result | PASS/FAIL |
|---|---|---|
| 1. Citations | `check_review.py`: 162 distinct keys, 0 dangling | **PASS** |
| 2. Numbers | no number in the round-1 draw changed. The new numbers (22.3%, 942, 50 test apps, 0.7%) were each checked against the source above | **PASS** |
| 3. Evidence | `build_evidence.py`: 1,048 rows (VERIFIED 757, MANUAL 291), 0 sources without a row, 0 NOT FOUND / WRONG PAGE, exit 0. The new rows for ruflo l. 97, T18 pp. 7–8, C19 p. 1 and A25 p. 14 are the passages confirmed above | **PASS** |
| 4a–c. Abstract 150; boxes present; 162 works | unchanged | PASS |
| **4d. Word count** | **15,043** body words (+114 from the fixes) against 9,000–11,000 | **FAIL** |
| 5. Coverage | themes 10/20/12/19/20/20/16/23/22; 70 repo citations, 28 repos | **PASS** |
| 6. Source labelling | m4 makes the AlphaEvolve vendor measurement explicit; no labels removed | **PASS** |
| 7. Table 4 | unchanged; 10/10 rows cited | **PASS** |

### Nit (does not block)
- **n1.** F30 is cited as "p. 78", which is the PDF page index. The page's printed number is 77, and readers
  of the report will look for the printed page. Suggest "p. 77" in §1.2 and §11.3, or "PDF p. 78".

### Round-2 verdict

**GRADE PASS except word count (author decision pending).**

Every reader finding at major severity or above is fixed and confirmed against its source. All criteria
except 4d pass. The only open FAIL is the body word count (15,043 against 9,000–11,000), which is Sharif's
decision: cut about 4,000 words per the round-1 plan, or change the threshold in
`docs/plans/07_literature_review.md`. m7 (redundancy) and n1 are minor and do not block.
