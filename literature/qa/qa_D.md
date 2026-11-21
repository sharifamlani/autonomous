# QA D: abstract and §§13–17

Scope: `sections/00_abstract.tex`, `13_synthesis.tex` (incl. Figure 2), `14_implications.tex` (incl. Table 4),
`15_agenda.tex`, `16_conclusion.tex`, `17_endmatter.tex`, ledger `ledger/13_17.tsv`. QA run 2026-11-21.

**Coverage.** 232 ledger rows (225 original + 7 added). All 183 VERIFIED rows: quote confirmed on the stated
PDF page by `build_evidence.py`; claim-vs-source read in context for every number in these sections. All 49
MANUAL rows checked by hand: web pages re-fetched raw with curl (V17, C15, F32, T28, S20, V31, F14); issues via
`gh api` with state (gastown#2707 closed, sandbox-runtime#97 open, AI-Scientist-v2#133 open, autoresearch#599
open); repo files read at the pinned clones (harbor 96c86af, RD-Agent 484776c, mini-swe-agent 04d809c,
AI-Scientist-v3 f8ae47d, superpowers 22f0b46, MetaGPT 11cdf46, autoresearch 228791f); this repo's own files
(CLAUDE.md, public/_README.md, PUBLIC_REPOS.md, docs/plans/07, build_evidence.py).

**Abstract numbers vs body and sources:** 99.4% (C12 p.1 = §1, §7, §12), 88% (F30 p.78, printed p.77 = §1, §11),
61.8% of workflows, best of 16 (C19 p.1; "application accuracy is the percentage of workflows that pass", p.5 = §1,
§7), 70.4% of 54 (S15 p.2 = §1, §8), 288 / 237 (papers.tsv 288 rows all verified; PUBLIC_REPOS.md l.9 = §2). All
match after fixes 1–2.

**Confidence levels P1–P6** checked against the body: P1 moderate, P2 strong, P3 moderate, P4 moderate, P5
suggestive, P6 strong are each justified by the evidence the body presents; Table 4 ratings map onto them
consistently. P4's justification was corrected (fix 10) without changing the level.

| # | section | severity | finding | source checked (ID, page) | fix made | status |
|---|---|---|---|---|---|---|
| 1 | Abstract | major | "about 88% of one laboratory's pull requests still need human steering" drops "or human code authorship" from the source | F30 p.78 (printed 77) | "still need human steering or human-written code"; ledger claim updated | fixed |
| 2 | Abstract | major | "This review synthesizes 288 papers and 237 repositories" overstates use: the review cites 162 of the 288 (55 are web reports) and 28 repos; §2 says the review "rests on" the corpus | papers.tsv (288 rows); PUBLIC_REPOS.md l.9; `check_review.py` (162 cited) | "Drawing on 288 papers and reports and 237 open-source repositories" | fixed |
| 3 | Abstract | minor | Absolutes "Agents succeed ... They fail"; abstract was at 149/150 words, so fixes 1–2 needed room | check_review.py word count | "Agents tend to succeed ... and fail"; area list compressed to "from agent design to reliability and cost"; now exactly 150 words | fixed |
| 4 | Abstract ledger | minor | 288 row gave source_id `literature/papers.tsv` but quoted docs/plans/07 | docs/plans/07 l.14; papers.tsv | source_id set to the plan doc; count re-checked against papers.tsv in the claim | fixed |
| 5 | §13, Fig 2, SP3 | major | "A separate checker that reads only the builder's account": TeamBench's verifier reads the full requirements plus read-only workspace and executor logs; it cannot execute commands | T18 p.3 §2.1, p.12 Table (permissions) | "cannot run the code and sees only the builder's evidence" / "with read-only access"; Fig 2 and SP3 reworded to "evidence"; T18 p.3 row added | fixed |
| 6 | §13 | minor | "An external signal the builder can reach is gamed" (absolute) | §6 evidence (V3, V17, R26) | "tends to be gamed" | fixed |
| 7 | §13 P1, Fig 2, SP7 | major | "computable metric and a held-out set [S31, A25]": S31 reports on holdout, but AlphaEvolve's claim is an automated evaluator, not a held-out set | S31 p.5; A25 p.1, p.21 | "computable metric, often scored on held-out data" (P1); "where possible" (Fig 2); "ideally scored on held-out data" (SP7) | fixed |
| 8 | §13 P1 | major | "raised the best agent's pass rate from 22.7% to 84.0%": 22.7% is claude-fable-5-1's closed score; the best closed score is gpt-6-astra's 28.0%. The agent is the best only in the open variant | C29 p.12 table | "raised the pass rate of the strongest agent in that setting from 22.7% to 84.0%"; ledger claims corrected | fixed |
| 9 | §13 P4 | blocker | "A team with enforced roles beat a solo agent by a mean of +0.5 points (p = 0.20)": the paper's finding is "Full team is not significantly better than Solo" | T18 p.6 §3.3 | "was not significantly better than a solo agent using the same model (+0.5 points, p = 0.20)" | fixed |
| 10 | §13 P4, SP5, §15 Q1 | major | "cost-matched" / "at a matched budget" attributed to T18, T25 (and T12 in §15): none is budget-matched (T18 fixes the model across conditions; T25 workflows use up to 4.34x the tokens; T12 does not match budgets). Only T9 matches sample count or budget | T18 p.2, p.6; T25 p.1; T12 p.6–7; T9 p.1 | P4 adds T9 (-0.042 vs matched baselines) and says "controlled comparisons ... only some match budgets"; SP5 "With the same model, and especially at a matched budget ... [T18,T25,T9]"; §15 "closest controlled studies" | fixed |
| 11 | §13 P4 | major | Isolated worktrees with test-gated merges presented as help without its cost; the gain (57.2 to 63.3) came at about twice the cost (3.3 to 6.5) | T20 p.5 table and §3.4 | "at about twice the cost"; T20 cost row added | fixed |
| 12 | SP5 | minor | "The gains that survive come from ..." implies they passed a matched-budget test, which T20 did not | T20 p.5 | "The reported gains come from ..." | fixed |
| 13 | §13 P6 | minor | "Identical runs of one agent varied more than agents differed": one ML task; the unit is agent-model pairings | F24 p.1 | "On one task, identical runs of an agent-model pairing varied more than the pairings differed"; row added | fixed |
| 14 | §14 | major | "The team methods reviewed in Section 4 ... report no measured success rates": §4 also reviews MetaGPT's and ChatDev's papers, which do report results; the evidence (our _README) covers the repositories only, and notes MetaGPT's claims live in its papers | public/_README.md l.417, 457, 497, 578; §4 text | "The open-source team methods reviewed in Section 4 (BMAD-METHOD, spec-kit, MetaGPT and gastown) ... none of their repositories reports a measured success rate" | fixed |
| 15 | §14 | major | The author's plugin is described as if it exists ("One builds an application ..."); `plugin/` is planned for Phase 11 and does not exist | CLAUDE.md §2 (plugin/ "planned, Phase 11"), l.37–38, 79–82 | "two planned commands. One is to build ...; the other is to run ..." | fixed |
| 16 | Disclosure | blocker | "The author built the open-source project described in Section 14": not built yet | CLAUDE.md §2; no `plugin/` on disk | "The author is building ..."; ledger row added | fixed |
| 17 | Disclosure | major | Says the QA pass happened but not that it was also done by AI agents; no repo URL given for the "public" evidence file; long `\texttt` path overflowed the line | CLAUDE.md l.13 | "In a separate quality-assurance pass, AI agents that had not drafted the sections they checked compared every number and citation with its source"; repo URL added; paths set with `\url` (overfull box gone) | fixed |
| 18 | §14 | minor | "the one cell ... that gave reliable evidence, while the instrument itself was sound" reads as a time clause; Figure 1's caption says "only while the instrument itself is sound" | 06_verification.tex Fig 1 caption | "and only while the instrument itself was sound" | fixed |
| 19 | §14 | minor | "hand off through files": CLAUDE.md says files and cross-session messages | CLAUDE.md l.105 | "through files and messages" | fixed |
| 20 | §15 Q1 | minor | "the one long-running comparison with an independent evaluator" (absolute, and the source is lab-authored but unlabelled) | T28 (re-fetched): one prompt, solo 20 min $9 vs harness 6 hr $200, judged by the author | "in our corpus, an Anthropic engineering post" | fixed |
| 21 | SP3 | minor | "In small studies by their builders": V15 is small (55 tasks) but nothing supports "small" for V29 (Microsoft Research) | V15 p.1; V29 p.1 | "In studies by the teams that built them" | fixed |
| 22 | Ledger (Table 4, FI8) | major | Both F32 rows quoted a different OpenAI page ("Research acceleration: The view inside OpenAI", Sept. 2026), which is not in papers.tsv; the cited F32 page ("The jagged frontier") does not contain "over half of successful 4-8 hour tasks" or "preliminary" | F32 page re-fetched raw; companion page re-fetched | Replaced with verbatim F32 quotes (zero-intervention success caveat; 23%→46%, 13%→35%) that support the sentences | fixed |
| 23 | Ledger (§16) | major | V17 quote "RE-Bench Total \| 39 \| 128 \| 30.4%" is not verbatim (pipes inserted into the table text) | V17 page re-fetched | "Total 39 128 30.4%" with table location | fixed |
| 24 | Ledger | minor | Rows needed for the claims as now worded: T18 read-only verifier, T9 (§13 P4, SP5), T20 cost, F24 one task, Disclosure plugin status and repo URL | as above | 7 rows added, all VERIFIED or MANUAL-checked | fixed |
| 25 | Ledger | minor | MetaGPT rows gave line numbers without the pinned commit | public/manifest.tsv | "(clone @ 11cdf46)" added | fixed |
| 26 | §7 (07_building.tex l.7) | major | Same wording as #8 ("raised the best agent's pass rate from 22.7% to 84.0%") in the body | C29 p.12 | none: outside my files | open (outside assigned files; §7 owner) |
| 27 | §11 (11_reliability.tex), §12 Table (12_measurement.tex) | major | F32 cited for "over half of its successful four-to-eight-hour tasks involved at least one intervention" and "preliminary"; both come from the September companion post, not the F32 page, and that post has no papers.tsv ID | F32 and companion page re-fetched | none: outside my files. Either add the companion post to papers.tsv and cite it, or cite only what F32 says | open (outside assigned files; §11/§12 owners) |

Checked without a finding (sample of load-bearing items): F19 2.2–6.0 pts; F25 38.5% (of runs after a first
mistake); F20 100%/44% (50 SWE-bench Verified tasks); T23 91.49% of the 9.33% visible resolutions; S10 55%/82%;
V3 54%→9% and "much less pronounced" for Claude Opus 4.1; S19 ~10 steps at 70% ≈ 3%; C15 ≥59.4% of 138
(both "flawed test cases" and "material issues" phrasings are on the page); D13 82.7% of 81; T12 49.48% vs 45.72%
and Flash 45.47% vs 48.46%; H20 53%→54.4% and context-management gain smaller on Claude 4.5; R1 "narrows, but
does not eliminate"; R6 17/23 retrospective counterfactual; R9 expertise and peer-rated quality; gastown#2707
22 sessions, 9 rigs, closed; sandbox-runtime#97 open; autoresearch#599 (agent owns train.py, which calls
evaluate_bpb); MetaGPT run_tests=False and QaEngineer hire commented out; CLAUDE.md roster and launch
constraints match §14, with no private details and no marketing language.

Final runs: `build_evidence.py` → 1021 rows, VERIFIED 745, MANUAL 276, 0 NOT FOUND (whole paper; 1 gap left in
§06, not mine). My sections: VERIFIED 183, MANUAL 49. `check_review.py --cites` → PASS (162 keys, 0 dangling).
Build: 0 undefined references. Abstract 150/150 words. (Body word count FAIL, 14,704 against 9,000–11,000,
was already failing before this pass and is not within my sections' control.)
