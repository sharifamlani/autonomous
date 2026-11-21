# H28 Yan (2025): Don't Build Multi-Agents

- **Citation:** Yan, W. (2025, June 12). *Don't Build Multi-Agents.* Cognition blog.
- **Link:** https://cognition.com/blog/dont-build-multi-agents (301 from cognition.ai/blog/dont-build-multi-agents)
- **Fetched:** 2026-11-21 (title, author and date checked on the fetched page).
- **Why no PDF:** a company opinion/engineering post; there is no PDF version.

## What it says (from the fetched page)

- Context engineering is "the #1 job of engineers building AI agents" and means doing context
  delivery "automatically in a dynamic system".
- Principle 1: "Share context, and share full agent traces, not just individual messages."
  Principle 2: "Actions carry implicit decisions, and conflicting decisions carry bad results."
- Parallel subagents working from isolated summaries make inconsistent choices (a Flappy Bird example
  where one builds a Mario-style background and another a mismatched bird); "running multiple agents
  in collaboration only results in fragile systems"; "The decision-making ends up being too dispersed."
- Preferred design: a single-threaded linear agent (with a compression model for very long tasks).
  Claude Code's subagents are cited as a safe use: they answer narrow questions rather than write
  code in parallel.

## Limits

- Company opinion from the maker of Devin; anecdotal, a toy example, no experiments or numbers.
  Measured evidence on the same question: H11 (multi-agent gains and losses range from +80.8% to -70.0%).
