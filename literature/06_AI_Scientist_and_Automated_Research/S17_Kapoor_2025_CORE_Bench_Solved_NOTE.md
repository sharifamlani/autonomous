# S17 Kapoor (2025): CORE-Bench is solved (using Opus 4.5 with Claude Code)

- **Citation:** Kapoor, S. (2025, December 3). "CORE-Bench is solved (using Opus 4.5 with Claude Code)."
  HAL (Holistic Agent Leaderboard) insights post, Princeton; the scores are on the HAL CORE-Bench Hard
  leaderboard page.
- **Links:** https://hal.cs.princeton.edu/insights (post title, author, date) and
  https://hal.cs.princeton.edu/corebench_hard (leaderboard numbers).
- **Fetched:** 2026-11-21. Both pages were read through a page-summarising fetch tool, not as raw HTML,
  so the quotes below are the tool's quotations of the page; the insights excerpt it returned stops
  after "Earlier this week, Nicholas Carlini reached out to share that an updated scaffold that uses...".
- **Why no PDF:** a leaderboard page and a short blog post; there is no paper. The benchmark itself is
  S8 (Siegel et al., 2024).

## What it says (as quoted by the fetch tool)

- The leaderboard page states "We have now declared [CORE-Bench solved]".
- Top entry: Claude Code (scaffold submitted by Nicholas Carlini) with Claude Opus 4.5 scores
  "77.78% (95.5% w/ manual validation)", total cost $87.16 (the page warns that reported costs are
  overstated for some models by up to 2x).
- The same page's CORE-Agent entries for Opus 4.5 score 42.22%; the best CORE-Agent entry is Opus 4.1
  at 51.11%. The update says the Claude Code scaffold "drastically outperforms the CORE-Agent
  scaffold we used, especially after fixing a few grading errors via manual scoring."
- The raw-to-validated jump (77.78% to 95.5%) comes from correcting grading errors by hand, not from
  re-running the agent; the page does not give the method of that manual validation.

## Limits

- Summarised through a fetch tool; the post body and the manual-validation method were not seen in full.
- The 95.5% is a score after the benchmark's authors re-graded; the raw automated score is 77.78%.
- One agent scaffold run by a Claude Code expert; not an independent replication.
