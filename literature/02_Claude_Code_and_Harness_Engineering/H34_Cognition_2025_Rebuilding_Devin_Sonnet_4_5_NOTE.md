# H34 Cognition (2025): Rebuilding Devin for Claude Sonnet 4.5: Lessons and Challenges

- **Citation:** The Cognition Team, "Rebuilding Devin for Claude Sonnet 4.5: Lessons and Challenges", Cognition blog, 2025-09-29.
- **Link:** https://cognition.com/blog/devin-sonnet-4-5-lessons-and-challenges
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor blog post (Cognition), not an arXiv paper.

## What it says (quoted from the page)

- Headline: the rebuilt Devin is "2x faster" and "12% better on our Junior Developer Evals" (vendor self-reported).
- "This 'context anxiety' can actually hurt performance." As the window fills the model summarises progress and becomes more decisive, sometimes leaving tasks incomplete; the model consistently underestimates how many tokens remain and is "very precise about these wrong estimates".
- Workaround: prompt reminders at both the start and end, and "enabling the 1M token beta but cap usage at 200k".
- "Sonnet 4.5 is notably more proactive about writing and executing short scripts and tests to create feedback loops"; it also used overly creative workarounds (fetching a page's HTML to check React work).
- Parallel tool calls use up context faster, which feeds the context anxiety.
