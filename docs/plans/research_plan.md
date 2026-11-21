# The research plan (ROADMAP Phases 4.6–8)

> Written 2026-11-21, approved by Sharif the same day ("yes"), with two additions from him: study
> open-source repos for their process and lessons, not only their code; and find out now whether a
> plugin can stand up the whole agent team. Then a third: start from our own skills (agent-team,
> shipping and development flywheel with its hackathon mode, parallel-agent-orchestration, and the
> rest), because they hold lessons from real runs.

## The goal

Before designing the kit, learn what is already known about getting AI agents to build working apps
and do accurate research on their own. Copy what works, avoid what fails, and only test ourselves
what nobody has answered.

## The 9 topics, each with one question

| # | Topic | The question it answers |
|---|---|---|
| 01 | How agents are built | Which agent designs hold up outside demos? |
| 02 | Claude Code setup | What Claude Code setup makes long, unattended runs work? |
| 03 | Coding agents | How far can one coding agent get on real bugs, and what helps it most? |
| 04 | Agent teams | Does a team of specialised agents beat one strong agent? |
| 05 | Testing and checking | Which checks catch an agent's bugs before a human does? |
| 06 | AI scientists | Can an agent produce research findings that hold up? |
| 07 | Data analysis agents | How accurate are analysis agents on questions with known answers? |
| 08 | Research integrity | What stops an analysis, human or AI, from finding what it wanted? |
| 09 | Failure and cost | How and why do agents fail on long tasks, and what does a task cost? |

## The founding question: can a plugin stand up the team? (row 4.8, now)

Sharif, 2026-11-21: the kit may need four or more agents (Main, builder, QA, a tester that uses the
app like a real user, and others), each with its own prompt, information and a shared registry. Can
the plugin create all of that inside Claude Code, or do we need a different framework?

Answered with two things, not opinion:
1. **The documented facts:** what a plugin can ship and start (agents, skills, hooks, scripts,
   commands, background sessions, Agent SDK, agent teams), from the official Claude Code docs.
2. **A hands-on test:** a throwaway plugin that, from one command, creates the team's files
   (prompts, registry), starts separate agents for Main, builder, QA and tester, and shows they can
   pass work to each other, unattended.

The answer is one of: **plugin alone works**; **plugin plus a launcher script**; **plugin is the
wrong wrapper** (then another framework, e.g. the Agent SDK). If it is anything but the first, Sharif
hears it the same day (red flag rule), because it changes the deliverable (D1).

## The steps

0. **Our own playbook first (row 4.9).** Inventory the skills in `.claude/skills/`, the ones built
   from real projects: `agent-team` (roles, handoffs, registry, lessons, Pitwall retro),
   `shipping-flywheel` and `development-flywheel` (with its hackathon mode), `pm-lead-session`,
   `parallel-agent-orchestration`, `solo-sprint-dispatch`, `autonomous-plan`,
   `autonomous-hardening-loop`, `research-report` and the rest. For each: what it does, which kit
   part it could become, and the lessons it already carries. The research then checks these against
   the papers and repos instead of starting from zero. The inventory stays local (the skills hold
   personal details); the review cites it in scrubbed form.
1. **Trial topic (02)** and the **plugin test (4.8)**, in parallel with step 0.
2. **Independent check of the trial:** a separate agent re-downloads 3 papers at random and confirms
   they are real and say what we claimed. Fails → fix the scout's instructions, run again.
   **Report to Sharif:** what it found, time, cost, and the plugin test's answer, before going on.
3. **The other 8 topics**, two batches of four, each checked the same way.
4. **GitHub survey:** merge every repo found, re-check each on GitHub, keep the best ~20 as local
   copies. **For each kept repo, write down its process and its lessons learned:** how its agents
   are organised and handed work, how it tests and reviews, and what its contributor guides, design
   docs, postmortems and recurring issues say went wrong. These lessons feed the kit design, like
   the papers do.
5. **The literature review:** one document that pulls it all together: what the evidence says per
   topic, the repo lessons, and what both mean for how we build the kit.
6. **Final independent check** of all of the above, then Marketing's post #2.

Then Phase 9 designs the kit from the review.

## The rules every research agent follows

- No paper counts unless the agent fetched it in that run. No citing from memory.
- Every number is quoted from the paper, with where it appears.
- Every topic summary has a "the catch" section: what the evidence does not prove.
- GitHub stars are never evidence that something works.
- PDFs stay on Sharif's machine; the public repo lists the papers with links.

## Flowchart

```
 Sharif: go
     |
     +----------------------------+
     v                            v
 +-----------------+     +-----------------------+
 | trial: topic 02 |     | plugin test (4.8):    |
 +--------+--------+     | docs + hands-on build |
          v              +-----------+-----------+
 +------------------+                |
 | independent check|                |   not "plugin alone works"
 +--------+---------+                +----------------------------> tell Sharif same day
          | pass                     |
          v                          v
 +------------------------------------------+
 | report to Sharif: papers, time, cost,    |
 | plugin answer                            |
 +--------------------+---------------------+
                      v
 +-----------------------+   +----------------------+   +--------------+   +---------------+
 | 8 topics, 2 batches   |-->| GitHub survey +      |-->| literature   |-->| final check   |
 | of 4, each checked    |   | process and lessons  |   | review       |   | + post #2     |
 +-----------------------+   +----------------------+   +--------------+   +---------------+
                                                                                  |
                                                                                  v
                                                                        Phase 9: design the kit
```

## Where it ends up

```
literature/
├── 01_.../ … 09_.../README.md    # one summary per topic (PDFs stay local)
├── papers.tsv                    # every paper, with links
└── LITERATURE_REVIEW.md          # the write-up that pulls it all together
public/
├── _candidates/01-09.tsv         # repos found, per topic
└── _README.md                    # per kept repo: what it does, its process, its lessons learned
PUBLIC_REPOS.md                   # the GitHub survey
research/spikes/plugin_team.md    # the plugin test: what was tried, evidence, the answer
.agents/playbook_inventory.md     # LOCAL: our own skills, what each could become in the kit, their lessons
```

## Derisking (in order)

| # | What it proves | How | Pass | If it fails → |
|---|---|---|---|---|
| R1 | One scout meets the contract | trial topic 02 + independent check | checker PASS; ≥ 8 verified; 3/3 spot checks match | fix the scout prompt, rerun once, then tell Sharif |
| R2 | A plugin can stand up the team | plugin test (4.8) | team files created and ≥ 4 separate agents hand work to each other, unattended | tell Sharif the same day; propose the framework that does work |
| R3 | Scouts work in parallel | batch 1 (4 topics) | all 4 pass the checker; rows merge with 0 clashes | fix the merge step before batch 2 |
| R4 | End to end | all 9 topics + survey + review | every criterion below PASS | evaluator's recommendations, fix rounds |

## How we will know it is done

| What must be true | The bar | How measured |
|---|---|---|
| Our own skills are inventoried | every skill in `.claude/skills/` has a row: purpose, kit part, lessons | row count = skill count |
| The plugin question is answered with evidence | a written answer backed by a test run log | `research/spikes/plugin_team.md` |
| Every topic is covered | 9 summaries, ≥ 8 checked papers each (≥ 90 total) | `verify_literature.py --all` |
| The papers are real | checker PASS; evaluator spot checks match | evaluator re-fetches a random sample |
| Repos are real and current | ≥ 60 repos, metadata from GitHub | `gh api` re-check |
| Repo lessons are captured | every kept repo has process + lessons sections | count in `public/_README.md` |
| The review cites only real sources | 0 citations not on the paper list | citation check script |
| Someone else checked it | final grade from an agent that did not do the work | evaluator scorecard |
