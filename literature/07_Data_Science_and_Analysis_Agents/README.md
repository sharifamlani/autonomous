# 07 Data Science and Analysis Agents

## Role

This folder collects the evidence on agents that analyse data and are scored against known answers: the
benchmark family (InfiAgent-DABench, DA-Code, DSBench, DSEval, DiscoveryBench, BLADE,
ScienceAgentBench, MLE-bench, DABstep, KramaBench, DAB, QRData, and from round 2 RADAR, BixBench,
CausalReasoningBenchmark, P-Bench, LongDS, DSAEval), the agents the big labs built on them (DS-STAR; ERA and AIRA-dojo are
catalogued in folder 06), error analyses of what goes wrong (wrong method, silent data bugs, leakage, shortcuts),
reproduction studies, and audits of the benchmarks' own answer keys. Its central
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
| D16 | Nam et al., "DS-STAR: Data Science Agent for Solving Diverse Tasks across Heterogeneous Formats and Open-Ended Queries" (Google Cloud and KAIST) | 2025 | [arXiv:2509.21825](https://arxiv.org/abs/2509.21825) | Plan, code, then an LLM verifier that judges whether the plan is sufficient (not only whether the code ran); DABStep hard tasks 12.70% to 45.24% with Gemini-2.5-Pro; the same agent is the one D12 found silently wrong in 69.8% of its zero-scored runs |
| D17 | Gu et al., "RADAR: Benchmarking Language Models on Imperfect Tabular Data" (Google Research, U. Washington; NeurIPS 2025 Datasets and Benchmarks) | 2025 | [arXiv:2506.08249](https://arxiv.org/abs/2506.08249) | 2,980 table-query pairs with injected missing values, outliers and logical inconsistencies; o4-mini scores 100% on clean tables with code, then drops 59% on perturbed ones |
| D18 | Xing et al., "MMTU: A Massive Multi-Task Table Understanding and Reasoning Benchmark" (Microsoft, U. Michigan; NeurIPS 2025) | 2025 | [arXiv:2506.05587](https://arxiv.org/abs/2506.05587) | 28,000+ questions over 25 expert table tasks; GPT-5 reaches 69.6%, DeepSeek-R1 57.9%; a floor measurement for the table skills an analysis agent needs |
| D19 | Mitchener et al., "BixBench: a Comprehensive Benchmark for LLM-based Agents in Computational Biology" (FutureHouse) | 2025 | [arXiv:2503.00096](https://arxiv.org/abs/2503.00096) | Jupyter-notebook analysis capsules; 21% open-answer accuracy and "marginally better than random" in multiple choice, so the answer format changes the verdict |
| D20 | Sawarni et al., "CausalReasoningBenchmark: A Real-World Benchmark for Disentangled Evaluation of Causal Identification and Estimation" (Stanford) | 2026 | [arXiv:2602.20571](https://arxiv.org/abs/2602.20571) | 174 causal queries from 73 papers and 3 textbooks scoring design and estimate separately; strategy right in 81% of cases, full specification right in 38%; MIT metadata and code |
| D21 | Miao et al., "Fisher-R1: Training LLM Agents for Reliable Hypothesis Testing" (P-Bench; Stanford, UW-Madison) | 2026 | [arXiv:2608.07437](https://arxiv.org/abs/2608.07437) | 425 hypothesis-testing tasks with expert-audited answer keys in economics, biology and medicine; GPT-5.4 gets the reject decision right 58.3% but a close p-value only 30.5% on the hard split |
| D22 | Kohler et al., "Read the Paper, Write the Code: Agentic Reproduction of Social-Science Results" (ETH Zurich) | 2026 | [arXiv:2604.21965](https://arxiv.org/abs/2604.21965) | Agents re-implement 48 papers from the methods text and data only; coefficient signs match 75% to 91% of the time; root-cause labels were only 67% right on audit |
| D23 | Li et al., "The Silent Failures in Agentic Data Science" (CWI Amsterdam) | 2026 | [arXiv:2610.14115](https://arxiv.org/abs/2610.14115) | 220 tasks, six controlled tests: every framework-model pair has a failure mode in 43% or more of pipelines, and data leakage goes with better ranks |
| D24 | Xu et al., "LongDS-Bench: On the Failure of Long-Horizon Agentic Data Analysis" (Zhejiang U., Ant Group) | 2026 | [arXiv:2605.30434](https://arxiv.org/abs/2605.30434) | 68 multi-turn notebook-style tasks (2,225 turns); best model 48.45%, a drop of nearly 47 points from early to late turns, cascade and state errors dominate |
| D25 | Sun et al., "DSAEval: Evaluating Data Science Agents on a Wide Range of Real-World Data Science Problems" (Hong Kong Polytechnic U.) | 2026 | [arXiv:2601.13591](https://arxiv.org/abs/2601.13591) | 641 open-ended problems in a Jupyter-kernel sandbox scored by two LLM judges; Claude-Sonnet-4.5 best overall at about $1.08 per task, MiMo-V2-Flash about $0.007 |
| D26 | Cherry et al., "How Anthropic enables self-service data analytics with Claude" (Anthropic, vendor article, June 2026) | 2026 | [claude.com](https://claude.com/resources/articles/how-anthropic-enables-self-service-data-analytics-with-claude) | Vendor report: accuracy never above 21% without skills, about 95% with them, then a drift to about 65% in a month without upkeep; "the silent one" is the failure it does not catch |
| D27 | Rahman et al., "DSAgentBench: Can Agents Automate End-to-End Data-Science Workflows in Real Computer Environments?" (York U., Nanyang Tech. U., Salesforce AI Research) | 2026 | [arXiv:2608.10366](https://arxiv.org/abs/2608.10366) | 275 end-to-end workflow tasks run through a real desktop (notebooks, IDEs, terminal, browser), each with a deterministic evaluator; best agent Claude-4.6-Sonnet 56.70%, every open-source agent below 1% |

PDFs: D1-D25 and D27 (26 of 27); D26 is a `_NOTE.md` (a vendor web article with no PDF). Quotes below come from the PDF
text, extracted locally, except D26 (quoted from the fetched page) and where a line says
a quote is from a GitHub README (those were fetched with `gh api` on 2026-11-21 and are labelled).

## What it establishes

**Verdict:** accuracy against known answers is **moderate on easy, closed-form questions and low on
anything multi-step**, and the published numbers are unstable in both directions. They rise fast when a
harness is tuned to the benchmark (on the live DAB leaderboard a tuned-prompt row with per-query notes reaches 0.9917 against 0.8858 for the best untuned row; the paper's best agent scored 57% on an earlier 104-query set), and they are
partly capped or distorted by wrong answer keys (one audit puts a third of mismatches on the benchmark,
not the agent). The dominant failure is not a crash: it is a plausible, wrong number from a wrong
plan or a wrong implementation. Round 2 (D16-D27) sharpens this with newer models and statistics-specific
benchmarks: the right conclusion is reached far more often than the right number (D21, D20), data
artifacts and leakage break agents that score well on clean data (D17, D23), and the one large vendor
report says accuracy came from curated skills and decayed without upkeep (D26). For the kit this means
"the analysis ran" is never evidence, a known-answer study must audit its own labels first, and the
analysis agent needs checks that look at the data, not only at the code's exit status.

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
   strongest baseline on KramaBench Full Input (Section 4.5; the text does not say whether that is per task
   or per suite). RADAR still leaves silent errors in 28.1% of substantive deliveries, against 41.8% for
   DS-STAR (Section 4.3). D8 finds "Execution feedback is necessary for LLMs to generate useful programs"
   (Section 4.1). D10: "Agentic control flows drive the largest performance gains": an agent loop with
   Claude-3.7 reached 55.83% against 24.98% for the best fixed pipeline (Section 4). By contrast D6 reports
   that "effective reasoning prompts such as React and planning with a self-critic ... do not help improve
   the simple CodeGen agent", while a run given an oracle score "significantly improves" (Section 5.2): the
   gain needs a real external signal, which a known-answer check can supply but a self-critic cannot. D11
   also finds that giving schema descriptions and hints moved pass@1 by at most 5 points, and a hint that
   did not apply to a query could mislead the agent into changing a correct answer (Section 4.3).
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
   "85% samples" (Section 2.3.1), so the ceiling is an agent's consensus, not independent truth. D9's two
   annotators agreed on 97.3% of 75 answers (Cohen's κ = 0.94), and its scorer matched their judgment on
   all 75; D3 had people check its semantic-match function on 100 answers (Appendix F, reported 100%
   agreement).
7. **Contamination and gaming are measured only partly.** D4 found "no evidence of GPT-4o being
   over-reliant" on recognising competitions and no plagiarism or rule-breaking in medal runs, but "does
   not rule out subtler effects" (Section 4.2) and "make[s] no guarantees about future models" (Section
   6). D8 removes five test points per dataset and re-splits model-development data to defend against memorised data loaders (Section 2.2). D9 keeps
   a hidden test set so ground truths cannot leak into training data (Section 3.3); D1 keeps its test
   set closed (Section 2.4). The live DAB leaderboard (repo README, fetched 2026-11-21 with `gh api`, not
   a paper) shows the scale of the problem: its best row with a "tuned prompt" is 0.9917, and 0.8858 is the
   best row without one, against 57% in D11; its footnotes record trials "counted as non-passes" because
   agents "loaded external gold labels", rows where "Each note tells the agent how to solve that query", and a
   validator re-scored after the key listed one of 95 tied answers. D12 also adds an older model "motivated
   by concerns about benchmark contamination" (Section 4.5).
8. **Statistics-specific benchmarks show the right decision is not the right number.** D21's P-Bench
   (425 tasks, answer keys "audited by domain experts", three rollouts per task) scores a decision (Raw) and
   a p-value close to the canonical analysis (Strict): GPT-5.4 gets 92.9 Raw but 64.7 Strict on the easy split
   and 58.3 Raw but 30.5 Strict on the hard one, "the correct reject/fail-to-reject direction nearly twice as
   often as it produces a p-value close to the canonical analysis" (Section 5, Table 1). D20 splits causal
   analysis the same way: "the model correctly identifies the high-level strategy in 81% of cases,
   full identification-specification correctness drops to only 38%" with "the bottleneck ... in the nuanced
   details of research design rather than in computation" (Abstract; one baseline LLM). A grader that checks
   only the final verdict overstates reliability; the kit's known-answer grader should check the estimate and
   its standard error too. D19 adds that the answer format moves the score: 21% open-answer accuracy and
   "marginally better than random in a multiple-choice setting" (Abstract, 2025 models: GPT-4o and Claude 3.5
   Sonnet).
9. **Clean-data success does not carry over to dirty data, and accuracy hides methodology errors.** D17:
    "models like o4-mini achieve 100% on clean tables aided with code execution, performance drops by 59% on
    perturbed ones" (Section 1; perturbations injected programmatically so a naive computation is wrong). D23
    audits agent-written modelling pipelines for six controlled failures: "All framework-model configurations
    have at least one failure mode that occurs in 43% or more of the pipelines", and "All data leakage modes
    lead to improved rankings", so "evaluating agents solely by their scores can reward leakage modes"
    (Section 4.2). The agent frameworks in D23 used small or cheap models (Qwen, Gemini flash), so this is
    not a measurement of Claude Code; its test suite is still a ready-made leakage check.
10. **Long, stateful analysis degrades with turns.** D24's 68 tasks built from Kaggle notebooks (2,225 turns):
    "the best model reaches only 48.45% average accuracy, performance drops nearly 47 points from early to
    late turns, and long-horizon errors account for 52%-69% of failures" (Abstract); Claude-4.6-Sonnet scores
    41.56 and "uses the most steps but does not achieve the best accuracy" (Section 5.1), so a bigger step
    budget is not the fix. This is the closest evidence to a notebook agent that edits earlier cells. D27 moves the same problem to a real
    desktop (OSWorld-based, notebooks, terminal and browser, deterministic evaluators): "even the strongest agent,
    Claude-4.6-Sonnet, achieves only 56.70% task success, while all open-source agents remain below 1%"
    (Abstract, 15 models), which is also the closest published test of the kit's computer-use walk design.
11. **What the labs' agents add, and what they do not fix.** D16 reports that an LLM verifier judging plan
    sufficiency lifts DABStep hard-task accuracy "from 12.70% to 45.24%, an absolute improvement of over 32
    percentage points" with Gemini-2.5-Pro (Section 4.1); removing the data-file descriptions drops it to
    26.98% (Section 4.2), so the data summary matters as much as the verifier. D12's audit of the same agent
    still found 69.8% of its zero-scored runs silently wrong. AIRA-dojo (Toledo et al. 2025, FAIR at Meta, arXiv:2507.02554; catalogued in folder 06) shows the search loop itself can mislead:
    "selecting the final solution in a search graph by its test--rather than validation--score, would
    increase the medal rate by 9 to 13 % (absolute scale)" (Section 1, 5.3), so any propose-and-score loop in
    the kit needs a held-out check the agent cannot tune against. Google's ERA (Aygun et al. 2025, arXiv:2509.06503; folder 06) beats the published method on
    "eight of the nine methods in overall score" and by "14% overall improvement" on one task, but needs a
    "scorable task" with a numeric metric, which a statistics question rarely has.
12. **Anthropic's own account says curated context, not model strength, set accuracy, and silent errors
    remain.** D26 (vendor article, not a study): "Without skills, Claude's ability to answer analytics
    questions accurately didn't exceed 21% on our evals", "consistently above 95% in aggregate" with skills,
    then "drift from ~95% at launch to ~65% over a month" when upkeep lapsed; an adversarial-review pass added
    6% accuracy "at the cost of 32% more tokens and 72% higher latency"; and "The failure mode none of this
    fully catches is the silent one." It matches D11 (wrong plan and wrong implementation, not wrong data) and
    D12.
13. **Agents can reproduce published analyses, but the keys and the judges are imperfect.** D22 (48 papers,
    four scaffolds including Claude Code with Opus 4.6, methods text and data only): reproduced coefficients
    "match the sign for the large majority of observations, ranging from 75% (SWE-Agent GPT-5.4) to 91%
    (OpenCode GPT-5.4)" against 68% for always guessing positive (Section 5.1); a human audit "confirms only
    33 of 49 error-source labels (67%)" (Section 5.3), and the largest source of divergences is the paper
    itself being under-specified. REPRO-Bench (Hu et al. 2025, UIUC, Findings of ACL 2025, arXiv:2507.18901; folder 06) is the cold counterpoint on an older harness: "CORE-Agent achieves the
    highest accuracy at 21.4%", below "the expected 25% accuracy of random guessing among four options"
    (Section 5), on the task of judging whether a paper reproduces, not of redoing it.

14. **Datasets we could use as a v0.1 known-answer task.** Read the licence before copying (CLAUDE.md §4);
   sizes are from the papers, licences from the repos' LICENSE files or README badges as fetched.

   | Candidate | Size and answer type | Licence | Fit for v0.1 |
   |---|---|---|---|
   | D1 DAEval | 257 questions, 52 CSVs, exact-match `@name[answer]` labels (public validation set; test closed) | repo Apache-2.0; README badge: data CC BY-NC 4.0 | Best fit: closed form, regex grader, small; data non-commercial (CC BY-NC 4.0, README badge only). Audit labels first (see 6) |
   | D14 QRData | 411 stats and causal questions, textbook and paper data, gold answers, 3% numeric tolerance | CC BY-NC 4.0 | Good for "right method" checks; non-commercial |
   | D9 DABstep | public dev set with answers plus hidden test; 450 tasks in all, factoid answers | dataset CC BY 4.0 (per the paper) | Good for multi-step; use dev set only |
   | D6 DiscoveryBench | 264 real tasks from papers (test split 239 queries), scored by a GPT-4 evaluator | ODC-By | Open-ended scorer adds judge bias |
   | D7 BLADE | 12 datasets, expert decisions as truth | code Apache-2.0, data ODC-By (README badges) | Tests method choice; scorer is an LM matcher |
   | D20 CausalReasoningBenchmark | 174 queries, 139 real datasets from 73 papers and 3 textbooks; structured design spec plus estimate and standard error | metadata, eval code and gold specs MIT; datasets keep their original licences ("Licensing and Access" paragraph) | Best fit for an econometrics-style task; scores design and estimate separately; check each dataset's licence before redistribution |
   | D21 P-Bench | 425 hypothesis-testing tasks with expert-audited keys (method, p-value, decision) | not found in the paper text; check the repo before use | Good for "right test, right p-value"; keys audited by the authors only |
   | D17 RADAR | 2,980 table-query pairs, 53 real datasets, injected artifacts | repo Apache-2.0; dataset licences listed per dataset in the paper's appendix (rows seen: CC BY 4.0, CC BY, Apache 2.0) | Method to borrow: perturb our own known-answer data; check each source licence |
   | D19 BixBench | 205 questions over 61 analysis capsules (v3 PDF), Jupyter notebooks | repo Apache-2.0; data licence not checked | Domain is bioinformatics; useful as a notebook-agent format |
   | D10 KramaBench, D11 DAB | 104 pipelines / DAB queries; reference sub-tasks | repos show no licence | Do not copy; read-only |
   | D4 MLE-bench | 75 Kaggle competitions, medals | MIT code; Kaggle data under competition rules | Too heavy: Lite split is 158 GB |

**Design implications for the kit:** (a) the analysis agent reports a number only with the code, the
rows and columns it used, and a check against the data (row counts after each join, no mutation of the
raw file); (b) the research factory's known-answer study uses a small closed-form set (D1 or D14 first),
pre-registers the grader, and has an auditor pass over the labels before any agent runs (D13, D15);
(c) run at least 3 times per arm and report the spread, since D4's pass@6 roughly doubles pass@1; (d) log
cost per task (D11, D8 report it, most do not); (e) keep a held-out slice and never put its labels in
the agent's reach (D8, D9, D11 leaderboard); (f) for a statistics or econometrics study, grade the
estimate and its standard error or p-value as well as the verdict, since conclusions are right far more
often than numbers (D20, D21); (g) add two cheap silent-error gates: a perturbed copy of the known-answer
data with injected artifacts (D17) and a leakage check before any model score is believed (D23); (h) any
loop that proposes and scores candidates must select on a split the agent cannot tune against (AIRA-dojo, folder 06); (i)
treat the analysis agent's context (data-model notes, skills) as maintained code with its own eval and a
drift check, because D26 reports 95% falling to about 65% without upkeep.

## The catch

- **Round-2 selection leans toward big labs and top universities, by instruction.** D16-D27 were chosen
  with a preference for Google, Meta, Microsoft, Anthropic and top-university authors. That is a filter on
  who wrote the paper, not on whether the result is right; D16, the folder-06 papers ERA and AIRA-dojo, and D26 are authored by the
  organisations whose products or agents they describe, and D21's authors built both the benchmark and the
  agent that wins on it.
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
- **Round-2 numbers are mostly single-model, single-benchmark, and some use weak models.** D20's 81% and
  38% come from one baseline LLM; D23's agent frameworks ran Qwen and a Gemini flash model, not a frontier
  model or Claude Code; REPRO-Bench's agents are 2024 scaffolds judging reproducibility, not doing analysis; D24
  and D25 score with task-level accuracy or LLM judges (D25's two judges were calibrated against three PhD
  annotators on one agent's log), which is weaker than a known answer. D22's root-cause labels were 67%
  right on audit, so its error shares are indicative. D18 and D17 measure table skills, not whole analyses; D27's open-source rows below 1% suggest harness or grounding failure, not analysis ability, and its 56.70% is one 2026 model on its authors' tasks.
- **D26 is a vendor article, not a study.** It reports Anthropic's own warehouse, evals and skills, with no
  public data, run counts or intervals; it shows what one organisation measured and does not show the kit
  would match it. D16 reports numbers taken largely from the public DABStep leaderboard and
  KramaBench's paper, where D12 shows the same agent still ships silent errors.
- **Licences and keys for the new datasets are not all checked.** D21's licence and D19's data licence were
  not found in the text; D20's gold specs are MIT but its datasets carry their own licences. No audit of
  D20, D21 or D19 answer keys exists beyond the authors' own checks, so D13/D15-style audits still apply.
- **Preprint quality varies.** D5, D6, D9, D11, D12, D13 and D15 are preprints; D12, D13 and D15 are 2026
  and unreplicated; so are D20 to D25 and D27 apart from D17 and D18 (conference-accepted). D1's arXiv page carries "work in progress"; D13's scope is data engineering, not
  analysis.
