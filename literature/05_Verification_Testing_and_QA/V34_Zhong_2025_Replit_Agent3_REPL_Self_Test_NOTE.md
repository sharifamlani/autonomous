# V34 Zhong (2025): Enabling Agent 3 to Self-Test at Scale with REPL-Based Verification

- **Citation:** Peter Zhong, Jacky Zhao and Ryan Carelli (Replit), "Enabling Agent 3 to Self-Test at Scale with REPL-Based Verification", Replit blog, 2025-12-15 (fetched via https://frontier.replit.com/automated-self-testing/, to which https://replit.com/blog/automated-self-testing redirects).
- **Link:** https://frontier.replit.com/automated-self-testing/
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor blog post (Replit), not an arXiv paper; the old replit.com/blog URL redirects to frontier.replit.com.

## What it says (quoted from the page)

- Failure mode: "Potemkin interfaces" are apps that look functional on first inspection but fail on interaction; buttons render and dashboards show numbers, yet event handlers are missing, data is mocked and links lead nowhere (fetch summary wording).
- Agent 3's autonomous runtime rose from about 20 minutes to over 200 minutes (roughly 10x); the self-testing flow runs multi-hundred-step tests at a median cost of $0.20 per session (vendor figures, fetch summary wording).
- Method: the agent writes Playwright JavaScript that runs in a notebook-style REPL (variables and browser sessions persist); it receives a stripped-down DOM with ARIA/test attributes, read-only database queries and new client and server logs; testing runs as a subagent because main-agent contexts often reach 80,000 to 100,000 tokens.
- Cost comparison (their estimate): a computer-use agent filling a 5-field form takes about $0.50 and 30-90 seconds; selecting a date 36 months ahead takes 36 model calls with browser-use but one call with code use.
