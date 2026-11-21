# Public Repos: GitHub survey

Open-source projects relevant to the kit: Claude Code plugins and harnesses, agent teams and
autonomous loops, coding agents and their benchmarks, verification and testing tools, research and
data-science agents, reproducibility tooling, and evaluation and cost tracking.

- **Surveyed:** 2026-11-21. 216 candidates from the nine literature scouts (`public/_candidates/`),
  merged to **203 unique repos** by `scripts/public/merge_candidates.py`. Stars, last push, license
  and archived status come from the GitHub API (`gh api repos/OWNER/REPO`) on that date, never from
  memory. The data is `public/candidates.tsv`.
- **Nothing here was run by us.** Feature claims come from READMEs and source files. A repo's stars
  or README numbers are never evidence that something works (CLAUDE.md §0): every number is
  **UNVERIFIED until one of our studies re-runs it.**
- **Flags:** `stale` = no push in the 12 months before the survey; `archived` = read-only upstream;
  `no license` = no LICENSE GitHub recognises, so **no copying** (read only); `also NN` = flagged by
  more than one theme. **Papers** = the `papers.tsv` IDs the scout linked the repo to.
- **Cloned:** the 20-repo shortlist below, pinned in `public/manifest.tsv`
  (`bash scripts/sync_public_repos.sh` refills them). Each has a process-and-lessons write-up in
  [`public/_README.md`](public/_README.md).

## Contents

1. [Headline findings](#1-headline-findings)
2. [The shortlist](#2-the-shortlist)
3. [License notes](#3-license-notes)
4. [All 203 repos, by theme](#4-all-203-repos-by-theme)

---

## 1. Headline findings

<!-- filled in after the shortlist write-ups (6.4, 6.5) -->

## 2. The shortlist

Twenty repos, chosen for what their **process and lessons** can teach the kit, not for stars alone.

| Group | Repo | Why it is on the list |
|---|---|---|
| Claude Code harness | [obra/superpowers](https://github.com/obra/superpowers) | Most-used skills methodology for Claude Code; we already use it |
| | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Reference layout and review bar for plugins (agents, skills, hooks) |
| | [wshobson/agents](https://github.com/wshobson/agents) | Large plugin marketplace of agents and commands: packaging at scale |
| | [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | Claude Code running unattended in CI: permissions without a human |
| | [anthropics/sandbox-runtime](https://github.com/anthropics/sandbox-runtime) | OS-level filesystem and network limits under auto mode (H17) |
| Teams and loops | [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Role-based agile method for AI builds: roles, handoff documents |
| | [gastownhall/gastown](https://github.com/gastownhall/gastown) | Multi-agent workspace manager for many Claude Code sessions |
| | [github/spec-kit](https://github.com/github/spec-kit) | Spec-driven development: detailed requirements before code (C29) |
| | [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) | Unattended Claude Code loop with exit detection |
| | [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT) | The original "AI software company" of roles (T1): what it learned |
| Coding agents and evals | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | Largest open coding agent: sandboxing, evaluation, contributor process |
| | [SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | A 100-line agent that holds up on SWE-bench: the simple baseline |
| | [UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | Evaluation framework: tasks, scorers, sandboxes, logs |
| | [harbor-framework/harbor](https://github.com/harbor-framework/harbor) | Agent evaluation framework behind Terminal-Bench: task packaging |
| | [commit-0/commit0](https://github.com/commit-0/commit0) | Build a library from scratch against its tests: closest to new-app |
| Research agents | [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | End-to-end automated research, and its documented failure modes |
| | [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | Research workflow with human check-in points |
| | [allenai/codescientist](https://github.com/allenai/codescientist) | Ai2's code-based discovery system with reviewed experiments |
| | [microsoft/RD-Agent](https://github.com/microsoft/RD-Agent) | Data-science and R&D agent loop (propose, implement, evaluate) |
| | [InfiAgent/InfiAgent](https://github.com/InfiAgent/InfiAgent) | InfiAgent-DABench (D1): known-answer data-analysis tasks, v0.1 study candidate |

## 3. License notes

- **38 repos have no license** GitHub recognises (`NONE`), among them `anthropics/skills` and
  `anthropics/claude-code`. They are read for ideas only; nothing is copied from them.
- **21 are `NOASSERTION`**: a LICENSE file exists but is not a standard one (custom, dual, or
  modified). The raw file is read before any copying (CLAUDE.md §4).
- **Copyleft:** 4 GPL-3.0 and 1 AGPL-3.0 (`qodo-ai/qodo-cover`). Copying their code would put the
  kit under the same terms; borrow ideas, not code.
- **8 are archived**, including `microsoft/autogen`, `METR/vivaria` and `METR/RE-Bench`: still
  readable, no longer maintained. **46 are stale** (no push in 12 months), mostly paper code.

## 4. All 203 repos, by theme

Grouped by the first theme that flagged the repo, sorted by stars. Regenerate with
`python scripts/public/merge_candidates.py`.

<!-- GENERATED: tables start -->

### 01. Agent architectures and orchestration (23)

| Repo | Stars | Last push | License | Flags | Papers | What it is |
|---|---:|---|---|---|---|---|
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 69292 | 2026-11-18 | Apache-2.0 |  | A13 | Memory layer for agents; its README self-reports LoCoMo 92.5 and LongMemEval 94.4 (vendor numbers, not independent). Lesson: test any memory |
| [microsoft/autogen](https://github.com/microsoft/autogen) | 61955 | 2026-11-12 | CC-BY-4.0 | archived, also 04 | A11 | Archived by Microsoft (README: no fixes, research-only, migrate to Agent Framework); holds A11 Magentic-One (python/packages/autogen-magenti |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 54926 | 2026-11-20 | MIT |  | A15 | patterns/agents/ holds minimal notebooks for A15's patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-opti |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 45217 | 2026-11-20 | MIT |  |  | Stateful graph orchestration with durable execution (resume after failure), human-in-the-loop interrupts and memory. Lesson: persist agent s |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | 30791 | 2026-11-21 | MIT |  |  | Production successor to Swarm: agents-as-tools, handoffs, guardrails, sessions, tracing. Lesson: built-in tracing and guardrails were the ad |
| [letta-ai/letta](https://github.com/letta-ai/letta) | 25505 | 2026-10-18 | Apache-2.0 |  |  | MemGPT successor; README says current source moved to letta-code, a coding-agent harness with terminal UI and server. Lesson: the memory-age |
| [openai/swarm](https://github.com/openai/swarm) | 22151 | 2026-04-15 | MIT |  |  | Experimental/educational handoff-and-routines library, now marked replaced by the OpenAI Agents SDK. Lesson: handoffs as plain function retu |
| [algorithmicsuperintelligence/openevolve](https://github.com/algorithmicsuperintelligence/openevolve) | 7834 | 2026-11-20 | Apache-2.0 |  | A25 | Open-source reimplementation of the AlphaEvolve loop (A25): LLM mutates code, programmatic evaluator scores it; a pattern for the kit's eval |
| [princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm) | 6087 | 2025-01-16 | MIT | stale | A3 | A3 code with all prompts; 5.5k completion tokens per Game-of-24 case. Lesson: search is for tasks the base model fails; log tokens per case  |
| [lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM) | 5722 | 2024-08-10 | Apache-2.0 | stale | A12 | A12 router framework with per-request cost threshold and a calibrate_threshold script. Lesson: calibrate the threshold on your own traffic;  |
| [ysymyth/ReAct](https://github.com/ysymyth/ReAct) | 4292 | 2024-02-06 | MIT | stale | A1 | A1 reference prompts and HotpotQA/ALFWorld code; frozen since 2024 (read-only). Lesson to borrow: 1-2 in-context trajectories were enough, a |
| [noahshinn/reflexion](https://github.com/noahshinn/reflexion) | 3438 | 2025-01-14 | MIT | stale | A2, A4, A5 | A2 code incl. LeetcodeHardGym; reflect-on-failure loop with a 1-experience memory. Lesson: the loop helped where a real test/oracle existed  |
| [jennyzzt/dgm](https://github.com/jennyzzt/dgm) | 2533 | 2025-08-13 | Apache-2.0 | stale | A22 | A22 reference code for the Darwin Godel Machine (self-modifying coding agent with an archive of agents); study how it sandboxes self-modific |
| [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench) | 2494 | 2026-11-21 | MIT |  | A9 | Successor to A9 with fixed airline/retail tasks and new domains; shows a benchmark needs ongoing task fixes. Lesson: grade by final database |
| [xingyaoww/code-act](https://github.com/xingyaoww/code-act) | 1721 | 2024-05-23 | MIT | stale | A20 | A20 CodeAct reference code and CodeActInstruct data; frozen since 2024-05, the live descendant is OpenHands (already in 04) |
| [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) | 1514 | 2026-03-18 | MIT |  | A9 | A9 benchmark: simulated user + DB-state grader + pass^k reliability metric. README warns its tasks are outdated and points to tau2-bench; le |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | 1236 | 2026-05-11 | MIT |  | A13 | A13 benchmark and memory-pipeline code (index/retrieve/read). README notes a 2025-09 cleaned dataset after history sessions interfered with  |
| [billxbf/ReWOO](https://github.com/billxbf/ReWOO) | 945 | 2023-07-28 | MIT | stale | A7, A8 | A7 code: planner/worker/solver split with #E variables. Lesson: plan-first cuts tokens ~5x on QA but needs a re-plan path when the environme |
| [TheAgentCompany/TheAgentCompany](https://github.com/TheAgentCompany/TheAgentCompany) | 822 | 2025-11-17 | MIT | stale | A14 | A14 self-hosted company environment with checkpoint graders, simulated colleagues and OpenHands baselines. Borrow checkpoint-based partial c |
| [harbor-framework/terminal-bench-2](https://github.com/harbor-framework/terminal-bench-2) | 451 | 2026-04-30 | Apache-2.0 | also 03 | A24, C18 | A24 task set (89 hard CLI tasks, each with instruction, Dockerfile, tests, oracle solution); model for the kit's own task format (unverified |
| [princeton-pli/hal-harness](https://github.com/princeton-pli/hal-harness) | 308 | 2026-07-01 | NONE | archived, no license, also 06 | A10, S17 | Archived harness for cost-controlled, parallel, reproducible agent evaluation (HAL) with Weave cost logging; README says work moved to agent |
| [google-deepmind/alphaevolve_results](https://github.com/google-deepmind/alphaevolve_results) | 306 | 2026-01-05 | Apache-2.0 |  | A25 | A25 results repository (discovered programs and verification notebooks) from AlphaEvolve; shows what an automated-evaluator loop produces an |
| [uiuc-kang-lab/agentic-benchmarks](https://github.com/uiuc-kang-lab/agentic-benchmarks) | 66 | 2025-07-31 | NONE | stale, no license | A18 | A18 Agentic Benchmark Checklist (ABC) materials; usable as a pre-flight checklist for the kit's own benchmark tasks; no detected license, so |

### 02. Harnesses, Claude Code and autonomy (31)

| Repo | Stars | Last push | License | Flags | Papers | What it is |
|---|---:|---|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 322959 | 2026-11-03 | MIT | also 04 |  | Skills library built around process (TDD, plans, subagent-driven development); study its workflow and how it evolved from real use |
| [anthropics/skills](https://github.com/anthropics/skills) | 198133 | 2026-11-16 | NONE | no license | H6 | Reference SKILL.md packages incl. skill-creator; H6 shows creator-written skills can hurt, so borrow the format, not auto-generation (no rep |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | 156486 | 2026-11-21 | NONE | no license |  | The platform itself: its issue tracker and changelog are where headless, permission and subagent regressions show up first; read, do not cop |
| [github/spec-kit](https://github.com/github/spec-kit) | 150853 | 2026-11-20 | MIT |  |  | Spec-driven development toolkit for coding agents (spec, plan, tasks); process to compare with the kit's founding promise + feature card |
| [openai/codex](https://github.com/openai/codex) | 136016 | 2026-11-21 | Apache-2.0 |  | H27 | Codex CLI: the H27 harness (AGENTS.md map, approvals, sandbox, compaction); compare its defaults with Claude Code's for the kit's permission |
| [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 108960 | 2026-11-21 | Apache-2.0 |  | H32 | Google's open-source terminal coding agent (Apache-2.0); a second large vendor harness to compare against openai/codex and Claude Code; rela |
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 93932 | 2026-11-21 | MIT | also 03 | C4, H3 | Open coding-agent platform with LLM-summary condensers and an SDK; compare its context management against H3's masking result |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 58476 | 2026-11-21 | NOASSERTION |  |  | Curated index of Claude Code skills, hooks, plugins and orchestrators; a scouting list for Phase 6 |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 47852 | 2026-11-21 | Apache-2.0 | also 05 |  | Official plugin marketplace: layout and manifest conventions for plugin/ and marketplace.json |
| [wshobson/agents](https://github.com/wshobson/agents) | 42748 | 2026-11-18 | MIT |  |  | Large Claude Code subagent/plugin collection; lessons on organising many agents into installable plugins and keeping each focused |
| [agentsmd/agents.md](https://github.com/agentsmd/agents.md) | 25626 | 2026-09-10 | MIT |  | H1, H2 | The cross-tool AGENTS.md convention (H1, H2); keep kit context files short given H1's cost finding |
| [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts) | 21123 | 2026-11-06 | MIT |  | H13 | autonomous-coding/ is the reference code for H13 (initializer + progress file + feature list); borrow its long-run process directly |
| [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) | 20840 | 2026-11-16 | MIT | also 03 | H10 | H10's agent-computer interface: tool design, edit linting and viewer-window guardrails the kit's tools can copy |
| [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | 8606 | 2026-11-20 | MIT |  |  | Fallback wrapper if a plugin alone cannot stand up the team (row 4.8): programmatic sessions, canUseTool permission callbacks |
| [harbor-framework/harbor](https://github.com/harbor-framework/harbor) | 7309 | 2026-11-21 | Apache-2.0 | also 03 | H6, V2 | Container harness used by SkillsBench (H6) to run agents on tasks; candidate runner for the kit's benchmark |
| [anthropics/sandbox-runtime](https://github.com/anthropics/sandbox-runtime) | 7206 | 2026-11-13 | Apache-2.0 |  | H24 | H24 code: the open-source filesystem and network sandbox behind /sandbox; candidate isolation layer for unattended kit runs |
| [humanlayer/advanced-context-engineering-for-coding-agents](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents) | 2834 | 2026-10-16 | NONE | no license |  | Practitioner write-up of research/plan/implement phases with intentional compaction; process lessons to test, not evidence (no license) |
| [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code) | 2248 | 2026-11-10 | NOASSERTION |  | H16 | H16 companion: source-level map of Claude Code (permission modes, 27 hook events, five-layer compaction); read to learn what the harness alr |
| [benchflow-ai/skillsbench](https://github.com/benchflow-ai/skillsbench) | 1929 | 2026-11-16 | Apache-2.0 |  | H6 | H6 benchmark with paired no-skill/curated-skill runs and deterministic verifiers; template for the kit's skill ablations |
| [ace-agent/ace](https://github.com/ace-agent/ace) | 1469 | 2026-08-24 | Apache-2.0 |  | H5 | H5 code: generator/reflector/curator loop with incremental playbook updates; model for a lessons.md that grows without collapse |
| [google-research/camel-prompt-injection](https://github.com/google-research/camel-prompt-injection) | 425 | 2025-06-20 | Apache-2.0 | stale | H18 | H18 code: capability-based policy layer around tool calls; pattern for deterministic data-flow rules in PreToolUse hooks |
| [microsoft/acon](https://github.com/microsoft/acon) | 132 | 2025-10-14 | MIT | stale | H4 | H4 code: failure-driven refinement of compression guidelines; a pattern for tuning the kit's compaction prompt |
| [microsoft/fides](https://github.com/microsoft/fides) | 125 | 2025-05-30 | MIT | stale | H19 | H19 code: information-flow labels and deterministic policy checks on agent planners; reference for confidentiality/integrity rules the kit's |
| [haoyuwang99/AgentSpec](https://github.com/haoyuwang99/AgentSpec) | 70 | 2026-01-15 | NONE | no license | H8 | H8 code: trigger/predicate/enforcement rule DSL, close to Claude Code hooks; read only (no license) |
| [ybkim95/agent-scaling](https://github.com/ybkim95/agent-scaling) | 63 | 2026-10-12 | MIT |  | H11 | H11 code: controlled single- vs multi-agent comparisons at fixed tools and compute; method for testing the kit's team size |
| [sunblaze-ucb/progent](https://github.com/sunblaze-ucb/progent) | 60 | 2026-11-18 | MIT |  | H9 | H9 code: deterministic least-privilege tool-call policies; pattern for PreToolUse/PermissionRequest hooks in unattended runs |
| [UCSB-NLP-Chang/Skill-Usage](https://github.com/UCSB-NLP-Chang/Skill-Usage) | 49 | 2026-04-08 | NONE | no license | H7 | H7 code: skill retrieval and query-specific refinement over 34k skills; read only (no license) |
| [facebookresearch/cca-swebench](https://github.com/facebookresearch/cca-swebench) | 45 | 2026-05-21 | MIT |  | H20 | H20 code: Confucius Code Agent evaluation on SWE-Bench; context management and cross-session notes ablations to reuse as a method |
| [JetBrains-Research/the-complexity-trap](https://github.com/JetBrains-Research/the-complexity-trap) | 20 | 2025-11-18 | MIT | stale | H3 | H3 code: observation masking vs summarization harness; reusable to test compaction choices on our own tasks |
| [yan5ui/cc-auto-mode-measurement](https://github.com/yan5ui/cc-auto-mode-measurement) | 12 | 2026-04-14 | NONE | no license | H17 | H17 code: AmPermBench stress test of Claude Code auto mode; read only (no license); shows how to probe the permission gate before an unatten |
| [SAILResearch/agentic_plugin_marketplace](https://github.com/SAILResearch/agentic_plugin_marketplace) | 0 | 2026-08-27 | NONE | no license | H12 | H12 replication data on 8,351 Claude Code plugins; how real plugins are maintained (no license, data only) |

### 03. Coding agents and SWE benchmarks (28)

| Repo | Stars | Last push | License | Flags | Papers | What it is |
|---|---:|---|---|---|---|---|
| [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) | 30826 | 2026-11-21 | Apache-2.0 |  | C11 | The harness C11 measured across 35 releases (no significant resolve-rate gain, nearly double the tokens). Lesson: pin the agent-harness vers |
| [SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | 9910 | 2026-11-16 | MIT | also 04/05 | C12, H11, T8, T9, V1 | ~100-line bash-only agent with a linear message history and one subprocess per action (trivially sandboxed); README claims >74% on SWE-bench |
| [SWE-bench/SWE-bench](https://github.com/SWE-bench/SWE-bench) | 6227 | 2026-09-18 | MIT |  |  | The benchmark harness itself: containerised Docker evaluation with fail-to-pass and pass-to-pass tests as the grader spec. Lesson from its i |
| [mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe) | 5442 | 2026-11-20 | Apache-2.0 |  | C35 | Open-source minimal CLI coding agent behind the C35 launch post (Devstral 2 numbers are vendor claims); a small Apache-2.0 harness to read f |
| [OpenAutoCoder/Agentless](https://github.com/OpenAutoCoder/Agentless) | 2138 | 2024-12-22 | MIT | stale | C2, C3 | C3's fixed three-phase pipeline (localise, repair, validate) with generated reproduction tests used to re-rank patches. Borrow the reproduct |
| [openai/SWELancer-Benchmark](https://github.com/openai/SWELancer-Benchmark) | 1429 | 2025-07-18 | NONE | archived, stale, no license | C16 | Task data and Docker image for C16: real freelance tasks graded by Playwright end-to-end tests; archived and unlicensed, so read for the gra |
| [openai/frontier-evals](https://github.com/openai/frontier-evals) | 1345 | 2026-10-12 | MIT | also 06 | S7 | Holds the SWE-Lancer eval (real freelance tasks graded by end-to-end tests, per its README). Borrow the idea of grading by user-visible end- |
| [harbor-framework/terminal-bench](https://github.com/harbor-framework/terminal-bench) | 1109 | 2026-11-21 | Apache-2.0 |  | C18 | Terminal-Bench task format (container, instruction, tests, oracle solution) and harness behind C18; the task-contract pattern the kit's benc |
| [facebookresearch/cwm](https://github.com/facebookresearch/cwm) | 922 | 2026-07-17 | NOASSERTION |  | C34 | Inference code and reproducibility artifacts for the CWM model in C34 (65.8% SWE-bench Verified with test-time scaling, vendor-run). License |
| [SWE-bench/SWE-smith](https://github.com/SWE-bench/SWE-smith) | 835 | 2026-11-16 | MIT |  |  | Turns any repo into runnable tasks: build env, synthesise task instances, keep those that break at least one unit test, generate issue text. |
| [SWE-Gym/SWE-Gym](https://github.com/SWE-Gym/SWE-Gym) | 764 | 2026-11-01 | Apache-2.0 |  |  | Training environments plus inference-time verifier scaling (context for retries). Its README carries a 'patch before use' warning about the  |
| [scaleapi/SWE-bench_Pro-os](https://github.com/scaleapi/SWE-bench_Pro-os) | 569 | 2026-09-22 | MIT |  | C9, C12, V2 | C9/C12 benchmark. V2 ships a locked protocol: offline agent phase, fresh-container re-grade of the patch, and an oracle run proving referenc |
| [multi-swe-bench/multi-swe-bench](https://github.com/multi-swe-bench/multi-swe-bench) | 364 | 2025-12-18 | Apache-2.0 |  | C17 | ByteDance multilingual issue-resolving benchmark that C17 cites; shows what happens to a Python-tuned agent on other languages |
| [R2E-Gym/R2E-Gym](https://github.com/R2E-Gym/R2E-Gym) | 353 | 2025-07-13 | Apache-2.0 | stale | C24 | C24 environments and the hybrid execution-based plus execution-free verifier code for best-of-k selection among agent attempts |
| [bytedance/web-bench](https://github.com/bytedance/web-bench) | 300 | 2026-04-30 | Apache-2.0 |  | C20 | C20 Web-Bench: 50 projects of 20 sequentially dependent tasks with end-to-end tests; a model for multi-step app-build tasks with scripted ch |
| [SWE-bench/experiments](https://github.com/SWE-bench/experiments) | 287 | 2026-09-03 | NONE | no license |  | Submission repo for the leaderboards: one metadata.yaml per entry, artifacts kept in the submitter's repo, and (since 2025-11-18) a rule tha |
| [microsoft/SWE-bench-Live](https://github.com/microsoft/SWE-bench-Live) | 263 | 2026-11-08 | MIT |  |  | Continuously refreshed task set (monthly additions) with an explicit protocol: the agent sees only problem_statement and the docker image, p |
| [SakanaAI/ALE-Bench](https://github.com/SakanaAI/ALE-Bench) | 237 | 2026-11-20 | Apache-2.0 |  |  | Official repo of ALE-Bench (Sakana AI, long-horizon algorithm engineering; named in the lab sweep, no library paper yet); its Sakana blog ti |
| [open-compass/AgentCompass](https://github.com/open-compass/AgentCompass) | 197 | 2026-11-20 | Apache-2.0 |  | C27 | Evaluation infrastructure C27 used to run SWE-Bench Pro with anti-hacking controls and trajectory audits; actively maintained |
| [multimodal-art-projection/NL2RepoBench](https://github.com/multimodal-art-projection/NL2RepoBench) | 194 | 2026-05-13 | NONE | no license | C22 | C22 repo-from-scratch benchmark: one requirements document, an empty workspace, graded by the original library's pytest suite; no license, s |
| [commit-0/commit0](https://github.com/commit-0/commit0) | 194 | 2026-02-24 | MIT |  | C22 | Library-from-scratch benchmark: agents rebuild a library from its spec and unit tests; the older relative of C22 for the new-app task |
| [OpenHands/benchmarks](https://github.com/OpenHands/benchmarks) | 134 | 2026-11-09 | MIT |  |  | OpenHands evaluation harness for SWE-bench and related suites; reference for running one benchmark with a pinned agent configuration |
| [logic-star-ai/baxbench](https://github.com/logic-star-ai/baxbench) | 111 | 2026-01-30 | MIT |  | C23 | C23 BaxBench: backend generation graded by functional tests plus executed security exploits; a pattern for adding a security grader to app t |
| [epoch-research/MirrorCode](https://github.com/epoch-research/MirrorCode) | 82 | 2026-09-15 | MIT |  | C32 | Public repo for MirrorCode (C32): executable-spec reimplementation tasks that a kit benchmark could borrow as a long-horizon app-build style |
| [LegoX/SWE-Lego](https://github.com/LegoX/SWE-Lego) | 80 | 2026-02-28 | Apache-2.0 |  | C25 | C25 recipe and the sequential-versus-parallel test-time-scaling experiments (turns versus rollouts under a latency budget) |
| [mnluzimu/WebGen-Bench](https://github.com/mnluzimu/WebGen-Bench) | 61 | 2026-07-10 | NONE | no license | C21 | C21 website-from-scratch benchmark with a web-navigation agent as grader and 647 UI test cases; no license, so read only |
| [ScalingIntelligence/codemonkeys](https://github.com/ScalingIntelligence/codemonkeys) | 59 | 2025-01-28 | MIT | stale | C10 | C10's code: pipeline split into context, generation and selection scripts, with a step that reproduces the paper figures and a selector that |
| [benchjack/benchjack](https://github.com/benchjack/benchjack) | 54 | 2026-05-25 | Apache-2.0 | also 05 | C26, V27 | C26 automated red-team auditor for agent benchmarks plus the Agent-Eval Checklist; run it against the kit's own graders before release |

### 04. Multi-agent software teams (17)

| Repo | Stars | Last push | License | Flags | Papers | What it is |
|---|---:|---|---|---|---|---|
| [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT) | 71371 | 2026-01-21 | MIT |  | T2 | SOP-encoded roles that hand each other structured documents (PRD, design) rather than chat (T2). Borrow: typed artifacts between roles and e |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | 55583 | 2026-11-20 | NOASSERTION |  |  | Agile role-based method (clarify, plan, build and verify, learn) with decisions kept explicit and context carried forward in written artifac |
| [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev) | 34829 | 2026-11-06 | Apache-2.0 |  | T1, T7 | The CEO/CTO/programmer/reviewer/tester waterfall of T1, kept on the chatdev1.0 branch; main is now a zero-code workflow platform. Borrow the |
| [gastownhall/gastown](https://github.com/gastownhall/gastown) | 18857 | 2026-11-14 | MIT |  |  | Mayor coordinator plus worker agents whose work state lives in git-backed hooks and a ledger rather than in agent memory. Borrow: durable ha |
| [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) | 16508 | 2026-11-20 | MIT |  | T13 | Open-source PR reviewer (formerly qodo-ai/pr-agent). Use it as a reference review agent whose comments can be scored for signal against T13' |
| [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | 10031 | 2026-11-21 | MIT |  | T17 | Runs Claude Code as a PR reviewer in CI on a fresh runner, so the reviewer starts without the builder's context, the pattern T17 says works  |
| [OpenBMB/AgentVerse](https://github.com/OpenBMB/AgentVerse) | 5164 | 2024-09-09 | Apache-2.0 | stale | T3, T10 | Recruit-decide-execute-evaluate loop of T3 with Solo vs Group setups. Lesson from T3/T10: the group was not reliably better than one agent;  |
| [anthropics/claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler) | 2838 | 2026-02-05 | CC0-1.0 |  | T16 | Working files of the 16-agent run in T16: current_tasks/ lock files, DESIGN_DOC.md, ideas/. Process to borrow: file-lock task claiming throu |
| [microsoft/Agensh](https://github.com/microsoft/Agensh) | 935 | 2026-11-03 | MIT |  | T21 | Orchestrator-free harness (shared Git workspace, message log, claim-and-verify loop) from T21; a model for coordination through files and gi |
| [FSoft-AI4Code/AgileCoder](https://github.com/FSoft-AI4Code/AgileCoder) | 467 | 2024-10-15 | MIT | stale | T5 | Sprint planning, backlog and review per sprint (T5): the agile alternative to ChatDev's waterfall. Borrow the backlog-plus-sprint-review str |
| [multi-agent-systems-failure-taxonomy/MAST](https://github.com/multi-agent-systems-failure-taxonomy/MAST) | 440 | 2025-07-23 | NONE | stale, no license | T7 | Failure taxonomy (14 modes) plus 1,600+ annotated traces and an LLM-judge annotator (T7). Borrow the taxonomy as the checklist for auditing  |
| [JiayiGeng/CAID](https://github.com/JiayiGeng/CAID) | 80 | 2026-04-02 | NONE | no license | T20 | Manager plus engineers in isolated git worktrees with test-gated merges (T20); no license, so read only and do not copy |
| [cooperbench/CooperBench](https://github.com/cooperbench/CooperBench) | 37 | 2026-11-20 | NONE | no license | T19 | CooperBench tasks and runner (T19): two-agent same-repo coding tasks with a Solo baseline, usable as a coordination stress test; no license, |
| [few-sh/harden-v0](https://github.com/few-sh/harden-v0) | 18 | 2026-07-03 | Apache-2.0 |  | T24 | Hacker-fixer-solver loop that hardens outcome verifiers (T24); a pattern for stress-testing the kit's tester and benchmark graders |
| [ybkim95/TeamBench](https://github.com/ybkim95/TeamBench) | 12 | 2026-09-22 | MIT |  | T18 | TeamBench (T18): Planner/Executor/Verifier with OS-enforced role separation and a Solo arm; a template for a role-separated, grader-anchored |
| [rm206/ParallACT_data_and_code](https://github.com/rm206/ParallACT_data_and_code) | 5 | 2026-11-03 | NONE | no license | T22 | ParallACT data and code (T22, linked from the paper's project page): orchestrator-free parallel agents vs single-agent oracle and serial han |
| [mahmoudsajjadi/pace](https://github.com/mahmoudsajjadi/pace) | 3 | 2026-11-19 | Apache-2.0 |  | T9 | Reviewer checklist and accounting utilities for equal-budget comparisons of multi-agent against single-agent (T9). Borrow: the baseline ladd |

### 05. Verification, testing and QA (23)

| Repo | Stars | Last push | License | Flags | Papers | What it is |
|---|---:|---|---|---|---|---|
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | 39950 | 2026-11-18 | Apache-2.0 |  |  | Lesson from its README: accessibility-tree snapshots instead of screenshots (fast, deterministic, no vision model) and a note that CLI-as-sk |
| [lm-sys/FastChat](https://github.com/lm-sys/FastChat) | 39548 | 2026-05-01 | Apache-2.0 |  | V13 | Process: llm_judge folder holds the MT-Bench pairwise and single-answer judge prompts (V13), with position-swap checks; borrow the swap-orde |
| [HypothesisWorks/hypothesis](https://github.com/HypothesisWorks/hypothesis) | 9199 | 2026-11-20 | NOASSERTION |  | V22 | Process: property-based testing library behind V22's agent; lesson: the agent writes its properties as Hypothesis tests, so each bug report  |
| [microsoft/fara](https://github.com/microsoft/fara) | 6259 | 2026-09-22 | MIT |  | V29 | Process: Microsoft computer-use agent repo that hosts the Universal Verifier and CUAVerifierBench (V29); lesson: rubric-based, screenshot-by |
| [qodo-ai/qodo-cover](https://github.com/qodo-ai/qodo-cover) | 5688 | 2026-04-05 | AGPL-3.0 |  | V5 | Process: coverage-driven test generation loop (README shows it is the Codium cover-agent tool V5 tested as CoverAgent; V5 found 59.6% of its |
| [anthropics/original_performance_takehome](https://github.com/anthropics/original_performance_takehome) | 4226 | 2026-01-22 | NONE | no license | V36 | Anthropic's original performance take-home, public so anyone can try it (V36: Opus 4.5 reached 1,487 cycles after 11.5 hours); a worked exam |
| [stryker-mutator/stryker-js](https://github.com/stryker-mutator/stryker-js) | 3404 | 2026-11-21 | Apache-2.0 |  |  | Process: mutation score as a CI badge on its own repo (dogfooding) with a public dashboard; lesson: report mutation score, not line coverage |
| [UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | 3302 | 2026-11-20 | MIT |  | V3 | Process: eval framework with sandboxed solvers and scorers; ImpossibleBench (V3) is built on it; candidate harness for the benchmark's grade |
| [xlang-ai/OSWorld](https://github.com/xlang-ai/OSWorld) | 3272 | 2026-11-14 | Apache-2.0 |  | V10 | Process: execution-based per-task checker scripts plus VM snapshots (V10); lesson: README announces OSWorld-Verified after community-reporte |
| [hcoles/pitest](https://github.com/hcoles/pitest) | 1893 | 2026-11-16 | Apache-2.0 |  | V18, V19 | Process: JVM mutation-testing tool used to score LLM tests in V19 and as a rule-based mutant baseline in V18; lesson: report mutation score, |
| [evalplus/evalplus](https://github.com/evalplus/evalplus) | 1840 | 2025-10-02 | Apache-2.0 | stale | V11 | Process: extend weak tests with many more generated inputs and re-score (V11); lesson: re-run the kit's own acceptance tests with augmented  |
| [web-arena-x/webarena](https://github.com/web-arena-x/webarena) | 1645 | 2025-11-26 | Apache-2.0 |  |  | Process: self-hosted web apps with state-based checks of what the agent actually changed (Anthropic evals post cites this pattern as backend |
| [boxed/mutmut](https://github.com/boxed/mutmut) | 1550 | 2026-11-19 | BSD-3-Clause |  | V4 | Process: mutants applied on disk, then tests re-run, survivors reviewed; README warns to have the mutated file committed first; borrow the s |
| [metauto-ai/agent-as-a-judge](https://github.com/metauto-ai/agent-as-a-judge) | 852 | 2026-03-28 | MIT |  | V15 | Process: an agent that inspects files and trajectory against a requirement list instead of judging the final answer (V15); borrow the requir |
| [OSU-NLP-Group/Online-Mind2Web](https://github.com/OSU-NLP-Group/Online-Mind2Web) | 214 | 2026-11-04 | MIT |  | V7 | Process: human-labelled trajectories used to calibrate an LLM judge (WebJudge, V7); README shows the judge must be re-validated when its bac |
| [plasma-umass/coverup](https://github.com/plasma-umass/coverup) | 117 | 2026-04-05 | Apache-2.0 |  | V5 | Process: measure coverage, prompt for tests, run, re-prompt on failure; V5 found 68.1% of its final suite validated buggy code; lesson: iter |
| [mmaaz-git/agentic-pbt](https://github.com/mmaaz-git/agentic-pbt) | 105 | 2025-11-03 | NONE | stale, no license | V22 | Process: Claude Code agent infers properties from code and docs, writes Hypothesis tests, and self-reviews bug reports (V22); lesson: a prop |
| [logic-star-ai/swt-bench](https://github.com/logic-star-ai/swt-bench) | 93 | 2026-11-04 | MIT |  | V2 | Process: a generated test only counts if it fails before the fix and passes after (V2); lesson: use fail-to-pass as the QA reviewer's test o |
| [safety-research/impossiblebench](https://github.com/safety-research/impossiblebench) | 82 | 2026-10-13 | MIT |  | V3 | Process: build an unsolvable task variant so any pass is proof of cheating (V3); lesson: run the reviewer against this to see if it catches  |
| [McGill-NLP/agent-reward-bench](https://github.com/McGill-NLP/agent-reward-bench) | 52 | 2026-08-16 | NONE | no license | V25 | Process: 1,302 expert-labelled web-agent trajectories for scoring judges (V25); lesson: a labelled set to measure the tester's judge precisi |
| [code-philia/WebTestPilot](https://github.com/code-philia/WebTestPilot) | 18 | 2026-10-01 | CC-BY-4.0 |  | V28 | Process: natural-language spec to E2E web test with symbolic pre/post-condition oracles over GUI elements, plus 4 bug-injected apps (V28); l |
| [githubnext/llmorpheus](https://github.com/githubnext/llmorpheus) | 17 | 2025-02-03 | MIT | archived, stale | V18 | Process: LLM-generated JavaScript mutants (a baseline in V18); lesson: masks a code location with a PLACEHOLDER and asks the model to fill i |
| [ServiceNow/agenthorizon](https://github.com/ServiceNow/agenthorizon) | 6 | 2026-11-14 | NONE | no license | V26 | Process: benchmark of long computer-use trajectories with swapped-instruction negatives for agentic judges (V26); lesson: how to test whethe |

### 06. AI scientists and research agents (22)

| Repo | Stars | Last push | License | Flags | Papers | What it is |
|---|---:|---|---|---|---|---|
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 15027 | 2025-12-19 | NOASSERTION |  | S1, S9 | Code for S1 (idea, experiment, write-up, simulated review). Lessons: its own README warns it executes LLM-written code and must be container |
| [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | 7537 | 2025-12-19 | NOASSERTION |  | S2, S10 | Code for S2 (agentic tree search, no human templates, VLM figure feedback). Borrow: the experiment-manager plus tree-search idea and the san |
| [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | 5934 | 2025-08-20 | MIT | stale | S3 | Code for S3: literature review, experimentation, report-writing stages with a co-pilot mode where a human checks each stage, checkpoint save |
| [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) | 5898 | 2025-10-16 | NONE | stale, no license |  | Large end-to-end research agent with a benchmark of two task levels (detailed idea vs reference-based ideation) run in Docker. Lesson: popul |
| [ResearAI/DeepScientist](https://github.com/ResearAI/DeepScientist) | 3418 | 2026-06-28 | Apache-2.0 |  | S27 | Code for S27: goal-directed discovery loop with a cumulative findings memory and staged validation; borrow the findings-memory and filter-be |
| [SakanaAI/ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve) | 1529 | 2026-11-20 | Apache-2.0 |  | A25 | Sakana AI's open-ended program-evolution framework (repo description: sample-efficient program evolution); a program-evolution system to com |
| [facebookresearch/MLGym](https://github.com/facebookresearch/MLGym) | 625 | 2025-08-10 | NOASSERTION | archived, stale | S30 | Code for S30: Gym-style environment and 13 open-ended AI research tasks with a performance-profile metric; archived and non-standard license |
| [jimmc414/Kosmos](https://github.com/jimmc414/Kosmos) | 607 | 2026-10-09 | NONE | no license | S13 | Unofficial open-source re-implementation of the Kosmos architecture (S13) that can be driven by Claude Code; self-declared alpha, runs code  |
| [NoviScl/AI-Researcher](https://github.com/NoviScl/AI-Researcher) | 416 | 2025-08-07 | MIT | stale | S5, S6 | Ideation agent and all data from S5 and S6 (ideas, 79 reviewers' blind reviews, 43 executed projects with reviews). Borrow: a ready ground t |
| [allenai/codescientist](https://github.com/allenai/codescientist) | 352 | 2026-03-25 | Apache-2.0 |  | S34 | Code for CodeScientist (S34): a research agent that turns papers and code blocks into experiments; useful for its review-and-replication eva |
| [ResearAI/Awesome-AI-Scientist](https://github.com/ResearAI/Awesome-AI-Scientist) | 316 | 2025-10-31 | Apache-2.0 | stale |  | Curated list of AI-scientist systems and benchmarks kept by the Westlake ResearAI group; use it to find newer systems, not as evidence. Apac |
| [allenai/agent-baselines](https://github.com/allenai/agent-baselines) | 159 | 2026-10-01 | Apache-2.0 |  | S19 | Ai2's 57-agent baseline set for AstaBench (S19); useful as a no-plugin comparison arm for the kit's benchmark |
| [allenai/asta-bench](https://github.com/allenai/asta-bench) | 144 | 2026-11-10 | Apache-2.0 |  | S19 | Ai2's AstaBench suite (S19): 2,400+ science-agent problems with cost-aware scoring and a leaderboard toolkit; borrow cost-normalised reporti |
| [SakanaAI/robust-kbench](https://github.com/SakanaAI/robust-kbench) | 108 | 2025-11-22 | Apache-2.0 |  | S28 | Code for S28: a benchmark rebuilt after LLM agents exploited loopholes in the original; borrow the pattern of verifying the verifier (multip |
| [siegelz/core-bench](https://github.com/siegelz/core-bench) | 80 | 2025-11-23 | MIT |  | S8 | Harness and dataset for CORE-Bench (S8): 270 reproduction tasks in 90 papers, each run in an isolated container or VM, answers checked again |
| [chchenhui/mlrbench](https://github.com/chchenhui/mlrbench) | 38 | 2026-09-08 | MIT |  | S16 | Code for S16: 201 workshop-derived tasks, an LLM judge with rubrics that reads execution logs and code, and a modular four-stage agent. Borr |
| [Agent4Science-UTokyo/Jr.AI-Scientist](https://github.com/Agent4Science-UTokyo/Jr.AI-Scientist) | 32 | 2026-04-08 | NONE | no license | S24 | Code and issue tracker for S24: baseline-paper-to-new-paper pipeline driven by coding agents, with a written risk report; no license detecte |
| [Lossfunk/ai-scientist-artefacts-v1](https://github.com/Lossfunk/ai-scientist-artefacts-v1) | 25 | 2025-11-10 | NONE | stale, no license | S11 | Prompts, plans and failure analyses from S11: four ideas, one paper, three failures; plan.md and agent.md written for Claude Code. Borrow: t |
| [chchenhui/fabscore](https://github.com/chchenhui/fabscore) | 24 | 2026-09-08 | MIT |  | S15 | Code for S15: extracts every number in a paper, has a coding agent check it against the code by static analysis and execution, and returns o |
| [niharshah/AIScientistPitfalls](https://github.com/niharshah/AIScientistPitfalls) | 12 | 2025-09-14 | NONE | stale, no license | S10 | Code and data for S10: controlled experiments that expose benchmark selection, data leakage, metric misuse and post-hoc selection in AI Scie |
| [Christine8888/replicationbench-release](https://github.com/Christine8888/replicationbench-release) | 11 | 2025-11-25 | MIT |  | S26 | Release of S26: 111 astrophysics replication tasks across 20 papers, run in sandboxes and scored against original results; a model for known |
| [Bad-Scientist/BadScientist](https://github.com/Bad-Scientist/BadScientist) | 2 | 2026-04-23 | MIT |  | S23 | Official repo of S23: fabrication-oriented paper generator and calibrated LLM-reviewer harness; use as a red-team test for any LLM-reviewer  |

### 07. Data science agents and benchmarks (26)

| Repo | Stars | Last push | License | Flags | Papers | What it is |
|---|---:|---|---|---|---|---|
| [huggingface/smolagents](https://github.com/huggingface/smolagents) | 30463 | 2026-11-20 | Apache-2.0 |  | D10, D12 | Code-writing agent library; its "smolagents DR" variant is the strongest baseline in D10 (55.83% overall vs 24.98% for the best fixed pipeli |
| [microsoft/RD-Agent](https://github.com/microsoft/RD-Agent) | 15440 | 2026-10-21 | MIT |  | D28 | R&D-Agent from D28: an MLE-bench agent split into two phases and six components; MIT-licensed and widely starred, but stars are not evidence |
| [openai/mle-bench](https://github.com/openai/mle-bench) | 1801 | 2026-04-24 | NOASSERTION |  | D4 | D4's 75 Kaggle competitions with medal grading (LICENSE file is MIT; GitHub reports NOASSERTION). Process to borrow: at least 3 seeds report |
| [WecoAI/aideml](https://github.com/WecoAI/aideml) | 1627 | 2026-10-16 | MIT |  | D4 | AIDE, the draft-debug-improve tree-search scaffold behind the D4 baselines (o1-preview 16.9%). README separates the algorithm, this lean res |
| [google-research/era](https://github.com/google-research/era) | 371 | 2026-10-13 | Apache-2.0 |  |  | Google Research's ERA (paper by Aygun et al. 2025, arXiv:2509.06503, catalogued in folder 06): tree search over LLM-written code against a s |
| [InfiAgent/InfiAgent](https://github.com/InfiAgent/InfiAgent) | 209 | 2025-05-29 | Apache-2.0 | stale | D1 | D1's DAEval: 257 closed-form data-analysis questions over 52 CSVs with a ReAct agent in a Docker sandbox; the "@name[answer]" label format m |
| [ucbepic/DataAgentBench](https://github.com/ucbepic/DataAgentBench) | 209 | 2026-11-20 | NONE | no license | D11 | D11's DAB: 5 trials per query, pull-request leaderboard that requires execution traces, and SUBMISSION_RUBRIC.md leakage checks. Lessons in  |
| [OSU-NLP-Group/ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench) | 186 | 2026-11-16 | MIT |  | D8, D15 | D8's 102 tasks from 44 papers. Process to borrow: Hugging Face copy holds inputs only while gold programs and eval data sit in a password-pr |
| [allenai/discoverybench](https://github.com/allenai/discoverybench) | 167 | 2025-06-09 | NOASSERTION | stale | D6 | D6's 264 real tasks derived from published papers plus 903 synthetic tasks, with agents/ and eval/ folders (LICENSE file is ODC-By; GitHub r |
| [Future-House/BixBench](https://github.com/Future-House/BixBench) | 154 | 2025-10-06 | Apache-2.0 | stale | D19 | FutureHouse's BixBench (D19): Jupyter-notebook analysis capsules with open-answer and multiple-choice grading, plus a custom agent harness.  |
| [zjunlp/DataMind](https://github.com/zjunlp/DataMind) | 154 | 2026-09-29 | NONE | no license | D21, D24 | Zhejiang University data-analysis agent repo; it is the only GitHub link on D24's first page (LongDS-Bench: 68 multi-turn tasks from Kaggle  |
| [LiqiangJing/DSBench](https://github.com/LiqiangJing/DSBench) | 132 | 2025-08-17 | NOASSERTION | stale | D3 | D3's 466 analysis and 74 modelling tasks from ModelOff and Kaggle (LICENSE file is MIT; GitHub reports NOASSERTION). README says OpenAI used |
| [yiyihum/da-code](https://github.com/yiyihum/da-code) | 108 | 2026-01-12 | MIT |  | D2 | D2's 500 data-wrangling, ML and EDA tasks with a per-task evaluation config, gold files and a timeout per run. Borrow: scorers per output ty |
| [mitdbg/Kramabench](https://github.com/mitdbg/Kramabench) | 79 | 2026-07-24 | NONE | no license | D10 | D10's 104 end-to-end pipeline tasks (633 sub-tasks, 1.7 GB) with reference pipelines, so intermediate steps are scored as well as the final  |
| [xxxiaol/QRData](https://github.com/xxxiaol/QRData) | 49 | 2025-02-18 | NOASSERTION | stale | D14 | D14's 411 statistics and causal questions with gold answers in benchmark/QRData.json plus eval.py (3 percent numeric tolerance); built from  |
| [behavioral-data/BLADE](https://github.com/behavioral-data/BLADE) | 40 | 2024-10-25 | Apache-2.0 | stale, also 08 | D7 | D7's 12 datasets with expert "multiverse" ground truth (variables, transformations, models chosen by independent analysts); code Apache-2.0, |
| [MetaCopilot/dseval](https://github.com/MetaCopilot/dseval) | 34 | 2024-06-24 | MIT | stale | D5 | D5's DSEval toolkit and four problem sets (Exercise, SO, LeetCode, Kaggle; 187, 202, 40, 396 problems per README) with validators that go be |
| [uiuc-kang-lab/ELT-Bench](https://github.com/uiuc-kang-lab/ELT-Bench) | 32 | 2026-11-17 | NONE | no license | D13 | The data-engineering benchmark audited in D13; README links REPRODUCE.md with the commands for every experiment and mentions mutation operat |
| [benjamin-kohler/social_science_replicability](https://github.com/benjamin-kohler/social_science_replicability) | 30 | 2026-11-20 | NONE | no license | D22 | ETH Zurich code for D22: extract methods from a paper, run the agent with information isolation (no original code or results), compare cell  |
| [MMTU-Benchmark/MMTU](https://github.com/MMTU-Benchmark/MMTU) | 23 | 2025-12-11 | NONE | no license | D18 | MMTU (D18, Microsoft and U. Michigan): 28,000+ table questions over 25 tasks with automatic graders (NeurIPS 2025). Lesson: even GPT-5 score |
| [XinmingTu/BenchGuard](https://github.com/XinmingTu/BenchGuard) | 16 | 2026-11-16 | NOASSERTION |  | D15 | D15's benchmark auditor, shipped as a Claude Code plugin (/benchguard-skill:audit-benchmark) that cross-checks the instruction, reference so |
| [kenqgu/RADAR](https://github.com/kenqgu/RADAR) | 14 | 2025-07-31 | Apache-2.0 | stale | D17 | RADAR (D17, Google Research / UW): programmatic injection of missing values, outliers and logical inconsistencies into real tables, with 260 |
| [uiuc-kang-lab/REPRO-Bench](https://github.com/uiuc-kang-lab/REPRO-Bench) | 11 | 2025-11-03 | NONE | stale, no license |  | REPRO-Bench (Hu et al. 2025, UIUC, arXiv:2507.18901, catalogued in folder 06): 112 social-science papers with reproduction packages and publ |
| [AMA-CMFAI/DSAEval](https://github.com/AMA-CMFAI/DSAEval) | 5 | 2026-08-27 | NONE | no license | D25 | DSAEval (D25, PolyU): 641 data-science problems over 285 datasets run in a Jupyter-kernel sandbox, scored by two LLM judges on reasoning, co |
| [vis-nlp/DSAgentBench](https://github.com/vis-nlp/DSAgentBench) | 5 | 2026-09-27 | Apache-2.0 |  | D27 | DSAgentBench (D27, York U. VIS-NLP lab): 275 end-to-end data-science workflow tasks on an OSWorld-based desktop (Jupyter, VS Code, terminal, |
| [trl-lab/ds-agent-failures](https://github.com/trl-lab/ds-agent-failures) | 0 | 2026-11-04 | MIT |  | D23 | Test suite from D23 (CWI): six controlled tests for data leakage and bad validation in agent-written pipelines, plus a failure-mode taxonomy |

### 08. Reproducibility and research integrity (15)

| Repo | Stars | Last push | License | Flags | Papers | What it is |
|---|---:|---|---|---|---|---|
| [the-turing-way/the-turing-way](https://github.com/the-turing-way/the-turing-way) | 2206 | 2026-11-14 | NOASSERTION |  |  | Community handbook on reproducible, ethical, collaborative data science; chapters and checklists to mine for the new-study checklist; licenc |
| [google-research/rliable](https://github.com/google-research/rliable) | 876 | 2024-08-12 | Apache-2.0 | archived, stale | R22 | Library from R22 (Agarwal): interval estimates, performance profiles and interquartile-mean aggregation for few-run results; borrow the stra |
| [facebookresearch/aira-dojo](https://github.com/facebookresearch/aira-dojo) | 180 | 2026-04-14 | NOASSERTION |  | R26 | Meta FAIR code for R26: AI research agents as search policies on MLE-bench with validation-vs-test selection experiments; read for how it se |
| [masurp/specr](https://github.com/masurp/specr) | 73 | 2026-10-16 | GPL-3.0 |  | R1 | R specification-curve package (define, run and plot all specifications); GPL-3.0 so tool not copy source; pairs with the specification-curve |
| [MUCollective/multiverse](https://github.com/MUCollective/multiverse) | 67 | 2026-09-11 | GPL-3.0 |  |  | R package that declares alternative analysis branches at each decision point and returns every outcome; GPL-3.0 so use as a reference or ext |
| [uwdata/boba](https://github.com/uwdata/boba) | 65 | 2021-04-25 | BSD-3-Clause | stale |  | Multiverse DSL: one template script plus a JSON of decision points compiles every universe, runs them all and merges outputs into one table; |
| [aeturrell/specification_curve](https://github.com/aeturrell/specification_curve) | 33 | 2026-11-20 | NONE | no license |  | Python specification-curve package, actively pushed; no detected license so read only; its API shows what a study agent should emit (all spe |
| [nbreznau/CRI](https://github.com/nbreznau/CRI) | 26 | 2025-01-06 | CC0-1.0 | stale | R11 | Data and workflow of R11 (73 teams): numbered literate notebooks with rendered HTML beside each, relative paths, Binder runtime pinned to a  |
| [janetmalzahn/llm-phacking](https://github.com/janetmalzahn/llm-phacking) | 18 | 2026-03-03 | MIT |  | R5 | Replication archive for R5. Borrow: its prompt matrix (2 framings x 4 nudges x 10 runs) is a ready red-team test for our study agent; every  |
| [codecheckers/codecheck](https://github.com/codecheckers/codecheck) | 12 | 2026-11-20 | NOASSERTION |  |  | CODECHECK process: an independent person re-runs the authors' code, lists the reproduced outputs in a manifest (codecheck.yml) and issues a  |
| [fusion-jena/computational-reproducibility-pmc](https://github.com/fusion-jena/computational-reproducibility-pmc) | 11 | 2024-11-22 | GPL-3.0 | stale | R28 | Pipeline of R28: finds notebooks linked to articles, installs declared dependencies, re-executes them and compares outputs; model for the ki |
| [codecheckers/register](https://github.com/codecheckers/register) | 7 | 2026-11-20 | NOASSERTION |  |  | Public register of CODECHECK certificates; shows how independent reproduction results are logged and published; borrow the register idea for |
| [egouldo/ManyAnalysts](https://github.com/egouldo/ManyAnalysts) | 5 | 2024-09-27 | GPL-3.0 | stale | R16 | Reproducible manuscript and analysis code for R16 (174 analyst teams); a worked model of how to report heterogeneity across analysts in a re |
| [zachrewolinski/stat-genie](https://github.com/zachrewolinski/stat-genie) | 3 | 2026-05-26 | NONE | no license | R4 | Code for R4: perturbation and null-shuffle sanity checks run through the Codex CLI on BLADE datasets; borrow the idea of a null arm that nee |
| [ml-preregister/preregistration-template](https://github.com/ml-preregister/preregistration-template) | 3 | 2023-12-06 | MIT | stale |  | Two-form markdown preregistration for predictive modelling (form A at start, form B before model testing) timestamped by git history, the sa |

### 09. Evaluation, reliability and cost (18)

| Repo | Stars | Last push | License | Flags | Papers | What it is |
|---|---:|---|---|---|---|---|
| [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | 80226 | 2026-11-20 | Apache-2.0 |  | F23 | Context-compression layer for tool outputs and logs (library, proxy, MCP server), named in F23 as a similar approach to its harness-side cos |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 63637 | 2026-11-21 | NOASSERTION |  | F7, F15 | Proxy that tracks spend per key; F15 names it as a documented way to attribute Claude Code spend. Borrow: a per-run key as the unit for cost |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | 37684 | 2026-11-21 | NOASSERTION |  |  | Open-source tracing and cost tracking for LLM apps (traces, per-model cost, evals). Borrow: one trace per kit run with cost attached, as the |
| [snarktank/ralph](https://github.com/snarktank/ralph) | 22313 | 2026-02-02 | MIT |  | F3, F4 | The plain Ralph pattern: each iteration is a fresh instance with clean context, and memory lives only in git history, progress.txt and prd.j |
| [ccusage/ccusage](https://github.com/ccusage/ccusage) | 19530 | 2026-11-21 | MIT |  | F12, F15 | Reads Claude Code's local JSONL logs to report tokens and dollars (it has daily and monthly reports). Borrow: the per-run $ and token accoun |
| [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) | 9738 | 2026-11-14 | MIT |  |  | Autonomous loop around Claude Code with a dual-condition exit gate (completion indicators AND an explicit EXIT_SIGNAL), a circuit breaker fo |
| [facebookresearch/meta-agents-research-environments](https://github.com/facebookresearch/meta-agents-research-environments) | 581 | 2026-09-30 | MIT |  | F26 | Meta's ARE platform and Gaia2 benchmark (F26): environments with verifiers, asynchronous events and time limits, budget-scaling curves. Borr |
| [METR/eval-analysis-public](https://github.com/METR/eval-analysis-public) | 348 | 2026-03-06 | NONE | no license | F1 | Code and run data behind the F1 time-horizon curves (logistic fit of success against log human minutes, hierarchical bootstrap, DVC pipeline |
| [chroma-core/context-rot](https://github.com/chroma-core/context-rot) | 323 | 2025-09-03 | MIT | stale |  | Scripts to replicate Chroma's context-rot report: needle-in-haystack variants, LongMemEval and repeated-words tasks at growing input length. |
| [microsoft/lost_in_conversation](https://github.com/microsoft/lost_in_conversation) | 308 | 2026-06-09 | MIT |  | F16 | Simulation code and data for F16 (sharded underspecified multi-turn tasks, 200,000+ simulated conversations). Borrow: the sharding idea for  |
| [METR/RE-Bench](https://github.com/METR/RE-Bench) | 171 | 2026-10-20 | NOASSERTION | archived | V37 | METR's RE-Bench tasks (named in V37 as a source of the MALT transcripts); the repo is archived and has no description, so check its README a |
| [microsoft/AgentRx](https://github.com/microsoft/AgentRx) | 168 | 2026-09-14 | MIT |  | F39 | Code for AgentRx (F39): constraint checks over failed trajectories to localise the first unrecoverable step; a candidate post-run diagnosis  |
| [TransluceAI/docent](https://github.com/TransluceAI/docent) | 150 | 2026-11-13 | NOASSERTION |  | F7 | Platform for reading agent transcripts at scale with custom rubrics; the tool HAL (F7) used to find shortcuts, tool-call failures and recove |
| [METR/vivaria](https://github.com/METR/vivaria) | 145 | 2026-10-07 | MIT | archived | F1 | METR's former evaluation and elicitation platform (task standard, web UI, CLI); archived, and its README says METR is moving its internal to |
| [ulab-uiuc/AgentDebug](https://github.com/ulab-uiuc/AgentDebug) | 108 | 2026-03-30 | MIT |  | F5 | Taxonomy (17 error types in 5 modules), 200 annotated failure trajectories and the AgentDebug pipeline from F5. Borrow: the taxonomy as the  |
| [McGill-DMaS/ODCV-Bench](https://github.com/McGill-DMaS/ODCV-Bench) | 15 | 2026-11-08 | MIT |  | F11 | 40 sandboxed bash scenarios where a KPI conflicts with a safety rule (F11), each in Mandated and Incentivized wording, scored by a four-mode |
| [YangzeLiu/eval-instrument-disclosure](https://github.com/YangzeLiu/eval-instrument-disclosure) | 0 | 2026-11-03 | NONE | no license | F12 | Reproduction scripts and maintainer reports behind F12, with dated correction notes after HAL's maintainers replied (a September per-model r |
| [earino/identical-runs-different-results](https://github.com/earino/identical-runs-different-results) | 0 | 2026-09-25 | MIT |  | F24 | Data, code and delivered programs for F24 (584 runs, 52 repeats per pairing). Borrow: the repeat-until-resolved design and the compliance ch |

<!-- GENERATED: tables end -->
