# 04 Multi Agent Software Teams

## Role

This folder collects the evidence on role-based agent teams for software: ChatDev, MetaGPT and their
successors, agent code review, debate and cross-checking, process models (waterfall, agile), failure
taxonomies, and head-to-head comparisons with one strong agent at matched cost. Its central question is
**do role-based multi-agent teams beat one strong agent?** It informs the app factory's shape
(Main + builder + QA + tester), whether each role earns its tokens, what the QA and tester handoffs
must contain, and how the benchmark must score a team against a no-team arm at equal budget.

## Contents

| ID | Citation | Year | Link | What it establishes |
|---|---|---|---|---|
| T1 | Qian et al., "ChatDev: Communicative Agents for Software Development" (ACL 2024) | 2023 | [arXiv:2307.07924](https://arxiv.org/abs/2307.07924) | The founding waterfall-of-roles team (CEO, CTO, programmer, reviewer, tester); beats a one-shot single-agent baseline and MetaGPT on its own metrics, at about 3× the tokens |
| T2 | Hong et al., "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework" (ICLR 2024) | 2023 | [arXiv:2308.00352](https://arxiv.org/abs/2308.00352) | Roles that hand each other structured documents; role ablation raises executability 1.0 → 4.0 for $0.915 → $1.385; executable feedback adds +4.2 / +5.4 pp |
| T3 | Chen et al., "AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors" | 2023 | [arXiv:2308.10848](https://arxiv.org/abs/2308.10848) | On HumanEval a group beats a CoT agent (83.5 → 89.0, GPT-4), but a single agent using the same scaffold ("Solo") captures most of the gain; group discussion hurt GPT-3.5 on 2 of 3 tasks |
| T4 | Huang et al., "AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation" | 2023 | [arXiv:2312.13010](https://arxiv.org/abs/2312.13010) | A separate test-designer agent beats one agent writing both code and tests (79.9 vs 71.3 pass@1 HumanEval) because same-agent tests are biased by the code; three agents cost far fewer tokens than ChatDev or MetaGPT |
| T5 | Nguyen et al., "AgileCoder: Dynamic Collaborative Agents for Software Development based on Agile Methodology" | 2024 | [arXiv:2406.11912](https://arxiv.org/abs/2406.11912) | Sprint and backlog process beats MetaGPT and ChatDev on HumanEval/MBPP and executability, at more tokens and time; no single-agent control |
| T6 | Tao et al., "MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution" | 2024 | [arXiv:2403.17927](https://arxiv.org/abs/2403.17927) | Four-role issue fixer on SWE-bench; removing the QA Engineer drops resolved from 13.94% to 10.63% |
| T7 | Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (NeurIPS 2025) | 2025 | [arXiv:2503.13657](https://arxiv.org/abs/2503.13657) | 1,642 annotated traces, 7 frameworks, 14 failure modes in 3 groups; 41% to 86.7% failure rates; role-spec fix +9.4%, added verification step +15.6% for ChatDev |
| T8 | Tran and Kiela, "Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets" | 2026 | [arXiv:2604.02460](https://arxiv.org/abs/2604.02460) | At matched thinking-token budgets a single agent equals or beats five multi-agent designs, except at tiny budgets and under heavily corrupted context, where a sequential team wins (Section 5.3; reasoning tasks, not coding) |
| T9 | Mohammadabadi, "More Agents, More Samples, or More Thinking? Untangling Coordination, Ensembling, and Test-Time Compute in Multi-Agent LLMs" | 2026 | [arXiv:2611.17610](https://arxiv.org/abs/2611.17610) | Synthesis of 9 studies / 516 configurations: against sample- or budget-matched baselines multi-agent averages -0.042 accuracy and is at or below baseline in 74% of contrasts |
| T10 | Zhang et al., "Stop Overvaluing Multi-Agent Debate -- We Must Rethink Evaluation and Embrace Model Heterogeneity" | 2025 | [arXiv:2502.08788](https://arxiv.org/abs/2502.08788) | 5 debate methods x 9 benchmarks x 4 models: none wins more than 20% of 36 scenarios against plain CoT; mixing different models is what helps |
| T11 | Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet" (ICLR 2024) | 2023 | [arXiv:2310.01798](https://arxiv.org/abs/2310.01798) | Without external feedback, same-model review degrades answers; debate at equal responses loses to majority voting (83.2 vs 85.3, GSM8K) |
| T12 | Zeng et al., "Benchmarking and Studying the LLM-based Agent System in End-to-End Software Development" | 2025 | [arXiv:2511.04064](https://arxiv.org/abs/2511.04064) | Controlled single vs developer-then-tester vs designer-developer-tester waterfall on one toolset: 45.7% vs 49.5% vs 27.7% of requirements; the design handoff hurt |
| T13 | Chowdhury et al., "From Industry Claims to Empirical Reality: An Empirical Study of Code Review Agents in Pull Requests" (MSR 2026) | 2026 | [arXiv:2604.03196](https://arxiv.org/abs/2604.03196) | Among 3,109 agent PRs (from AIDev's 19,450), bot-only review merges 45.20% vs 68.37% human-only; 60.2% of bot-only reviews are 0-30% signal |
| T14 | Qiu et al., "Adversarial Review: Structured Disagreement for Grounded Agentic Code Review" (ICML 2026 Workshop on DL4C) | 2026 | [arXiv:2608.18167](https://arxiv.org/abs/2608.18167) | Three agents (coder, reviewer, critic) beat a 5-agent team and one agent on LiveCodeBench and SWE-bench Verified (75.2 vs 71.6%), at 4.5× tokens; naive agreement ("false consensus") hides bugs |
| T15 | Xia et al., "Passes Alone, Fails Together: Benchmarking Semantic Coordination in Parallel LLM-Agent Development" (EXPRESS 2026) | 2026 | [arXiv:2609.25396](https://arxiv.org/abs/2609.25396) | Parallel agents' patches pass alone and fail merged in 97% of constructed runs; one message about the concurrent change recovers 82%; rare in mined real PRs |
| T16 | Carlini, "Building a C compiler with a team of parallel Claudes" (Anthropic Engineering) | 2026 | [anthropic.com](https://www.anthropic.com/engineering/building-c-compiler) | 16 parallel Claudes, ~2,000 sessions, ~$20,000: a team works when the task verifier is near-perfect and coordination is a lock file in git (note) |
| T17 | Yan, "Multi-Agents: What's Actually Working" (Cognition blog) | 2026 | [cognition.com](https://cognition.com/blog/multi-agents-working) | Parallel writers still fail; what works is several agents contributing intelligence while writes stay single-threaded, with a reviewer that shares no context with the coder (note) |
| T18 | Kim et al. (MIT, Google Research, Google DeepMind), "TeamBench: Evaluating Agent Coordination under Enforced Role Separation" | 2026 | [arXiv:2605.07073](https://arxiv.org/abs/2605.07073) | Planner/Executor/Verifier with OS-enforced separation, 851 templates: team vs solo is +0.5 points (p = 0.20); verifiers approve 49.4% of submissions the grader rejects; teams help only where solo is weak |
| T19 | Khatua et al. (Stanford, SAP Labs), "CooperBench: Why Coding Agents Cannot be Your Teammates Yet" | 2026 | [arXiv:2601.13295](https://arxiv.org/abs/2601.13295) | 652 two-agent tasks on real repos: cooperating agents succeed about 30% less than one agent doing both features, and a chat channel does not significantly help |
| T20 | Geng and Neubig (CMU), "Effective Strategies for Asynchronous Software Engineering Agents" (CAID) | 2026 | [arXiv:2603.21489](https://arxiv.org/abs/2603.21489) | A manager plus engineers in isolated git worktrees with test-gated merges beats the same-model single agent (Claude Sonnet 4.5: 57.2 to 63.3 PaperBench, 53.1 to 59.1 Commit0-Lite) at about 2x to 4x the cost |
| T21 | Zhan et al. (Microsoft Research), "Agensh: Scaling Organizational Intelligence to 1,024 Agents" | 2026 | [arXiv:2609.26781](https://arxiv.org/abs/2609.26781) | Orchestrator-free workers on a shared git workspace: 1 to 128 agents lifts the test-pass rate 19.31% to 28.78% on the five hardest ProgramBench tasks at the same 6-hour wall-clock; no cost reported |
| T22 | Mediratta et al. (UT Austin, NVIDIA), "Decentralized Multi-Agent Coordination and Communication in Shared Codebases" (ParallACT) | 2026 | [arXiv:2611.00314](https://arxiv.org/abs/2611.00314) | Parallel agents fall from 62% to 16% (Claude Code, Opus 4.8) on contradictory tasks vs a single-agent oracle; one serial handoff recovers 54% at the same cost; a message channel recovers little |
| T23 | Tang et al. (Notre Dame, Vanderbilt, Google), "How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions" | 2026 | [arXiv:2605.29442](https://arxiv.org/abs/2605.29442) | In real Claude Code, Codex and Cursor sessions, 22.58% of misalignment episodes are inaccurate self-reporting (claiming done before it works); 91.49% of visible resolutions need the user to correct the agent |
| T24 | Zhong et al. (CMU, Fewshot), "Hardening Agent Benchmarks with Adversarial Hacker-Fixer Loops" | 2026 | [arXiv:2606.08960](https://arxiv.org/abs/2606.08960) | 323 of 1,968 tasks (16%) in five terminal-agent benchmarks are hackable by frontier models from the task text alone; a hacker/fixer/solver loop drives attack success on KernelBench 62% to 0% |
| T25 | Fu et al. (BUPT, Zhejiang, HKUST, Westlake, Duke Kunshan), "Do More Agents Help? Evaluating Accuracy and Cost in LLM Multi-Agent Workflows" | 2026 | [arXiv:2606.05670](https://arxiv.org/abs/2606.05670) | Six multi-agent workflows vs one controller (GPT-4.1, ten benchmarks, 3 runs): one wins (79.70 vs 76.65), five trail by 1.71 to 8.76 points; debate costs 1.39x tokens, ChatEval 4.34x |
| T26 | Adams et al. (Meta), "Automating Low-Risk Code Review at Meta: RADAR, Risk Calibration, and Review Efficiency" | 2026 | [arXiv:2605.30208](https://arxiv.org/abs/2605.30208) | Production funnel auto-approving low-risk agent-era diffs: 535K+ reviewed, 331K+ landed, revert rate 1/3 and incident rate 1/50 of non-RADAR diffs (observational; only the safest diffs qualify) |
| T27 | Ugare and Chandra (Meta), "Agentic Code Reasoning" | 2026 | [arXiv:2603.01896](https://arxiv.org/abs/2603.01896) | An agent that reads (not runs) code to judge patch equivalence: 78.2% standard vs 88.8% with a structured "semi-formal" protocol at 2.8x the steps; execution-free review still misses real test differences |
| T28 | Rajasekaran, "Harness design for long-running application development" (Anthropic Engineering) | 2026 | [anthropic.com](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Planner, generator and a separate evaluator that drives the live app: solo $9 / 20 min vs full harness $200 / 6 h on one task; a later run $124.70 / 3 h 50 min; roles shrink as models improve (note) |
| H27 (filed in 02) | Lopopolo, "Harness engineering: leveraging Codex in an agent-first world" (OpenAI) | 2026 | [openai.com](https://openai.com/index/harness-engineering/) | One internal product, about 1,500 merged PRs by three engineers driving Codex, agents often self-merge, humans "aren't required" to review; no comparison arm (note) |
| T30 | Lin, "Scaling long-running autonomous coding" (Cursor) | 2026 | [cursor.com](https://cursor.com/blog/scaling-agents) | Hundreds of agents on one repo: locks and an integrator role failed; planners + isolated workers + a judge per cycle worked; no controlled numbers (note) |
| T31 | Anthropic, "Orchestrate teams of Claude Code sessions" (Claude Code docs) | 2026 | [code.claude.com](https://code.claude.com/docs/en/agent-teams) | Agent teams are experimental, interactive-only (not spawned under `-p`), cost "significantly more tokens"; "for sequential tasks, same-file edits ... a single session or subagents are more effective" (note) |

## What it establishes

**Verdict:** the evidence does **not** show that role-based teams beat one strong agent once cost is
held equal. The published wins come from four sources that are not "roles": weak baselines, extra
compute, an independent check against ground truth, and a small number of agents with narrow
communication. For the kit this means a Main + builder + QA + tester team is justified only to the
extent that QA and the tester are *independent verifiers that run the thing*, with the builder
writing serially; every extra role must beat a budget-matched single-agent arm in the benchmark.
Round 2 (T18-T31) strengthens this: lab-run controlled studies find a role split no better than solo
on average (T18, T25), parallel writers lose to one agent unless work is isolated and merges are
test-gated (T19, T20, T22), and an LLM verifier alone approves about half of failing work (T18).

1. **The original team papers beat weak baselines, and each other's claims conflict.** T1's one-shot
   single-agent baseline (GPT-Engineer) scores Quality 0.1419 against ChatDev's 0.3953 (Table 1), but
   uses 7,182 tokens against ChatDev's 22,949 and 15.6 s against 148.2 s (Table 3): the team gets about
   2.8× the quality for about 3.2× the tokens, and no single agent was given the same budget. T2 reports
   the opposite ranking against ChatDev: executability "3.75" for MetaGPT vs 2.25 (Table 1) and "85.9%
   and 87.7%" Pass@1 on HumanEval and MBPP (Section 4.2). T3's HumanEval table shows CoT 83.5, Solo 87.2,
   Group 89.0 with GPT-4 (Table 2): most of the gain is a single agent with a better scaffold, and "for
   GPT-3.5-Turbo, the Group setup underperforms the Solo setup in two of three tasks" (Section 3.1).
2. **Where roles help, the mechanism is independent checking, not the persona.** T4 finds a single
   agent writing its own tests reaches "71.3% and 79.4% pass@1" against "79.9% and 89.9%" with a separate
   test agent (Section 4.7), and explains why: "the tests designed by the same agent that generates the
   code can be biased by the code and lose objectivity". T6's ablation removes only QA: resolved falls
   "13.94" to "10.63" (Table 2). T2's "executable feedback" adds "4.2% and 5.4% in Pass @1" (Section 4.4).
   T11 supplies the converse: without external feedback a model reviewing its own work "struggle[s] to
   self-correct ... and at times, their performance even degrades" (Abstract). T17 (vendor) reports
   review "works best when the coding and review agents do not share any context beforehand".
3. **Equal-budget comparisons erase most multi-agent gains.** T8: "SAS is the best-performing system or
   statistically indistinguishable from the best for all budgets except the lowest one (100 tokens)"
   (Section 5.1); at 2,000 thinking tokens the average accuracy is 0.421 for the single agent against
   0.403 for debate and 0.389 for the sequential team (Table 1). T8 also finds the reverse when context is heavily corrupted: "Sequential is clearly better at α = 0.7" (Section 5.3). T10: "none of these MAD methods achieve
   a win rate higher than 20% when compared to CoT across 36 scenarios" (Section 1). T11, Table 7: debate
   at six responses 83.2 vs self-consistency at six responses 85.3. T9 pools nine studies: multi-agent
   "average[s] -0.042 in accuracy" against matched baselines and "equals or falls below the baseline in
   74% of these comparable contrasts" (Abstract); "positive returns require partitioned evidence,
   external verification, or error diversity across models" (Abstract). T10 agrees on the last point:
   model heterogeneity "improves SoM-average ... by 6.4%" (Section 4). Cross-reference H11 (theme 02):
   on SWE-bench Verified "all MAS architectures show slight degradation relative to SAS (mean 0.522)":
   hybrid -2.1%, centralized -3.1%, decentralized -5.4%, independent -14.9% (appendix results).
4. **Coding is where the gains are smallest, and the review loop is the exception.** T14 (ICML 2026 Workshop on DL4C)
   is the one head-to-head with Claude Code: on LiveCodeBench Zero-shot 77%, Single-reviewer 77%,
   Two-reviewers 75%, MARS (5 agents) 82%, AR (3 agents) 87% (Table 1), and on SWE-bench Verified
   75.2% vs 71.6% zero-shot vs 72.6% for MARS (Table 3, N=500), but "AR uses about 4.5× the tokens of
   Zero-shot". Note the single same-model reviewer added nothing; the gain needed a critic that audits
   the review, and naive pairs show "false consensus" (Section 7). T13 shows the field reality: "CRA-only
   PRs achieve a 45.20% merge rate, 23.17 percentage points lower than human-only PRs (68.37%)"
   and "60.2% of closed CRA-only PRs fall into the 0-30% signal range" (Abstract).
5. **Process shape matters: a design handoff can hurt, a test handoff can help.** T12 holds toolset and
   models fixed (Gemini-2.5) and varies only the workflow: developer-then-tester reaches 49.48%
   of requirements implemented, single agent 45.72%, designer-developer-tester 27.71% (Section 4,
   Table 3), with per-project cost in a similar band (about $4.85 to $7.05 in Table 3). The authors'
   cause: "Once the Dev Agent receives what it perceives as an authoritative implementation plan, it
   tends to prioritize this plan over direct engagement with the original requirement". Its failure
   analysis: "the primary reason for failure is not incorrect code implementation, but rather the
   omission of requirements and inadequate self-verification" (Section 1). T5's agile sprints beat
   MetaGPT by "7.71% and 6.19%" pass@1 (Section 1) but "requires more tokens and running time".
6. **Teams fail in characteristic ways, and fixes are mostly structural.** T7: "41% to 86.7% failure
   rate on 7 state-of-the-art open-source MAS" (Section 1); failures split into system design 41.8%,
   inter-agent misalignment 36.9% and task verification 21.3% (Figure 4). "Improving agent role
   specifications alone yields a +9.4% success rate increase for ChatDev" and "adding a high-level task
   objective verification step to ChatDev yields a +15.6% improvement" (Sections 4, FC1 and FC3). T7 notes
   agents skip verification "despite being prompted to perform thorough verification". T15 gives the
   parallel-builder failure: patches that pass alone fail merged "in 97% of runs" on constructed
   tasks, and "a message describing the completed concurrent change recovered 82% of runs" (Abstract).
7. **What a working team looks like in practice.** T16 (vendor): 16 parallel agents coordinate by
   writing "a text file to current_tasks/" under git; "it's important that the task verifier is nearly
   perfect, otherwise Claude will solve the wrong problem". T17: "multiple agents contribute intelligence
   to a task while writes stay single-threaded"; parallel writers make conflicting implicit choices (the page: "Actions carry implicit decisions", about "style, code patterns, how certain edge cases should be handled").
   Cross-reference H14 (theme 02): +90.2% for an orchestrator on research at about 15× the tokens of a
   chat, and "most coding tasks involve fewer truly parallelizable tasks than research".
8. **Round 2: lab-run controlled studies agree that a role split rarely beats solo on average, and
   that an LLM verifier is the weak link.** T18 (MIT, Google Research, Google DeepMind) enforces roles
   with OS permissions across 851 task templates: "Full Team is not significantly better than Solo on
   average ... +0.5 points (p = 0.20 ...) and the team wins on 68 of 155 tasks" (Section 3.3); teams
   help by 15.7 points in the lowest solo-score quintile and "trail Solo by 6.8-10.1 points" in the top
   three (Section 3.4). The verifier "approves 49.4% of submissions that the grader rejects (... n =
   1,083)", and removing it "raises mean partial score by 5.5 points" (Section 3.3); only 0.24 of the
   planner's spec-critical tokens reach the executor's channel (0.79 in the planner's own). T25
   (single GPT-4.1 controller vs six workflows, ten benchmarks, three runs) finds five of six
   workflows "trail by 1.71-8.76 percentage points" and LLM-Debate "loses 1.96 points in pooled accuracy
   while consuming 1.39 times the tokens" (Abstract). T27 gives the other side of verification:
   an agent that may only read code judges patch equivalence at 78.2% (standard) and 88.8%
   (structured protocol) but needs 28.17 steps against 10.08, and its misses are "missed execution
   differences" (Section 4.1, Table 2). So a read-only reviewer is useful, but the tester must run
   things.
9. **Parallel builders fail even when each agent is competent; serial handoff is the cheap fix.**
   T19 (Stanford, SAP) reports "GPT-5 and Claude Sonnet 4.5 based agents achieve only 25% with
   two-agent cooperation ... around 50% lower than a 'Solo' baseline" (Section 1) and that the chat
   channel's effect on success "is not statistically significant" (Section 5). T22 (UT Austin,
   NVIDIA) uses Claude Code with Opus 4.8: joint pass falls "from 62% to 16% on contradictory
   instances (p < 0.001)" against a single-agent oracle; with one hand-off "joint success rises
   significantly from 16% to 54%" at 1.18× the oracle's tokens, while a second round (ABAB) adds cost (1.88×) and
   no gain (Section 4.1, Table 1). T20 (CMU) shows what makes parallelism pay: isolated git
   worktrees and test-gated merges lift Claude Sonnet 4.5 from 57.2 to 63.3 (PaperBench) and 53.1 to
   59.1 (Commit0-Lite), but worktree-less "soft isolation" on PaperBench scores 55.5, below the 57.2
   single agent (Table 3). T21 (Microsoft Research) scales that to 1 to 128 agents on a shared git
   workspace: mean test-pass "from 19.31% to 28.78%" on the five hardest ProgramBench tasks (Section 3.1).
10. **Real-use evidence: the reviewer and tester roles exist because agents over-claim.** In 20,574
   real coding-agent sessions (T23), "Inaccurate Self-Reporting" is 22.58% of misalignment episodes
   (Section 4.1) and "91.49% of visible resolutions still require explicit user correction"
   (Abstract). Meta's production funnel (T26) auto-approves only low-risk diffs and reports a revert
   rate of 1/3 and a production-incident rate of 1/50 of non-RADAR diffs (Abstract). T24 shows the
   check itself is attackable: "323 (16%)" of 1,968 benchmark tasks are hackable by frontier models
   given only the task description, and an adversarial hacker/fixer/solver loop takes KernelBench
   attack success "from 62% to 0%" (Abstract). Vendor posts agree on shape, not on numbers:
   T28 (Anthropic) credits "separating the agent doing the work from the agent judging it" and
   shrinks the harness as models improve ("the boundary moved outward"); H27 (OpenAI) runs most
   review agent-to-agent with "minimal blocking merge gates"; T30 (Cursor) found that locks and an
   integrator role failed and that planners, isolated workers and a per-cycle judge worked; T31
   (Anthropic docs) says agent teams are experimental, cost "significantly more tokens", and are not
   spawned under `claude -p`.

**Design implications for the kit:** (a) keep one builder writing at a time, and when work must be
parallel, isolate it in separate git worktrees with merges gated by tests (T20, T22) or hand off
serially (T22); (b) make QA a fresh-context reviewer fed the diff and spec, not the builder's history;
(c) make the tester judge by running the app and tests (external ground truth), never by reading code
or by an LLM verdict alone (T18's 49.4% false-accept rate, T27's missed execution differences), and
harden the grader against being gamed (T24); (d) hand over the written spec, not a design document the
builder will treat as authoritative (T12), and do not expect a planner's detail to survive the
handoff (T18's 0.24 recall); (e) add the role only where solo is weak (T18's quintiles), and drop it
as the model improves (T28); (f) run the benchmark with a budget-matched single-agent arm and report
$/task for both; (g) distrust the builder's "done": the tester's run is the verdict (T23).

## The catch

- **Equal-cost coding evidence is thin and points both ways.** T9's pooled software contrasts are all negative for multi-agent (Table 6), but only two are budget-matched: SWE-bench Verified −0.017 and Terminal-Bench −0.067 under matched iterations, on 20 instances per cell; SWE-bench Lite −0.064 comes from a study where multi-agent cost a median 8.1× more, and HumanEval −0.048 and MBPP −0.082 from tables that "do not report matched tokens or cost". T12 is the one controlled software comparison at near-equal cost, and there the developer-then-tester pair beat the single agent (49.48% vs 45.72% at $6.64 vs $6.58 mean, Table 3), though with Gemini-2.5-Flash the single agent won (48.46% vs 45.47%), while the designer handoff lost. Other coding comparisons use a weak one-shot baseline (T1, T6's raw GPT-4 at 1.74%), benchmarks the authors flag as simple (T5), or pay more tokens for the win (T14's 4.5×, T5, T1). The kit's own benchmark has to
  supply the equal-cost software comparison.
- **Models are old or small in most team papers.** T1, T2, T3, T4, T5 and T6 use GPT-3.5/GPT-4 of 2023-24;
  H11 and T14 show that as single-agent baselines get stronger (above about 45% on SWE-bench Verified)
  the room for coordination shrinks. Results for Claude Opus-class agents with subagents are only in T14
  (one benchmark, a skill-form protocol) and the vendor notes.
- **Single runs and small samples.** T12 uses one benchmark with Gemini models only and three runs for
  a variance check, so its 3.8-point gap between developer-then-tester and single agent may not be
  robust; T14 reports one run per method; T15's 97% is on 12 constructed Django helpers and its
  mined-PR rate is near zero ("do not estimate how often these problems occur in practice").
- **Observational and vendor evidence.** T13 compares bot-only and human-only PRs that differ in
  many ways (no matching), so the 23-point merge gap is an association. T16 and T17 are
  vendor-authored with no single-agent control; T17's "58% severe" bug rate has no stated denominator.
- **Contested and self-reported leaderboards.** T1 and T2 each report beating the other on their own
  benchmarks, T5 reports beating both on a new benchmark it built (ProjectDev); none was independently
  re-run in this folder. T7's failure rates are on frameworks as of early 2025 and measure
  correctness differently across benchmarks (its Figure 5 notes they are "not directly comparable").
- **Preprint quality varies.** T9 is a single-author preprint of a meta-analysis built on nine studies
  with mixed designs; T8 and T12 are preprints; T15 is a workshop paper. Treat the direction as
  consistent across T8-T11 rather than any one effect size as settled.
- **Round 2 (T18-T31): newer models, but still not our setup and not equal cost.**
  - *Few comparisons are budget-matched.* T20's gains come at about 2x to 4x the single agent's cost
    (Claude Sonnet 4.5 on PaperBench $3.3 to $6.5, Commit0-Lite $1.9 to $8.1, Table 2), and a single agent
    given double the iterations improves little (Figure 2); the equal-cost question is open. T21 equalises
    wall-clock (6 h) only and reports no cost; T25 equalises step limits, not tokens. T22 and T19 compare
    against a single-agent "oracle" or Solo that is given the whole task, which is the right bar for the
    kit but is not a team of roles.
  - *Small or constructed task sets.* T21 uses five ProgramBench tasks and one model family; T22 has 85
    (Claude) and 155 (open-weight) constructed instances; T19 uses two agents only; T18's team-vs-solo
    result is a 155-task ablation with one model (Gemini-3 Flash) and its 49.4% false-accept rate "is a
    property of our sampled role-mixing distribution, not of any single model" (Section 3.7 discussion).
  - *Coordination benchmarks are not app building.* T18, T19 and T22 build tasks where agents must
    coordinate on shared code; T20 and T21 use PaperBench, Commit0 and ProgramBench; T25 is mostly
    reasoning and QA benchmarks (coding is HumanEval and MBPP). None runs a builder + QA + tester pipeline
    on a user-facing app walked by an agent; the kit's own benchmark has to.
  - *Observational and vendor evidence.* T23 detects misalignment only when the developer pushes back
    (latent failures are excluded) and uses GPT-5.4 to annotate. T26's revert and incident rates compare
    RADAR-reviewed diffs, which are pre-filtered to the safest ones, against all other diffs: it shows
    the funnel is safe, not that reviewer agents reduce defects. T28 to T31 are vendor-authored posts or
    docs with no matched single-agent arm, and Cursor's and OpenAI's results (H27, T30) are not graded
    by an outside party.
  - *Preprints.* Every new arXiv paper here is a 2026 preprint without a listed venue; T20, T22 and T24
    were revised or posted after the models they test were released, and none has been independently
    replicated in this folder.
