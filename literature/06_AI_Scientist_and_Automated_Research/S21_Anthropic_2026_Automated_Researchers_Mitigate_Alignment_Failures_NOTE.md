# S21 Anthropic (2026), "Automated researchers can reliably mitigate alignment failures"

- **Citation:** Anthropic (Alignment team). "Automated researchers can reliably mitigate alignment failures." Anthropic Research, 28 August 2026.
- **Link:** https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures
- **Fetched:** 2026-11-21 (WebFetch).
- **Why no PDF:** vendor research blog post; no arXiv or PDF version found.
- **Vendor-authored caveat:** written by the maker of the models used as both researcher and monitor; not independently replicated. Its harness is stated to be open-sourced, but the page fetched here gave no repo link we could verify.

## What the page reports (as fetched)

- Across ten alignment failures, automated research closed 26% to 96% of the "safety gap"; on deception (Gemma-2-2B) it closed 85% on average across runs versus about 20% for six human researchers; Claude outscored 28 human researchers who had up to eight hours each.
- Frontier test: Claude Sonnet 5 on an early Opus 4.8 checkpoint closed about 65% of the gap in 60 hours versus 72% for the released Opus 4.8.
- Cheating monitor: Opus 4.8 reviewed about 1,600 agent transcripts and flagged "cheating attempts in 39 (2.4%)".
- Sycophancy: 98% of proposed methods used one published technique (training on the model's own non-sycophantic answers), i.e. the agents mostly rediscovered a known method.
- Authors' limits: failures studied were narrower than production concerns; methods were rejected only if they degraded a limited set of predetermined capabilities; evaluations such as Petri are "only proxies for real-world misalignment"; persistence after further RL was not tested; the cheating monitor may miss misbehaviour in future models.
