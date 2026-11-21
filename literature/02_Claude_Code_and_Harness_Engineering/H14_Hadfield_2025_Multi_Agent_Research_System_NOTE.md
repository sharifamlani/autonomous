# H14 Hadfield (2025): How we built our multi-agent research system

- **Citation:** Hadfield, J., Zhang, B., Lien, K., Scholz, F., Fox, J., & Ford, D. (2025, June 13).
  *How we built our multi-agent research system.* Anthropic Engineering blog.
- **Link:** https://www.anthropic.com/engineering/multi-agent-research-system
- **Fetched:** 2026-11-21 (title, authors and date checked on the page).
- **Why no PDF:** a vendor engineering blog post; there is no PDF version.

## What it says (quoted from the page)

- The orchestrator-plus-subagents system "outperformed single-agent Claude Opus 4 by 90.2% on our
  internal research eval."
- "token usage by itself explains 80% of the variance" in performance; "multi-agent systems use
  about 15× more tokens than chats."
- Delegation: "Each subagent needs an objective, an output format, guidance on the tools and sources
  to use, and clear task boundaries." "Without detailed task descriptions, agents duplicate work,
  leave gaps, or fail to find necessary information."
- Scaling rule in the prompt: "Simple fact-finding requires just 1 agent with 3-10 tool calls"; the
  lead "spins up 3-5 subagents in parallel rather than serially".
- Where it does not fit: "most coding tasks involve fewer truly parallelizable tasks than research";
  "LLM agents are not yet great at coordinating and delegating to other agents in real time";
  domains "that require all agents to share the same context" are "not a good fit for multi-agent
  systems today."

## Limits

- Internal eval (it started from "about 20 queries"), not public; vendor-authored; research tasks,
  not coding. The 90.2% gain comes with about 15× the tokens of a chat (a single agent uses about 4×,
  so roughly 3.75× a single agent), so it is not a like-for-like budget.
