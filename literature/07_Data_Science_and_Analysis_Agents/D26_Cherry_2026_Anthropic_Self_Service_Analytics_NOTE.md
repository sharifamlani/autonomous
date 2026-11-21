# D26 Cherry (2026): How Anthropic enables self-service data analytics with Claude

- **Citation:** Cherry, J., Peng, C., Jiao, J., Leder, J., Chang, C. (2026, June 3). *How Anthropic enables
  self-service data analytics with Claude.* Anthropic (claude.com resources).
- **Link:** https://claude.com/resources/articles/how-anthropic-enables-self-service-data-analytics-with-claude
- **Fetched:** 2026-11-21 (title, byline and date checked on the page).
- **Why no PDF:** a vendor article on a web page; there is no PDF version.

## What it says (quoted from the page)

- Headline: "At Anthropic, 95% of business analytics queries are automated via Claude, with ~95% accuracy
  in aggregate."
- Skills matter: "Without skills, Claude's ability to answer analytics questions accurately didn't exceed
  21% on our evals." "Adding skills gets these numbers consistently above 95% in aggregate and regularly
  around 99% in certain domains."
- Drift: "We watched our offline accuracy drift from ~95% at launch to ~65% over a month" (as the data model
  changed and the skills were not kept up to date).
- Adversarial review "increased accuracy by 6% within our eval set, but at the cost of 32% more tokens and
  72% higher latency."
- Three failure modes cover most wrong answers: "Concept <> entity ambiguity", "Data staleness",
  "Retrieval failure".
- A negative result: "We gave the agent direct grep access to our entire dashboard, transformation, and
  analyst-notebook SQL"; accuracy moved by less than a point in either direction.

## Limits (the authors')

- "The failure mode none of this fully catches is the silent one." and "though we don't have a robust
  solution yet."
- The 95% is an aggregate over Anthropic's own business questions; the eval suite and offline results do
  not guarantee a wrong answer will not occur.

## Caveats for the kit

- Vendor-authored, about Anthropic's own data warehouse and its own evals; no public data, no run counts,
  no confidence intervals, no baseline from another vendor. It is a process description (offline evals
  with known answers, ablations with the eval set held fixed, drift tracking, provenance footers), not a
  replicable benchmark. Treat the numbers as one organisation's report, not as evidence the kit will match.
