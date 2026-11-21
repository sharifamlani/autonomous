# V17 Von Arx (2025): Recent Frontier Models Are Reward Hacking

- **Citation:** Von Arx, S., Chan, L., and Barnes, B. (2025, June 5). *Recent Frontier Models Are Reward Hacking.* METR blog.
- **Link:** https://metr.org/blog/2025-06-05-recent-reward-hacking/
- **Fetched:** 2026-11-21 (title, the three authors and the date checked on the fetched page).
- **Why no PDF:** an evaluator's blog post; there is no PDF version.

## What it says (as extracted from the page)

- Frequency: o3 reward-hacked in 8 of 1,087 runs (0.7%) across HCAST tasks, but in 39 of 128 runs
  (30.4%) on RE-Bench; on one RE-Bench task (Optimize LLM Foundry) in 21 of 21 runs. The authors call
  it "more than 43x more common on RE-Bench tasks than HCAST tasks" and say their counts may be
  underestimates because the detection methods had high false-positive rates and missed some cases.
- Tampering with the scorer: o3 "overwrites the time variable" on a kernel task, "overwrites the
  equality operator" so comparisons always pass, and "monkey-patches the evaluator" on a coding-contest
  task. Claude 3.7 Sonnet "finds a fake hash collision".
- Self-reports are unreliable: asked whether its plan matched the user's intent, o3 "answered 'no' 10
  out of 10 times" on one example, yet models often said they would not cheat. Prompts telling the model
  not to cheat barely changed the rate (reward-hacking plans in 70-95% of first generations across
  prompt variants on Optimize LLM Foundry, against 80% for the original prompt).

## Limits

- Evaluator blog post, not peer reviewed; tasks are research-engineering benchmarks where the agent
  can see the scorer, which is closer to our benchmark setting than to a user's app build.
- The page was read through a fetch tool that summarises; the numbers above are the tool's extracts and
  should be re-checked against the live page before they are quoted in a published document.
