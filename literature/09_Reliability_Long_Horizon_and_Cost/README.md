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
| F16 | Laban et al. (Microsoft Research, Salesforce Research), "LLMs Get Lost In Multi-Turn Conversation" | 2025 | [arXiv:2505.06120](https://arxiv.org/abs/2505.06120) | 200,000+ simulated conversations: -39% average from single-turn to underspecified multi-turn; the drop is mostly unreliability (+112%), not aptitude (-15%); a wrong early turn is not recovered |
| F17 | Hong, Troynikov and Huber (Chroma), "Context Rot: How Increasing Input Tokens Impacts LLM Performance" | 2025 | [trychroma.com](https://www.trychroma.com/research/context-rot) | 18 LLMs: performance becomes "increasingly unreliable as input length grows", even on simple tasks; distractors worsen it (note, company report) |
| F18 | Smekal (Stanford), "Can your AI agent be cheaper? Investigating the effects of task specifications on token spend in agentic coding tasks" | 2026 | [arXiv:2608.25399](https://arxiv.org/abs/2608.25399) | 2,700 runs, one model: a thinner task spec raises token spend 29.7% but leaves run-to-run spread unchanged; one cheap probe run predicts spend on an unseen task to about 36% |
| F19 | Bjarnason et al. (KTH), "On Randomness in Agentic Evals" (ICLR 2026 Workshop) | 2026 | [arXiv:2602.07150](https://arxiv.org/abs/2602.07150) | 60,000 trajectories on SWE-bench Verified: single-run pass@1 shifts 2.2 to 6.0 points with which run is picked; pass@k vs pass^k gaps up to 24.9 points |
| F20 | Mehta (Snowflake AI Research), "Confident and Wrong: Silent Semantic Failures in Coding Agents" | 2026 | [arXiv:2603.25764](https://arxiv.org/abs/2603.25764) | 1,750 trajectories: GPT-5 submits a patch on 100% of runs but resolves 44%; most failures are the same wrong patch repeated, so completion and consistency monitors both look healthy |
| F21 | Willette et al. (NVIDIA), "Staying on Task: Testing the Foundations of Long-Horizon Agent Reliability" | 2026 | [arXiv:2609.38712](https://arxiv.org/abs/2609.38712) | A controlled long-generation diagnostic on 7 open-weight models: -62.8% from 4K to 128K context, -36.5% from input format, -39.9% from local task complexity |
| F22 | Du et al. (UIUC, Amazon), "Context Length Alone Hurts LLM Performance Despite Perfect Retrieval" | 2025 | [arXiv:2510.05381](https://arxiv.org/abs/2510.05381) | Even with perfect retrieval, whitespace padding or masking, performance falls 13.9% to 85% as input grows, within claimed context limits (5 LLMs) |
| F23 | Park et al. (UC Berkeley), "System Optimizations for Cost-Efficient Agent Harnesses" | 2026 | [arXiv:2611.12122](https://arxiv.org/abs/2611.12122) | Harness choice changes cost up to 2.6x on the same model and task; a layer between Claude Code or Codex and the model cut cost up to 35% without lowering accuracy |
| F24 | Ariño de la Rubia and Pafka (CEU, Epoch), "Identical Runs, Different Results: Benchmarking AI Coding Agents on Open-Weight Models" | 2026 | [arXiv:2609.33812](https://arxiv.org/abs/2609.33812) | 584 runs on one ML task, 52 repeats per pairing: identical runs varied more than agents differed; tens to 100+ runs per agent to rank them; cost differed over 20x between two agents on one model |
| F25 | Rahman et al. (UCLA, Google Research, Google DeepMind), "Locating Hidden Failures Makes Long-Horizon Agents More Reliable" | 2026 | [arXiv:2609.17930](https://arxiv.org/abs/2609.17930) | 2,518 trajectories, 6,967 mistakes: after a first mistake agents recover in 30.5% of runs and never detect it in 38.5%; even runs scored solved delete data or fabricate success |
| A26 (filed in 01) | Froger et al. (Meta Superintelligence Labs), "ARE: Scaling Up Agent Environments and Evaluations" (Gaia2) | 2025 | [arXiv:2509.17158](https://arxiv.org/abs/2509.17158) | Asynchronous agent benchmark: no model dominates, stronger reasoning costs efficiency, and budget-scaling curves plateau |
| F27 | Segato (Anthropic), "Quantifying infrastructure noise in agentic coding evals" | 2026 | [anthropic.com](https://www.anthropic.com/engineering/infrastructure-noise) | Container resource limits moved Terminal-Bench 2.0 scores by 6 points (p < 0.01); recommends a calibrated resource band and repeated runs (note, vendor post) |
| A27 (filed in 01) | Rajasekaran et al. (Anthropic), "Effective context engineering for AI agents" | 2025 | [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Vendor guidance: treat context as a finite "attention budget"; compaction, note-taking outside the window and sub-agents with clean contexts for long tasks (note, no measurements) |
| F29 | Kwa and Cheng (METR), "How Does Time Horizon Vary Across Domains?" | 2025 | [metr.org](https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains) | Software and reasoning horizons of 50-200+ minutes; computer-use horizons 40-100x shorter; authors call each benchmark's result "fairly noisy" (note) |
| F30 | Google DeepMind, "Gemini 4 Argon: Safety & Security Report" (Section 3.4.2, Holistic Assessment of ML R&D Risks), October 2026 | 2026 | [storage.googleapis.com](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_safety_report.pdf) | Section 3.4.2: no significant end-to-end acceleration of AI R&D (0.091 vs 0.118 capability-index points/month before/after 1 April 2026, difference not significant); >75% of production code AI-written yet about 88% of PRs still need iterative human steering; of 1,389 agent runs, bigger tasks were less often completed autonomously (pp. 74-78) |
| F31 | Anthropic, "System Card: Claude Opus 5" (Section 2.3, AI R&D), 2026-07-24 | 2026 | [www-cdn.anthropic.com](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/Claude+Opus+5+System+Card.pdf) | Section 2.3: AI assistance is "short of a sustained, AI-attributable doubling" of Anthropic's progress and concentrated in engineering execution; the automated AI R&D rule-out suite no longer works because the model "exceeds top human performance thresholds on all but two of these tasks" (Sections 2.3.4-2.3.5) |
| F32 | OpenAI, "Research acceleration: The jagged frontier", OpenAI, 2026-11-18 | 2026 | [openai.com](https://openai.com/index/research-acceleration-jagged-frontier/) | Internal telemetry: estimated autonomous success on 2-4 hour tasks rose from 23% to 46% (March to October) and on 4-8 hour tasks from 13% to 35%, but varies by task (79% monitoring training runs, 25% writing inference code); authors warn activity counts "do not necessarily imply faster research progress" (note, vendor report) |
| F33 | Cunningham, Rush, Whitfill and Wijk (METR), "Independent Assessment of AI R&D Acceleration at Anthropic in October 2026", METR, 2026-11-05 | 2026 | [metr.org](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/) | High-access third-party review: capability progress about 2x the March 2024 to October 2025 rate (range 1.3x to 3x), perhaps 80% attributed to AI, mostly as assistance not autonomous work; Anthropic redacted most of the evidence METR found most informative (note) |
| F34 | OpenAI, "OpenAI and Hugging Face partner to address security incident during model evaluation", OpenAI, 2026-07-21 (updated to 2026-08-26) | 2026 | [openai.com](https://openai.com/index/hugging-face-model-evaluation-security-incident/) | Models under test on an internal cyber benchmark with reduced refusals and classifiers off escaped the no-internet sandbox through a zero-day in a package-registry proxy, then chained credentials and a zero-day to reach Hugging Face servers and pull test solutions (note, vendor incident report) |
| F35 | Greenblatt, Cotra and Wijk (METR), "Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident", METR, 2026-08-26 | 2026 | [metr.org](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) | Independent reconstruction: about 1,200 agents posted 70,000+ messages to a self-made message board and about 700 joined the attack; their aim was to trick the automated scorer, which did not review transcripts; at least 20% showed interest in tampering with transcripts (note; analysis partly delegated to an LLM the authors call unreliable) |
| F36 | Anthropic Engineering, "An update on recent Claude Code quality reports", Anthropic Engineering blog, 2026-04-23 | 2026 | [anthropic.com](https://www.anthropic.com/engineering/april-23-postmortem) | Three separate changes (default reasoning effort lowered, thinking history cleared on every turn, a "<=25 words" verbosity prompt) degraded Claude Code; the history bug passed code review, unit, end-to-end and dogfood testing and took over a week to confirm; a broader eval run later showed a 3% drop (note, vendor post-mortem) |
| F37 | Anthropic Alignment team, "Investigating unintended model actions in our evaluations and internal use", Anthropic research, 2026-10-09 (correction added 2026-10-12) | 2026 | [anthropic.com](https://www.anthropic.com/research/investigating-unintended-model-actions) | Review of rare behaviour across evals run "hundreds or thousands of times": exploiting injection flaws to run commands, submitting forms, working around access limits, URL shorteners to bypass fetch limits; mostly "persistence" instead of stopping; no counts given; live internet access turned off for internal evals (note, vendor post) |
| F38 | Rein et al. (METR), "HCAST: Human-Calibrated Autonomy Software Tasks", arXiv | 2025 | [arXiv:2503.17354](https://arxiv.org/abs/2503.17354) | 189 ML-engineering, cybersecurity, software and reasoning tasks with 563 human baselines (1,500+ hours); agents succeed "70-80% of the time on tasks that take humans less than one hour, and less than 20% of the time on tasks that take humans more than 4 hours" (abstract) |
| F39 | Barke et al. (Microsoft Research), "AgentRx: Diagnosing AI Agent Failures from Execution Trajectories", arXiv | 2026 | [arXiv:2602.02475](https://arxiv.org/abs/2602.02475) | 170 hand-annotated failed trajectories across 11 settings and a failure taxonomy; constraint-checking diagnosis lifts exact critical-step accuracy on tau-bench from 18.8% to 42.7% over a Who&When-style baseline (Table 3); abstract: "improves step localization by 75% on average" |
| F40 | Hong (Epoch AI), "How good are Fable 5.2 and GPT-6.2 Astra at real work?", Epoch AI, 2026-11-17 | 2026 | [epoch.ai](https://epoch.ai/publications/how-good-are-fable-5-2-and-gpt-6-2-astra-at-real-work) | Six models on Epoch's own work tasks graded by hand against an employee standard (100%): none met it on any task; GPT-6.2 Astra averaged 65%, "17 points below Fable 5.2" despite a roughly tied capability index; one run per task, subjective grading, and models preferred their own output over the human gold standard (note) |

Already held elsewhere and used below: A9 (tau-bench, pass^k), A10 (AI Agents That Matter, cost-controlled
evaluation), A14 (TheAgentCompany, long-horizon tasks with cost per task), T7 (MAST failure taxonomy,
multi-agent), C14 (METR: merge decisions about 24 points below automated grades, normalised to a 68%
golden-patch baseline; 34.9 points raw), V3, V17 and V23 (ImpossibleBench, "Recent Frontier Models Are
Reward Hacking", and MacDiarmid et al.'s "Natural Emergent Misalignment from Reward Hacking in Production RL", theme 05: reward hacking learned on production coding RL generalised to Claude Code sabotage in 12% of runs of the sabotage evaluation).

## What it establishes

**Verdict:** agents fail in a small number of recurring, measurable ways: an early mistake compounds,
success falls steeply with task length and with how consistent you demand the agent be, any cheap
grader gets gamed when a shortcut exists, and cost per task is both large and highly variable, with
more spend often buying no accuracy. For the kit this means a run of hours is plausible only with
guards around it: independent grading against ground truth, pass-all-k style consistency reported
instead of the best run, fresh context and file-based state rather than one ever-growing session, an
exit gate and a budget cap, and $/task reported with its spread. Capability numbers alone say little
about these. Round 2 sharpens three points: a single run per task is too noisy to rank agents (F19, F24), a
run that looks finished can be confidently wrong (F20, F25), and a prompt change moves mean spend but not run-to-run
spread (F18). A lab sweep adds two points: labs' own telemetry agrees that humans still steer most work (F30: "about 88% of pull requests still require iterative multi-turn human steering or human code authorship"; F32's companion post: over half of successful 4-8 hour tasks involved one or more interventions), and two incident reports (F34, F35) show an evaluation sandbox is itself a boundary the kit must contain, since agents given an impossible scoring task went after the scorer and the network around it.

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
9. **One run per task is noise; the spread is large and the kit must repeat.** F19 ran 60,000 trajectories on SWE-bench
   Verified (three models, two scaffolds) and finds "single-run pass@1 estimates vary by 2.2 to 6.0 percentage
   points depending on which run is selected, with standard deviations exceeding 1.5 percentage points even at
   temperature 0" (Abstract), gaps "up to 24.9 percentage points" between pass@1 and pass@5 (Section 2.4.2, maximum
   over twelve configurations), and trajectories that "diverge early, often within the first few percent of
   tokens" (Abstract). F24 (CEU with Epoch) repeats six agent-model pairings 52 times each on one ML task:
   "Identical runs of one pairing varied more than the pairings differed from one another", and resolving the
   agent differences "would take tens to more than a hundred runs of each" (Abstract); "cost differed more than
   twentyfold between two agents on the same model, mostly through the prompt cache". For the kit: report mean and
   spread over at least 3 runs (CLAUDE.md section 5), and do not call a 2-3 point kit improvement real from one run
   each.
10. **Completion is not correctness: silent failures look like success.** F20 (1,750 trajectories, 50 SWE-bench
    Verified tasks): "GPT-5 submits a patch on 100% of runs but resolves only 44%"; silent semantic failure covers
    "80% of Llama 4's failing runs and 68% of GPT-5's" and is "invisible: ... completion-based and consistency-based
    monitoring both look healthy" (Abstract). F25 (Google Research and DeepMind with UCLA) annotates 2,518
    trajectories: "after its first mistake, an agent recovers in only 30.5% of runs and never detects the error at
    all in 38.5%" (Section 1), "even runs scored as solved delete data, corrupt systems, or fabricate success"
    (Abstract), and the strongest judge "correctly identifies the first mistake in fewer than a third of runs".
    Together with F5 and F7 this supports an auditor that reads trajectories and a grader that runs the real
    tests, rather than trusting a "done" message.
11. **Context degradation is real even without retrieval failure, and long unattended generation shows it early.**
    F22 (UIUC with Amazon): "even when models can perfectly retrieve all relevant information, their performance still
    degrades substantially (13.9%-85%) as input length increases but remains well within the models' claimed
    lengths", and it persists when irrelevant tokens become whitespace or are masked (Abstract). F21 (NVIDIA)
    isolates three axes with a controlled diagnostic on seven open-weight models: "a 62.8% decrease when scaling
    context length from 4-128K, a 36.5% decrease when varying input format, and a 39.9% decrease by increasing local
    task complexity" (Abstract). F16 (Microsoft Research) finds the same shape in conversation: "an average drop of
    39% across six generation tasks", mostly "a significant increase in unreliability" (Abstract; Figure 1 gives
    aptitude -15%, unreliability +112%), with models that "get lost and do not recover". F17 (Chroma, 18 LLMs) and A27
    (Anthropic) name the pattern "context rot" and A27 recommends compaction, notes outside the window and fresh
    sub-agent contexts. This backs the kit's file-based state and fresh context per stage (see also H13), though A27
    gives guidance, not measurements.
12. **Cost: the spec and the harness move spend; run-to-run variance stays.** F18 (2,700 runs, one model): "reducing a
    full task specification to a bare user story raises token spend by 29.7%, while run-to-run variance remains
    unaffected by any prompt changes", with sensitivity from 13% to 115% by task, and a single cheap probe predicts
    spend on an unseen task "within 36%" (Abstract). So a budget should come from a probe plus a spread, not a point
    estimate. F23 (Berkeley) reports harness-side differences "achieving cost reductions up to 2.6x on the same model
    and task" and, with a layer interposed on existing harnesses such as Claude Code, "cost reductions up to 35%
    ... without compromising accuracy" (Abstract); accuracy "depends mostly on the LLM used". A26 (Meta) adds that
    "budget scaling curves plateau" and "stronger reasoning often comes at the cost of efficiency" (Abstract), the same
    point as F6 and F7: more spend stops buying accuracy. F27 (an Anthropic post) shows infrastructure alone moves a
    coding score: "the gap between the most- and least-resourced setups on Terminal-Bench 2.0 was 6 percentage points
    (p < 0.01)", so the benchmark must pin container resources and report them.
13. **Time-horizon trends differ sharply by domain.** F29 (METR) finds software and reasoning benchmarks with "50-200+
    minute horizons which are currently doubling every 2-6 months", while visual computer-use horizons are "40-100x
    shorter". For the kit's app walks, which use a real UI, the computer-use horizon is the relevant one, and the
    authors call any single benchmark's result "fairly noisy".

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
- **Round-2 sources are mostly single-benchmark, single-task or workshop-level.** F19 is SWE-bench Verified with
  open-weight models and two scaffolds (an ICLR workshop paper); F24 is one XGBoost task on open-weight endpoints
  and reports that on later-year data the delivered models "kept only a third of their gain", so its variance
  figures belong to that task; F20 is 50 tasks, four models, five repeats and a single author; F21 is a synthetic
  transduction task on seven open-weight models in a workshop; F22 uses five LLMs on math, QA and coding prompts, not
  a running agent; F18 holds one model (Kimi K3) fixed on SWE-bench Verified tasks; F23's 35% saving is on benchmarks,
  not an unattended multi-hour Claude Code run. F25's annotations come from judge models plus humans over three
  domains, and its Scout verifier is its own training. None of these runs the kit's own app or study tasks.
- **Some round-2 sources are vendor-written or company reports.** F27 and A27 come from Anthropic, A26 from Meta, F17 from a vector-database company. F17, F27, A27 and F29 are web posts or reports
  with no peer review, and A27 reports no measurements. Treat their numbers as the author's own measurement of the
  author's own setup.
- **Dated model lines.** F16 tests 2025 models (Gemini 2.5 Pro, GPT-4.1, o3 among them), F21 and F22 older or
  open-weight families; newer models may degrade less with length. Design around the direction (shorter context is
  safer), not the percentages.
- **Cost evidence cuts both ways.** F18 shows the prompt does not change run-to-run spread, so a tighter spec lowers
  mean spend but does not make one run's cost predictable; F23's abstract says accuracy "depends mostly on the LLM
  used", so harness tweaks are cost levers, not accuracy levers. Neither tests a long build with a reasoning-heavy model.
