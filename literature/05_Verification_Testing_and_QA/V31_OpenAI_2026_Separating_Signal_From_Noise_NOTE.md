# V31 OpenAI (2026): Separating signal from noise in coding evaluations

- **Citation:** OpenAI (2026, July 8). *Separating signal from noise in coding evaluations.* OpenAI blog (no named authors).
- **Link:** https://openai.com/index/separating-signal-from-noise-coding-evaluations/
- **Fetched:** 2026-11-21 (title, date and publisher checked on the fetched page, read through a summarising fetch tool, so quotes should be rechecked on the live page before publication).
- **Why no PDF:** a vendor blog post; there is no PDF version.

## What it says (as read on the page)

- "we estimate that ~30% of SWE-bench Pro tasks are broken." An automated datapoint-analysis pipeline
  flagged 200 tasks (27.4%); a human annotation campaign (five engineers per task, reviewing
  independently) marked 249 (34.1%).
- Four recurring defects: overly strict tests, underspecified prompts, low-coverage tests, misleading prompts.
- Humans labelled more tasks broken than the agent pipeline; low-coverage tests were the most common
  human-selected issue (9.4% of the benchmark vs 4.1% for the agent pipeline).
- OpenAI states "we retract our earlier recommendation to adopt SWE-Bench Pro" (see V30).

## Limits

- Vendor-authored, not peer reviewed. Shows that even the benchmark picked to replace a flawed one had
  broken graders, so a grader needs auditing before it is trusted, including the kit's own.
