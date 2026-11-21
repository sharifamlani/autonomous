# H13 Young (2025): Effective harnesses for long-running agents

- **Citation:** Young, J. (2025, November 26). *Effective harnesses for long-running agents.* Anthropic Engineering blog.
- **Link:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **Fetched:** 2026-11-21 (title, byline "Written by Justin Young" and date checked on the page).
- **Why no PDF:** a vendor engineering blog post; there is no PDF version.

## What it says (quoted from the page)

- Setup: "The very first agent session uses a specialized prompt that asks the model to set up the
  initial environment" (an `init.sh`, "a claude-progress.txt file that keeps a log of what agents
  have done", and an initial git commit).
- A JSON feature list of over 200 features, all starting as failing; the prompt says "It is
  unacceptable to remove or edit tests because this could lead to missing or buggy functionality."
- "the next iteration of the coding agent was then asked to work on only one feature at a time."
  "This incremental approach turned out to be critical to addressing the agent's tendency to do too
  much at once."
- Git as recovery: "This allowed the model to use git to revert bad code changes and recover working
  states of the code base."
- Browser testing: "Providing Claude with these kinds of testing tools dramatically improved
  performance" (Puppeteer MCP, testing as a human user would).
- Failure modes seen: the agent tried "to one-shot the app"; it "marks features as done
  prematurely" and "leaves the environment in a state with bugs or undocumented progress".

## Limits (the authors')

- "Claude can't see browser-native alert modals through the Puppeteer MCP."
- "it's still unclear whether a single, general-purpose coding agent performs best across contexts,
  or if better performance can be achieved through a multi-agent architecture."
- Vendor-authored; no success rates, costs or run counts are reported. Optimised for full-stack web
  apps only. Reference code: `anthropics/claude-quickstarts` (`autonomous-coding/`).
