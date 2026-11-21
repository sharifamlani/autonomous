# H31 Martin (2026): Scaling Managed Agents: Decoupling the brain from the hands

- **Citation:** Lance Martin, Gabe Cemaj and Michael Cohen (Anthropic), "Scaling Managed Agents: Decoupling the brain from the hands", Anthropic Engineering blog, 2026-04-08.
- **Link:** https://www.anthropic.com/engineering/managed-agents
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor engineering blog post (Anthropic), not an arXiv paper.

## What it says (quoted from the page)

- Three parts: a "session" (a durable log of everything in a run; the harness reads slices of it so context lives outside Claude's window), a "harness" (the loop that calls Claude and routes tool calls; it holds no state that must survive a crash) and a "sandbox" (where Claude runs code; treated as replaceable, credentials kept out of reach of generated code). Each sits behind its own interface (fetch summary wording).
- Containers are disposable: a failed one surfaces as a tool-call error and Claude can retry on a new one; a crashed harness restarts and resumes from the session log (fetch summary wording).
- "our p50 TTFT dropped roughly 60% and p95 dropped over 90%" after decoupling (TTFT = time to first token).
- Managed Agents is described as "a hosted service in the Claude Platform that runs long-horizon agents on your behalf", designed to outlast any single harness implementation.
