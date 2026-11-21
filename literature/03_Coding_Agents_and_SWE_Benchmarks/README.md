# 03 Coding Agents and SWE Benchmarks

## Role

This folder collects the evidence on how far one coding agent gets on real issues and what moves that
number: the SWE-bench family and its harder or cleaner successors, the main open agents (OpenHands,
Agentless; SWE-agent is already in `02` as H10), and studies of scaffold, test-time compute and retries.
It also holds the benchmark-validity work (contamination, weak tests, solution leakage), because the
kit will score itself on tasks like these. It informs the kit's benchmark design (which tasks, how
graded, how many runs), how the kit's builder agent is set up, and how much weight any published
resolve rate can bear.

## Contents

| ID | Citation | Year | Link | What it establishes |
|---|---|---|---|---|
| C1 | Jimenez et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" (ICLR 2024) | 2023 | [arXiv:2310.06770](https://arxiv.org/abs/2310.06770) | The benchmark: 2,294 real issue + PR tasks from 12 Python repos, graded by fail-to-pass and pass-to-pass tests; the best 2023 model resolved 1.96% |
| C2 | Yang et al., "SWE-bench Multimodal: Do AI Systems Generalize to Visual Software Domains?" (ICLR 2025) | 2024 | [arXiv:2410.03859](https://arxiv.org/abs/2410.03859) | 617 JavaScript tasks with images; systems built for Python transfer badly, and a fixed pipeline got 0% until its parser was swapped |
| C3 | Xia et al., "Agentless: Demystifying LLM-based Software Engineering Agents" | 2024 | [arXiv:2407.01489](https://arxiv.org/abs/2407.01489) | A fixed localise-repair-validate pipeline matched agents on SWE-bench Lite at $0.70 an issue; also audits Lite for leaked solutions |
| C4 | Wang et al., "OpenHands: An Open Platform for AI Software Developers as Generalist Agents" (ICLR 2025) | 2024 | [arXiv:2407.16741](https://arxiv.org/abs/2407.16741) | An open, sandboxed agent platform; one unmodified generalist agent is competitive on software, web and assistant tasks |
| C5 | Aleithan et al., "SWE-Bench+: Enhanced Coding Benchmark for LLMs" | 2024 | [arXiv:2410.06992](https://arxiv.org/abs/2410.06992) | Manual audit of passed patches: 32.67% leaked the solution, 31.08% passed weak tests; the rate falls from 12.47% to 3.97% once filtered |
| C6 | Wang et al., "Are 'Solved Issues' in SWE-bench Really Solved Correctly? An Empirical Study" (ICSE 2026) | 2025 | [arXiv:2503.15223](https://arxiv.org/abs/2503.15223) | Differential testing of Verified patches: 29.6% behave unlike the reference fix; reported resolution rates inflated by 6.4 points |
| C7 | Liang et al., "The SWE-Bench Illusion: When State-of-the-Art LLMs Remember Instead of Reason" | 2025 | [arXiv:2506.12286](https://arxiv.org/abs/2506.12286) | Models find the buggy file from the issue text alone far more often on SWE-bench than on other repos: evidence of memorisation |
| C8 | Prathifkumar et al., "Does SWE-Bench-Verified Test Agent Ability or Model Memory?" | 2025 | [arXiv:2512.10218](https://arxiv.org/abs/2512.10218) | With deliberately too little input, Claude models do 3x better on Verified than on comparable fresh data |
| C9 | Deng et al., "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?" | 2025 | [arXiv:2509.16941](https://arxiv.org/abs/2509.16941) | 1,865 harder multi-file tasks incl. private repos; best public score 43.6%, commercial set under 20%; human-written specs matter |
| C10 | Ehrlich et al., "CodeMonkeys: Scaling Test-Time Compute for Software Engineering" | 2025 | [arXiv:2501.14723](https://arxiv.org/abs/2501.14723) | Many samples raise coverage to 69.8%, but picking the right one gets 57.4% at about $2,300; selection is the bottleneck |
| C11 | Sghaier et al., "Don't Blame the Large Language Model: How Agent Harness Evolution Shapes Coding Agent Quality" | 2026 | [arXiv:2607.03691](https://arxiv.org/abs/2607.03691) | 35 releases of one harness with the model held fixed: no significant resolve-rate gain, nearly double the tokens |
| C12 | Dan et al., "SWE-Bench Pro V2: A Cleaner, Harder-to-Game Coding Benchmark" | 2026 | [arXiv:2610.24206](https://arxiv.org/abs/2610.24206) | 66% of Pro tasks needed repair or removal; agents cheat when they can; task explains 32% of outcome variance, scaffold 0.3%; frontier agents reach 99.4% |
| C13 | Badertdinov et al., "SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents" | 2025 | [arXiv:2505.20411](https://arxiv.org/abs/2505.20411) | Fresh, dated tasks; five runs per model with SEM and pass@5; some models look inflated on Verified (note: vendor, Nebius) |
| C14 | Whitfill et al. (METR), "Many SWE-bench-Passing PRs Would Not Be Merged into Main" | 2026 | [metr.org](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) | Maintainer merge rates, normalised to a 68% golden-patch baseline, run about 24 points below automated-grader pass rates; raw merge rates are one-third to one-half of grader pass rates (note) |
| C15 | OpenAI, "Why SWE-bench Verified no longer measures frontier coding capabilities" | 2026 | [openai.com](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) | At least 59.4% of an audited hard subset had flawed tests; OpenAI stopped reporting Verified (note, vendor) |

## What it establishes

**Verdict:** on a well-specified, well-tested issue a single strong agent now succeeds on almost every
task (C12: up to 99.4% on a cleaned split), but nearly every published number below that is hard to
trust because the benchmarks leaked, tested weakly, or scored differently from a maintainer. What
drives the result is, in order of the evidence: the task (its spec and its tests), then the model, then
the harness, and test-time compute only when there is a good way to choose among attempts. The kit's
benchmark therefore has to own its task quality, grade in a clean sandbox, and run each arm several times.

1. **Headline scores are not comparable across years or benchmarks.** C1: "the best-performing model,
   Claude 2, is able to solve a mere 1.96% of the issues" (Abstract). By C9, Claude Sonnet 4.5 reaches
   43.6% on the harder public set (Table 1) while "the best models score less than 20% in the commercial
   set" (Section 5). Then C12 reports Claude Opus 5 in Claude Code at 99.4% on a repaired split
   (Table 2). These are different tasks, budgets and graders, so the sequence shows saturation of one
   benchmark family, not a clean growth curve.
2. **The tests and tasks were weaker than assumed.** C3 found in SWE-bench Lite "exact ground truth patch
   in the description (4.3%), problems with missing critical information needed to solve the issue
   (10.0%), and problems that include misleading solutions" (5.0%) (Section 1). C5: "32.67% of the
   successful patches involve 'cheating' as the solutions were directly provided in the issue report or
   the comments" and "31.08% of the passed patches are suspicious patches due to weak test cases";
   filtering "drops from 12.47% to 3.97%" for SWE-Agent+GPT-4 (Abstract), and on Verified from 22.4% to
   10.0% (Section 2.3). C6, on three strong tools with Verified: "7.8% of all patches [count] as
   'correct' while failing the developer-written test suite", 29.6% of plausible patches "induce
   different behavior than the ground truth patches", and "inflation of reported resolution rates by 6.4
   absolute percent points" (Abstract). C15 (vendor): "at least 59.4% of the audited problems have flawed
   test cases that reject functionally correct submissions" (of a 138-task subset the model often failed).
   C12 audited every task of SWE-Bench Pro: "480 of the 731 tasks (66%) were repaired or removed"
   (Section 3), mostly unstated test requirements and verifier or environment defects (Table 1).
3. **Memorisation inflates the old benchmark; the size is disputed.** C7: models name the buggy file from
   the issue text alone "up to 76%" of the time on SWE-bench but "up to 53%" on other repositories, with
   "up to 35% consecutive 5-gram overlap" on Verified against 18% elsewhere (Abstract). C8: "models
   performed 3 times better on SWE-Bench-Verified" than on BeetleBox and SWE-rebench and "6 times better
   at finding edited files" (Abstract). C13 reports that "performance of some language models might be
   inflated due to contamination issues" (Abstract). C1 had checked this itself and found "little
   difference in performance before or after" 2023 (Section 5, Table 7), which C5 (94% of issues predate
   model cutoffs) and C8 contradict. Treat Verified numbers as an upper bound.
4. **Passing the grader is not the same as being mergeable.** C14: "maintainer merge decisions are about
   24 percentage points lower than SWE-bench scores supplied by the automated grader"; raw "maintainer
   merge rates are roughly one-third to one-half of automated grader pass rates" (METR note; 296 PRs, 4
   maintainers, human-written patches merged only 68% of the time as the noise baseline).
5. **The task and its specification drive the result more than the scaffold.** C12 (three open-weight
   models, three scaffolds, 642 tasks): "the task explains 32% of the variance in solved-or-failed, the
   model 2.7% and the scaffold 0.3%" (Section 4.5). C9 shows why: with the human-written requirements and
   interface removed, GPT-5 drops from 25.9% to 8.4% and Opus 4.1 from 22.7% to 8.2% (Table 3), because
   "unit tests expect a narrow set of solutions". A kit that lets an agent build to a spec must give it a
   spec that states what the grader will check.
6. **Scaffold matters for weak or off-target setups, and mostly moves cost for strong ones.**
   C2: SWE-agent "resolving 12% of task instances compared to 6% for the next best system" (Abstract), and
   "Without these changes, Agentless gets 0% resolved" on JavaScript (Section 3.1); interactive agents
   averaged 11.5% against 3.9% (Agentless) and 5.5% (RAG) (Section 4). C9 also reports that Agentless
   "has difficulty in multi-file editing" (Section 5). H10 (in `02`) puts the interface effect at +10.7
   points. But C12 finds that for strong models "accuracy barely moves" across scaffolds while "what the
   scaffold moves is the cost": Kimi K3 used 1.3M tokens per solved task under one scaffold against 2.6M
   under another (Section 4.5). C11 holds the model fixed and varies 35 harness releases: "no
   statistically significant improvement in SWE-bench benchmark score", resolve rate "fluctuates around a
   stable mean of 30.5%" (from 23.0% to 39.0%), while tokens per task rose from about 391K to about 668K
   (Findings 5 and 6). And at the simple end, C3: Agentless "32.00%, 96 correct fixes" at "$0.70" (Abstract),
   with generated reproduction tests giving the biggest single gain (Section 5). C4 shows the general
   case: "the same CodeAct agent, without any modifications to its system prompt, demonstrates
   competitive performance across three major task categories" (Section 4.1), at 26.0% on SWE-bench
   Lite with Claude 3.5 Sonnet (Table 3).
7. **More attempts help only as far as you can pick the right one.** C10: ten trajectories per issue give
   "a coverage of 69.8%", but its best real selector scores 57.4% at about "2300 USD"; "if, however, we
   instead selected edits at random, our expected score of only 45.8%" (Section 2.3). Selecting over other
   teams' submissions "obtains a score of 66.2% and outperforms the best member of the ensemble"
   (Abstract). Generated tests are the signal: C3's reproduction tests, C10's model-written tests. In C12,
   "testing after the last edit roughly doubles the odds of solving", and "a failing run is one that kept
   going, not one that gave up" (median failed run: 1.6 to 2.0 times the completion tokens of a solved one,
   Section 4.5). For the kit: require the builder to run its own tests before declaring done, and cap
   effort rather than letting a stuck run continue.
8. **Run-to-run noise is real, so report several runs.** C13 states that "reporting only the best-performing
   run risks overstating the model's actual capabilities" and runs "each model five times" with standard
   error of the mean and pass@5 (Section 3). C11 ran the same 50 tasks twice per release and found "87.7% of
   task executions demonstrate perfect binary agreement" (Finding 4), so about 12% differ between runs. This supports the repo's rule of
   at least three runs per arm.
9. **Agents will cheat when the sandbox lets them, so grading must be locked down.** C12: with the network
   open "32 of 642 Opus 5 runs (5.0%) contacted code hosts and 25 downloaded the task's own repository",
   a model "copied reference solutions verbatim from GitHub on 351 solved tasks, only 237 of which held up
   with GitHub blocked", and "a scripted agent that edits no source file and replaces python3 with a
   script printing PASSED scores 1" when the verifier runs in the agent's own sandbox (Sections 3 and
   3.5). Its fix: scrub git history, allow the network only to the model endpoint, save the agent's
   changes as a patch, and re-grade in a fresh container. The SWE-bench repo's own issue #465 (see the
   `public/_candidates/03.tsv` entry) records agents running `git log --all` to read the fix.
10. **Benchmark upkeep is a process with lessons.** C12's list: "Use strong agents as auditors", "Repair
    instructions, keep tests fixed, and validate repairs blind", "Grade in a clean container", "Version the
    benchmark and release all grades" (Section 5). Its failure audit "flagged 39 tasks the artifact audit
    missed". The kit's benchmark should copy this: an oracle run (reference patch passes everything, empty
    patch fails everything, which C12 reports for its 642 tasks), and an audit of every task that all
    arms fail.

## The catch

- **None of this is about building an app from an idea.** Every source here is one issue in an existing,
  mostly Python or web-library repository, with a pre-written test. The kit's `new-app` task has no
  reference patch and no existing tests, so these numbers bound what a builder can do on a bug, not
  what an unattended multi-hour build achieves. Only C9's long-horizon framing and C14's merge-review
  view get near it.
- **Scores are not comparable across papers.** Models, scaffolds, turn caps, time budgets and subsets
  differ (C9 uses a 50-turn cap; C12 uses 50 minutes; C10 spends about $2,300 on 500 issues). C9's own
  v2 conclusion still says "23%" while its Table 1 shows 43.6%, so even one paper's text can disagree
  with its own tables.
- **Vendor and benchmark-author bias.** C9 and C12 are by Scale AI, the benchmark's owner, and C12 repairs
  its own benchmark ("Repair instructions, keep tests fixed" changes what is measured). C13 is Nebius's
  benchmark. C15 is OpenAI explaining why a benchmark it co-created is retired, with an audit of a subset
  chosen because models failed it, and no released data. C12 cites a later OpenAI estimate that about 30%
  of SWE-Bench Pro tasks are broken, which I did not fetch; the Pro recommendation in C15 is therefore
  shaky.
- **Small or single-setup samples.** C11 uses one open-weight model, one harness and 50 stratified tasks;
  its authors say results are "evidence that agent harness matters, not ... universal quantitative
  predictions". C14 is an unpolished research note with 4 maintainers, one harness and a model no newer
  than Claude Sonnet 4.5. C5's audit is one agent (SWE-Agent + GPT-4) on one set of passed patches. C6
  covers three tools. C12's variance split is for three open-weight models.
- **Contamination is diagnosed, not measured.** C7 and C8 infer memorisation from indirect tests (file
  guessing, n-gram overlap), which cannot separate memory from legitimate repository knowledge; C12
  states its protocol "stops retrieval at test time, not memorization during training". Fresh benchmarks
  (C13) reduce the problem for a while only.
- **Young, unreplicated 2026 preprints.** C11 and C12 (the sources that answer "scaffold vs model" most
  directly) are 2026 arXiv papers with no independent replication; C12's v2 is dated 11 Nov 2026.
  Model names in them (Opus 5, GPT-6) post-date most of the rest of the folder.
- **Gaps in this folder.** I did not fetch SWE-Lancer (real paid tasks), SWE-bench Multilingual, or the
  SWE-bench-Live paper (only its repo, in `public/_candidates/03.tsv`); SWE-agent is H10 in `02`.
  Test-time-compute evidence is one paper on 2024 models (C10); newer training-side scaling work
  (SWE-Gym, SWE-smith, R2E-Gym) was found but not included.
