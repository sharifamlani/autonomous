# Kit v0.1 architecture: the starting design we iterate on

**Companion to** `docs/plans/09_kit_v01_design.md` (the why, the benchmark, the criteria). This file
is the **how**: components, the run folder, the state machines, the file contracts, who may touch
what, and the knobs we will turn when we iterate. Every choice cites the lesson (L1–L11, CLAUDE.md
§0.5) or spike that drives it. Anything marked **[iterate]** is a deliberate first guess the
benchmark will test.

## 1. The core choice: the conductor is code, the players are agents

```
   An orchestra: the score and the conductor's baton are fixed in advance; the musicians play.
   Nobody lets the violinist decide that the concert went well.
```

The control loop (what runs next, when to retry, when to stop, whether the work passed) is a
**deterministic Python state machine** (`team.py`). The agents do the creative work (write the
spec, write code, review, use the app, analyse data) and hand back **files**. The orchestrator
moves to the next state only on a machine-readable verdict file, never on an agent saying "done".

Why: the review's strongest finding is that agents fail when they decide their own success (L1, L2),
and that deterministic controls beat model judgment for permissions and flow (L7). A loop in code
also makes every run comparable and every change a one-line config diff (L10).

**[iterate]** An LLM "Main" that decides the flow is a later benchmark arm, not the default.

## 2. Components

```
 +-----------------------------------------------------------------------------------------+
 |  USER: /autonomous:new-app "<idea>"   or   /autonomous:new-study "<question>" <data>   |
 +--------------------------------------------+--------------------------------------------+
                                              v
 +--------------------------------------------+--------------------------------------------+
 | 1. ENTRY SKILL (plugin/skills/new-app|new-study/SKILL.md)                               |
 |    thin: validates input, creates the run folder, starts team.py in the background,    |
 |    waits, then summarises RUN_REPORT.md for the user. Holds no control logic.          |
 +--------------------------------------------+--------------------------------------------+
                                              v
 +--------------------------------------------+--------------------------------------------+
 | 2. ORCHESTRATOR  team.py  (deterministic state machine + process supervisor)            |
 |    reads kit.toml -> runs the pipeline -> starts one `claude -p` per role step ->       |
 |    enforces caps -> reads verdict files -> writes run.json, ledger.tsv, RUN_REPORT.md   |
 +------+----------------------+----------------------+----------------------+-------------+
        v                      v                      v                      v
 +-------------+      +----------------+      +----------------+      +----------------+
 | 3. ROLES    |      | spec-writer    |      | builder        |      | qa  ||  tester |
 | (agents/*.md|      | analyst        |      | (app/ only)    |      | replicator     |
 |  + prompts) |      +-------+--------+      +-------+--------+      +-------+--------+
 +-------------+              |  every tool call passes through        |
                              v                                        v
 +-----------------------------------------------------------------------------------------+
 | 4. POLICY  hooks/gate.py  (PreToolUse + PermissionRequest)                              |
 |    knows the role from AUTONOMOUS_ROLE (set by team.py); enforces folder fences and the |
 |    command allow-list; logs every allow/deny to gate.log. No model judgment.            |
 +--------------------------------------------+--------------------------------------------+
                                              v
 +-----------------------------------------------------------------------------------------+
 | 5. RUN FOLDER  runs/<id>/  (the shared board: all state and handoffs are files)         |
 +-----------------------------------------------------------------------------------------+
                                              ^
 +--------------------------------------------+--------------------------------------------+
 | 6. BENCHMARK  benchmark/run.py + graders (outside the kit; reads the run folder after)  |
 +-----------------------------------------------------------------------------------------+
```

| Component | Owns | Never does | Lesson |
|---|---|---|---|
| Entry skill | user I/O, starting and summarising | decides pass/fail | L1 |
| team.py | flow, caps, verdict reading, cost sums, the report | writes app code or judges quality | L1, L7, L8 |
| Roles | one job each, output files in a fixed format | read files outside their fence; change state | L1, L3, L5 |
| gate.py | permissions, fences, logging | ask a model whether something is allowed | L7 |
| Run folder | all state | hold secrets (env vars stay in the process) | — |
| Benchmark | grading, scorecards, trial log | ship inside the plugin | L10, L11 |

## 3. The run folder (the shared board)

```
runs/<YYMMDD-HHMM>-<slug>/            # short path (Windows long-path limit, spike 4.8)
├── run.json          # id, kind, task, arm, kit version, model per role, caps, state, status
├── kit.toml          # the exact config this run used (copied in; the iteration knob)
├── registry.json     # per role step: session_id, pid, started, ended, exit, cost_usd, turns
├── ledger.tsv        # append-only: time, role, event, cost_usd, cumulative_usd
├── gate.log          # every hook decision: time, role, tool, target, allow|deny, rule
├── spec/             # spec.md (features, user walks), rubric.md (QA's checklist)
├── checks/           # HIDDEN from builder: walk.yaml (tester's steps + expected state),
│                     #   api_tests/ (pytest), created by spec-writer before any code
├── app/              # git repo; the builder's only writable folder
├── handoffs/         # NNN-<from>-<to>.md, append-only notes between roles (context, repros)
├── evidence/r<N>/    # test output, screenshots, walk logs, per round
├── verdicts/         # r<N>-qa.json, r<N>-tester.json (the only thing team.py acts on)
└── RUN_REPORT.md     # written by team.py from the files above, never by an agent
```

The study kind swaps `spec/ checks/ app/` for `data/dev/`, `sealed/` (held-out, analyst cannot
read), `study/` (PREREG.md, analysis.py, replicate.ipynb, TRIAL_LOG.tsv, RESULT.md).

## 4. new-app: the state machine

```
 INIT --> SPEC --> SPEC_CHECK --> BUILD(r) --> CHECK(r) --+--> both PASS ----------> REPORT: DONE
            |          |              ^          QA || TEST|
            |          |              |                    +--> any FAIL, r < R ----> BUILD(r+1)
            |          |              +--- repro + verdicts ---+
            |          |                                   +--> any FAIL, r = R ----> REPORT: STUCK
            |          +-- checks don't run / not tied to spec --> SPEC (once) --> REPORT: STUCK
            +-- builder/any role writes STUCK.md -----------------------------------> REPORT: STUCK
   any state: $ cap, wall-clock cap, turn cap, or 3 identical errors ---------------> REPORT: CAP
```

| State | Who runs | Input | Output (contract) | Exit rule (team.py) |
|---|---|---|---|---|
| SPEC | spec-writer | idea | `spec/spec.md`, `spec/rubric.md`, `checks/walk.yaml`, `checks/api_tests/` | files exist and parse |
| SPEC_CHECK | team.py | checks | checks run against an empty app and **fail** (proves they test something) | all checks fail on empty app |
| BUILD(r) | builder (resumed each round with `--resume`) | spec, rubric, prior verdicts and repros | commits in `app/`, `evidence/r<N>/build.txt` (its own test run), `app/RUN.md` (how to start it) | commit exists + RUN.md parses |
| CHECK(r) | qa and tester **in parallel**, fresh sessions | app at the commit sha | `verdicts/r<N>-qa.json`, `verdicts/r<N>-tester.json` + evidence | both files valid JSON |
| REPORT | team.py | everything | `RUN_REPORT.md`, final `run.json.status` | — |

- **R = 3 rounds** **[iterate]**. The builder keeps its context across rounds; checkers start fresh
  every round so they don't anchor on last round's story (L4).
- The builder **may run its own app and its own tests** (L3) but cannot read `checks/` (L1).
- QA reads the diff and runs the tests against `rubric.md`; it reads the builder's handoff note
  only **after** writing its verdict draft (L4).
- The tester starts the app from `RUN.md` and walks `walk.yaml` with CUA in an isolated Chrome
  profile (D7), one screenshot per step. Playwright is the fallback for web apps **[iterate]**.

## 5. new-study: the state machine

```
 INIT --> SEAL --> PREREG --> COMMIT --> DEV(t) --> LOOK --> REPLICATE --> REPORT: DONE | STUCK | CAP
```

| State | Who runs | Output (contract) | Exit rule (team.py) |
|---|---|---|---|
| SEAL | team.py (`seal.py`) | `data/dev/`, `sealed/heldout.*` (outside analyst's fence), split hash in run.json | hash recorded |
| PREREG | analyst | `study/PREREG.md` (hypothesis, estimand, decision rule, analysis.py interface) | required headings present |
| COMMIT | team.py | git commit of PREREG; sha + time in run.json | commit exists; **sealed/ untouched** (gate.log) |
| DEV(t) | analyst | `analysis.py` run on dev; one TRIAL_LOG row per trial | trial cap (default 10) **[iterate]** |
| LOOK | team.py, not the analyst | runs `analysis.py --split heldout` **once**; output to `study/heldout_result.json` | runs once; a second run is refused |
| REPLICATE | replicator (fresh session, copy of `study/`) | Run All of `replicate.ipynb`; `verdicts/replicate.json` comparing every number in the RESULT draft | every number matches within rounding |
| REPORT | analyst writes RESULT.md prose; team.py writes RUN_REPORT.md | — | — |

## 6. File contracts (what makes the loop deterministic)

**Verdict** (`verdicts/r<N>-<role>.json`), the only thing team.py acts on:

```json
{ "role": "tester", "round": 2, "sha": "3f9c2e1",
  "verdict": "FAIL",
  "checks": [ { "id": "W3", "status": "FAIL", "expected": "total shows $42.50",
                "observed": "total shows $40.00", "evidence": "evidence/r2/W3.png" } ],
  "repro": "1. Add Ann $20, Bob $22.50  2. Open Summary  3. Total reads $40.00",
  "notes": "free text, ignored by team.py" }
```

Rules: `verdict` is `PASS` only if every check is `PASS` **and** each has an evidence file that
exists (team.py verifies the files, L2). A missing or malformed verdict counts as `FAIL`, loudly
(L8). Every claim is labelled `observed` (seen in the running app) or `inferred` (read from code);
only observed checks can pass the tester's verdict (idea borrowed from rea, §9).

**STUCK.md** (any role): what was tried, the blocking fact, what a human would need to decide.
The prompt tells every role this is an honourable exit, better than a forced pass (L8).

**Handoff** (`handoffs/NNN-<from>-<to>.md`): free text for context. team.py never parses it.

## 7. Roles

| Role | cwd | Can read | Can write | Tools | Max turns | Produces |
|---|---|---|---|---|---|---|
| spec-writer | `spec/` | idea | `spec/`, `checks/` | Read, Write, Edit, Bash (allow-list) | 60 | spec, rubric, checks |
| builder | `app/` | `spec/`, `app/`, `verdicts/`, `handoffs/` | `app/`, `evidence/`, `handoffs/` | Read, Write, Edit, Bash (allow-list) | 200 | commits, build evidence |
| qa | `app/` (read-only) | `spec/rubric.md`, `app/`, `evidence/` | `verdicts/`, `evidence/` | Read, Bash (tests only) | 60 | QA verdict |
| tester | run root | `spec/`, `checks/walk.yaml`, `app/RUN.md` | `verdicts/`, `evidence/` | CUA, Bash (start app only) | 120 | tester verdict + screenshots |
| analyst | `study/` | `data/dev/`, `study/` | `study/` | Read, Write, Edit, Bash, NotebookEdit | 150 | PREREG, analysis.py, notebook |
| replicator | copy of `study/` | its copy, `data/dev/` | `verdicts/` | Read, Bash, NotebookEdit | 60 | replication verdict |

Same model for every role in v0.1 (decision 9-C). Per-role models are a knob in kit.toml **[iterate]**.

## 8. Policy, caps and supervision

**gate.py** (one script, two hook events):
- **Fences:** path rules per `AUTONOMOUS_ROLE` (table §7). Reads and writes outside the fence are
  denied, including through Bash (`cat`, `cp`, `type`, redirects into fenced paths are matched).
- **Allow-list:** project-local commands (python, node, npm/pnpm, pytest, git without push, the
  app's start command); package installs only from the default registries; no `curl | sh`, no
  `rm -rf` outside the run folder, no network except localhost and package registries **[iterate]**.
- **Logging:** every decision to `gate.log`. A deny tells the agent which rule fired, so it can
  adapt instead of retrying blindly.
- The fences are a seatbelt, not a vault: the review counts sandbox escapes as real (H17); the
  benchmark grader re-checks `checks/` hashes after every run to detect tampering.

**Caps** (team.py, from kit.toml): run $ cap and wall-clock cap (decision 9-B); per-step max turns
(§7); 3 identical consecutive errors ends the step. team.py sums each child session's
`total_cost_usd` from `--output-format json` into ledger.tsv (a parent's cost omits its children,
spike 4.8) and kills the process tree at a cap.

**Launch line per role step** (spike 4.8 shape):
`claude -p "<step task>" --plugin-dir <kit> --append-system-prompt-file prompts/<role>.md
--output-format json --max-turns <n> --model <m>` with cwd and `AUTONOMOUS_ROLE` set; fix rounds add
`--resume <session_id>` from registry.json.

## 9. Ideas borrowed (not dependencies)

| From | Idea | Where it lands |
|---|---|---|
| rea (`morluto/rea`, MIT) `AGENTS.md` | Label every finding as observation, derivation, inference or unknown; never claim a reproduction you did not run | verdict contract §6 (`observed` vs `inferred`) |
| rea | "Real-*" CI lanes that run against real tools, separate from unit tests | benchmark smoke tasks run the real CLI end to end |
| rea agent environments | Turn a recorded web session into a replayable environment with reward checks | later benchmark tasks (Phase 13), not v0.1 |
| mini-swe-agent (review Table 3) | separate caps with a named exit status | caps §8, `CAP` status |
| harbor (review Table 3) | tests copied in only after the agent runs | `checks/` fence + grader re-check |
| RD-Agent (review Table 3) | answer file placed in the workspace only at grading time | `sealed/` + LOOK state |

## 10. The knobs: how iteration works

Everything we expect to change lives in `kit.toml`, so a kit change is a config diff, logged as one
trial and kept only if the scorecard improves (L10):

```toml
[app]
roles        = ["spec-writer", "builder", "qa", "tester"]   # drop "tester" = Future Issue 1 arm
max_rounds   = 3
checker_mode = "parallel"          # or "sequential"
walk_driver  = "cua"               # or "playwright"
[study]
max_dev_trials = 10
replicator     = true
[caps]
app_usd = 30   app_minutes = 120   study_usd = 10   study_minutes = 60
[models]
default = "claude-opus-5-5"        # per-role overrides allowed
[exits]
stuck_exit = true                  # false = Future Issue 3 arm
```

## 11. Deliberately not in v0.1

Built-in agent teams (don't run under `-p`, spike 4.8); an LLM orchestrator; parallel builders and
worktrees (one builder is enough for one small app; L6 applies when we add a second); staging/RC/tag
steps of the full flywheel (one app per run); marketing or auditor roles in the kit (L5); external
MCP servers as dependencies (L7).

## 12. What the user sees: RUN_REPORT.md (the only "UI")

```
# Run 261122-0915-expense-splitter        status: DONE        kit 0.1.0
Idea: "an app where friends log shared expenses and see who owes whom"
Cost $18.40 · 1 h 22 min · 2 build rounds · 0 interventions

Checks (hidden, written before the build)     12/12 PASS (observed in the running app)
  W1 add a person ............ PASS  evidence/r2/W1.png
  W3 totals per person ....... PASS  evidence/r2/W3.png   (FAILED in round 1: $40.00 vs $42.50)
  ...
QA (rubric.md)                                 PASS  verdicts/r2-qa.json
How to run it yourself: app/RUN.md
```

## 13. Risks this architecture must retire first (mapped to the plan's smokes)

| Risk | Smoke |
|---|---|
| team.py can't kill a runaway session tree on Windows | S1 |
| hooks don't see `AUTONOMOUS_ROLE`, or Bash bypasses a fence | S2 |
| the entry skill's background wait dies before team.py finishes (`-p` 10-minute background cap; needs `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`) | S1, S8 |
| CUA walk needs a human for the first-run browser prompt | S4 |
| analyst reaches `sealed/` | S5 |
