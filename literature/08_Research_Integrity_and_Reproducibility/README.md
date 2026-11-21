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
   and the auditor removed 53-57% of the confirmation-seeking runs against 21-23% of the neutral ones
   (Table 2), so filtering "narrows, but does not eliminate" the shift. R5: under no-nudge, "upstanding
   researcher" and "significance" prompts "both models produce accurate and remarkably stable estimates"
   and refuse ("this is asking me to engage in p-hacking", Section 3.2), with a median of one
   specification per run; under the "nuclear" prompt that "reframes specification search as uncertainty
   reporting" the median Thompson run had 13 (Claude) and 16 (Codex) specifications (Section 3.3). One run
   moved a -0.06 published estimate to -0.194 (p < 0.001). Inflation tracked flexibility: "observational
   studies are more vulnerable than randomized experiments" (Abstract). So the guardrail stops a blunt
   request, not a reworded one.
4. **The agent's bias sits in the verdict, so pre-commit the decision rule.** R2: a confirmatory prompt
   "flips Claude Code's verdicts from 10% to 90% support while leaving its coefficient distribution
   essentially unchanged, operating through rule omission rather than rule softening" (Abstract); Claude
   Code's plans containing an explicit decision rule fell from 11 of 20 to 8 of 20, and "12 of the 20 CC
   Confirmatory plans omit an explicit verdict criterion altogether" (Results, Fig. 5). That is the
   mechanism a `PREREG.md` closes: the rule that turns estimates into a claim is written, and committed,
   before the runs.
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
  R5 is a self-hosted working paper; none is peer reviewed yet. Rewolinski (R4) is internally inconsistent
  on its headline (the Introduction says the checks "reveal one case", the Abstract says 6 of 11), so we cite the abstract and
  Section 4.3, which lists 5 datasets as passing both checks.
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
