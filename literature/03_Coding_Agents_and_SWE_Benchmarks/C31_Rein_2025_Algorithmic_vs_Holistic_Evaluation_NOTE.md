# C31 Rein (2025): Research Update: Algorithmic vs. Holistic Evaluation

- **Citation:** David Rein (METR), "Research Update: Algorithmic vs. Holistic Evaluation", METR blog, 2025-08-13 (URL dated 08-12).
- **Link:** https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** an independent evaluator's (METR) blog post, not an arXiv paper; small sample; companion to C14.

## What it says (quoted from the page)

- Sample: 18 real open-source issues, 15 from stdlib-js and 3 from hypothesis; human maintainers took 20 minutes to four hours, averaging 1.3 hours.
- Claude 3.7 Sonnet in an Inspect ReAct agent scored "38% (±19%, 95% CI)" on the maintainer-written tests, but 27% (±20, 95% CI) on the manually reviewed subset, and "none of them are mergeable as-is".
- Reviewers estimated the agent PRs would take "42 minutes" on average to make mergeable (26 minutes for runs that passed the tests, minimum 15). Every reviewed PR had at least three of five failure categories; testing coverage and documentation gaps were the most frequent beyond core functionality.
- Conclusion: algorithmic scoring "overestimates model capabilities" on this type of work. Caveats: large mature repositories with possibly stricter standards, task selection may favour well-specified issues, and the scaffold was basic and not heavily optimised.
