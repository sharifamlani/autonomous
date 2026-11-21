# V36 Hume (2026): Designing AI-resistant technical evaluations

- **Citation:** Tristan Hume (Anthropic), "Designing AI-resistant technical evaluations", Anthropic Engineering blog, 2026-01-21.
- **Link:** https://www.anthropic.com/engineering/AI-resistant-technical-evaluations
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor engineering blog post (Anthropic), not an arXiv paper.

## What it says (quoted from the page)

- The performance-engineering take-home (1,000+ candidates since early 2024) was beaten twice: Claude Opus 4 beat most human applicants within the 4-hour limit; after the limit was cut to 2 hours, "Claude Opus 4.5 matched even those" and its 2-hour score "matched the best human performance within that time limit" (fetch summary wording for the second clause).
- "The original worked because it resembled real work. The replacement works because it simulates novel work." A transposition problem fell quickly; a Zachtronics-style puzzle set held up against Opus 4.5 on one medium-hard puzzle.
- Clock cycles (lower is better): Opus 4 after many hours 2,164; Opus 4.5 casual session 1,790; Opus 4.5 after 2 hours in the harness 1,579; Opus 4.5 after 11.5 hours 1,487; Opus 4.5 in an improved harness after many hours 1,363. The original take-home is public on GitHub.
