# T30 Lin (2026): Scaling long-running autonomous coding

- **Citation:** Lin, W. (2026, January 14). *Scaling long-running autonomous coding.* Cursor blog
  (research).
- **Link:** https://cursor.com/blog/scaling-agents
- **Fetched:** 2026-11-21 (title, author and date checked on the page).
- **Why no PDF:** a vendor blog post; there is no PDF version.

## What it says (paraphrased from the page; no direct quotes)

- Scale: hundreds of concurrent agents on one project, over 1 million lines of code and trillions
  of tokens across experiments (the post's own totals); one browser build ran close to a week (about 1,000 files).
- What failed: shared-file locking (agents held locks too long; twenty agents slowed to the throughput
  of two or three); optimistic concurrency was simpler but, without hierarchy, agents avoided hard
  tasks and made small safe changes; an "integrator" role for quality control and conflict resolution
  created more bottlenecks than it solved (paraphrased).
- What worked: planners that explore and create tasks (and spawn sub-planners), workers that take a
  task and push when done without coordinating with other workers, and a judge that decides at the
  end of each cycle whether to continue; the next cycle starts fresh to counter drift.
- Model choice by role: GPT-5.2 judged better at extended autonomous work and as planner; Opus 4.5
  tended to stop early in the author's runs (paraphrased).

## Limits

- Vendor-authored, no controlled comparison (no single-agent arm, no cost or success rate per
  design), and the output was reviewed by the team, not graded. The same post says one migration passed CI and early checks but still needed
  careful review (paraphrased).
- The coordination design is worker-isolated with a central planner, the opposite of T16's
  peer lock-file design and consistent with T17: an unevaluated pattern, not a result.
