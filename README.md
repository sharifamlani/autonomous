# Autonomous

**A Claude Code kit for autonomous app development and autonomous research, built in public.**

Give Claude Code an app idea and walk away; come back to a working app that an agent has tested live,
with the review verdicts and evidence attached. Give it a research question and data; come back to a
pre-registered, reproducible study whose numbers check out. That is the goal. This repo builds the
kit, measures whether it works, and shares it.

> **Status: early.** The research foundation is being built (literature, GitHub survey, protocols).
> The plugin is not installable yet. Progress: [`ROADMAP.md`](ROADMAP.md) §0.

## What you will get

| Part | What it is | Status |
|---|---|---|
| **The kit** | An open-source Claude Code plugin: `/autonomous:new-app` and `/autonomous:new-study` | planned (v0.1) |
| **The benchmark** | Public tasks (app specs with scripted user walks, studies with known answers) run unattended and scored per version on success, accuracy, cost, hours and human interventions | planned (v0.1) |
| **The showcase** | The apps and studies the kit made, a short white paper, and the build log | planned |

## How it is built

- **Evidence first.** Every design choice cites a paper in [`literature/`](literature/README.md), a
  surveyed GitHub repo in [`public/`](public/_README.md), or one of our own pre-registered studies in
  `research/`. A README's claims or a star count are not evidence.
- **Two factories.** App work runs a build → independent review → live user walk → release loop.
  Research runs a pre-register → log every trial → one held-out look → reproducible report loop.
- **Independent grading.** Every milestone is graded against written criteria by an evaluator agent
  that did not do the work.

## Repo map

| Path | What is there |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | The rules: goals, protocols, conventions |
| [`ROADMAP.md`](ROADMAP.md) | The build sequence and where we are |
| [`literature/`](literature/README.md) | Papers by theme, with a verified catalogue |
| [`public/`](public/_README.md) | Third-party GitHub repos we read and borrow from (clones local, manifest committed) |
| `research/` | Studies: templates, trial log, one folder per study |
| `scripts/` | `new_study.py`, `sync_public_repos.sh`, `literature/verify_literature.py` |

## Setup (for working on the repo)

```
git clone https://github.com/sharifamlani/autonomous && cd autonomous
bash scripts/sync_public_repos.sh                     # refill public/ at the pinned commits
python scripts/literature/verify_literature.py --all  # check the literature library
python scripts/new_study.py <slug> --title "<title>"  # start a study
```

## License

[MIT](LICENSE). Third-party code in `public/` keeps its own license.
