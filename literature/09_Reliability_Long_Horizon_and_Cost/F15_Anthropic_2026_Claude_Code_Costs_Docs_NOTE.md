# F15 Anthropic (2026): Manage costs effectively (Claude Code docs)

- **Citation:** Anthropic, "Manage costs effectively", Claude Code documentation, accessed 2026-11-21.
- **Link:** https://code.claude.com/docs/en/costs
- **Fetched:** 2026-11-21 (page fetched in this session; title "Manage costs effectively" checked on the
  page). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page, which changes with each Claude Code version.
- **Why no PDF:** official vendor documentation, a web page with no PDF or arXiv version. It is a
  description of the vendor's product and pricing, not a measurement study.

## What it says (quoted from the page)

- Typical spend: "Across enterprise deployments, the average cost is around $13 per developer per
  active day and $150-250 per developer per month, with costs remaining below $30 per active day for 90%
  of users." Per-developer costs "vary widely based on model selection, codebase size, and usage
  patterns such as running multiple instances or automation". These are interactive developer figures,
  not unattended runs.
- Multi-agent cost: "Agent teams use approximately 7x more tokens than standard sessions when teammates
  run in plan mode, because each teammate maintains its own context window"; token usage "is roughly
  proportional to team size".
- Why long sessions cost more: "Claude Code sends your full conversation with every request", so "a
  one-line question in a session that has been open all day still draws usage for the whole
  conversation"; a cache miss after a break "reprocesses your full context"; idle scheduled tasks,
  cross-session messages and goal check-ins each "send your full context". `/compact` "is itself a
  large request".
- Tracking: `/usage` shows session cost computed locally from token counts at list price ("The figure
  is an estimate"); OpenTelemetry export or a gateway gives per-user cost; the cost figure also "counts toward
  `--max-budget-usd`" (the page names this budget flag but does not describe it further).
- Levers listed: clear between tasks, pick the model to match the job (Sonnet for most coding), lower
  effort level or thinking budget, delegate verbose output to subagents, keep CLAUDE.md under 200
  lines, give "verification targets" and use plan mode to avoid "expensive re-work".
