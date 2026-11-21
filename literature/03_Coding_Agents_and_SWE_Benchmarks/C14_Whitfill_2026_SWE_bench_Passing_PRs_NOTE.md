# C14 Whitfill (2026): Many SWE-bench-Passing PRs Would Not Be Merged into Main

- **Citation:** Whitfill, P., Wu, C., Becker, J., & Rush, N. (2026, March 10). *Many SWE-bench-Passing PRs Would Not Be Merged into Main.* METR research note.
- **Link:** https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
- **Fetched:** 2026-11-21 (page fetched directly; title, contributors "Parker Whitfill, Cheryl Wu, Joel Becker, and Nate Rush" and date "March 10, 2026" checked on the page).
- **Why no PDF:** a web-only research note ("Notes are unpolished research updates"); there is no PDF or arXiv version.

## What it says (quoted from the page)

- Design: "we had 4 active maintainers from 3 SWE-bench Verified repositories review 296 AI-generated
  pull requests (PRs)". Maintainers accepted or requested changes and gave the core reason (core
  functionality failure, patch breaks other code, or code quality).
- Noise control: "we also record maintainer merge decisions on 47 original human-written PRs that
  were actually merged into main (hereafter 'golden patches')"; scores are reported "as % of golden
  baseline", and "the golden baseline is 68%".
- Main result: "on average maintainer merge decisions are about 24 percentage points lower than
  SWE-bench scores supplied by the automated grader", and the rate of improvement "is 9.6 pp/yr
  slower for maintainer merge decisions".
- Raw (unnormalised) view: "maintainer merge rates are roughly one-third to one-half of automated
  grader pass rates".
- Models covered (conditional merge-rate figure): Claude 3.5 Sonnet (Old), Claude Sonnet 3.7,
  Claude Opus 4, GPT-5, Claude Sonnet 4.5.

## Limits (the authors')

- "We are not claiming that agents have a capability limitation that prevents them from passing
  maintainer review. It seems likely that better prompting and agent elicitation could resolve many
  of the remaining problems of code quality, not following repo standards, etc."
- "We are not comparing AI to humans in equal conditions. While models only have one attempt at
  submitting a solution, human developers iterate with feedback in most cases."
- "The most recent model in our study is Claude Sonnet 4.5, but more recent models might have
  different results." One agent harness, a subset of one benchmark, four reviewers.
