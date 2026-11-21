# H26 Anthropic (2025): Managing context on the Claude Developer Platform

- **Citation:** Anthropic (2025, September 29). *Managing context on the Claude Developer Platform.* Claude blog (product update; no named author).
- **Link:** https://claude.com/blog/context-management (redirected from anthropic.com/news/context-management)
- **Fetched:** 2026-11-21 (title and date checked on the fetched page).
- **Why no PDF:** a vendor product post; there is no PDF version.

## What it says (from the fetched page)

- Two features, public beta, tested with Claude Sonnet 4.5: context editing, which "automatically
  clears stale tool calls and results from within the context window when approaching token limits",
  and a client-side file-based memory tool ("operates entirely client-side through tool calls").
- On "an internal evaluation set for agentic search": context editing alone "delivered a 29%
  improvement"; "combining the memory tool with context editing improved performance by 39% over
  baseline."
- In a 100-turn web search evaluation, context editing cut token consumption by 84% and let workflows
  finish that would otherwise fail from context exhaustion.

## Limits

- Vendor-authored, about its own product. The evaluation set is internal and unpublished; baseline,
  sample size, metric and run count are not given, and "improvement" is not defined.
- Web-search workloads, not coding. Independent evidence that clearing old tool results is safe:
  H3 (observation masking matches LLM summarization on SWE-bench Verified).
