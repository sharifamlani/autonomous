# H33 Katz (2026): Improved token efficiency for longer agent runs

- **Citation:** Jediah Katz, Connor O'Keefe and Calvin Yee (Cursor), "Improved token efficiency for longer agent runs", Cursor blog (Research), 2026-09-23.
- **Link:** https://cursor.com/blog/improved-token-efficiency
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor blog post (Cursor), not an arXiv paper; measured by the vendor's own A/B tests.

## What it says (quoted from the page)

- Harness changes "reduced token costs for users by 7% without reducing agent quality".
- Trimming instructions allowed "us to trim roughly 66% of our system prompt"; earlier MCP-tool work cut total tokens 46.9% in sessions that called an MCP tool; moving built-in tools to dynamic loading cut static-context description tokens 60%; explicit cache breakpoints cut cold cache misses 20%; numbering every tenth line of a file read instead of every line cut cache-read tokens 1.6% (fetch summary figures).
- Method: A/B tests on a large user base, which the authors treat as more reliable than evals because evals often cover "hard" problems that do not reflect real traffic; they tracked token usage, cost, latency, tool-call errors and overall agent usage to check quality did not drop.
