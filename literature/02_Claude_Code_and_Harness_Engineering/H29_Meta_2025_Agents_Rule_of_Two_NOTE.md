# H29 Meta (2025): Agents Rule of Two: A Practical Approach to AI Agent Security

- **Citation:** Meta (2025, October 31). *Agents Rule of Two: A Practical Approach to AI Agent Security.* Meta AI blog (no named author on the page).
- **Link:** https://ai.meta.com/blog/practical-ai-agent-security/
- **Fetched:** 2026-11-21 (title, publisher and date checked on the fetched page).
- **Why no PDF:** a company policy/blog post; there is no PDF version.

## What it says (from the fetched page)

- Prompt injection is "a fundamental, unsolved weakness in all LLMs", so until agents can reliably
  detect and refuse it, an agent should satisfy no more than two of three properties in a session:
  [A] processing untrustworthy inputs, [B] access to sensitive systems or private data, [C] changing
  state or communicating externally.
- A task that needs all three "at a minimum requires supervision" (human-in-the-loop approval or
  another reliable validation); starting a fresh session is one way to avoid the combination.
- The rule is "a supplement, and not a substitute" for least privilege and does not cover every threat.

## Limits

- A design heuristic from the vendor, with no experiments or numbers. For an unattended kit the
  consequence is design-time: decide which of A, B, C each agent holds, since no human is there to
  supply the supervision. Compare the tested policy engines H9, H18 and H19.
