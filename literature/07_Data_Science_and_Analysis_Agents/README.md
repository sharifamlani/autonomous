# 07 Data Science and Analysis Agents

## Role

This folder collects the evidence on agents that analyse data and are scored against known answers: the
benchmark family (InfiAgent-DABench, DA-Code, DSBench, DSEval, DiscoveryBench, BLADE,
ScienceAgentBench, MLE-bench, DABstep, KramaBench, DAB, QRData), error analyses of what goes wrong
(wrong method, silent data bugs, shortcuts), and audits of the benchmarks' own answer keys. Its central
question is **how accurate are data-analysis agents against known answers?** It informs the research
factory's known-answer study in v0.1 (which dataset, which grader, how many runs), what the kit's
analysis agent must verify before it reports a number, and which of our own gates catch silent errors.

## Contents

| ID | Citation | Year | Link | What it establishes |
|---|---|---|---|---|
| D1 | Hu et al., "InfiAgent-DABench: Evaluating Agents on Data Analysis Tasks" | 2024 | [arXiv:2401.05507](https://arxiv.org/abs/2401.05507) | 257 closed-form questions over 52 CSVs graded by exact match; GPT-4 reaches 78.99% (the easy end); labels were produced by an agent agreeing with itself three times, then human-filtered |
| D2 | Huang et al., "DA-Code: Agent Data Science Code Generation Benchmark for Large Language Models" (EMNLP 2024) | 2024 | [arXiv:2410.07331](https://arxiv.org/abs/2410.07331) | 500 wrangling, ML and EDA tasks with per-task scorers; GPT-4 agent scores 30.5%; error analysis names hallucinated file names, debug loops and misread task context |
| D3 | Jing et al., "DSBench: How Far Are Data Science Agents from Becoming Data Science Experts?" (ICLR 2025) | 2024 | [arXiv:2409.07703](https://arxiv.org/abs/2409.07703) | 466 analysis + 74 modelling tasks; best agent solves 34.12% of analysis tasks; humans score 64.06% on a 10-competition sample |
| D4 | Chan et al., "MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering" (ICLR 2025) | 2024 | [arXiv:2410.07095](https://arxiv.org/abs/2410.07095) | 75 Kaggle competitions graded against human leaderboards; o1-preview + AIDE medals in 16.9%; pass@6 roughly doubles pass@1; contamination and rule-break checks built in |
| D5 | Zhang et al., "Benchmarking Data Science Agents" (DSEval) | 2024 | [arXiv:2402.17168](https://arxiv.org/abs/2402.17168) | Four agents, one query, one correct answer; validators for intactness (did the agent alter the input data?); LLM-bootstrapped annotation with human revision |
| D6 | Majumder et al., "DiscoveryBench: Towards Data-Driven Discovery with Large Language Models" | 2024 | [arXiv:2407.01725](https://arxiv.org/abs/2407.01725) | 264 real tasks derived from published papers; best system scores 25%; a no-data baseline measures memorised findings; biology 0%, engineering 7% |
| D7 | Gu et al., "BLADE: Benchmarking Language Model Agents for Data-Driven Science" (EMNLP 2024) | 2024 | [arXiv:2408.09667](https://arxiv.org/abs/2408.09667) | Ground truth from independent expert analyses, because open questions have several valid analyses; experts agree with each other 75-80% but with LM-generated decisions only 13-27% |
| D8 | Chen et al., "ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery" (ICLR 2025) | 2024 | [arXiv:2410.05080](https://arxiv.org/abs/2410.05080) | 102 tasks from 44 papers; best agent 32.4% (34.3% with expert hints); agents caught reading test labels instead of training a model |
| D9 | Egg et al., "DABstep: Data Agent Benchmark for Multi-step Reasoning" | 2025 | [arXiv:2506.23719](https://arxiv.org/abs/2506.23719) | 450 factoid tasks from Adyen payments data, public dev set with answers plus hidden test set; best 14.55% on hard tasks vs 76.39% on easy |
| D10 | Lai et al., "KramaBench: A Benchmark for AI Systems on Data-to-Insight Pipelines over Data Lakes" (ICLR 2026) | 2025 | [arXiv:2506.06541](https://arxiv.org/abs/2506.06541) | 104 end-to-end pipelines with reference sub-tasks; best 55% (62% with perfect retrieval); nine human experts also fail, mostly on pipeline design (46%) |
| D11 | Ma et al., "Can AI Agents Answer Your Data Questions? A Benchmark for Data Agents" | 2026 | [arXiv:2603.20576](https://arxiv.org/abs/2603.20576) | Multi-database queries; best of three frontier agents 57% pass@1 (Claude Code + Sonnet 4.6: 48%); 90% of wrong answers are a wrong plan or a wrong implementation, not wrong data |
| D12 | Yan et al., "Fail Loudly: An Auditable Runtime for Agentic Data Analysis" | 2026 | [arXiv:2609.32528](https://arxiv.org/abs/2609.32528) | 69.8% of an agent's zero-scored runs returned normal-looking wrong results; a runtime that checks each operation against what the agent saw lifts KramaBench by 28.8-35.9% relative |
| D13 | Zanoli et al., "ELT-Bench-Verified: Benchmark Quality Issues Underestimate AI Agent Capabilities" | 2026 | [arXiv:2603.29399](https://arxiv.org/abs/2603.29399) | A data-engineering benchmark's answer key audited: 82.7% of failed tasks hold a benchmark-attributable error; fixing it moves 22.66% to 32.51% with the same agent |
| D14 | Liu et al., "Are LLMs Capable of Data-based Statistical and Causal Reasoning? Benchmarking Advanced Quantitative Reasoning with Data" (QRData, Findings of ACL 2024) | 2024 | [arXiv:2402.17644](https://arxiv.org/abs/2402.17644) | 411 statistics and causal questions with unique gold answers from textbook data; GPT-4 58%; of GPT-4's wrong answers 44% chose a wrong method or knowledge |
| D15 | Tu et al., "Who Guards the Benchmarks? Automated Auditing of LLM Agent Benchmarks" (BenchGuard, COLM 2026) | 2026 | [arXiv:2604.24955](https://arxiv.org/abs/2604.24955) | An LLM auditor found 12 author-confirmed defects in ScienceAgentBench, including tasks that are unsolvable and metrics that silently corrupt scores |

PDFs: D1-D15 (15 of 15). Quotes below come from the PDF text, extracted locally, except where a line says
a quote is from a GitHub README (those were fetched with `gh api` on 2026-11-21 and are labelled).

## What it establishes

**Verdict:** accuracy against known answers is **moderate on easy, closed-form questions and low on
anything multi-step**, and the published numbers are unstable in both directions. They rise fast when a
harness is tuned to the benchmark (a public leaderboard row reaches 99%, against 57% for the best agent in its own paper), and they are
partly capped or distorted by wrong answer keys (one audit puts a third of mismatches on the benchmark,
not the agent). The dominant failure is not a crash: it is a plausible, wrong number from a wrong
plan or a wrong implementation. For the kit this means "the analysis ran" is never evidence, a
known-answer study must audit its own labels first, and the analysis agent needs checks that look at the
data, not only at the code's exit status.

1. **Headline accuracy depends on how hard the question is, not on "data analysis" as such.** Closed-form
   questions on one CSV: D1 reports "GPT-4 outperforms others with an accuracy of 78.99%" (Section 3.3).
   Real analyses with several files and steps: D2 "The most advanced model, GPT-4, achieves only a 30.5%
   score" (Section 5.2); D3 "the best agent solving only 34.12% of data analysis tasks" (Abstract); D6
   "even the best system scores only 25%" (Abstract); D8 "the best-performing agent can only solve 32.4% of
   the tasks independently and 34.3% with expert-provided knowledge" (Abstract); D14 "GPT-4 achieves an
   accuracy of 58%" (Abstract). The same benchmark split by difficulty shows it directly: D9 finds
   o4-mini at 76.39% on easy tasks but "only 14.55% accuracy on the Hard tasks" (Section 4.2). Most of these
   use 2024 models; the newer papers are higher but not high: D10 "the best system reaches only 55%
   end-to-end accuracy in the full data-lake setting" and "Even with perfect retrieval, the accuracy tops
   out at 62%" (Abstract); D11 "the best agent (GPT5.5) reaches only 57% pass@1, no agent exceeds 70%
   pass@5" (Section 4), with Claude-Sonnet-4.6 under Claude Code at 48% and "the least accurate despite
   being the most expensive" (Section 4.2). D11 spent "$4,346" on three agents in three variants (Section 1).
2. **Wrong method and wrong implementation, not wrong data, are what go wrong.** D11 classifies wrong
   answers: "FM4 (incorrect implementation) is the most common at 57%, followed by FM2 (incorrect plan) at
   31%, FM3 (incorrect data selection) at 11%" so "FM2 and FM4 account for 90% of incorrect answers"
   (Section 4.4). Its examples are the silent kind: "a regex for MALE matches inside FEMALE and mislabels
   gender" (Section 4.4). D14 sampled 50 of GPT-4's wrong answers: 44% were knowledge-recall errors "like
   choosing a wrong hypothesis test, or using statistical methods to address a causal question", 34% data
   analysis, 16% equation formulation, 6% calculation (Appendix A.6, Table 7). D2's error analysis adds
   "Agents often make incorrect assumptions about the environment, such as presuming file names" and
   "Misinterpretation of Task Context ... leading to premature termination" (Section 5.4). D9 observes
   that agents are "considerably more prone to fail when they face a task in which they need to follow
   rules implicitly mentioned in the context" and often give "conversational text instead of outputting a
   number or apply incorrect rounding" (Section 4.3).
3. **Silent errors are the common case.** D12 audited zero-scored runs of DS-STAR (an agent that already
   verifies iteratively): "Among 580 zero-scored DS-STAR runs across KramaBench, DA-Code, and DABStep, 405
   (69.8%) delivered normal-looking but incorrect results without reporting failure" (Section 1). Its
   examples: two Top-5 rankings merged "without a pairing condition" into a well-formed 25-row table, and a
   successful inner join that "silently loses one year" (Figure 1B, 1C). D5 names a related silent bug:
   an agent that "unintentionally modifies the data ... violating intactness" (Figure 2); its validators
   check this explicitly. D8 saw agents cheat on the answer: "when asked to develop a machine learning
   model, they may directly read and report the ground-truth labels in the test set without writing the
   training code. Such perfect results are actually cheating" (Section 2.2).
4. **What helps is feedback from the data, not more reasoning prompts.** D12's runtime rejects an operation
   whose declared inputs conflict with what the agent observed; it reaches "overall scores of 0.723 with
   full source retrieval and 0.747 with gold sources supplied, corresponding to relative gains of 35.9% and
   28.8% over the strongest baselines" (Abstract), and "RADAR costs $1.16 ... versus $6.38" for the
   strongest baseline on KramaBench Full Input (Section 4.5; the text does not say whether that is per
   task or per suite). D8 finds "Execution feedback is necessary for LLMs to generate useful programs"
   (Section 4.1). D10: "Agentic control flows drive the largest performance gains": an agent loop with
   Claude-3.7 reached 55.83% against 24.98% for the best fixed pipeline (Section 4). By contrast D6 reports
   that "effective reasoning prompts such as React and planning with a self-critic ... do not help improve
   the simple CodeGen agent", while a run given an oracle score "significantly improves" (Section 5.2): the
   gain needs a real external signal, which a known-answer check can supply but a self-critic cannot.
   D11 also finds that giving schema descriptions and hints moved pass@1 by at most 5 points, and a hint
   that did not apply to a query could mislead the agent into changing a correct answer (Section 4.3).
5. **Open-ended analysis has no single right answer, and experts disagree too.** D7 builds ground truth
   from "independent analyses by expert data scientists" because tasks have "multiple valid approaches"
   (Abstract); experts agreed with each other on 75% (transformations) and 80% (conceptual variables), but
   "agreement on LM-generated decisions was much lower, at 27% ... and 13%" (Section 3). LMs reach
   "precision below 35%" in forming statistical models with the right variables and "coverage@10 below 13%"
   (Section 7). D10's nine human experts failed mostly on "Incorrect pipeline design (46%)" and "Lack of
   domain knowledge (24%)" (Appendix F), and D3's humans score 64.06% task-level accuracy on a 10-competition
   sample against 33.65% for the best agent (Table 8). A known-answer study should therefore use
   closed-form questions and report a human reference where it can.
6. **The answer key is part of the experiment, and it is often wrong.** D13 audited ELT-Bench: "82.7% of
   these 81 tasks contain at least one benchmark-attributable error", at column level "33.0% of all
   mismatches are benchmark-attributable rather than genuine agent failures", and fixing the key "rais[es]
   SRDT from 22.66% to 32.51% with the same agent and model" (Section 1; ELT-Bench is data engineering,
   not analysis; its re-run uses Claude Sonnet 4.5 inside SWE-Agent). D15 found 12
   author-confirmed defects in ScienceAgentBench (D8) despite "multiple rounds of manual validation",
   "including fatal errors rendering tasks unsolvable" and "metric mismatches that silently corrupt
   scores" (Abstract, Section 5.1). D1's labels come from OpenAI's ADA agent: "Only the answer is kept when
   ADA consistently generates the same answer in all trials" (Section 2.1), then human filtering keeps
   "85% samples" (Section 2.3.1), so the ceiling is an agent's consensus, not independent truth. D9
   validated its scorer against two annotators (97.3% agreement, Appendix A.2); D3 had people check its
   semantic-match function on 100 answers (Appendix F, reported 100% agreement).
7. **Contamination and gaming are measured only partly.** D4 found "no evidence of GPT-4o being
   over-reliant" on recognising competitions and no plagiarism or rule-breaking in medal runs, but "does
   not rule out subtler effects" (Section 4.2) and "make[s] no guarantees about future models" (Section
   6). D8 removes five test points per dataset and re-splits model-development data to defend against memorised data loaders (Section 2.2). D9 keeps
   a hidden test set so ground truths cannot leak into training data (Section 3.3); D1 keeps its test
   set closed (Section 2.4). The live DAB leaderboard (repo README, fetched 2026-11-21 with `gh api`, not
   a paper) shows the scale of the problem: its best row with a "tuned prompt" is 0.9917, and 0.8858 is the
   best row without one, against 57% in D11; its footnotes record trials "counted as non-passes" because
   agents "loaded external gold labels", rows whose notes "tell the agent how to solve that query", and a
   validator re-scored after the key listed one of 95 tied answers. D12 also adds an older model "motivated
   by concerns about benchmark contamination" (Section 4.5).
8. **Datasets we could use as a v0.1 known-answer task.** Read the licence before copying (CLAUDE.md §4);
   sizes are from the papers, licences from the repos' LICENSE files or README badges as fetched.

   | Candidate | Size and answer type | Licence | Fit for v0.1 |
   |---|---|---|---|
   | D1 DAEval | 257 questions, 52 CSVs, exact-match `@name[answer]` labels (public validation set; test closed) | repo Apache-2.0; README badge: data CC BY-NC 4.0 | Best fit: closed form, regex grader, small. Audit labels first (see 6) |
   | D14 QRData | 411 stats and causal questions, textbook and paper data, gold answers, 3% numeric tolerance | CC BY-NC 4.0 | Good for "right method" checks; non-commercial |
   | D9 DABstep | public dev set with answers plus hidden test; 450 tasks in all, factoid answers | dataset CC BY 4.0 (per the paper) | Good for multi-step; use dev set only |
   | D6 DiscoveryBench | 264 real tasks from papers (test split 239 queries), scored by a GPT-4 evaluator | ODC-By | Open-ended scorer adds judge bias |
   | D7 BLADE | 12 datasets, expert decisions as truth | code Apache-2.0, data ODC-By (README badges) | Tests method choice; scorer is an LM matcher |
   | D10 KramaBench, D11 DAB | 104 pipelines / DAB queries; reference sub-tasks | repos show no licence | Do not copy; read-only |
   | D4 MLE-bench | 75 Kaggle competitions, medals | MIT code; Kaggle data under competition rules | Too heavy: Lite split is 158 GB |

**Design implications for the kit:** (a) the analysis agent reports a number only with the code, the
rows and columns it used, and a check against the data (row counts after each join, no mutation of the
raw file); (b) the research factory's known-answer study uses a small closed-form set (D1 or D14 first),
pre-registers the grader, and has an auditor pass over the labels before any agent runs (D13, D15);
(c) run at least 3 times per arm and report the spread, since D4's pass@6 roughly doubles pass@1; (d) log
cost per task (D11, D8 report it, most do not); (e) keep a held-out slice and never put its labels in
the agent's reach (D8, D9, D11 leaderboard).

## The catch

- **Most scores are from older models and bare scaffolds.** D1, D2, D3, D6, D7, D8 and D14 evaluate
  GPT-4-era or earlier models; D5 uses GPT-3.5 with each agent. Only D11, D12 and D13 use Claude 4.x-class
  or current models, and D11's numbers are already far below the live DAB leaderboard (the README now
  lists 12 datasets and 54 queries, so the figures are not directly comparable). Nothing here measures
  Claude Code with subagents and skills on analysis tasks, except the single Claude Code row in D11.
- **Benchmarks are not studies.** Every benchmark scores a final answer against a key. None measures
  whether a whole analysis (data cleaning choices, model choice, honest reporting) would survive peer
  review; D7 and D6 get closest, and both score with an LM-based matcher whose own error is a source of
  noise (D6 uses a GPT-4 evaluator; D7 reports validating its modules on 615 outputs).
- **The keys are noisy, so accuracy numbers have an unknown floor.** D13 attributes a third of column
  mismatches to the benchmark and D15 finds author-confirmed defects in a second one; I did not find an audit of DA-Code, DSBench,
  DABench or DABstep, so their keys are unchecked, not clean. D1's labels come from an agent's consensus.
- **Silent-error rates are from one auditor on one agent.** D12's 69.8% is one preprint by independent
  researchers, on DS-STAR runs with a DeepSeek-V4-Flash backbone; the main text I read does not say how
  each of the 580 runs was labelled, and the system proposed in D12 is evaluated by its authors only.
  D11's failure shares come from an LLM judge (GPT-5) that agreed exactly with one author on 67% of 30
  trajectories (Section 4.4), though the ranking of failure types held.
- **Human baselines are thin.** D3's human score is 10 sampled competitions, D14's is 50 questions and
  three students, and D10's is nine participants; none is a large expert sample.
- **Vendor and leaderboard evidence.** D4 is OpenAI's own benchmark; the DAB leaderboard figures come
  from a README and rely on self-submitted runs, some with per-query tuning, so they show saturation by
  tuning, not general ability.
- **Preprint quality varies.** D5, D6, D9, D11, D12, D13 and D15 are preprints; D12, D13 and D15 are 2026
  and unreplicated. D1's arXiv page carries "work in progress"; D13's scope is data engineering, not
  analysis.
