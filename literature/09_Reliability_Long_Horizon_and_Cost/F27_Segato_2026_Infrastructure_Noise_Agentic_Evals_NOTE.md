# F27 Segato (2026): Quantifying infrastructure noise in agentic coding evals (Anthropic)

- **Citation:** Gian Segato (Anthropic), "Quantifying infrastructure noise in agentic coding evals",
  Anthropic Engineering blog, published 2026-02-05.
- **Link:** https://www.anthropic.com/engineering/infrastructure-noise
- **Fetched:** 2026-11-21 (page fetched in this session; title, author and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor engineering blog post, with no PDF or arXiv version.
- **Vendor-authored caveat:** written by Anthropic about its own evaluation setup; no outside replication.

## What it says (quoted from the page)

- Resource limits move scores: "the gap between the most- and least-resourced setups on Terminal-Bench
  2.0 was 6 percentage points (p < 0.01)."
- Infra errors fall from 5.8% to 2.1% when going from strict enforcement to 3x headroom (p < 0.001), while
  success differences from 1x through 3x stay "within the margins of noise" (p = 0.40); the lift at
  uncapped resources over 1x is p < 0.01.
- Recommendation: specify both a guaranteed allocation and a separate hard kill threshold per task, and
  "The band between them should be calibrated so that scores at the floor and ceiling fall within noise
  of each other."
- On repeated runs for shared coding evals: "running at multiple times and on multiple days would help
  average out the noise."
