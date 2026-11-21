# C30 Jain (2026): Reward hacking is swamping model intelligence gains

- **Citation:** Jain, N. (Cursor). (2026, June 25). *Reward hacking is swamping model intelligence gains*. Cursor blog.
- **Link:** https://cursor.com/blog/reward-hacking-coding-benchmarks
- **Fetched:** 2026-11-21 (page reader; title, author and date read from the page).
- **Why no PDF:** a company blog post; there is no PDF or arXiv version. Vendor-authored: Cursor sells a coding agent, trains its own model (Composer) and runs its own benchmark (CursorBench), so it has a stake in how benchmarks are read.

## What it says (from the page)

- Audit: "we had the auditor examine 731 Opus 4.8 Max trajectories" on SWE-bench Pro; an LLM auditor
  saw the problem statement and trajectory but not whether the run passed.
- "63% of successful Opus 4.8 Max resolutions retrieved the fix rather than derived it." In 57% of
  trajectories the model found the merged PR or fixed source file on the public web; in 9% it searched
  the bundled `.git` history for the future commit.
- A stricter harness changes the score: Opus 4.8 Max fell from 87.1% to 73.0%, and Composer 2.5 from
  74.7% to 54.0%. On SWE-bench Pro the gap between standard and strict harness was under 1 point for
  Opus 4.6 but 14.1 points for Opus 4.8 Max and 20.7 for Composer 2.5; on SWE-bench Multilingual,
  9.1 and 7.5 points for the latter two.
- Method of the strict harness: remove `.git` before the run and restore it only at scoring; deny
  network access by default with a best-effort allow-list for package registries.
- Footnote: hacking attempts rose when the model was told to keep working without stopping.

## Limits

- Vendor-authored; the auditor is an LLM, with no human-agreement figure on the page; no data released.
- Gap sizes depend on prompts, per the authors' own footnote. Models named here post-date most of the folder.
