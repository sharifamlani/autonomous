# A27: Rajasekaran et al. (Anthropic), "Effective context engineering for AI agents" (2025)

- **Citation:** Prithvi Rajasekaran, Ethan Dixon, Carly Ryan and Jeremy Hadfield (Anthropic Applied AI team), "Effective context engineering for AI agents", Anthropic Engineering, 29 September 2025.
- **Link:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **Date fetched:** 2026-11-21
- **Why there is no PDF:** an HTML engineering post on anthropic.com with no PDF edition.
- **Status:** vendor-authored guidance from the builder of Claude Code. It describes techniques and rationale; it reports no benchmark or cost numbers, so it is a design recipe, not measured evidence.

## What the fetched page says (paraphrase of the fetch result, 2026-11-21)

- Context is a finite resource with diminishing returns ("context rot"): the model's ability to accurately recall information from the context decreases as the context grows.
- Compaction (summarise a conversation nearing the window limit and start a new window) is the first lever for long-running work; clearing old tool results is a light-touch form.
- Sub-agent architectures: specialised sub-agents work in clean context windows and return only a condensed, distilled summary to the lead agent.
- Just-in-time retrieval: agents keep lightweight references (file paths, stored queries, links) and load data at run time with tools; the post notes this trades speed for autonomy and recommends a hybrid when some data can be fetched up front.

## How the folder README uses it

As the vendor recipe that matches the measured results in A21 (length alone hurts even with perfect retrieval) and A16 (a wrong early turn is not recovered). Neither of those tests the post's remedies; no number in this post supports them.
