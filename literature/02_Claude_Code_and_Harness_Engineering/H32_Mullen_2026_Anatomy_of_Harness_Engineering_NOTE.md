# H32 Mullen (2026): The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents

- **Citation:** Taylor Mullen and Christian Gunderman (Google), "The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents", Google Developers Blog, 2026-09-09.
- **Link:** https://developers.googleblog.com/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor developer-blog post (Google), not an arXiv paper; guidance, no measurements.

## What it says (quoted from the page)

- "Behavioral evaluations are often a better measure of confidence" than composite benchmark scores, which can shift without explaining why (fetch summary wording for the second clause).
- "Evals belong to the second phase of development": build the agent first, add evaluations once it can handle its own development work.
- The suite exists to give "unshakeable confidence that a new prompt tweak, tool schema change, or model upgrade" did not degrade behaviour.
- A strong framework "separates behavioral assertions into fast, deterministic, unit-style checks that run locally"; evals "assert on intermediate execution steps, like specific tool calls or file modifications" rather than exact output strings.
- Because outputs are nondeterministic the authors advise against blocking pull requests on a single run and recommend tracking "aggregate pass rates over time"; for complex tasks, outcome-based grading such as an LLM judge so correct but unexpected paths are not penalised.
