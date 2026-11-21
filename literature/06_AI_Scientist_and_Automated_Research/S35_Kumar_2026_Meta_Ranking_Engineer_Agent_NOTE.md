# S35 Kumar (2026): Ranking Engineer Agent (REA): The Autonomous AI Agent Accelerating Meta's Ads Ranking Innovation

- **Citation:** Ashwin Kumar, Erwin Gao, Matan Levi, Sheela Yadawad, Sherman Wong, Sneha Iyer and Vinodh Kumar Sunkara (Meta), "Ranking Engineer Agent (REA): The Autonomous AI Agent Accelerating Meta's Ads Ranking Innovation", Engineering at Meta (DevInfra, ML Applications), 2026-03-17.
- **Link:** https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea/
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor engineering blog post (Meta), not an arXiv paper; results are the company's own.

## What it says (quoted from the page)

- REA is an autonomous agent that drives the end-to-end ML experimentation lifecycle for ads ranking models: it generates hypotheses, launches training jobs, debugs failures and iterates on results (fetch summary wording).
- It hands the wait for a training job to a background system and goes dormant, then resumes where it left off; it keeps "persistent state and memory across multiround workflows spanning days or weeks", in three phases (Validation, Combination, Exploitation).
- Human oversight: engineers approve the exploration plan and its estimated GPU compute cost before execution and grant access through preflight checklist reviews; REA operates "with human oversight at key strategic decision points" and pauses when compute thresholds are reached.
- Results (vendor): "REA-driven iterations doubled average model accuracy over baseline across six models"; "three engineers delivered proposals to launch improvements for eight models", work that previously needed two engineers per model.
