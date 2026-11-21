# H30 Bolin (2026): Unrolling the Codex agent loop

- **Citation:** Michael Bolin (OpenAI), "Unrolling the Codex agent loop", OpenAI blog (Engineering), 2026-01-23.
- **Link:** https://openai.com/index/unrolling-the-codex-agent-loop/
- **Fetched:** 2026-11-21 (page fetched in this session; title, authors and date taken from the fetch
  output). The fetch tool passes pages through a small model; the text below was copied from its output
  and should be re-checked against the live page.
- **Why no PDF:** a vendor engineering blog post (OpenAI), not an arXiv paper; first of a series on the Codex harness.

## What it says (quoted from the page)

- "context window management is one of the agent's many responsibilities."
- "Cache hits are only possible for exact prefix matches within a prompt"; when hits occur, "sampling the model is linear rather than quadratic". Changing tools, model, sandbox or working directory can cause cache misses, so Codex appends new messages instead of editing earlier ones.
- Codex does not use `previous_response_id`: every request is stateless (supports Zero Data Retention), at the cost of resending the growing conversation each turn (fetch summary wording).
- Compaction: once the token count passes a threshold Codex replaces the history with "a new, smaller list of items that is representative of the conversation"; it moved from a manual `/compact` summary to the Responses API `/responses/compact` endpoint, which returns a `compaction` item, triggered automatically past `auto_compact_limit`.
