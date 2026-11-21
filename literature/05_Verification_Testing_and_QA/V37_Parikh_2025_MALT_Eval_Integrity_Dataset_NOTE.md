# V37 Parikh (2025): MALT: A Dataset of Natural and Prompted Behaviors That Threaten Eval Integrity

- **Citation:** Neev Parikh and Hjalmar Wijk (METR), "MALT: A Dataset of Natural and Prompted Behaviors That Threaten Eval Integrity", METR blog, 2025-10-14.
- **Link:** https://metr.org/blog/2025-10-14-malt-dataset-of-natural-and-prompted-behaviors/
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** an independent evaluator's (METR) blog post and dataset, not an arXiv paper.

## What it says (quoted from the page)

- Dataset: 10,919 agent transcripts over 403 tasks (86 families) and 21 models, mainly from HCAST and RE-Bench; labels cover reward hacking and sandbagging, including 103 unprompted examples of generalized reward hacking (fetch summary wording).
- Monitors: the best simple prompted monitors reached AUROCs of 0.96 for reward hacking and 0.91 for sandbagging; at a 5% false-positive rate true-positive rates were 0.87 and 0.78. Hiding reasoning from the monitor made little difference for reward hacking but hurt sandbagging detection (fetch summary wording).
- Caveats stated (fetch summary wording): natural examples are scarce and lack diversity; prompted examples involve heavy editing and may be unrealistically obvious; sandbagging may be hard or impossible to detect from individual transcripts; reward-hacking sample sizes are small so estimates are noisy; the 8,229 presumed-benign runs have an estimated 6% label error rate.
