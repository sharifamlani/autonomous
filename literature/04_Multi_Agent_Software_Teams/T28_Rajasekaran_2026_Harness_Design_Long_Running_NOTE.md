# T28 Rajasekaran (2026): Harness design for long-running application development

- **Citation:** Rajasekaran, P. (2026, March 24). *Harness design for long-running application
  development.* Anthropic Engineering (Labs team).
- **Link:** https://www.anthropic.com/engineering/harness-design-long-running-apps
- **Fetched:** 2026-11-21 (title, author and date checked on the page).
- **Why no PDF:** a vendor engineering post; there is no PDF version.

## What it says (quoted from the page)

- Design: a planner, a generator and an evaluator agent; the evaluator drives the live app (Playwright
  MCP) and grades against criteria agreed with the generator before each sprint (27 criteria for one
  sprint of the level editor).
- Why a separate judge: "Separating the agent doing the work from the agent judging it proves to be a
  strong lever to address this issue."
- Cost of the full team (Opus 4.5, retro game maker): solo run 20 min and $9; full harness 6 hr and
  $200. "The harness was over 20x more expensive, but the difference in output quality was
  immediately apparent."
- Updated harness (Opus 4.6, browser audio workstation): planner 4.7 min / $0.46; three build rounds
  and three QA rounds; total 3 hr 50 min and $124.70.
- The roles shrink as models improve: "On 4.6, the model's raw capability increased, so the boundary
  moved outward." The sprint construct was dropped; the evaluator stayed for tasks near the edge of
  what the generator can do alone.

## Limits

- Vendor-authored, a single task family per experiment (games, a music app, front-end design), no
  repeated runs and no matched-cost single-agent arm: the solo-vs-harness comparison differs in more
  than the evaluator, and the post gives no with-versus-without-evaluator numbers.
- Quality is judged by the author and the evaluator agent, not by an external grader.
