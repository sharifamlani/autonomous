# C36 Bui (2026): Measuring What Matters with Jules

- **Citation:** Nghi Bui, Georgios Evangelopoulos and Zack Elliott (Google), "Measuring What Matters with Jules", Google Developers Blog, 2026-06-22.
- **Link:** https://developers.googleblog.com/measuring-what-matters-with-jules/
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor developer-blog post (Google), not an arXiv paper; preliminary, internal codebases only.

## What it says (quoted from the page)

- Proactive coding agents should be judged on their insight policy: whether they decide what matters, what evidence supports it, and whether to interrupt the developer (fetch summary wording).
- Raising the exploration budget "from two rounds to three raised Hit@5 from 33% to 57%"; with one round the average top score was 4.5 out of 5 (fetch summary wording).
- Method: 705 bugs (1,178 CLs) from internal Google codebases, clustered by time and content; the codebase is reverted to its pre-fix state, the agent investigates for up to three rounds, an LLM judge scores each insight 1 to 5; metrics are average top score and Hit@K.
- Stated limits: preliminary results on an initial sample, data only from internal Google codebases, planned extension to public GitHub issues and PRs.
