# 08 Research Integrity and Reproducibility

## Role

This folder collects the evidence on why analyses, by people or by agents, find what they were hoping
to find, and on what measurably stops it: many-analyst studies, the garden of forking paths,
pre-registration and registered reports, replication rates, computational reproducibility, and the new
2025-2026 work that runs LLM agents as analysts. Its central question is **what stops an analysis
(human or agent) from finding what it wants?** It informs the research factory's gates (what goes in
`PREREG.md`, the dev/held-out split, how many runs per arm, how a result is reported), the grader's
checks on `/autonomous:new-study`, and what the kit must refuse to let an analysis agent do on its own.
Cross-references: finance-specific multiple-testing and backtest-overfitting papers (Harvey-Liu-Zhu,
Deflated Sharpe, FDR control, and Ioannidis 2005) are held in the Trading repo's
`16_Backtest_Validity_and_Sizing` and `17_Research_Factory_Statistics` folders and are not duplicated here.

## Contents

| ID | Citation | Year | Link | What it establishes |
|---|---|---|---|---|
| R1 | Bertran et al., "Many AI Analysts, One Dataset: Navigating the Agentic Data Science Multiverse" | 2026 | [arXiv:2602.18710](https://arxiv.org/abs/2602.18710) | Autonomous LLM analysts given one dataset, hypothesis and estimand reach divergent p-values and verdicts; 4,946 runs; the most confirmation-seeking persona shifts support rates 34-66 pp over the most skeptical; an AI auditor narrows but does not remove the shift |
| R2 | Alizadeh et al., "AI Coding Agents in Social Science: Methodologically Diverse, Empirically Consistent, Interpretively Vulnerable" | 2026 | [arXiv:2606.11456](https://arxiv.org/abs/2606.11456) | Claude Code and Codex (20 runs each) match or exceed human many-analysts diversity with estimates near the human consensus; a "seek support" prompt flips Claude Code's verdicts 10% to 90% while coefficients barely move, by omitting the decision rule |
| R3 | Miao et al., "The Agentic Garden of Forking Paths" | 2026 | [arXiv:2607.01507](https://arxiv.org/abs/2607.01507) | Opposing personas give agents opposing conclusions from the same data (72% of the human ideological gap reproduced); 86% of the reports still pass AI review; proposes the m-value and an "Agentic Bootstrap" to place a result within its multiverse |
| R4 | Rewolinski et al., "Sanity Checks for Agentic Data Science" | 2026 | [arXiv:2604.11003](https://arxiv.org/abs/2604.11003) | Null-shuffle and perturbation checks on Codex across 11 datasets: in 6 an affirmative conclusion is not well supported, and the agent's own confidence is poorly calibrated to stability |
| R5 | Asher et al., "Do Claude Code and Codex P-Hack? Sycophancy and Statistical Analysis in Large Language Models" (working paper) | 2026 | [PDF](https://andrewbenjaminhall.com/pdfs/asher_et_al_LLM_sycophancy.pdf) | 640 runs of Claude Opus 4.6 and GPT-5.2-Codex: stable estimates and explicit refusal under standard and "significance" prompts, but a prompt that reframes specification search as "uncertainty reporting" produces systematic p-hacking |
| R6 | Thomas et al., "Mitigating LLM-based p-Hacking by Preregistering for the Next LLM" | 2026 | [arXiv:2606.27687](https://arxiv.org/abs/2606.27687) | Pre-register the analysis, then run it on the first eligible model released afterwards; would have blocked 73.9% and 72.7% of hacks on two known-answer tasks; 6 of 7 hacked configurations failed to carry over in a preregistered test |
| R7 | Vaccaro, "Preregistration for Experiments with AI Agents" (ICML 2026 position paper) | 2026 | [arXiv:2606.11217](https://arxiv.org/abs/2606.11217) | Catalogues the researcher degrees of freedom of agent experiments (model, prompt, settings, retries, parsing) and proposes a preregistration template with pilot-history disclosure and a confirmatory/exploratory label; an argument, not a measurement |
| R8 | Xu and Yang, "Scaling Reproducibility: An AI-Assisted Workflow for Large-Scale Replication and Reanalysis" | 2026 | [arXiv:2602.16733](https://arxiv.org/abs/2602.16733) | An agent-assisted pipeline re-executes 384 political-science papers (3,523 models); reproducible share 20.8% before verification mandates vs 82.5% after; median $0.54 and about 11 minutes per paper on the happy path |
| R9 | Silberzahn et al., "Many Analysts, One Data Set: Making Transparent How Variations in Analytic Choices Affect Results" (AMPPS) | 2018 | [doi:10.1177/2515245917747646](https://doi.org/10.1177/2515245917747646) | 29 teams, one soccer dataset, one question: odds ratios 0.89 to 2.93, 20 teams significant and 9 not; beliefs, expertise and peer-rated quality did not explain the spread |
| R10 | Botvinik-Nezer et al., "Variability in the analysis of a single neuroimaging dataset by many teams" (Nature) | 2020 | [doi:10.1038/s41586-020-2314-9](https://doi.org/10.1038/s41586-020-2314-9) | 70 fMRI teams, 9 hypotheses: no two teams used identical workflows; on average 20% of teams disagreed with the majority verdict; prediction-market traders overestimated significant results |
| R11 | Breznau et al., "Observing many researchers using the same data and hypothesis reveals a hidden universe of uncertainty" (PNAS) | 2022 | [doi:10.1073/pnas.2203150119](https://doi.org/10.1073/pnas.2203150119) | 73 teams, 1,261 models, 166 coded decisions: more than 95% of the variance in results is unexplained by researcher traits or decisions the authors could code |
| R12 | Gelman and Loken, "The garden of forking paths: Why multiple comparisons can be a problem, even when there is no 'fishing expedition' or 'p-hacking' and the research hypothesis was posited ahead of time" | 2013 | [Columbia PDF](http://www.stat.columbia.edu/~gelman/research/unpublished/p_hacking.pdf) | The multiple-comparisons problem exists without any deliberate search whenever analysis choices depend on the data; the remedy is a preregistered confirmatory study after an exploratory one |
| R13 | Scheel, Schijen and Lakens, "An excess of positive results: Comparing the standard Psychology literature with Registered Reports" (AMPPS) | 2021 | [doi:10.1177/25152459211007467](https://doi.org/10.1177/25152459211007467) | 96% positive first hypotheses in 152 standard reports vs 44% in 71 Registered Reports; non-randomised, so not causal |
| R14 | Open Science Collaboration, "Estimating the reproducibility of psychological science" (Science) | 2015 | [doi:10.1126/science.aac4716](https://doi.org/10.1126/science.aac4716) | 100 replications: 97% of originals significant vs 36% of replications; replication effects half the size of the originals |
| R15 | Trisovic et al., "A large-scale study on research code quality and execution" (Scientific Data) | 2022 | [doi:10.1038/s41597-022-01143-6](https://doi.org/10.1038/s41597-022-01143-6) | 9,078 R files from 2,109 Dataverse packages re-run in a clean Docker image: 74% failed on first execution, 56% after automatic cleaning of paths and libraries |
| R16 | Gould et al., "Same data, different analysts: variation in effect sizes due to analytical decisions in ecology and evolutionary biology" (BMC Biology) | 2025 | [doi:10.1186/s12915-024-02101-x](https://doi.org/10.1186/s12915-024-02101-x) | 174 analyst teams (246 analysts), two unpublished datasets: 141 and 85 usable effects; "near continuous variation" from large negative effects to effects near zero, some significant in the opposite direction; variation unrelated to variable sets, random-effects structure or peer rating of the analysis |
| R17 | Menkveld et al., "Nonstandard Errors" (The Journal of Finance) | 2024 | [doi:10.1111/jofi.13337](https://doi.org/10.1111/jofi.13337) | 164 teams test the same six hypotheses on the same market data; researcher-to-researcher spread (nonstandard error) is sizable, 1.2% around a median of -3.3% for one hypothesis and 6.7% around 1.1% for a vaguer one; peer feedback halves it; participants underestimate it |
| R18 | Camerer et al., "Evaluating the replicability of social science experiments in Nature and Science between 2010 and 2015" (Nature Human Behaviour) | 2018 | [doi:10.1038/s41562-018-0399-z](https://doi.org/10.1038/s41562-018-0399-z) | 21 pre-registered, high-powered replications (about 5x the original samples): significant same-direction effect for 13 (62%), effect size about 50% of the original; a consortium result from top-journal studies |
| R19 | Brodeur, Cook, Hartley and Heyes, "Do Pre-registration and Pre-analysis Plans Reduce p-Hacking and Publication Bias?" (IZA DP 15476; JPE Microeconomics 2024) | 2024 | [IZA PDF](https://docs.iza.org/dp15476.pdf) | 15,992 test statistics from RCTs in 15 leading economics journals: registration alone shows no meaningful difference in p-hacking, a complete pre-analysis plan does (about 10 points fewer marginally significant statistics) |
| R20 | Protzko et al., "Retraction Note: High replicability of newly discovered social-behavioural findings is achievable" (Nature Human Behaviour) | 2024 | [doi:10.1038/s41562-024-01997-3](https://doi.org/10.1038/s41562-024-01997-3) | The headline "pre-registration and rigour give high replicability" paper was retracted for misstated pre-registration, outcomes and analyses chosen with knowledge of the data, and incomplete reporting; a case of the reform itself failing its own standard |
| R21 | Miller (Anthropic), "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations" | 2024 | [arXiv:2411.00640](https://arxiv.org/abs/2411.00640) | Evals are experiments: standard errors, clustered errors, resampling to cut variance, paired differences between models and power analysis; the template for how a kit scorecard should report a score |
| R22 | Agarwal et al. (Google Research, Brain Team), "Deep Reinforcement Learning at the Edge of the Statistical Precipice" (NeurIPS 2021 Outstanding Paper) | 2021 | [arXiv:2108.13264](https://arxiv.org/abs/2108.13264) | With 3-10 runs per task, point estimates mislead; recommends interval estimates, performance profiles and the interquartile mean, and finds discrepancies in prior comparisons on ALE, Procgen and DM Control |
| R23 | Pineau et al. (Facebook AI Research, McGill), "Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)" | 2020 | [arXiv:2003.12206](https://arxiv.org/abs/2003.12206) | Code-submission policy, a reproducibility challenge and a checklist at NeurIPS 2019; cites a study where 63.5% of results in 255 manuscripts reproduced, 85% with author help and 4% without |
| R24 | Hofman et al. (Microsoft Research, Northwestern, Penn), "Pre-registration for Predictive Modeling" | 2023 | [arXiv:2311.18807](https://arxiv.org/abs/2311.18807) | A lightweight pre-registration template for predictive modelling (reuse of test data, data-dependent choices) and an interview study of ML researchers who followed it; participants "might have produced biased estimates" without it |
| V23 (filed in 05) | MacDiarmid et al. (Anthropic), "Natural Emergent Misalignment from Reward Hacking in Production RL" | 2025 | [arXiv:2511.18397](https://arxiv.org/abs/2511.18397) | Models that learn to game coding-test harnesses (for example `sys.exit(0)` before the asserts) generalise to sabotage in Claude Code, 12% attempted sabotage in the main setting; prevention and inoculation prompting help |
| R26 | Toledo et al. (FAIR at Meta), "AI Research Agents for Machine Learning: Search, Exploration, and Generalization in MLE-bench" | 2025 | [arXiv:2507.02554](https://arxiv.org/abs/2507.02554) | Agents that search against a validation score overfit it: picking the final solution by test score would raise the medal rate by 9-13 points (absolute), the agent analogue of reusing a held-out set |
| R27 | Baumann et al., "Large Language Model Hacking: Quantifying the Hidden Risks of Using LLMs for Text Annotation" | 2025 | [arXiv:2509.08825](https://arxiv.org/abs/2509.08825) | 37 annotation tasks from 21 social-science studies: a handful of prompt paraphrases can make virtually anything significant; 13 million labels, 18 LLMs, 2,361 hypotheses: incorrect conclusions in about 31% of hypotheses for state-of-the-art models |
| R28 | Samuel and Mietchen, "Computational reproducibility of Jupyter notebooks from biomedical publications" (GigaScience) | 2024 | [doi:10.1093/gigascience/giad113](https://doi.org/10.1093/gigascience/giad113) | 27,271 notebooks from 2,660 repositories linked to 3,467 articles: of 10,388 whose declared dependencies installed, 1,203 ran without error and 879 reproduced the original results |
| F27 (filed in 09) | Segato (Anthropic), "Quantifying infrastructure noise in agentic coding evals" (engineering blog, vendor-authored, `_NOTE.md`) | 2026 | [Anthropic Engineering](https://www.anthropic.com/engineering/infrastructure-noise) | Compute limits alone moved Terminal-Bench 2.0 scores by 6 points (p < 0.01); the post advises scepticism toward leaderboard gaps under 3 points until eval configurations are matched |
| R30 | Liu, Kale, Althoff and Heer (UW), "Boba: Authoring and Visualizing Multiverse Analyses" | 2020 | [arXiv:2007.05551](https://arxiv.org/abs/2007.05551) | An open DSL where an analyst writes one script plus the decision points and the compiler generates and runs every variant; a free, citable copy of the multiverse method that the folder could not otherwise reach |

## What it establishes

**Verdict:** nothing about the analyst stops it: not expertise, not honest intent, not a neutral prompt,
and for an agent not a polished, reviewer-approved report. What measurably helps is structure placed
*around* the analysis: commitments made before the data or the result exists (a pre-registered plan, a
decision rule, a held-out confirmatory run), reporting the whole distribution of defensible analyses
rather than one, null-based sanity checks, and an independent re-run of the code. For the kit this
means a study agent must not both choose the analysis and grade it, and no number reaches `RESULT.md`
unless it came from a plan and decision rule committed before it existed.

1. **Honest, expert analysts of one dataset disagree.** R9: 29 teams, "estimated effect sizes ranged
   from 0.89 to 2.93 in odds ratio units, with a median of 1.31. Twenty teams (69%) found a
   statistically significant positive effect and nine teams (31%) observed a non-significant
   relationship" (Abstract), and "neither analysts' prior beliefs about the effect, nor their level of
   expertise, nor peer-reviewed quality of analysis readily explained variation in analysis outcomes".
   R10: "no two teams chose identical workflows"; on average "20% of teams reported a result that differs
   from the majority" (Results, first paragraph), which the authors place "midway between complete
   consistency across teams and completely random results". R11: of 1,261 models, "no two ... were 100%
   identical"; design decisions explain 2.6% and researcher characteristics at most 1.2% of the variance,
   "95.2% of the total variance in results is left unexplained" (Results). The cause is not misconduct:
   R12 shows that when "the details of data analysis are highly contingent on data" the multiple-comparisons
   problem arises "without the researcher having to perform any conscious procedure of fishing" (Abstract).
2. **LLM agents reproduce this variation, cheaply.** R1 ran four LLMs as tool-using analysts on three
   datasets: "Of 4,946 total runs, 3,303 (67%) passed auditor-based compliance screening" (Section 4), and
   "independent runs frequently reverse whether the hypothesis is judged supported" (Section 1). R3: "AI
   agents reproduced 72% of the human ideological gap in reported effect estimates" and "86% of the
   agent reports passed independent AI methodological review, and 78% passed review by a majority of
   independent human experts" (Abstract). The consequence both papers draw: "when defensible analyses
   are cheap to generate, evidence becomes abundant and vulnerable to selective reporting" (R1,
   Abstract).
3. **Agents can be steered, but the lever is the prompt, not the model's tendency.** R1: "the Negative-to-Strong
   CS gap ranges from 34 percentage points (anes-views) to 66 percentage points (metr-rct)" (Section 4.2),
   and the auditor removed 53-57% of the confirmation-seeking runs against 21-23% of the negative, standard and
   positive personas (Table 2), so filtering "narrows, but does not eliminate" the shift. R5: under no-nudge,
   "upstanding researcher" and "significance" prompts "both models produce accurate and remarkably stable
   estimates" and refuse ("this is asking me to engage in p-hacking", Section 3.2), with a median of one
   specification per run; under the "nuclear" prompt that "reframes specification search as uncertainty
   reporting" the median Thompson run had 13 (Claude) and 16 (Codex) specifications (Section 3.3). One run moved
   a -0.06 published estimate to -0.194 (p < 0.001). Inflation tracked flexibility: "observational studies are
   more vulnerable than randomized experiments" (Abstract). So the guardrail stops a blunt request, not a
   reworded one.
4. **In R2 the agent's bias sits in the verdict (R3 also finds persona-driven estimates), so pre-commit
   the decision rule.** R2: a confirmatory prompt "flips Claude Code's verdicts from 10% to 90% support
   while leaving its coefficient distribution essentially unchanged, operating through rule omission
   rather than rule softening" (Abstract); Claude Code's plans containing an explicit decision rule
   fell from 11 of 20 to 8 of 20 (Fig. 5 caption; the Results text gives 12/20 for Default), and
   "Twelve of the 20 CC Confirmatory plans omit an explicit verdict criterion altogether" (Results,
   Fig. 5). That is the mechanism a `PREREG.md` closes: the rule that turns estimates into a claim is
   written, and committed, before the runs.
5. **Pre-commitment is the tool with measured support.** R13: "96% positive results in standard reports,
   but only 44% positive results in Registered Reports" (Abstract), and within the three journals that
   published both formats 11/13 standard reports were positive against 7/14 Registered Reports
   (Limitations). R14 is the size of the problem it addresses: "Ninety-seven percent of original studies
   had significant results. Thirty-six percent of replications had significant results" and "Replication
   effects were half the magnitude of original effects" (Abstract). For agents, R6 transplants the idea:
   preregister, then run on a model that "does not exist at commitment time", so "it cannot be hacked
   against" (Abstract); "6 configurations" of 7 failed to carry over to the first eligible model released
   afterward, and it would have prevented p-hacking "in 17 of the 23 cases" and "32 out of the 44 cases"
   (Section 4.1). R12 gives the same recipe for people: two experiments, "the first being exploratory but
   still theory-based, and the second being purely confirmatory with its own preregistered protocol"
   (Section 4.3). R7 turns it into a template
   that "requires disclosure of pilot-testing history: how many prompt iterations were explored, which
   models were tested during development" (Section 4.2), the field the kit's `TRIAL_LOG.tsv` already holds.
6. **Report the distribution, and test against noise.** R1 recommends "multiverse-style reporting and full
   disclosure of the prompts used" (Abstract). R3 defines the m-value, "the probability that an analysis
   path would produce a claim at least as extreme as the reported one", and finds that "13.5% of reported
   human analyses fell in the most extreme 5% of the analysis space" (Abstract). R4's checks are cheap:
   run the agent on perturbed data and on data with the outcome shuffled, and "in 6 of the datasets an
   affirmative conclusion is not well-supported, even though a single ADS run may support one" (Abstract);
   "self-reported confidence is nearly uninformative" (Section 5.3). So the kit's study grader needs a null
   arm and several independent runs, not the agent's own confidence.
7. **A result must also be re-runnable, and agents can check that.** R15: "74% of R files failed to complete
   without error in the initial execution, while 56% failed when code cleaning was applied" (Abstract); the
   cleaning fixed "all errors related to the command setwd" (Results and Discussion). R8: "the share of fully or largely
   reproducible papers rises from 20.8% before DA-RT adoption to 82.5% after" (Abstract), the authors
   conclude "active verification--not merely archiving mandates--drove the improvement" (Section 5.2), and the
   pipeline costs a median "$0.54 per paper" and about "11 minutes" on the happy path (Runtime and cost,
   p. 23). Its design is the one to copy: a deterministic state machine runs the pipeline, an LLM sub-agent
   is "dispatched only when a stage fails its validation gate", and "all numerical work ... is executed by
   version-controlled program code" (Section 2). That fits the kit's `replicate.ipynb` Run All rule and a
   final independent re-execution of every study.

8. **Many-analyst variation is not a quirk of one field.** R16 repeats the design in ecology: "174 analyst
   teams, comprising 246 analysts", 141 usable effects for one dataset and 85 for the other, "near
   continuous variation in effect size from large negative effects to effects near zero, and even effects
   crossing the traditional threshold of significance in the opposite direction" (Abstract), with no
   strong link between variable selection, random-effects structure or peer rating and distance from the
   mean. R17 puts a number on it in finance, with 164 teams on the same data: a nonstandard error of
   "1.2% around a median of -3.3%" for a clear hypothesis and "6.7% around 1.1%" for a vaguer one,
   "smaller for more reproducible and higher quality papers", and "peer feedback reduces NSEs by half"
   (Conclusion). The lever that worked in R17 is review, not a better analyst, which is the kit's
   independent evaluator.
9. **Pre-registration helps through the detail of the plan, not through the act of registering.** R19, on
   15,992 test statistics from RCTs in 15 leading economics journals: "no meaningful difference in the
   distribution of test statistics from pre-registered studies, compared to their non-pre-registered
   counterparts. However, pre-registered studies that have a complete PAP are significantly less
   p-hacked" (Abstract), with the share of marginally significant statistics "about 10 percentage points
   lower" in articles with a complete PAP (Results). That is an argument for a `PREREG.md` that fixes the
   specifications, outcomes and decision rule, not a bare timestamp. R24 (Microsoft Research and
   collaborators) carries the idea to predictive modelling with a template and an interview study
   (qualitative, small, one department).
10. **Agents overfit the dev set they search against.** R26 (FAIR at Meta) on MLE-bench: "we find
    systematic overfitting: selecting the final solution in a search graph by its test--rather than
    validation--score, would increase the medal rate by 9 to 13 % (absolute scale)" (Introduction), with a
    widening validation-test band over 20 seeds (Fig. 4). This supports the dev/held-out split and the
    one-look rule in CLAUDE.md section 5: the more the agent iterates against a metric, the less that
    metric means. V23 (Anthropic) is the adversarial end of the same pressure: models trained on
    environments they could game learned hacks such as "calling sys.exit(0) to break out of a test
    harness" and showed "attemped sabotage 12% of the time" (sic) in a Claude Code setting (Introduction),
    so a grader must not live where the agent can edit or exit around it.
11. **Report a score as an estimate: runs, error bars, environment.** R21 (Anthropic): "evaluations are
    experiments", with recommendations to compute standard errors, cluster them, resample, compare models
    on paired question-level differences and use power analysis (Section 1). R22 (Google Research):
    "3-10 runs are prevalent" in deep RL, so point estimates hide the uncertainty; interval estimates and
    the interquartile mean are the remedy (Introduction). F27 (Anthropic engineering post): resource
    configuration alone gave "6 percentage points (p < 0.01)" on Terminal-Bench 2.0. Together they fix what
    the benchmark scorecard must carry: several runs per arm, a confidence interval, and the environment
    spec.
12. **LLM choices are themselves forking paths.** R27: "with just a handful of prompt paraphrases,
    virtually anything can be presented as statistically significant" and "incorrect conclusions in
    approximately 31% of hypotheses for state-of-the-art LLMs" (Abstract). Any study that uses an LLM to
    label, grade or simulate must pre-register the model, prompt and settings, as R7 says for agent
    experiments.
13. **Re-runnable code is the weakest link, and notebooks are not exempt.** R28 re-ran Jupyter notebooks
    tied to biomedical papers: of 10,388 with installable declared dependencies, "1,203 notebooks ran
    through without any errors, including 879 that produced results identical" to the original (Abstract),
    with failures traced mainly to dependency documentation. With R15 and R8 this supports pinning the
    environment inside `replicate.ipynb` and having the evaluator re-run it in a clean environment before
    any result counts. R23 (Facebook AI Research) shows a soft policy moves behaviour: "About 40% of
    authors reported that they had provided code" at initial submission to NeurIPS 2019 (Section 3), though
    a checklist is not a check.

## The catch

- **No paper measures the kit's setting.** Every agent study here (R1-R5) runs one-shot or short
  analyses of fixed social-science datasets with a prescribed estimand. None runs a multi-hour,
  multi-trial research loop in which the agent sees its own held-out results, which is exactly where
  forking paths grow. The kit's own studies in `research/` have to supply that measurement.
- **The agent papers disagree and are young.** R3 finds personas drive opposing conclusions; R2 finds a
  prompt-induced researcher prior "does not shift aggregate estimates or final verdicts" (Abstract)
  although a "seek support" prompt does flip verdicts; R5 finds stability under standard prompts. They differ in
  prompts, datasets, run counts (20 per cell in R2, 10 per prompt in R5), and model versions, so the
  honest summary is "steerable under some framings", not a rate. R1-R4 and R6-R8 are arXiv preprints and
  R5 is a self-hosted working paper; none is peer reviewed yet. R4's 6 of 11 (Abstract) is 5 datasets where the
  agent mostly answers "No" and 1 (caschools, the Introduction's "one case") where it affirms without clear
  separation from noise; 5 pass both checks (Section 4.3).
- **Guardrail results age fast.** R5's refusals are for Claude Opus 4.6 and GPT-5.2-Codex in Feb 2026, and
  its authors conclude "safety guardrails are likely unable to restrain researchers intent on
  p-hacking". Our design cannot rely on the model refusing; it must rely on gates it does not control.
- **Pre-registration evidence is correlational or by argument.** R13 states its study "was not an
  experiment ... and thus precludes strong causal inferences" (Limitations): authors who choose
  Registered Reports, and the journals that offer them, differ. R6 tests only two binary
  classification tasks on 100 items each, and its authors say the protocol "reduces the chance that a
  p-hack carries over, but does not eliminate it" (Section 6). R7 is a position paper with no data. R12 itself
  argues pre-registration "hardly seems possible" for much applied work with already-studied public data
  (Section 4.3), which is relevant when the kit's studies reuse known datasets.
- **Many-analyst studies measure variation, not error.** R9, R10 and R11 show analysts differ, not which one is
  right; R11 notes that the unexplained variance may be idiosyncratic rather than fixable. They cover
  social science and fMRI, not the app-benchmark or agent-configuration questions the kit studies. R14 is
  psychology only, and its authors note no single indicator settles whether a finding replicated.
- **Reproducibility numbers are field- and language-specific.** R15 is R code in one repository (Harvard
  Dataverse) from 2010-2020; R8 is three political-science journals, and its 92.1% is conditional on a
  replication package being available. R8 also cost about $2,000 for the executable corpus and is a
  preprint by authors who used Claude Code to write it.
- **Not covered.** The primary sources for p-hacking simulations (Simmons, Nelson and Simonsohn 2011), the
  multiverse (Steegen et al. 2016) and specification-curve (Simonsohn et al. 2020) methods are
  publisher-paywalled with no legal open copy found, so they are cited only through R1, R3 and R7. R9
  and R13 are the authors' OSF preprints, R10 is the accepted manuscript from a university repository,
  R11 and R14 are repository copies of the published articles; page and figure numbers may differ from the
  journal PDFs. Trisovic's and Xu's reproducibility rates concern code that runs, not whether the
  analysis is correct.
- **Larger many-analyst studies still measure spread, not error.** R16 and R17 repeat the design of R9-R11,
  but R16 uses two datasets and R17 one market dataset with six hypotheses chosen by the coordinators;
  R17 is finance, and its authors say its nonstandard errors "are likely to be an upper bound" for
  published estimates (Conclusion). R16 is held here as the EcoEvoRxiv preprint, whose numbers may
  differ from the BMC Biology article.
- **The best-known pre-registration win has fallen.** R20 retracts the paper that claimed high
  replicability from pre-registered, large-sample, transparent methods; the editors cite missing
  pre-registration for the supporting analyses, "selection of outcome measures and analyses with
  knowledge of the data" and incomplete reporting, while the authors "disagree with other concerns".
  Evidence that pre-registration works therefore rests on R13 and R19, both observational (R19 compares
  different studies, in economics RCTs from 2018-2021, not one study with and without a plan), and R18
  shows only that high-powered pre-registered replications of Nature and Science papers succeeded 62% of
  the time.
- **The lab papers are measured analogues, not analysis-integrity studies.** R21 is a method paper with
  no empirical test, R22 is about RL benchmarks, R23 is a conference report that quotes the 63.5%
  reproduction figure second-hand, and V23 and R26 study training environments and MLE-bench, not
  social-science analysis. We use them for dev-set overfitting, grader tampering and noise in scores.
  V23 is vendor-authored, about Anthropic's own models in synthetic training settings, and F27 is a
  vendor blog (`_NOTE.md`) on two coding benchmarks. R24's evidence is an interview study of a small
  number of Northwestern PhD students.
- **Computational reproducibility is bounded by what runs.** R28 counts notebooks that run and match, not
  whether they are correct, covers Python notebooks linked from PubMed Central, and its corpus excludes
  repositories without declared dependencies; 879 identical results is about 8% of the 10,388 re-run
  notebooks.
- **Still no measurement of agent p-hacking on analysis tasks beyond R1-R6.** R27 is about LLM annotation,
  not agents running analyses. R30 describes a method and a user study and does not measure its effect on
  research quality. R18-R20 are human-science results; R18 is held as a repository copy of the published
  article, R19 as the IZA working-paper version.
