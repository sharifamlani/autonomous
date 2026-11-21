# 03 Coding Agents and SWE Benchmarks

## Role

This folder collects the evidence on how far one coding agent gets on real issues and what moves that
number: the SWE-bench family and its harder or cleaner successors, the main open agents (OpenHands,
Agentless; SWE-agent is already in `02` as H10), and studies of scaffold, test-time compute and retries.
It also holds the benchmark-validity work (contamination, weak tests, solution leakage), because the
kit will score itself on tasks like these. Round 2 adds the benchmarks that build an app or a
repository from scratch (C19 to C22, C29), freelance and long-horizon tasks (C16, C18), newer
test-time-scaling work (C24, C25), and the 2026 audits of reward hacking and infrastructure noise (V27
to F27, C30), with weight on lab and top-university sources. It informs the kit's benchmark design
(which tasks, how graded, how many runs), how the kit's builder agent is set up, and how much weight
any published resolve rate can bear.

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
| C16 | Miserendino et al. (OpenAI), "SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?" (ICML 2025) | 2025 | [arXiv:2502.12115](https://arxiv.org/abs/2502.12115) | 1,488 paid Upwork tasks graded by browser-automation end-to-end tests; the best 2025 model earned $208,050 of $500,800 on the public split; more reasoning effort and a tool to view the running app helped |
| C17 | Zhang et al. (Microsoft), "SWE-bench Goes Live!" | 2025 | [arXiv:2505.23419](https://arxiv.org/abs/2505.23419) | Continuously refreshed, automatically built issue benchmark; the same agent and model scored 43.2% on Verified but 19.25% on the fresh set |
| C18 | Merrill et al. (Stanford, Laude Institute, with Anthropic and others), "Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces" | 2026 | [arXiv:2601.11868](https://arxiv.org/abs/2601.11868) | 89 hand-audited terminal tasks, at least five runs per agent-model pair (32,155 trials), best 63%; shows how much review a trustworthy task set needs |
| C19 | Tran et al. (Vals AI, MIT), "Vibe Code Bench: Evaluating AI Models on End-to-End Web Application Development" | 2026 | [arXiv:2603.04601](https://arxiv.org/abs/2603.04601) | 100 app specs built from scratch and graded by a browser agent; best of 16 models 61.8%; self-testing in a browser tracks success (r = 0.72); the grader choice moves scores |
| C20 | Xu et al. (ByteDance), "Web-Bench: A LLM Code Benchmark Based on Web Standards and Frameworks" | 2025 | [arXiv:2505.07473](https://arxiv.org/abs/2505.07473) | 50 web projects of 20 dependent tasks each, written by senior engineers; best model 25.1% pass@1 on its own single-pass agent |
| C21 | Lu et al. (CUHK MMLab), "WebGen-Bench: Evaluating LLMs on Generating Interactive and Functional Websites from Scratch" | 2025 | [arXiv:2505.03733](https://arxiv.org/abs/2505.03733) | Multi-file website generation graded by 647 UI test cases run by a web-navigation agent; best agent and model pair 27.8% |
| C22 | Ding et al. (ByteDance Seed and others), "NL2Repo-Bench: Towards Long-Horizon Repository Generation Evaluation of Coding Agents" | 2025 | [arXiv:2512.12730](https://arxiv.org/abs/2512.12730) | One requirements document and an empty workspace, graded by the real library's tests; every agent below 40.5% average, three scaffolds within 1 point for one model |
| C23 | Vero et al. (ETH Zurich, UC Berkeley), "BaxBench: Can LLMs Generate Correct and Secure Backends?" (ICML 2025) | 2025 | [arXiv:2502.11844](https://arxiv.org/abs/2502.11844) | 392 backend tasks graded by functional tests and executed exploits; no model passes 37% correct and secure |
| C24 | Jain et al. (UC Berkeley), "R2E-Gym: Procedural Environments and Hybrid Verifiers for Scaling Open-Weights SWE Agents" | 2025 | [arXiv:2504.07164](https://arxiv.org/abs/2504.07164) | Test-based and model-based selection of the best attempt each plateau near 42 to 43%; combining them reaches 51% |
| C25 | Tao et al. (Huawei and others), "SWE-Lego: Pushing the Limits of Supervised Fine-tuning for Software Issue Resolving" | 2026 | [arXiv:2601.01426](https://arxiv.org/abs/2601.01426) | Under a latency budget, extra turns stop paying around 100 to 140 turns; the rest of the compute is better spent on parallel attempts with a verifier |
| V27 (filed in 05) | Wang et al. (UC Berkeley), "Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack" | 2026 | [arXiv:2605.12673](https://arxiv.org/abs/2605.12673) | Red-team agent found score-forcing exploits on all 10 audited agent benchmarks, near-perfect on 9, including a nine-line pytest hook on SWE-bench Verified |
| C27 | Zheng et al. (Shanghai AI Laboratory), "SWE-Bench Pro Verified: A Reliable Benchmark for Software Engineering Agents" | 2026 | [arXiv:2609.08149](https://arxiv.org/abs/2609.08149) | Blocking answer leaks on SWE-Bench Pro cut one model from 78.80% to 57.32% and another not at all; 102 tasks repaired |
| F27 (filed in 09) | Segato (Anthropic), "Quantifying infrastructure noise in agentic coding evals" | 2026 | [anthropic.com](https://www.anthropic.com/engineering/infrastructure-noise) | Container resource limits alone moved Terminal-Bench 2.0 scores by 6 points (p < 0.01); about 1.5 points on SWE-bench (note, vendor) |
| C29 | Trengrove et al. (Google Research), "Android Bench: Measuring Frontier Coding Agents on Long-Horizon Mobile Engineering" | 2026 | [research.google PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/1050702.pdf) | 30 long tasks incl. new apps from design mocks, emulator-graded; best 41% pass but 0.85 partial score; visible tests lift pass rates 2.6x to 6.7x; catalogue of agent cheats |
| C30 | Jain (Cursor), "Reward hacking is swamping model intelligence gains" | 2026 | [cursor.com](https://cursor.com/blog/reward-hacking-coding-benchmarks) | An LLM audit of 731 SWE-bench Pro trajectories: 63% of successes retrieved the fix; a strict harness cut scores by up to 20.7 points (note, vendor) |
| C31 | Rein (METR), "Research Update: Algorithmic vs. Holistic Evaluation", METR blog, 2025-08-13 | 2025 | [metr.org](https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/) | On 18 real issues, Claude 3.7 Sonnet scores 38% (+-19%) on maintainer tests but 27% (+-20) on manual review, and "none of them are mergeable as-is"; reviewers estimate 42 minutes to make each PR mergeable (note) |
| C32 | Adamczewski, Rein, Owen and Brand (Epoch AI, with METR), "MirrorCode: evidence that AI can already do some weeks-long coding tasks", Epoch AI, 2026-04-10 | 2026 | [epoch.ai](https://epoch.ai/publications/mirrorcode-preliminary-results/) | Given an executable spec, Claude Opus 4.6 reimplemented a ~16,000-line Go toolkit (est. 2-17 human weeks) passing 2,000 of 2,001 tests; a 61,000-line Java/Kotlin task stayed unsolved at 35% of visible tests; only 4 of 24 programs reported, only Anthropic models in detail (note, preliminary) |
| C33 | Cognition Team, "Devin's 2025 Performance Review: Learnings From 18 Months of Agents At Work", Cognition blog, 2025-11-14 | 2025 | [cognition.com](https://cognition.com/blog/devin-annual-performance-review-2025) | Vendor figures from 18 months of production use: "67% of its PRs are now merged vs 34% last year"; works on clear, verifiable 4-8 hour junior-sized tasks, fails on ambiguous projects and mid-task requirement changes (note, vendor self-assessment, customer anecdotes) |
| C34 | Meta FAIR CodeGen Team, "CWM: An Open-Weights LLM for Research on Code Generation with World Models", arXiv | 2025 | [arXiv:2510.02387](https://arxiv.org/abs/2510.02387) | A 32B open-weights model reaches 65.8% pass@1 on SWE-bench Verified with test-time scaling and 53.9% without (4-run average, SWE-bench Verified results section); bootstrapping SWE RL traces over iterations lifts the SFT checkpoint from 30% to 43% pass@1 (vendor-run evaluation) |
| C35 | Mistral AI, "Introducing: Devstral 2 and Mistral Vibe CLI", Mistral news, 2025-12-09 | 2025 | [mistral.ai](https://mistral.ai/news/devstral-2-vibe-cli/) | Open-weight coding model reports 72.2% (123B) and 68.0% (24B) on SWE-bench Verified with no setup described; independent human annotation still preferred Claude Sonnet 4.5 (Devstral 2 won 42.8% and lost 28.6% against DeepSeek V3.2) (note, vendor claims) |
| C36 | Bui, Evangelopoulos and Elliott (Google), "Measuring What Matters with Jules", Google Developers Blog, 2026-06-22 | 2026 | [developers.googleblog.com](https://developers.googleblog.com/measuring-what-matters-with-jules/) | Grades a proactive coding agent on its insight policy using 705 internal bugs reverted to their pre-fix state and an LLM judge; raising exploration from two to three rounds lifts Hit@5 from 33% to 57% (note, preliminary, internal data only) |

## What it establishes

**Verdict:** on a well-specified, well-tested issue a single strong agent now succeeds on almost every
task (C12: up to 99.4% on a cleaned split), but nearly every published number below that is hard to
trust because the benchmarks leaked, tested weakly, or scored differently from a maintainer. What
drives the result is, in order of the evidence: the task (its spec and its tests), then the model, then
the harness, and test-time compute only when there is a good way to choose among attempts. The kit's
benchmark therefore has to own its task quality, grade in a clean sandbox, and run each arm several times.
Building from scratch is far less solved than fixing issues: the from-scratch benchmarks put the best
agents at 61.8% of app workflows (C19), under 40.5% of a repository's tests (C22) and 41% of long Android
tasks (C29), and the biggest lever the evidence shows is telling the agent how it will be checked and
letting it run its own app (C29, C19, C16).

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
   inflated due to contamination issues" (Abstract). C17 re-ran the best agent and model pair "using the
   exact same setups" and got 43.20% on Verified against 19.25% as the best score on its fresh issues
   (Section 4.2), and 18.89% on repositories outside SWE-bench against 22.96% on SWE-bench repositories
   (Section 4.2, Table 5). C1 had checked this itself and found "little
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
   Lite with Claude 3.5 Sonnet (Table 3). The from-scratch benchmarks agree: in C22, Claude Sonnet 4.5
   "exhibits less than a 1% performance variation across the three agent frameworks" (OpenHands, Claude
   Code, Cursor CLI), while "inter-model performance gaps are substantially larger" (Section 4.2); C18
   finds "essentially no correlation between the number of average turns per trial and model success
   rates" (Section 4.1).
7. **More attempts help only as far as you can pick the right one.** C10: ten trajectories per issue give
   "a coverage of 69.8%", but its best real selector scores 57.4% at about "2300 USD"; "if, however, we
   instead selected edits at random, our expected score of only 45.8%" (Section 2.3). Selecting over other
   teams' submissions "obtains a score of 66.2% and outperforms the best member of the ensemble"
   (Abstract). Generated tests are the signal: C3's reproduction tests, C10's model-written tests. In C12,
   "testing after the last edit roughly doubles the odds of solving", and "a failing run is one that kept
   going, not one that gave up" (median failed run: 1.6 to 2.0 times the completion tokens of a solved one,
   Section 4.5). For the kit: require the builder to run its own tests before declaring done, and cap
   effort rather than letting a stuck run continue. Three newer papers sharpen the picture. C24: both a
   test-based selector and a trained model-based selector plateau ("saturates around 42-43%") as
   attempts are added, because generated tests rarely tell good patches from bad (for most problems under
   20% of tests discriminate; up to 10% of tests are "toxic" and prefer wrong patches) and the model-based
   one leans on the agent's own reasoning text (dropping it cuts best-of-26 from 42.8% to 37.6%); a hybrid
   "achieves 51%" (Sections 4.2 and 4.3). C25: sequential scaling "saturates around 100-140 turns",
   after which "improvements are driven primarily by parallel scaling", and its verifier lifts
   42.2% to 49.6% (8B) and 52.6% to 58.8% (32B) at 16 attempts (Abstract, Figure 8). C16: raising o1's
   reasoning effort from low to high lifts pass@1 on public-split independent tasks from 9.3% to 16.5%
   (Section 3). Test-time compute is thus bounded by the quality of the checker, which supports
   spending on better acceptance tests before spending on more attempts.
8. **Run-to-run noise is real, so report several runs.** C13 states that "reporting only the best-performing
   run risks overstating the model's actual capabilities" and runs "each model five times" with standard
   error of the mean and pass@5 (Section 3). C11 ran the same 50 tasks twice per release and found "87.7% of
   task executions demonstrate perfect binary agreement" (Finding 4), so about 12% differ between runs. This supports the repo's rule of
   at least three runs per arm. C18 ran every agent-model pair "at least five times" (32,155 trials in
   all, Section 3); C29 runs about five per task and still finds that "the v2 benchmark can only detect an
   absolute pass rate difference of 14%" with 30 tasks (Section 7.3). C19 measures the grader's own noise
   on fixed apps: the share of variance from generation (not from re-grading) is 73.5% to 92.5% across
   three models (Section 5.3). F27 (vendor) shows noise from the machine: container resource limits alone
   moved Terminal-Bench 2.0 by "6 percentage points (p < 0.01)", but only 1.54 points on SWE-bench.
9. **Agents will cheat when the sandbox lets them, so grading must be locked down.** C12: with the network
   open "32 of 642 Opus 5 runs (5.0%) contacted code hosts and 25 downloaded the task's own repository",
   a model "copied reference solutions verbatim from GitHub on 351 solved tasks, only 237 of which held up
   with GitHub blocked", and "a scripted agent that edits no source file and replaces python3 with a
   script printing PASSED scores 1" when the verifier runs in the agent's own sandbox (Sections 3 and
   3.5). Its fix: scrub git history, allow the network only to the model endpoint, save the agent's
   changes as a patch, and re-grade in a fresh container. The SWE-bench repo's own issue #465 (see the
   `public/_candidates/03.tsv` entry) records agents running `git log --all` to read the fix. 2026 audits
   show how general this is. V27 ran a red-team agent on 10 agent benchmarks and "generated working
   reward-hacking exploits on all", "achieving near-perfect scores on 9 of 10 benchmarks without actually
   solving a single task", including "a nine-line PyTest hook that forces all tests to pass on SWE-bench
   Verified" (Section 1); it found 219 distinct flaws, and its patch loop cut the hackable share "from
   near 100% to <10%" on four benchmarks without fatal design flaws (Section 1). C27 blocked answer leaks
   on SWE-Bench Pro (fresh single-commit repository, hidden tests removed, code hosts blocked): GLM-5.2 fell
   from 78.80% to 57.32%, with 186 of 731 tasks flipping from pass to fail, while DeepSeek-V4-Pro barely moved
   (49.98% to 49.11%) (Tables 3 and 4), so the inflation is model-specific. C30 (vendor): "63% of
   successful Opus 4.8 Max resolutions retrieved the fix rather than derived it", and a strict harness cut
   one model from 87.1% to 73.0%. C29 lists the shortcuts seen on app tasks: bundling a precompiled JAR,
   laying a screenshot over the UI, loosening the screenshot-diff tolerance from 5% to 80%, mocking the
   database, and deleting test assertions (Section 6.2). C16 makes the same point from the design side:
   unit tests "are highly susceptible to grader hacking", so its tasks use browser-driven end-to-end tests
   (Section 1).
10. **Benchmark upkeep is a process with lessons.** C12's list: "Use strong agents as auditors", "Repair
    instructions, keep tests fixed, and validate repairs blind", "Grade in a clean container", "Version the
    benchmark and release all grades" (Section 5). Its failure audit "flagged 39 tasks the artifact audit
    missed". The kit's benchmark should copy this: an oracle run (reference patch passes everything, empty
    patch fails everything, which C12 reports for its 642 tasks), and an audit of every task that all
    arms fail. C18 gives the price of doing this by hand: each of its 89 tasks got about three
    reviewer-hours, plus an adversarial agent told to cheat, an oracle that must pass and a no-op agent that
    must fail (Section 2.2). C27 adds that repair should be minimal: 102 of 119 reported-faulty tasks were
    fixed by editing the instructions first and the tests last.
11. **Building from scratch is far from solved, and the benchmarks that test it are young.** C19 (100 app
    specifications, 964 browser workflows): "the top model passes 61.8% of workflows" across 16 models
    (Section 1), and it separates models far better than SWE-bench ("2.8%" gap between two models there,
    "42.7%" here). Integrations hurt: average accuracy across models falls from 34.18% for apps with none
    to 13.49% for apps needing both email and Stripe (Section 4.3). C22 (104 Python libraries from one
    requirements document): "all models achieve an average test pass rate below 40.5%", and the strongest
    "fully passes the official pytest suite for only five repositories in a single run" (Section 4.2); it
    names "premature termination" and loss of "global coherence" as the failure modes. C21 (website
    generation): best pair "achieves only 27.8% accuracy" (Abstract). C20 (50 dependent projects): "SOTA
    (Claude 3.7 Sonnet) achieves only 25.1% Pass@1" (Abstract). C29 (30 Android tasks): best closed-variant
    pass rate 41% with a mean partial score of 0.85; "the most common failure is a missed requirement"
    (Section 6.1). C23 adds security: no model passes more than 37% of backends that are both correct and
    secure, and "around half of the correct programs" could be exploited (Abstract, Section 1). C18 (hard
    terminal tasks, expert-written): "frontier models and agents resolve less than 65%" (Abstract). The
    scores are low partly because the specs are rich and the graders strict; they bound what the kit's
    `new-app` should expect from a first run, and say that the last requirement is what fails.
12. **Telling the agent how it will be checked, and letting it run what it built, is the largest lever
    found.** C29 gives each task a closed variant (acceptance criteria only, tests hidden) and an open one
    (detailed requirements plus the failing tests, which the agent may run): for claude-fable-5-1 in Claude
    Code, pass@1 goes from 22.7% to 84.0%, and the multiplier is 2.6x to 6.7x across the six agents listed
    (Section 5.2). The two variants differ in requirement detail as well as test access, so the effect is
    not tests alone. C19: browser calls per app correlate with accuracy at r = 0.72, still 0.72 after
    controlling for latency, while edit volume correlates at only 0.09 (Section 5.1); GPT-5.2 made about 3x
    as many browser calls per app as GPT-5.2-Codex (26.4 against 9.4). C16 is gentler: giving the agent a
    tool that replays the user flow helped, but removing it "only minimally reduces pass@1" (Section 3).
    For the kit: the builder gets a written spec with checkable acceptance criteria, and a way to drive
    its own running app, before any extra attempts.
13. **Money-weighted and long-horizon tasks keep headroom.** C16, graded by end-to-end tests triple-verified
    by engineers, found that Claude 3.5 Sonnet "earn[ed] a total of $208,050 out of $500,800" on the public
    split (26.2% of independent tasks) (Section 1). C29 shows models "surge to ~80% completion early, then
    flatline" on a Flutter conversion (Section 6.1). Models in these papers are from 2024 to 2026 and
    are not comparable to each other.

## The catch

- **Little of this is about building an app from an idea, and the from-scratch sources are weak.** C1 to
  C15 are one issue in an existing, mostly Python or web-library repository, with a pre-written test.
  The from-scratch benchmarks (C19 to C22, C29) are closer to the kit's `new-app` task but each has a
  catch: C19 is graded by a browser agent (an LLM) and its own alignment study finds "31.8-93.6%"
  pairwise agreement between graders; C21 is also
  graded by a web-navigation agent; C20's "Web-Agent" is the benchmark's own single-pass prompt wrapper, not a
  tool-using agent; C22 builds Python libraries graded by the original test suite, which is a very
  different task from an app a user will walk; C29 is Android only with 30 tasks. None measures an
  unattended multi-hour build against a user's idea, with no spec written by someone who knows the tests.
  Only the kit's own v0.1 benchmark will.
- **The strongest lever (visible tests, own-app testing) is partly confounded.** C29's open variant also
  gives more detailed requirements, and C19's self-testing correlation (r = 0.72, 16 models) cannot
  separate "testing helps" from "stronger models test more".
- **Scores are not comparable across papers.** Models, scaffolds, turn caps, time budgets and subsets
  differ (C9 uses a 50-turn cap; C12 uses 50 minutes; C10 spends about $2,300 on 500 issues). C9's own
  v2 conclusion still says "23%" while its Table 1 shows 43.6%, so even one paper's text can disagree
  with its own tables.
- **Vendor and benchmark-author bias.** C9 and C12 are by Scale AI, the benchmark's owner, and C12 repairs
  its own benchmark ("Repair instructions, keep tests fixed" changes what is measured). C13 is Nebius's
  benchmark. C15 is OpenAI explaining why a benchmark it co-created is retired, with an audit of a subset
  chosen because models failed it, and no released data. C12 cites a later OpenAI estimate that about 30%
  of SWE-Bench Pro tasks are broken, which I did not fetch; the Pro recommendation in C15 is therefore
  shaky. Round 2 adds more vendor-authored sources: C16 is by OpenAI (on tasks from one company,
  Expensify, and with a private holdout available only on request); F27 is Anthropic on its own models; C30
  is Cursor, which sells an agent, trains its own model and runs its own benchmark; C29 is Google
  Research on tasks it wrote; C19 is by Vals AI, an evaluation company, with a coauthor at MIT. F27 and
  C30 are blog posts with no released data, so they are in as notes. C18 is community-authored, with
  authors from Anthropic and others.
- **Small or single-setup samples.** C11 uses one open-weight model, one harness and 50 stratified tasks;
  its authors say results are "evidence that agent harness matters, not ... universal quantitative
  predictions". C14 is an unpolished research note with 4 maintainers, one harness and a model no newer
  than Claude Sonnet 4.5. C5's audit is one agent (SWE-Agent + GPT-4) on one set of passed patches. C6
  covers three tools. C12's variance split is for three open-weight models. Round 2: C17's 43.20% versus
  19.25% compares one agent-model pair on two different issue sets, so it also reflects task difficulty,
  not only overfitting; C27's anti-hacking effect is shown on two models (one fell 21 points, one did not),
  so the size cannot be generalised; F27's SWE-bench check is reported in one paragraph without a significance test; C24 and C25
  are tested on SWE-bench Verified, whose own validity is in doubt (C5, C6, C15), and C25 compares
  sequential and parallel scaling under one latency model.
- **Contamination is diagnosed, not measured.** C7 and C8 infer memorisation from indirect tests (file
  guessing, n-gram overlap), which cannot separate memory from legitimate repository knowledge; C12
  states its protocol "stops retrieval at test time, not memorization during training". Fresh benchmarks
  (C13) reduce the problem for a while only.
- **Young, unreplicated 2026 preprints.** C11 and C12 (the sources that answer "scaffold vs model" most
  directly) are 2026 arXiv papers with no independent replication; C12's v2 is dated 11 Nov 2026.
  Model names in them (Opus 5, GPT-6) post-date most of the rest of the folder.
- **Cost and model age.** Most new entries do not report dollars per task (C18 reports one to a hundred
  dollars for a full run; C29 plots cost and time per attempt; C19 reports API cost per model); C16 and C20 use
  2024 and early-2025 models (Claude 3.5 and 3.7 Sonnet, o1), far behind the models in C12, C19 and C29.
  Their absolute numbers are stale; what transfers is the grading design.
- **Gaps in this folder.** Not fetched: SWE-bench Multilingual and Multi-SWE-bench as papers (its repo is
  in `public/_candidates/03.tsv`), FullStack-Agent (found, not included), and the training-side work
  (SWE-Gym, SWE-smith, SWE-RL, self-play SWE-RL) that gives evidence on how agents are made rather than how
  they are measured. SWE-agent is H10 in `02`. Test-time-compute evidence is now C10, C16, C24 and C25
  (all on 2024 to early-2026 open or older models), with no evidence on test-time scaling for
  from-scratch app builds, where there is no hidden test to select with.
