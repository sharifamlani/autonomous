# F36 Anthropic (2026): An update on recent Claude Code quality reports

- **Citation:** Anthropic Engineering (no author named), "An update on recent Claude Code quality reports", Anthropic Engineering blog, 2026-04-23.
- **Link:** https://www.anthropic.com/engineering/april-23-postmortem
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor post-mortem (Anthropic), not an arXiv paper.

## What it says (quoted from the page)

- Three changes affected Claude Code, the Agent SDK and Cowork (not the API): default reasoning effort moved from high to medium on March 4 (reverted April 7; Anthropic called it "the wrong tradeoff"); a change meant to clear old thinking once after an hour idle instead cleared it every turn (March 26, fixed April 10), making Claude seem forgetful and repetitive; and a verbosity system prompt ("keep text between tool calls to ≤25 words", April 16, reverted April 20) hurt coding quality (fetch summary wording).
- Detection (fetch summary wording): each change hit a different slice of traffic on a different schedule, so the combined effect looked like broad, inconsistent degradation; internal usage and evals initially failed to reproduce it; the thinking-history bug passed human and automated code reviews, unit tests, end-to-end tests, automated verification and dogfooding, and took over a week to confirm.
- A broader evaluation suite run during ablations found a 3% drop for both Opus 4.6 and 4.7, which led to the reversal of the verbosity prompt change (fetch summary wording).
- Planned changes: more staff on the public build, broad per-model evals for every system prompt change, ablations, model-specific gating, soak periods and gradual rollouts.
