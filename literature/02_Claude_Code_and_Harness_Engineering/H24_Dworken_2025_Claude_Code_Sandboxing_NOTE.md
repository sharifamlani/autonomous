# H24 Dworken (2025): Beyond permission prompts: making Claude Code more secure and autonomous

- **Citation:** Dworken, D., and Weller-Davies, O. (2025, October 20). *Beyond permission prompts: making Claude Code more secure and autonomous* (browser title "Making Claude Code safer with sandboxing"). Anthropic Engineering blog.
- **Link:** https://www.anthropic.com/engineering/claude-code-sandboxing
- **Fetched:** 2026-11-21 (title, authors and date checked on the fetched page).
- **Why no PDF:** a vendor engineering blog post; there is no PDF version.

## What it says (from the fetched page)

- Default: Claude Code "asks for permission before making modifications or running any commands";
  frequent requests cause "approval fatigue".
- Internal usage: sandboxing "safely reduces permission prompts by 84%."
- Effective sandboxing "requires both filesystem and network isolation"; the sandboxed bash tool uses
  Linux bubblewrap and macOS seatbelt and covers subprocesses.
- Claude Code on the web runs each session in an isolated cloud sandbox; git credentials and signing
  keys stay outside it behind a proxy. The sandbox runtime is open source (research preview);
  `/sandbox` turns it on.

## Limits

- Vendor-authored, internal usage data; no run counts, tasks or definition of "prompt" for the 84%.
- Covers the bash tool; other tools and MCP servers are separate (see the H17 finding that file edits
  bypass the auto-mode classifier).
