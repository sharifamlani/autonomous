# H27 Lopopolo (2026): Harness engineering: leveraging Codex in an agent-first world

- **Citation:** Lopopolo, R. (2026, February 11). *Harness engineering: leveraging Codex in an agent-first world.* OpenAI blog.
- **Link:** https://openai.com/index/harness-engineering/
- **Fetched:** 2026-11-21 (title, author and date checked on the fetched page).
- **Why no PDF:** a vendor engineering post; there is no PDF version.

## What it says (from the fetched page)

- An internal product built over five months with no hand-written code: about 1,500 merged pull
  requests, three engineers initially driving Codex (3.5 PRs per engineer per day), roughly a million
  lines of code; the authors estimate about a tenth of the hand-coding time.
- AGENTS.md as a map: one large instruction file fails, so AGENTS.md is about 100 lines and points to
  a structured `docs/` directory, "the system of record" ("give Codex a map, not a 1,000-page
  instruction manual"). Anything outside the repository is invisible to the agent.
- Mechanical enforcement: "These constraints are enforced mechanically via custom linters (Codex-generated,
  of course!) and structural tests"; lint errors carry remediation instructions for the agent.
- Entropy: agents copy bad patterns, so recurring background agents scan for drift and open small
  refactoring PRs ("Technical debt is like a high-interest loan").

## Limits

- Vendor-authored, about OpenAI's own product and staff; one project, no comparison arm, no cost
  figures, and no quality metrics beyond throughput. Agrees with H1 (short context files) but is not
  evidence for it.
