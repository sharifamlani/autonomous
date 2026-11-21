# H25 Aizawa (2025): Writing effective tools for agents, with agents

- **Citation:** Aizawa, K. (2025, September 11). *Writing effective tools for agents: with agents.* Anthropic Engineering blog.
- **Link:** https://www.anthropic.com/engineering/writing-tools-for-agents
- **Fetched:** 2026-11-21 (title, author and date checked on the fetched page).
- **Why no PDF:** a vendor engineering blog post; there is no PDF version.

## What it says (from the fetched page)

- Tools are a contract between deterministic software and non-deterministic agents: "More tools don't
  always lead to better outcomes." Consolidate multi-step work into single tools (a `schedule_event`
  rather than `list_users` + `list_events` + `create_event`).
- Namespacing by service/resource helps tool choice; prefix versus suffix naming had "non-trivial
  effects" on evaluations.
- Return high-signal fields, not low-level IDs: resolving UUIDs to names "significantly improves
  Claude's precision in retrieval tasks by reducing hallucinations."
- A `response_format` option (detailed or concise): the concise example used about a third of the
  tokens (72 vs 206 tokens). Claude Code caps tool responses: "we restrict tool responses to 25,000
  tokens by default."
- Evaluate tools with realistic multi-step tasks; "Even small refinements to tool descriptions can
  yield dramatic improvements" (Claude Sonnet 3.5 reached state of the art on SWE-bench Verified after
  tool description refinements).

## Limits

- Vendor-authored; the comparison of Claude-optimised vs human-written MCP servers is shown as charts
  with no figures in the text; no sample sizes. Practical advice, not a controlled study (compare H10).
