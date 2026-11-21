# F17 Hong (2025): Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma)

- **Citation:** Kelly Hong, Anton Troynikov and Jeff Huber (Chroma), "Context Rot: How Increasing Input
  Tokens Impacts LLM Performance", Chroma Technical Report, 2025-07-14.
- **Link:** https://www.trychroma.com/research/context-rot
- **Fetched:** 2026-11-21 (page fetched in this session; the old research.trychroma.com address redirects
  here; title, authors and date taken from the fetch output). The fetch tool passes pages through a small
  model; the text below was copied from its output and should be re-checked against the live page.
- **Why no PDF:** a company technical report published as a web page, with no PDF or arXiv version. Not
  peer reviewed; Chroma is a vector-database company.

## What it says (quoted from the page)

- "We evaluate 18 LLMs" across closed-source and open-weights families (including GPT-4.1, Claude 4,
  Gemini 2.5 and Qwen3).
- "model performance varies significantly as input length changes, even on simple tasks", and becomes
  "increasingly unreliable as input length grows."
- "Distractors have non-uniform impact on model performance": a single distractor lowers performance
  against the baseline and four make it worse.
- Limits stated by the authors: "this evaluation is not exhaustive of real-world use cases"; they "do not
  explain the mechanisms behind this performance degradation"; and input length can be confounded with
  task difficulty.
