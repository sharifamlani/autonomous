# Literature

The evidence base for the repo's North Star: a Claude Code kit that builds working apps and runs
accurate research on its own (CLAUDE.md, Goals). The folders read in the order you would build that
system: **how agents are built → how they build software → how they do research → how they fail and
what they cost.** Every design choice in the kit cites a paper, a public repo, or one of our own
studies in `research/`.

**Start with `LITERATURE_REVIEW.md`** (written in ROADMAP Phase 7): the synthesis of everything below
and what it implies for the kit's agents, prompts and gates. This README is the index and scoreboard.

```
literature/
├── papers.tsv                                   # machine-readable catalogue: one row per paper (verified)
│
│  PART I: FOUNDATIONS (how agents are built and run)
├── 01_Agent_Architectures_and_Orchestration/    # A   ReAct, Reflexion, planning, orchestrator-worker, routing
├── 02_Claude_Code_and_Harness_Engineering/      # H   subagents, skills, hooks, context engineering, SDK, plugins
│
│  PART II: AUTONOMOUS APP DEVELOPMENT
├── 03_Coding_Agents_and_SWE_Benchmarks/         # C   SWE-bench family, SWE-agent, OpenHands, Agentless
├── 04_Multi_Agent_Software_Teams/               # T   role-based teams, code review agents, process
├── 05_Verification_Testing_and_QA/              # V   test generation, mutation testing, LLM-as-judge, GUI/computer-use testing
│
│  PART III: AUTONOMOUS RESEARCH AND DATA SCIENCE
├── 06_AI_Scientist_and_Automated_Research/      # S   end-to-end research agents, idea generation, paper writing
├── 07_Data_Science_and_Analysis_Agents/         # D   data-analysis agents and benchmarks (MLE-bench, DSBench, ...)
├── 08_Research_Integrity_and_Reproducibility/   # R   many-analysts, forking paths, pre-registration, replication
│
│  PART IV: RELIABILITY AND COST
└── 09_Reliability_Long_Horizon_and_Cost/        # F   failure taxonomies, long-horizon autonomy, reward hacking, token cost
```

A folder exists on disk only once its first paper lands. Until then it is listed here as planned.

## Scoreboard

Filled as each folder lands: papers held, verdict on the folder's central question, and the catch.

| Folder | Papers | Central question | Verdict | The catch |
|---|---|---|---|---|
| 01 | — | Which agent architectures hold up outside demos? | — | — |
| 02 | 15 | What configuration of Claude Code makes long unattended runs work? | A lean, measured harness: good tools, small curated skills, old tool output dropped, permissions enforced at each tool call, progress kept in files + git; big generated context files, self-written skills and default multi-agent splits often add cost without gain | Almost no evidence from multi-hour unattended runs; the long-run sources are vendor posts with little data |
| 03 | — | How far can a single coding agent get on real issues, and what drives it? | — | — |
| 04 | — | Do role-based multi-agent teams beat one strong agent? | — | — |
| 05 | — | Which checks catch agent bugs before a human does? | — | — |
| 06 | — | Can an agent produce research whose findings survive review? | — | — |
| 07 | — | How accurate are data-analysis agents against known answers? | — | — |
| 08 | — | What stops an analysis (human or agent) from finding what it wants? | — | — |
| 09 | — | How and why do autonomous agents fail, and what does a task cost? | — | — |

## Conventions

- **Paper IDs** are a folder prefix plus a number (`C4`, `S12`). IDs never change; each prefix lives
  in one folder; new papers take the next free number. A gap is a reserved slot.
- **PDFs are local only** (gitignored): the public repo publishes the indexes and `papers.tsv`, not the
  papers. `scripts/literature/fetch_papers.py` re-downloads every PDF from its `papers.tsv` link.
- **File names:** `<ID>_<FirstAuthor>_<Year>_<Short_Title>.pdf`. A paper we cannot download gets
  `<ID>_<FirstAuthor>_<Year>_<Short_Title>_NOTE.md` with the citation, link and why.
- **Each folder's README** has the same four sections: **Role** (why the folder exists), **Contents**
  (a table: ID, citation, year, link, what it establishes), **What it establishes** (the folder's
  verdict with numbers quoted from the papers), **The catch** (what the evidence does not show).
  Its first line is `# NN <Title>`.
- **`papers.tsv`** columns: `id, folder, first_author, year, title, venue, url, arxiv_or_doi, file,
  verified`. `verified` = the title, first author and year were checked against the fetched source.
  No paper enters without a fetched source: a citation recalled from memory is not evidence.
- **Citing a number:** cite the paper ID and quote the PDF, not a README paraphrase.
- **GitHub repos** found while reading go to `public/_candidates/<NN>.tsv` and, once surveyed, to
  `PUBLIC_REPOS.md`. A repo's stars are never evidence that a method works.
- **Overlap with Trading:** research-integrity and multiple-testing papers already held in
  `Trading/literature/16_Backtest_Validity_and_Sizing` and `17_Research_Factory_Statistics` are
  cross-referenced from folder 08, not duplicated.
- Run `python scripts/literature/verify_literature.py --all` after any change to `literature/`.
