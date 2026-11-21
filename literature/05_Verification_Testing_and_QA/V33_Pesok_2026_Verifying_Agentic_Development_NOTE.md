# V33 Pesok (2026): Verifying Agentic Development at Scale

- **Citation:** Ido Pesok (Cognition), "Verifying Agentic Development at Scale", Cognition blog, 2026-05-29.
- **Link:** https://cognition.com/blog/testing-development
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor blog post (Cognition), not an arXiv paper; no pass/fail rates reported.

## What it says (quoted from the page)

- Method (fetch summary wording): "Test plan first" (Devin writes a plan grounded in the source code before testing, which the author says reduces invented app paths); "Annotate expectations" (Devin logs expected behaviour before each action and marks assertions as passed, failed or untested, making it harder to rationalise unexpected results as passes); repeated steps such as login moved into a deterministic testing skill in the repo to cut flakiness.
- Each run produces a test report with labelled screenshots and a chaptered video.
- Known limitations (fetch summary wording): screenshots taken too early or late can miss transient UI such as toasts; models sometimes run JavaScript to force app states instead of using the UI like a real user would; the team is addressing this with evals and harness guardrails.
- Scale claims: engineers ran "10 to 20 Devins in parallel"; test runs approved per day "have more than doubled" in a couple of months. No success rates are given.
