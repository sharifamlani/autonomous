# V16 Grace (2026): Demystifying evals for AI agents

- **Citation:** Grace, M., Hadfield, J., Olivares, R., and De Jonghe, J. (2026, January 9). *Demystifying evals for AI agents.* Anthropic Engineering blog.
- **Link:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- **Fetched:** 2026-11-21 (title, the four authors and the publication date checked on the fetched page).
- **Why no PDF:** a vendor engineering blog post; there is no PDF version.

## What it says (quoted from the page)

- Three grader types: "Agent evaluations typically combine three types of graders: code-based,
  model-based, and human" (section "Types of graders for agents"). Code-based graders are "Brittle to
  valid variations that don't match expected patterns exactly"; model-based graders are
  "Non-deterministic" and "Requires calibration with human graders for accuracy"; human graders are
  "Gold standard quality" but "Expensive" and "Slow".
- Grade what was produced: "it's often better to grade what the agent produced, not the path it took"
  (Step 5, "Design graders thoughtfully").
- Graders must resist gaming: "Make your graders resistant to bypasses or hacks." and "The agent
  shouldn't be able to easily 'cheat' the eval." The post describes Claude "gaining an unfair advantage
  on some tasks by examining the git history from previous trials" (Step 4).
- Variance: "Regardless of agent type, agent behavior varies between runs, which makes evaluation
  results harder to interpret than they first appear"; a consistent 0% pass rate "is most often a
  signal of a broken task, not an incapable agent" (Step 2).
- Computer-use and browser agents (section "Computer use agents"): "Evaluation requires running the
  agent in a real or sandboxed environment"; for WebArena it cites "backend state verification for
  tasks that modify data", such as confirming "an order was actually placed, not just that the
  confirmation page appeared".

## Limits

- Vendor-authored guidance, not a measured study: no success rates, run counts or costs for the
  practices it recommends.
- The page was read through a fetch tool that summarises; quotes above are the tool's extracts of the
  page and should be re-checked against the live page before they are quoted in a published document.
