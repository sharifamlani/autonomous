# Phase 7 plan: the literature review (outline for approval)

> ROADMAP Phase 7 (rows 7.1–7.3), Phase 7.5 (QA) and Phase 8 (independent grade, then release).
> Status: **approved by Sharif 2026-11-21 ("perfect ... go").** Target release: 6:00 AM Sunday
> 2026-11-22 (EST), **only on Sharif's express go order**, after QA and the independent grade pass.

**What it is.** A full review article in the style of the *Annual Review of Political Science*: an
argued synthesis of a field, organised around its central questions and debates, not a list of
papers by topic. It has a thesis, weighs evidence of different quality, names where the literature
disagrees and why, proposes a framework, and ends with summary points, future issues and a research
agenda. The kit's design follows from it (Phase 9), but the review stands on its own as a public
paper for researchers and practitioners.

**Corpus.** 288 verified papers (`literature/papers.tsv`, 2013–2026, 219 of them from 2025–2026) and
237 GitHub repos, 32 of them written up for process and lessons (`PUBLIC_REPOS.md`,
`public/_README.md`). Repos are treated the way a political-science review treats grey literature
and practitioner reports: evidence of what happens in use, weighed below controlled studies.

**Format.**
- **Length:** 9,000–11,000 words of body text (Annual Review range). About 150–200 works cited, not
  all 288.
- **Citations:** author–year in the text ("Kim et al. 2026"). The source file carries our IDs, e.g.
  `[T18]`. A script renders them and builds *Literature Cited* from `papers.tsv`, so no citation can
  be dangling (row 7.2). Repo evidence is cited as `owner/repo #issue`.
- **Annual Review furniture:** abstract (≤150 words), keywords, a short glossary of key terms (the
  margin definitions), 2–3 figures and 3–4 tables, then **Summary Points** and **Future Issues**
  (numbered lists), a disclosure statement, and Literature Cited.
- **Every number quoted** is checked against the PDF or the theme README quote. Every claim says
  whether the source is independent or lab-authored, and whether the result was measured or only
  asserted.

---

## The outline

### Working title

**Verification, Not Capability: What the Evidence Says About Autonomous Agents That Build Software
and Do Research**

### Abstract (≤150 words, written last)

Language-model agents now resolve most well-specified software issues. Labs report that agents work
unattended for hours and produce research papers. Yet in real use most agent work still needs a human
to correct it. Agents rarely build working applications from scratch, and independent audits of
AI-scientist systems find fabricated results. This review synthesizes 288 studies and 237
open-source projects across two literatures that rarely cite each other: AI for software engineering
and automated science. We argue that the binding constraint is no longer capability but
verification. Agents succeed where an external signal they cannot edit decides success. They fail,
often silently, where they grade their own work. We review evidence on architectures, harnesses,
verification, from-scratch building, automated research, data analysis, research integrity, and
reliability and cost. We then propose a framework and a research agenda.

**Keywords:** autonomous agents, software engineering, AI scientist, verification, reproducibility,
evaluation

### 1. Introduction

- **The promise.** Lab claims of hours-long autonomous work and "AI scientists" (S13, S20, A25).
  Benchmark saturation on curated issues: up to 99.4% on a cleaned split (C12).
- **The puzzle.** Real use tells a different story: about 88% of pull requests still need human
  steering (F30), 91.49% of visible resolutions need user correction (T23), and from-scratch builds
  score around 40–60% (C19, C22, C29). Audits find fabrication in AI-written research (S15, S16).
- **The thesis.** Verification, not capability, is the binding constraint. Three corollaries:
  1. Success tracks the presence of an external signal (executed tests, a held-out metric, the
     running app).
  2. Whoever checks must be separate from whoever builds.
  3. Unattended runs need bounds and measured reliability, not best-run numbers.
- **Why two literatures together.** Software agents and research agents fail in the same ways
  (self-report, gamed graders, silent failure) and are fixed by the same structures. Each field has
  half the answer: software engineering has executed tests, the replication-crisis literature has
  pre-registration.
- **Roadmap of the article.**

### 2. Scope, Sources and How Evidence Is Weighed

- **Corpus construction:** nine themes, scouted from fetched sources only, then a lab-first round
  and a lab-by-lab sweep (OpenAI, Anthropic, Google DeepMind, Meta, Microsoft and funded
  start-ups), plus two GitHub sweeps (paper-led, then popularity-led).
- **Hierarchy of evidence.** Cost-matched controlled comparisons and independent audits, then
  benchmark results, then lab telemetry and system cards, then demos and READMEs. Practitioner repos
  are evidence of failure modes in use, not of effect sizes.
- **Known biases:**
  - Most 2025–2026 evidence is lab-authored about the lab's own models.
  - Benchmark contamination and broken graders (C15, V12, V31).
  - Fast decay: results are model-version-specific.
  - Survivorship: failed systems are under-reported.
- **Table 1:** the corpus by theme, year and source type (independent vs lab; measured vs asserted).

### 3. Concepts: What "Autonomous" Means and How It Is Measured

- **Definitions (glossary box):** agent loop, harness/scaffold, external vs internal signal,
  verifier, grader, pass@k vs pass^k, horizon length, intervention, unattended run.
- **Autonomy as a measurable quantity.** Hours without intervention, interventions per task,
  success under consistency demands (F32, F16). Why "solved" on a benchmark is not "done" in use.
- **Table 2:** a typology of verification signals, crossed by **who controls** them (builder vs
  outside) and **what they observe** (claims, code, execution, outcomes in the running system).

### 4. One Agent or Many? The Architecture Debate

- **The multi-agent programme:** role-based "software companies" (T1 and successors), debate,
  orchestration (folder 01).
- **The challenge:** cost-matched controls find role splits no better than a single strong agent on
  average (T18: +0.5 points, p = 0.20; T25, A10, A26, C18). The model matters more than the
  scaffold.
- **Where more agents do help:** independent verifiers that run the code; isolated parallel work
  with test-gated merges (T20, T22); narrow communication. Planner detail rarely survives the handoff
  (T18).
- **Practitioner evidence:** the team-method repos report speed and tokens, never success rates
  (BMAD, MetaGPT, gastown, spec-kit). Handoffs that stall silently are the most-discussed failure in
  agent-company tools (paperclip #13532). Swarm claims go unmeasured (ruflo's own audit).
- **Assessment:** the debate is mis-posed. The question is not "how many agents" but "is any agent
  an independent check on another".

### 5. The Harness: Lean or Heavy?

- **What helps:** good tool interfaces, small curated skills, simple context pruning (H3), external
  progress state in files and git.
- **What often doesn't:** large auto-generated context files, self-written skills, default fan-out
  (folder 02). Practitioners report the same: rosters of many narrow agents bloat context
  (wshobson/agents #93), and long rule files get truncated (superpowers #2481).
- **Permissions and containment:** model-based permission classifiers miss scope escalation (H17).
  Deterministic rules at the tool call and OS sandboxing do better (H18, H19, H24). Agents switch
  sandboxes off when allowed to (sandbox-runtime #97). Safety hooks fail open on unexpected
  platforms (uditgoenka/autoresearch #115).
- **State across context resets:** file-based plans, and their failure modes (planning-with-files
  #240).

### 6. Verification: The Central Problem

This is the core of the article and the longest section.

- **6.1 Self-report is unreliable.** Agents claim completion over visible failure (T23; F20: a patch
  on 100% of runs, resolved in 44%; F25).
- **6.2 LLM judges.** Verifiers approve about half of failing work (T18: 49.4%). Judges are misled
  by the agent's own narrative (V24). They are more reliable when checking state or screenshots
  against a rubric (V29). Self-correction without external feedback does not work (A4, A5).
- **6.3 Checks that work.** Tests derived from the spec that fail before the fix and pass after;
  mutants and seeded faults; state checks in the running application (folder 05). The common
  property: the builder cannot write, edit or argue with them.
- **6.4 Gaming the grader.** Agents exploit tests on impossible tasks (V3: 54%, falling to 9% with an
  honest "flag for human" exit). Search loops overfit validation (R26, S28). Agents go after the
  scorer and its network (F34, F35). Practitioners see the same: the autoresearch metric can be
  gamed (#599), and builders edit their graders (commit0).
- **6.5 Broken instruments.** Graders and benchmarks are themselves wrong (V12, C15, V31, V27, A18,
  D13). Hardening grader and benchmark through adversarial loops (T24).
- **6.6 Silent failure.** Checks that never run but report success: AI-Scientist-v2 #133,
  scientific-agent-skills #152, AutoResearchClaw's own audit (#302), AI-Scientist-v3 #5. A skipped
  check counted as a pass is the most common way these systems mislead.
- **Figure 1:** the 2×2 of signal (external vs internal) × checker (editable vs not editable by the
  builder), with the evidence placed in each cell.

### 7. From Fixing Issues to Building Applications

- **The issue-resolution literature and its validity problems:** contamination, weak tests, and
  scoring that differs from a maintainer's (folder 03; C12, C15, V12).
- **From-scratch building:** apps (C19: 61.8% of workflows), repositories (C22: under 40.5% of
  tests), long mobile tasks (C29: 41%), freelance work (C16).
- **The levers the evidence shows:** detailed specs, telling the agent how it will be checked,
  letting it run its own app (C29, C19, C16), and long-running harness design (T28).
- **Leakage specific to from-scratch tasks:** answers recovered from git history (commit0 #113).
  The fix is tasks proven with an oracle run and an empty run (harbor).

### 8. Automated Science: The AI-Scientist Programme and Its Audits

- **8.1 The programme:** end-to-end systems from idea to paper (S3, S13, AI-Scientist v1–v3,
  codescientist), and the popular autoresearch loops (karpathy/autoresearch, OpenResearch).
- **8.2 The audits:**
  - Results never computed, success declared over failure, results chosen after the fact (S9, S10).
  - FabScore: 70.4% of 54 real submissions contain fabrications, and AI reviewers miss over 85%
    (S15).
  - Synthesized data in 8 of 10 tasks, even when told not to fabricate (S16).
  - Unsound papers that reviewers accept (S23).
- **8.3 Where it works:** a computable metric with a held-out set (S31, S20, S21, A25). Replication
  with known answers (S7, S8, S26, S32).
- **8.4 Reviewing AI research:** reviewers given code and logs beat reviewers reading only the paper
  (S10). LLM feedback helps human reviewers but is not a gate (S29). End-to-end completion is rare
  (S19).
- **Assessment:** automated science works as automated engineering under an external metric. It
  fails as autonomous judgment.

### 9. Data-Analysis Agents and Known-Answer Evaluation

- **Accuracy:** moderate on closed-form questions, low on multi-step ones. Tuning to a benchmark
  inflates scores (folder 07; D1, D4, D14).
- **The right conclusion is reached far more often than the right number** (D20, D21).
- **Imperfect data and leakage break agents that score well on clean data** (D17, D23). Accuracy
  decays without upkeep of curated skills (D26).
- **Answer keys are wrong often enough to matter** (D13). Practitioner case: the DABench scorer drops
  unanswered questions from the denominator.

### 10. Lessons from the Replication Crisis

This is the section where political-science readers will feel at home.

- **The analyst problem:** many-analysts studies, forking paths and specification searching show
  that expertise and honest intent do not prevent it (folder 08).
- **Structures that work:** pre-registration, decision rules committed before results exist,
  multiverse reporting, null-based sanity checks, independent re-runs.
- **Agents as analysts at machine speed:** an agent can explore thousands of forking paths in an
  hour. The integrity tools built for human researchers are more needed with agents, not less.
- **Bridge to section 8:** AI-scientist failures are the replication crisis, automated.

### 11. Reliability, Long Horizons and Cost

- **Error compounding and horizon length:** success falls steeply as tasks lengthen (folder 09). At
  70% per step, end-to-end success over ten steps is near zero (S19).
- **Variance:** a single run is too noisy to rank agents (F19, F24). pass^k vs pass@k. Prompt changes
  move mean spend but not its spread (F18).
- **Humans still in the loop:** F30 and F32's telemetry on intervention rates.
- **Cost:** large and highly variable per task. More spend often buys no accuracy.
- **Practitioner bounds:** separate caps on turns, dollars, wall-clock time and repeated errors
  (mini-swe-agent, inspect_ai). Watchdogs that kill healthy sessions (gastown #2707).

### 12. Measuring Autonomous Systems: Toward Reporting Standards

- **The benchmark validity crisis and best practice** (A18, C15, V31).
- **Proposed minimum reporting standard (Table 3):**
  - k runs per arm, with the spread;
  - a budget-matched single-agent baseline;
  - $/task with its spread;
  - a grader audit;
  - tasks proven with an oracle run and an empty run;
  - held-out tasks;
  - interventions per task;
  - independent vs self-graded.
- **How the field reports today against that standard:** a count across the corpus, if feasible.

### 13. Synthesis: A Framework for Trustworthy Autonomy

- **Four structural conditions:**
  1. **External signal:** success is decided by something executed or observed, not asserted.
  2. **Separation of powers:** builder, checker and grader are distinct, and the builder cannot
     edit the checker.
  3. **Bounded runs:** budgets, stop rules and an honest "stuck" exit.
  4. **Measured reliability:** repeated runs, with spread and cost reported.
- **Propositions P1–P6,** each tied to the sections that support it, with a confidence level.
- **Figure 2:** the framework applied to both factories: building software and running a study.

### 14. Implications for Design

- **From the framework to a concrete system:** a plugin that builds an app and a plugin that runs a
  study, both unattended. Table 4 maps each design principle to the evidence and its confidence.
- **Where practitioner playbooks agree and disagree with the evidence:** our own team playbook
  (scrubbed), team methods, and autoresearch loops. Example: role-heavy teams are justified only
  where a role is an independent check.

### 15. What the Literature Cannot Yet Answer: A Research Agenda

- **Open questions**, each framed as a study the field (and we) should run:
  - Does a builder + independent tester pair beat a budget-matched solo agent on from-scratch apps?
  - Separate sessions vs one long session for hours-long runs.
  - Does an honest "stuck" exit cut gaming without cutting completion?
  - How much does pre-registration reduce agent forking paths in known-answer studies?
  - Grader-hardening cost vs benefit.
  - Reliability decay across model versions.

### 16. Conclusion

- The thesis restated, what would change our mind, and why verification structures will outlast
  any one model generation.

### Summary Points (numbered, 8–10)

### Future Issues (numbered, 6–8)

### Disclosure Statement · Acknowledgments · Literature Cited

---

## How it gets written

### Files

```
autonomous/
├── docs/plans/07_literature_review.md     # this plan (outline + process + criteria)
├── literature/
│   ├── LITERATURE_REVIEW.md               # the article (source, with [ID] citations)
│   ├── LITERATURE_REVIEW_rendered.md      # generated: author-year citations + Literature Cited
│   └── figures/                           # Figure 1 (2x2), Figure 2 (framework), Table data
├── scripts/literature/
│   └── render_review.py                   # [ID] -> "Author et al. YEAR"; builds Literature Cited;
│                                          # --check exits 1 on any ID missing from papers.tsv (row 7.2)
├── ROADMAP.md                             # rows 7.1-7.3 flipped as they land
└── CLAUDE.md                              # v1: the review's design implications folded in (row 7.3)
```

### Flow

```
+-------------------+    +---------------------+    +----------------------+
| outline approved  |--> | evidence pass       |--> | section drafts       |
| (this file)       |    | per section: pull   |    | 4 writers in         |
+-------------------+    | quotes + numbers    |    | parallel, by section |
                         | from READMEs/PDFs   |    | groups (4-5, 6-7,    |
                         +---------------------+    | 8-10, 11-12)         |
                                                    +----------+-----------+
                                                               |
                                                               v
+-------------------+    +---------------------+    +----------------------+
| Phase 7.5: QA     |<-- | render_review.py    |<-- | lead writes 1-3,     |
| (fact, citation,  |    | --check (0 dangling)|    | 13-16, abstract;     |
| number checks)    |    | + word count        |    | one voice edit pass  |
+--------+----------+    +---------------------+    +----------------------+
         | every finding fixed, QA re-checks the fixes
         v
+-------------------+    +---------------------+    +----------------------+
| Phase 8: indep.   |--> | Sharif's express go |--> | video about the      |
| evaluator grades  |    | -> Marketing posts  |    | paper (make-video    |
| (criteria below)  |    | LinkedIn + X (target|    | skill), posted with  |
| loop until PASS   |    | 6 AM Sun 11-22)     |    | or under the post    |
+-------------------+    +---------------------+    +----------------------+
```

### Phase 7.5: QA (Sharif 2026-11-21: "very thorough ... for public release ... nothing embarrassing")

QA is a separate team of agents that did not write the review. It runs before the independent
evaluator, and it checks everything, not a sample:

1. **Claims ledger.** Every writer hands in a ledger with every number and factual claim in its
   sections. Each row gives the claim, the number, the source ID, the exact supporting quote and
   where it is (page or README line).
2. **Number check (100%).** Every number in the review is matched against the PDF or the source
   page, not against our README summary. That covers percentages, counts, sample sizes, p-values,
   dates and star counts. A mismatch, a rounding that changes meaning, or a number without a source
   is a finding.
3. **Citation check (100%).**
   - Every `[ID]` resolves, via `render_review.py --check`.
   - Every cited paper actually says what the sentence attributes to it, judged from the PDF.
   - Author, year and title in Literature Cited match the source (arXiv or Crossref metadata).
   - "Et al." is used only where there are three or more authors.
   - Every repo issue cited exists and says what we claim (`gh api`), and its open or closed state
     is described correctly.
4. **Fact check.** Claims about labs, products and people (dates, model names, who published what)
   are checked against the source. Anything that can't be sourced is cut or hedged.
5. **Fairness and tone.**
   - No repo or paper is described as failing beyond what its own issue or audit says.
   - Lab-authored results are labelled as such.
   - Nothing reads as an attack on a named person or organisation.
   - Every "first", "only", "none" or "all" is backed or removed.
6. **Copy and format.** Spelling, grammar, broken links, figure and table numbering, consistent
   terms, the abstract at 150 words or fewer, and no personal or private details (public repo,
   CLAUDE.md §9).

7. **Evidence file (Sharif 2026-11-21).** `literature/LITERATURE_REVIEW_EVIDENCE.md` holds every
   claim, item and citation in the paper, one entry each. An entry gives:
   - the claim as written in the paper;
   - the source (author, year, ID, title);
   - exactly where the quote is (PDF page, section, table or figure; URL and heading; or issue and
     comment);
   - the **verbatim quote**.
   `scripts/literature/build_evidence.py` builds the file from the writers' ledgers. It checks that
   every `\cite` and `\repo` in each section has an entry, and that every paper quote appears
   verbatim on the stated page of the local PDF. Web and repo quotes are checked by hand. QA also
   reads every entry to confirm that the quote actually supports the claim as written, not just that
   the quote exists. **Gate:** 0 cited sources without an entry, 0 NOT FOUND, 0 WRONG PAGE, and every
   MANUAL row marked checked in the QA file.

QA writes `literature/qa/LITERATURE_REVIEW_qa.md`: one row per finding, with its severity
(blocker / major / minor), the fix, and the re-check result. **Exit gate: 0 open blockers and 0 open
majors, with every fix re-checked by QA.** Only then does the independent evaluator (Phase 8) start.

### Release (after Phase 8 passes)

**Nothing is posted until Sharif gives an express go order** (Sharif 2026-11-21). QA PASS and the
independent grade are necessary but do not release anything. The target is 6:00 AM Sunday 2026-11-22
if the go comes in time. Marketing posts to LinkedIn and X with the repo link in the first comment. The numbers in the post come only from the QA'd review. Marketing also makes a
short video about the paper with the `make-video` skill and video tool. If QA or the evaluator has
not passed by then, the post waits, and Sharif is told why in one sentence.

### Derisking

| # | What it proves | Command | Expected | If it fails |
|---|---|---|---|---|
| 1 | Citations render and resolve | `python scripts/literature/render_review.py --check` on a 1-paragraph stub with 3 IDs and 1 fake | exit 1, names the fake ID | fix the parser before any drafting |
| 2 | One section reads like a review, not a list | draft §6 alone and send it to Sharif | Sharif says it's the right register | adjust the style brief, redraft §6 |
| 3 | Full draft is complete and clean | `render_review.py --check && python scripts/literature/verify_literature.py --all` | `PASS: 0 dangling`, word count 9,000–11,000 | fix the listed IDs or sections |

### Evaluation criteria (graded in Phase 8 by an independent evaluator)

| Criterion | Metric + threshold | How measured | Evidence |
|---|---|---|---|
| Every citation is real | 0 IDs missing from `papers.tsv` | `render_review.py --check` | script output |
| Every claim has verbatim evidence | 0 cited sources without an entry in `LITERATURE_REVIEW_EVIDENCE.md`; 0 NOT FOUND / WRONG PAGE | `build_evidence.py` exit 0 + QA row per MANUAL entry | evidence file + QA file |
| Numbers match their sources | ≥ 20 of 20 randomly sampled quoted numbers match the PDF or README quote | evaluator re-fetches and compares | scorecard rows |
| It is a review article, structured as one | abstract ≤ 150 words; Summary Points and Future Issues present; 9,000–11,000 words; ≥ 150 works cited | script counts | script output |
| Covers the corpus | each of the 9 themes cited ≥ 8 times; ≥ 15 repo citations | script counts by ID prefix | script output |
| Source quality is labelled | every number in §§4–12 says whether its source is independent or lab-authored, and measured or asserted | evaluator checks a sample of 20 | scorecard rows |
| Kit implications are traceable | every row in Table 4 cites ≥ 1 paper or repo | evaluator checks all rows | scorecard rows |

Sharif's read of the register (section 6 sample, then the full draft) is a separate sign-off, not a
criterion.
