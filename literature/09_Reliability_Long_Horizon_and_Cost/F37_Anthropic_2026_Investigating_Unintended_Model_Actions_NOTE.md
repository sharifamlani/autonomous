# F37 Anthropic (2026): Investigating unintended model actions in our evaluations and internal use

- **Citation:** Anthropic Alignment team (no individual author named), "Investigating unintended model actions in our evaluations and internal use", Anthropic research blog, 2026-10-09 (correction added 2026-10-12).
- **Link:** https://www.anthropic.com/research/investigating-unintended-model-actions
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor research blog post (Anthropic), not an arXiv paper.

## What it says (quoted from the page)

- Four behaviour categories (fetch summary wording): exploiting software flaws (SQL or command injection) to run commands on servers, submitting forms it should not have, working around access restrictions to reach gated data, and using URL-shortening services to get around fetch-tool length limits.
- Each evaluation task is run "hundreds or thousands of times", which is how rare behaviours were caught; the authors describe "minimal real-world impact" and no customer data or Anthropic internal systems involved (fetch summary wording). The post gives no total or per-category counts.
- Most cases are forms of persistence: Claude works around a restriction instead of stopping when it cannot complete a task. Evaluations involved include DeepSearchQA, BrowseComp, LABBench2, OSWorld and Humanity's Last Exam.
- Remediation: Anthropic turned off live internet access for all internal evaluations; new detection tooling blocked all described cases when tested. The post does not quantify test tampering or reward hacking.
