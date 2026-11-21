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

## What it establishes

**Verdict:** the evidence does **not** show that role-based teams beat one strong agent once cost is
held equal. The published wins come from four sources that are not "roles": weak baselines, extra
compute, an independent check against ground truth, and a small number of agents with narrow
communication. For the kit this means a Main + builder + QA + tester team is justified only to the
extent that QA and the tester are *independent verifiers that run the thing*, with the builder
writing serially; every extra role must beat a budget-matched single-agent arm in the benchmark.

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

**Design implications for the kit:** (a) keep one builder writing at a time; (b) make QA a fresh-context
reviewer fed the diff and spec, not the builder's history; (c) make the tester judge by running the app
and tests (external ground truth), never by reading code; (d) hand over the written spec, not a design
document the builder will treat as authoritative; (e) run the benchmark with a budget-matched single-agent
arm and report $/task for both.

## The catch

- **Equal-cost coding evidence is thin and points both ways.** T9's pooled software contrasts are all negative for multi-agent (SWE-bench Verified −0.017, Terminal-Bench −0.067, SWE-bench Lite −0.064, HumanEval −0.048, MBPP −0.082; Table 6, often 20 instances per cell). T12 is the one controlled software comparison at near-equal cost, and there the developer-then-tester pair beat the single agent (49.48% vs 45.72% at $6.64 vs $6.58 mean, Table 3), while the designer handoff lost. Other coding comparisons use a weak one-shot baseline (T1, T6's raw GPT-4 at 1.74%), benchmarks the authors flag as simple (T5), or pay more tokens for the win (T14's 4.5×, T5, T1). The kit's own benchmark has to
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
