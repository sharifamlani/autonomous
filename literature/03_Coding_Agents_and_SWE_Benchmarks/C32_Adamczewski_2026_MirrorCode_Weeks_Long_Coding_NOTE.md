# C32 Adamczewski (2026): MirrorCode: evidence that AI can already do some weeks-long coding tasks

- **Citation:** Tom Adamczewski, David Rein, David Owen and Florian Brand (Epoch AI, co-developed with METR), "MirrorCode: evidence that AI can already do some weeks-long coding tasks", Epoch AI publication, 2026-04-10. METR's own page (https://metr.org/blog/2026-04-10-mirrorcode-preliminary-results/) is a linkpost with no figures.
- **Link:** https://epoch.ai/publications/mirrorcode-preliminary-results/
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** an independent evaluator's (Epoch AI) web report, not an arXiv paper; preliminary results.

## What it says (quoted from the page)

- Claude Opus 4.6 reimplemented gotree, "a bioinformatics toolkit with ~16,000 lines of Go and 40+ commands" (Rust version 7,644 lines); the authors estimate a skilled engineer without AI help would need "2-17 weeks".
- It passed 2,000 of 2,001 gotree tests (99.95%); "one billion tokens costs around $550" in their setup and runs typically used 2-3 million output tokens.
- Not solved: Pkl, about 61,000 lines of Java/Kotlin; the best Rust run passed 256 of 733 visible tests (35%) and used 90% of its token budget.
- Caveats stated: relies on a detailed executable specification so it does not show AI can handle arbitrary software tasks; memorisation risk (screened, not ruled out); only four of 24 target programs written up; only Anthropic models reported in detail; code quality mixed; human baselines for the longest tasks do not exist and the gotree estimate comes from four informal expert guesses.
