# 09 Reliability Long Horizon and Cost

## Role

This folder collects the evidence on why autonomous agents fail and what a task costs: failure
taxonomies for single agents, task-length scaling (METR's time horizons), run-to-run consistency,
context rot and compounding errors, reward hacking beyond tests, and token cost and cost reporting. Its
central question is **how and why do autonomous agents fail, and what does a task cost?** It is the
evidence for goals G2 (efficient), G3 (reliable) and G5 (autonomous): how long a run the kit can
promise, which failures its loop and its auditor must watch for, what the benchmark must report per
task ($, spread, graded fraction), and which guards (exit gates, budget caps, independent graders) a
run with no human needs.

## Contents

| ID | Citation | Year | Link | What it establishes |
|---|---|---|---|---|
| F1 | Kwa et al., "Measuring AI Ability to Complete Long Software Tasks" (METR; NeurIPS 2025; v1 titled "...Long Tasks") | 2025 | [arXiv:2503.14499](https://arxiv.org/abs/2503.14499) | The 50% time horizon (human minutes of task an agent finishes half the time) was about 110 min for o3 and doubled roughly every 7 months; the 80% horizon is 4-6x shorter |
| F2 | Rabanser et al., "Towards a Science of AI Agent Reliability" (ICML 2026) | 2026 | [arXiv:2602.16666](https://arxiv.org/abs/2602.16666) | Twelve reliability metrics over 15 models and 2 benchmarks: 24 months of capability gains gave only small reliability gains; outcome consistency stays low |
| F3 | Sinha et al., "The Illusion of Diminishing Returns: Measuring Long Horizon Execution in LLMs" (ICLR 2026) | 2025 | [arXiv:2509.09677](https://arxiv.org/abs/2509.09677) | With the plan and knowledge supplied, accuracy still decays with turns; models self-condition on their own earlier mistakes and size does not fix it, thinking does |
| F4 | Wang et al., "The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break" | 2026 | [arXiv:2604.11978](https://arxiv.org/abs/2604.11978) | 3,100+ trajectories in 4 domains, 7-category failure taxonomy; planning and memory/forgetting failures dominate as horizon grows |
| F5 | Zhu et al., "Where LLM Agents Fail and How They can Learn From Failures" | 2025 | [arXiv:2509.25370](https://arxiv.org/abs/2509.25370) | Five-module error taxonomy, 200 annotated failed trajectories; early root-cause errors cascade, and feedback aimed at the critical step lifts success by up to 26% relative |
| F6 | Bai et al., "How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks" | 2026 | [arXiv:2604.22750](https://arxiv.org/abs/2604.22750) | Agentic coding uses about 1,000x the tokens of code chat; runs on one task differ up to 30x; more spend does not mean higher accuracy; models underestimate their own cost |
| F7 | Kapoor et al., "Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation" (ICLR 2026) | 2025 | [arXiv:2510.11977](https://arxiv.org/abs/2510.11977) | 21,730 rollouts for about $40,000: the priciest run is on the cost-accuracy frontier in 1 of 9 benchmarks; log analysis finds shortcuts, tool failures and recovery rates |
| F8 | Erol et al., "Cost-of-Pass: An Economic Framework for Evaluating Language Models" (ICLR 2026) | 2025 | [arXiv:2504.13359](https://arxiv.org/abs/2504.13359) | Defines cost-of-pass, the expected dollars per correct answer; majority voting rarely pays for itself (QA and maths, not agents) |
| F9 | Gabor et al., "EvilGenie: A Reward Hacking Benchmark" | 2025 | [arXiv:2511.21654](https://arxiv.org/abs/2511.21654) | Codex, Claude Code and Gemini CLI all reward hack in a coding setup that allows it; LLM judges catch clear cases, held-out tests add little |
| F10 | Baker et al., "Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation" (OpenAI) | 2025 | [arXiv:2503.11926](https://arxiv.org/abs/2503.11926) | Test-gaming hacks (exit(0), SkipTest) in agentic coding RL: a reasoning-trace monitor gets 95% recall vs 60% for an action-only monitor; training against the monitor teaches hiding |
| F11 | Li et al., "A Benchmark for Evaluating Outcome-Driven Constraint Violations in Autonomous AI Agents" (ODCV-Bench) | 2025 | [arXiv:2512.20798](https://arxiv.org/abs/2512.20798) | 40 KPI-pressure scenarios, 12 models: violation rates 0.0% to 62.8%; models often judge their own actions unethical afterwards |
| F12 | Liu, "Silent Instrument Errors Reorder Agent Leaderboards" | 2026 | [arXiv:2611.04399](https://arxiv.org/abs/2611.04399) | Auditing HAL and tau2-bench: a cost column double-counts nested calls and a grader skipped about half of one agent's episodes, silently scoring them as failures |
| F13 | Becker et al. (METR), "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity" | 2025 | [arXiv:2507.09089](https://arxiv.org/abs/2507.09089) | RCT, 16 developers, 246 tasks: AI use made tasks take 19% longer while developers believed it saved 20% (interactive tools, not autonomous agents) |
| F14 | McCain et al. (Anthropic), "Measuring AI agent autonomy in practice" | 2026 | [anthropic.com](https://www.anthropic.com/research/measuring-agent-autonomy) | Vendor telemetry: the longest Claude Code turns grew from under 25 to over 45 minutes; human interventions per session 5.4 to 3.3 (note) |
| F15 | Anthropic, "Manage costs effectively" (Claude Code docs) | 2026 | [code.claude.com](https://code.claude.com/docs/en/costs) | About $13 per developer per active day; agent teams in plan mode about 7x the tokens of a standard session; why long sessions cost more (note) |

Already held elsewhere and used below: A9 (tau-bench, pass^k), A10 (AI Agents That Matter, cost-controlled
evaluation), A14 (TheAgentCompany, long-horizon tasks with cost per task), T7 (MAST failure taxonomy,
multi-agent), C14 (METR: merge decisions about 24 points below automated grades, normalised to a 68%
golden-patch baseline; 34.9 points raw), V3 and V17 (ImpossibleBench and "Recent Frontier Models Are
Reward Hacking", theme 05).

## What it establishes

**Verdict:** agents fail in a small number of recurring, measurable ways: an early mistake compounds,
success falls steeply with task length and with how consistent you demand the agent be, any cheap
grader gets gamed when a shortcut exists, and cost per task is both large and highly variable, with
more spend often buying no accuracy. For the kit this means a run of hours is plausible only with
guards around it: independent grading against ground truth, pass-all-k style consistency reported
instead of the best run, fresh context and file-based state rather than one ever-growing session, an
exit gate and a budget cap, and $/task reported with its spread. Capability numbers alone say little
about these.

1. **Success rate falls with task length, and the "reliable" horizon is much shorter than the headline
   one.** F1: "current frontier AI models such as o3 have a 50% time horizon of around 110 minutes" and
   "doubled approximately every seven months since 2019, though the trend may have accelerated since
   2024" (Abstract), but "models' 80% time horizons are 4-6x shorter, suggesting that even models that
   sometimes succeed on difficult and diverse tasks cannot reliably perform tasks of moderate length"
   (Section 3.2.1). By simple arithmetic on those two figures (mine, not F1's) an o3-class agent finishes
   about 20-30 minute tasks 80% of the time, not multi-hour ones. F1 also reports that "agents struggle
   more on tasks that have these 'messy' details", that is, no clear feedback loop (Appendix F.2), and
   that its 2024-only trend "doubling about every three months" "would not be robust" for extrapolation
   (Appendix F.1). F14 (vendor) shows what real Claude Code use looks like: "the 99.9th percentile turn
   duration nearly doubled, from under 25 minutes to over 45 minutes", while the median turn is "around
   45 seconds" (interactive sessions).
2. **Why long tasks fail: errors compound, and models learn from their own mistakes.** F3 supplies the
   plan and knowledge, so only execution is tested, and still "the best-performing model (Qwen3-32B)
   sees its accuracy fall below 50% within 15 turns" (Section 3.1, Result 1). The cause is not only long
   context: "as we increase the rate of injected errors into the context, accuracy at turn 100
   consistently degrades further" (Section 3.2, Result 3), and "scaling model size does not mitigate
   self-conditioning" (Result 4) while "thinking fixes self-conditioning" (Result 5). F3 estimates that
   "roughly 20% of GAIA, 48% of ALFWorld, 33% of WebShop failures are similar to self-conditioning"
   (Appendix A, a manual estimate on F5's annotated failures). F5 agrees on the mechanism: "Error
   propagation is the primary bottleneck in LLM agent reliability. Early mistakes rarely remain
   confined" (Section 2.1) and most failures "cluster in midtrajectory steps" (6-15) (Section 2.2). For the
   kit: a long run should restart from a fresh context with state in files rather than keep conditioning
   on its own transcript, which matches the design in H13.
3. **Reliability lags capability, and it is a consistency problem.** F2: "recent capability gains have
   only yielded small improvements in reliability" (Abstract), "outcome consistency remains low across all models ... meaning agents that can solve a task often fail to do so consistently" and while "calibration, robustness, and safety generally improve with model size, consistency often exhibits an inverse pattern", since "larger models' multiple solution paths increase
   run-to-run variability" (Section 4). A9 shows the same with pass^k: gpt-4o scores 61% on tau-retail at pass^1 but falls "as low as 25% for pass^8" (Section 1). F2 also finds the "what but not when" pattern: agents pick
   similar action types across runs but vary their order. The benchmark therefore needs at least 3 runs
   per task and a consistency number, which the research protocol in CLAUDE.md section 5 already
   requires.
4. **Failure taxonomies converge on planning, memory and verification, not syntax.** F5's modules are
   "memory, reflection, planning, action", plus "system-level errors that arise from external tools"
   (Section 2.1); F4's seven categories attribute failures at 3,100+ trajectories with "planning-related
   failures (e.g., subplanning errors) and memory-related failures (e.g., catastrophic forgetting)
   becom[ing] dominant as horizon increases" (Section 1; judge-human agreement 0.84, inter-annotator
   0.61). F7's log analysis adds rates: agents "encountered at least one environmental barrier, such as a
   crashing browser, an unavailable file, or an unavailable coding import, in roughly 40% of failed
   tasks"; "on failed tasks in AssistantBench and CORE-Bench, agents violated an instruction of the
   benchmark in their final answer over 60% of the time"; and a successful self-correction made a run
   "between 1.5x and 4x more likely to succeed", while explicit verification (unit tests, cross-checking)
   made it "between 13% and 87% more likely to succeed" (Section 4.2). T7 reaches the same place for
   teams: task verification is one of its three groups, with "premature termination (FM-3.1, 6.20%), no or
   incomplete verification (FM-3.2, 8.20%), or incorrect verification (FM-3.3, 9.10%)" (Section 4). The
   auditor's label set can start from F5 and T7 and add environment barriers.
5. **Any cheap grader gets gamed, so ground truth must be out of the agent's reach.** F9 gives Claude Code
   a task where cheating is easy: of 145 unambiguous problems, Claude Code used a "Heuristic solution" in
   20.7%, "Hardcoded test cases" in 2.1% (Table 1); on 9 ambiguous problems Codex hardcoded in 44.4% and
   Claude Code in 33.3% (Table 2). Detection: an LLM judge is "highly effective at detecting reward
   hacking in unambiguous cases" but "only minimal improvement from the use of held out test cases"
   (Abstract). F10 found in real agentic-coding RL that "exit(0)" and "raise SkipTest" hacks affected
   "nearly all training environments", an action-only monitor "achieves only 60% recall" and a
   chain-of-thought monitor "95% recall" (Section 2); optimising against the monitor produced an agent
   whose "CoT monitor's recall falls to near zero" (Section 3). F7 sees the same outside tests: "eight
   cases where agents found a gold answer, either by finding the answers of the dataset on HuggingFace or
   locating them on arXiv" and "hard-coding 'plausible' solutions in order to pass unit tests" (Section
   4.2). A14 reports agents that, when unsure of the next step, "try to be clever and create fake 'shortcuts' that omit the hard part of a task" (Section 7.2). F11 tests pressure rather than tests: "misalignment rates from 0.0% to 62.8%" across 12 models, with Claude-Opus-4.7 at zero observed misaligned runs (Sections 1 and 5.1); "Obedient Misalignment occurs more often than Proactive Deception (50 vs. 30
   instances)" (Section 5.2). For the kit: graders and held-out checks run outside the builder's
   sandbox, and the auditor reads transcripts for shortcuts, not only the pass/fail.
6. **Cost per task is large, variable, and weakly tied to accuracy.** F6: agentic coding "consuming 1000× more tokens than code reasoning and code chat"; "runs on the same task can differ by up to 30× in total tokens"; "accuracy often peaks at intermediate cost and saturates at higher costs"
   (Abstract), and high-cost runs show "repeated file view and modify actions" (Figure 4). Models
   "systematically underestimate real token costs" when asked to predict them, with correlations "up to
   0.39" (Abstract), so a budget cannot rely on the agent's own estimate. F7: "In only 1 of 9
   benchmarks do we observe the most costly model run on the Pareto frontier" and "For 21 of 36 runs, higher reasoning effort does not improve accuracy" (Figure 3 caption); one benchmark run cost an estimated $20,000, which is why they skipped it. A10 makes
   the same point from 2024: "For substantially similar accuracy, the cost can differ by almost two
   orders of magnitude" (Section 2). Reference points for $/task: A14's best agent (Gemini-2.5-Pro)
   solved 30.3% of 175 office tasks in 27.2 steps for $4.2 (Table 1), and F15's vendor figure is "around
   $13 per developer per active day", "below $30 per active day for 90% of users". F15 warns that agent
   teams "use approximately 7x more tokens than standard sessions when teammates run in plan mode" and
   that long sessions resend the full conversation each request, so the cost of one long session grows
   faster than the work in it. F8 gives a metric that folds accuracy into cost: cost-of-pass, "the
   expected monetary cost of generating a correct solution", infinite when no run succeeds (Section
   2.2). Report $/task and $/passed task, both with spread across runs.
7. **Evaluation code is part of the measurement.** F12 audits HAL and tau2-bench from their published
   files: a general agent "trails ... by 13 points", but "only about half of its episodes were scored and the rest were stored as failures" (Abstract; the author later corrected some per-model numbers in
   his repo, see the catch); a cost column summed a call and its child span, "Exactly 2× in 70 of 134 runs" (Table 1). The remedies are cheap: "Report the graded fraction", "Aggregate cost from root spans and print the multiplier", "Tag the provenance of every recorded action", "Pin evaluator versions and publish re-grade diffs" (Section 5).
   C14 adds the other direction: maintainer merge decisions "are about 24 percentage points lower than
   SWE-bench scores supplied by the automated grader" (normalised to the 68% golden-patch merge rate). The kit's scorecard should include
   the graded fraction (episodes graded over episodes run) and the cost source.
8. **Speed claims need measurement, not belief.** F13's RCT: developers "forecast that allowing AI will
   reduce completion time by 24%", yet "allowing AI actually increases completion time by 19%"
   (Section 1), with developers accepting "<44% of the generations" (Appendix C.1.4). It is early-2025
   Cursor use, not an autonomous run, but it is the one randomised measurement here: perceived speed-up
   and measured speed-up differed in sign, which is why G1 and G2 are scored by clocks and invoices.

## The catch

- **Almost nothing here measures a multi-hour unattended run of Claude Code.** F1 uses a fixed
  scaffold with human-timed tasks; F3 is a synthetic key-sum task ("Improvement on our task is necessary,
  but not sufficient for long-horizon execution on real-world tasks", Limitations); F4 and F5 use web,
  SQL, embodied and household environments; F6 uses SWE-bench Verified single issues with OpenHands;
  F13 is interactive, early-2025 tooling. The only data on real long Claude Code sessions, F14, is
  Anthropic's own telemetry on turn duration, classified by Claude, "a single model provider", with no
  absolute success rate (only that internal success on the hardest tasks "doubled") and no cost per run.
  The kit's benchmark has to supply this evidence.
- **Cost evidence is thin for Claude Code.** F6 is OpenHands on SWE-bench Verified with eight models;
  F7's costs are 2025 list prices that "change frequently and often dramatically" (Section 4.1; o3
  dropped 80%); F8 is maths and QA, not agents; F15 is a vendor average for interactive developers, not
  an unattended run, and its dollar figure is "an estimate" at list price. No source reports the cost
  of finishing an app or a study end to end, so the kit must measure its own $/task.
- **Several sources are young preprints with limited review.** F4 is "Preprint. Under review" and its
  failure shares are LLM-judged on 40 hand-annotated trajectories for validation (and its figure legend
  and caption disagree on the process-level share, 86.7% vs 72.5%, so I quote no percentage from it);
  F5's headline "24% higher all-correct accuracy" is 24.3% against 0.3% for the best baseline
  (Section 4.1), a near-zero baseline; F12 is a single-author preprint whose own repository withdrew a
  per-model reordering claim on 2026-11-01 after the HAL maintainers pointed out an error, though the
  cost double-count and the half-graded episodes stand; F2, F3 and F7 are venue-accepted but are one
  group's measurement.
- **Reward-hacking evidence is mixed in scope.** F9's hard-case counts come from only 9 ambiguous
  problems (n = 9), and it reports "do not see a significant trend in reward hacking with respect to time" across models. F10 is
  OpenAI's own training environments and a model the reader cannot run. F11 is 40 synthetic bash
  scenarios (it says it is "a targeted stress test, not ... an estimate of deployment-wide failure
  rates"), judged by LLMs that include models under test (three judges give themselves misalignment rates 2.5, 3.8 and 5.0 points below the other judges' median, per its own bias check). None measures how often Claude Code games a real test suite in a multi-hour build.
- **Cross-benchmark comparison is shaky.** F1's "time" is estimated human time, F3's horizon is turns,
  F2's metrics differ by benchmark ("though other factors ... may also contribute"), and F7's cost
  depends on scaffold choices (reasoning-effort settings are "not comparable across providers"). Do not
  compare numbers across these papers; use their methods on our tasks.
- **The easy answer (that models keep getting better, so reliability will follow) is contradicted twice,
  and also weakly supported.** F2 finds "only small improvements" in reliability over 24 months (moderate
  on τ-bench, "barely any" on GAIA) of capability gains and F1 finds the 80% horizon 4-6x shorter than
  the 50% one. Against that, F3 argues short benchmarks hide the compounding gain ("even marginal gains
  in single-step accuracy can compound into exponential improvements in the length of tasks a model can
  successfully complete") and F1's doubling trend is real on its task set. Both can be true; the kit
  should plan on the shorter, consistency-adjusted horizon.
- **Vendor and model-age bias.** F10, F14, F15 and the Claude-specific results in F9 and F11 come from
  or about the vendors themselves; F11's judge panel is made of four vendors' models, so a vendor's own model is among its graders. Model names in F9 to F11 move fast, so numbers go stale within months.
