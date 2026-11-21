# QA-C: Sections 9-12 (data analysis, replication, reliability, measurement and Table 3)

Scope: `literature/review/sections/09_data.tex`, `10_replication.tex`, `11_reliability.tex`,
`12_measurement.tex` (including Table 3); ledgers `review/ledger/09_10.tsv` and `11_12.tsv`.
Every citation, number and ledger row was checked against the source: the PDF page for papers; a raw
re-fetch for web pages (curl, tags stripped); `gh api` or the pinned clone in `public/` for repos.

| # | section | severity | finding | source checked (ID, page) | fix made | status |
|---|---|---|---|---|---|---|
| 1 | 9 | blocker | Ledger quote for D23 ("small, inexpensive models") was NOT FOUND: it strung Figure 1's axis labels together, and the paper never calls its models small or inexpensive | D23 p. 2 Fig. 1; p. 6 §4.1 | Text now reads "smaller models (two Qwen models that run on commodity hardware and Gemini 3.7 Flash)"; the quote is replaced by the verbatim p. 6 sentence | fixed |
| 2 | 11 | blocker | "over half of its successful four-to-eight-hour tasks involved at least one intervention" and "preliminary" were attributed to F32, but both come from a separate OpenAI post (2026-09-06, view-inside-openai) that is not in papers.tsv. A raw re-fetch of the F32 URL has 0 matches for either quote, so the sentence stitched two posts and two time windows together (QA-D flagged this too) | F32 URL re-fetched raw; companion URL re-fetched | Companion claim cut. The sentence now uses F32's own words: the March-October 2026 window, "success without human intervention", "humans are still central to AI development", and its caution about "researchers' changing choices". Companion ledger rows removed; four F32 rows added | fixed |
| 3 | 12 (Table 3) | blocker | The interventions row cited F32 for the same companion-post claim ("over half ... involved an intervention") | F32 URL re-fetched raw | Row now reads "One lab estimates success without human intervention at 35% on its 4--8 hour tasks \citep{F32}"; ledger row replaced | fixed |
| 4 | 9 | major | QRData was grouped under "tasks spanning several files and steps", but most QRData questions use a single data sheet | D14 p. 3 §2.1 | Now "On harder, multi-step tasks ... QRData's statistical and causal questions, most of which use a single data sheet"; ledger row added | fixed |
| 5 | 9 | major | "Tuning to a benchmark inflates scores quickly" and "these figures measure tuning, not general ability" claimed more than the leaderboard shows: the untuned row (0.8858) is also far above the paper's 57%, and nothing measures speed | ucbepic/DataAgentBench README (gh api raw), lines 30-47, 109, 176; D11 p. 1 | "quickly" dropped. Text now says the leaderboard's 54 queries differ from the paper's 104, so neither figure is comparable with 57%, and the top rows partly measure tuning | fixed |
| 6 | 9 | major | `\repofile{ucbepic/DataAgentBench}` had no matching ledger row: the source_id was "ucbepic/DataAgentBench README.md". The 54-query row quoted a footnote that does not state the total | DAB README line 176 | source_id normalized on 5 rows; the 54-query quote replaced with README line 176 | fixed |
| 7 | 9 | major | D23: "every data-leakage mode improved the agent's ranking". The paper compares each pipeline's rank with the rank expected for its configuration, and an LLM judge detected the failures | D23 p. 7 §4.2, p. 3 §3.1 | Now "improved a pipeline's ranking" and "detected failures with an LLM judge"; ledger row added | fixed |
| 8 | 9 | major | D26: the drift from ~95% to ~65% was quoted without its stated cause (skill documents left unmaintained), so it read as unexplained model decay | D26 web page re-fetched raw | Added "as the skill documents went unmaintained"; ledger row with the verbatim cause added | fixed |
| 9 | 11 | major | F3: "the best model in one study falls below 50% within 15 turns". That figure is for the best of seven open Qwen3/Gemma3 models answering without thinking tokens. The same study reports GPT-5 thinking executing over 2,100 steps | F3 p. 5 §3.1 Setup, p. 6 Result 1, p. 2 | Rescoped to "the best of seven open models tested without thinking (Qwen3-32B)", with the GPT-5 result added; 2 ledger rows added | fixed |
| 10 | 11 | major | F14: the drop from 5.4 to 3.3 interventions per session is for Anthropic's internal Claude Code users from August to December, not general traffic | F14 web page re-fetched raw | Text rescoped to internal users, August to December; ledger quote replaced with the full sentence | fixed |
| 11 | 12 (Table 3) | major | T18: "a full team beat a single agent by a mean of +0.5 points (p = 0.20)". The source says Full Team "is not significantly better than Solo" | T18 p. 6 §3.3 | Now "was not significantly better than a single agent (mean +0.5 points, p = 0.20)"; ledger row added | fixed |
| 12 | 12 | major (fairness) | Harbor: "merged single-run comparisons" implied the merges broke a written rule. The aa-lcr row dates from 2026-04-25, and git history did not settle whether the ≥ 2-runs rule existed at that time | harbor clone @ 96c86af: ADAPTER_CONTRIBUTING.md l. 251, 331, 349; parity_summary.csv (14 merged single-run rows across 8 adapters); git log | Both sentences now say the summary "still lists" merged single-run comparisons. This is true whatever the date order; the count row was added to the ledger | fixed |
| 13 | 9 | minor | Grader rows used the source_id "InfiAgent/InfiAgent eval_closed_form.py" (nonstandard) | InfiAgent clone @ 3d6c4a7, l. 36, 113 | source_id normalized | fixed |
| 14 | 9 | minor (fairness) | "Two issues reporting wrong labels remain open": the issues report suspected errors, not confirmed ones | InfiAgent/InfiAgent #28, #29 (gh api: both open) | Now "Two open issues report apparently wrong labels" | fixed |
| 15 | 9 | minor | "its ceiling is an agent's consensus" was unclear | D1 p. 4 §2.1 | Now "its answer key rests on one agent's agreement with itself" | fixed |
| 16 | 9 | minor | The D21 conflict-of-interest sentence was ambiguous ("the gap concerns a model they did not build") | D21 p. 3, p. 10 | Now names GPT-5.4 explicitly | fixed |
| 17 | 10 | minor | Plain "Section~8" | 08_science.tex label | Now `Section~\ref{sec:science}` | fixed |
| 18 | 11 | minor | inspect_ai was cited through a plain \href | inspect_ai clone @ cf72dbc, docs/setting-limits.qmd | Now `\repofile{UKGovernmentBEIS/inspect_ai}{docs/setting-limits.qmd}`; the existing ledger row matches | fixed |
| 19 | 11 | minor | Stray punctuation `\citep{F23},.` | n/a | Removed the comma | fixed |
| 20 | 11 | minor | gastown: the issue describes a "session-hygiene plugin" that classified sessions as zombies, not a watchdog | gastownhall/gastown #2707 (gh api, closed) | Now "a session-cleanup plugin ... misidentified healthy sessions as zombies" | fixed |
| 21 | 12 | minor | V31: "flagged by an automated pipeline". The post calls the method a human-supervised agent review | V31 web page re-fetched raw | Wording corrected | fixed |
| 22 | 12 | minor | Harbor parity example did not name the model | parity_summary.csv l. 3 (claude-haiku-4-5) | Added "with Claude Haiku 4.5" | fixed |
| 23 | 12 | minor | Plain "Section~15" | 15_agenda.tex label | Now `Section~\ref{sec:agenda}` | fixed |
| 24 | 11 | minor | Ledger sentence_start values had drifted from the text ("Noise also enters from outside the model", old §9/§11 starts) | n/a | sentence_start updated to match the current text | fixed |

## Verified without change (summary)
- §9: D1 78.99% (gpt-4-0613, validation set), D2 30.5%, D3 34.12%, D6 25% and the self-critic/oracle result,
  D9 76.39/14.55, D11 57%, 90% and the MALE/FEMALE example, D12 405/580 (69.8%) with independent and Purdue
  authors, D16 affiliations and verifier, D13 82.7% of 81 and 22.66→32.51, D15 12 defects, D17 100%/59%,
  D20 81/38, D21 58.3/30.5, D26 21%/95% (raw fetch), DAB leaderboard rows 1 and 12 (gh api), InfiAgent #28/#29
  open, grader denominator.
- §10: R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R30, R3, R4, R8, R1, R2, R5, R27, R26, R6,
  R7, S9, S10, S15, S16; every number matches its page.
- §11: F1, F38, F5, F25, S19, F19, A9, F24, F2, F27 (raw fetch), F30 p. 78, F6, F7, F23, A10, F8; mini-swe-agent
  defaults (cost_limit 3.0; step and wall-clock default 0 = off) and exit statuses; #585 is a closed PR;
  claude-code-action #674 (closed, one user); inspect_ai limits headings.
- §12: A18, C15 and V31 (raw fetch; dated 2026-02-23 and 2026-07-08), C12, D13, F12, A10, T18 49.4%, harbor
  oracle, nop and overlap rules.

## Final checks
- `python scripts/literature/build_evidence.py`: 1041 ledger rows; VERIFIED 752, MANUAL 289; 0 NOT FOUND;
  0 cited sources with no ledger row.
- Sections 9-12 (221 rows): §9 VERIFIED 33 / MANUAL 14; §10 VERIFIED 55; §11 VERIFIED 44 / MANUAL 19;
  §12 VERIFIED 37 / MANUAL 19; 0 WRONG PAGE or NOT FOUND. Every MANUAL row was re-checked by hand
  (raw fetch, gh api or the pinned clone).
- `python scripts/literature/check_review.py --cites`: PASS, 162 distinct keys, 0 dangling.
- `bash scripts/literature/build_review.sh`: builds; no undefined references; no overfull boxes from sections 9-12.
