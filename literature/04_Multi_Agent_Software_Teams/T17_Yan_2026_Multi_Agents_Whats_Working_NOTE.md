# T17 Yan (2026): Multi-Agents: What's Actually Working

- **Citation:** Yan, W. (2026, April 22). *Multi-Agents: What's Actually Working.* Cognition blog
  (follow-up to "Don't Build Multi-Agents", 2025-06-12).
- **Link:** https://cognition.com/blog/multi-agents-working
- **Fetched:** 2026-11-21 (title, author and date checked on the page; the 2025 post
  https://cognition.com/blog/dont-build-multi-agents was fetched the same day for its two principles).
- **Why no PDF:** a vendor blog post; there is no PDF version.

## What it says (quoted from the page)

- "Our original observations still hold today for parallel-writer swarms." What works now are "setups
  where multiple agents contribute intelligence to a task while writes stay single-threaded."
- Review loop: "Devin Review catches an average of 2 bugs per PR, of which roughly 58% are severe";
  "we found this technique to work best when the coding and review agents do not share any context
  beforehand."
- Failure modes: parallel agents make conflicting implicit decisions about "style, edge cases, and
  code patterns"; managers "default to being overly prescriptive"; "Agents assume they share state with
  their children when they don't."
- Cost: "the explosion of agent usage has resulted in an explosion of costs."
- The 2025 post's two principles: "Share context, and share full agent traces, not just individual
  messages" and "Actions carry implicit decisions, and conflicting decisions carry bad results."

## Limits

- Vendor-authored opinion from the maker of Devin; the 58%-severe figure is the vendor's own count
  with no stated denominator, benchmark or comparison against a single agent.
