# H23 Hughes (2026): How we built Claude Code auto mode: a safer way to skip permissions

- **Citation:** Hughes, J. (2026, March 25). *How we built Claude Code auto mode: a safer way to skip permissions.* Anthropic Engineering blog.
- **Link:** https://www.anthropic.com/engineering/claude-code-auto-mode
- **Fetched:** 2026-11-21 (title, byline "John Hughes" and date checked on the fetched page).
- **Why no PDF:** a vendor engineering blog post; there is no PDF version.

## What it says (from the fetched page)

- Problem: approval fatigue. "in practice users accept 93% of them anyway."
- Design: two layers. A server-side prompt-injection probe screens tool outputs; a transcript
  classifier (Sonnet 4.6) gates each action. The classifier runs in two stages: a fast single-token
  filter, then chain-of-thought only if the first stage flags the action. It is "reasoning-blind by
  design": it sees user messages and tool calls, not Claude's own messages or tool outputs.
- Edits inside the project directory skip the classifier. A deny-and-continue loop escalates to the
  human after 3 consecutive or 20 total denials.
- Numbers reported: real traffic (n=10,000) stage-1 false-positive rate 8.5%, falling to 0.4% after
  stage 2; real overeager actions (n=52) false-negative rate 6.6% at stage 1, rising to 17% after
  stage 2; synthetic exfiltration (n=1,000) false-negative rate 1.8% then 5.7%.
- "The 17% false-negative rate on real overeager actions is the honest number."

## Limits

- Vendor-authored, about its own product. The overeager test set is small (n=52).
- The authors say auto mode "is not a drop-in replacement for careful human review on high-stakes
  infrastructure"; prompt engineering to fix misses "stops short of checking whether it's consent"
  produced no net benefit.
- An independent stress test (H17) finds a far higher false-negative rate on ambiguous DevOps tasks.
