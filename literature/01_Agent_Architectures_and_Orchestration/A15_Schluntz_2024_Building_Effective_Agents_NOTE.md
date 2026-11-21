# A15: Schluntz and Zhang (Anthropic), "Building effective agents" (2024)

- **Citation:** Erik Schluntz and Barry Zhang, "Building effective agents", Anthropic Engineering, 19 December 2024 (page last modified 2026-10-09 per its metadata).
- **Link:** https://www.anthropic.com/engineering/building-effective-agents
- **Date fetched:** 2026-11-21
- **Why there is no PDF:** an HTML engineering post on anthropic.com with no PDF edition. Author names: the post itself reads "Written by Erik S. and Barry Zhang"; the reference notebooks in anthropics/claude-cookbooks (`patterns/agents/README.md`, fetched 2026-11-21) credit it as "by Erik Schluntz and Barry Zhang".
- **Status:** vendor guidance from the builder of Claude Code; it reports no benchmark numbers, so it is a design recipe, not measured evidence.

## Passages the folder README relies on (verbatim, fetched 2026-11-21)

- Workflows vs agents: "Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage".
- Start simple: "we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all. Agentic systems often trade latency and cost for better task performance".
- Orchestrator-workers: "a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results."
- Routing: "Routing classifies an input and directs it to a specialized followup task."
- Evaluator-optimizer: "one LLM call generates a response while another provides evaluation and feedback in a loop."
- Frameworks: they "often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug."
- Tool design: "think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good agent-computer interfaces (ACI)."
- Cost of autonomy: "The autonomous nature of agents means higher costs, and the potential for compounding errors. We recommend extensive testing in sandboxed environments, along with the appropriate guardrails."
- Evidence standard: "you should consider adding complexity only when it demonstrably improves outcomes."
