# T16 Carlini (2026): Building a C compiler with a team of parallel Claudes

- **Citation:** Carlini, N. (2026, February 5). *Building a C compiler with a team of parallel
  Claudes.* Anthropic Engineering blog (Safeguards team).
- **Link:** https://www.anthropic.com/engineering/building-c-compiler
- **Fetched:** 2026-11-21 (title, author and date checked on the page).
- **Why no PDF:** a vendor engineering blog post; there is no PDF version. Code and the working
  files of the run are public at https://github.com/anthropics/claudes-c-compiler.

## What it says (quoted from the page)

- Setup: the author "tasked 16 agents with writing a Rust-based C compiler, from scratch, capable of
  compiling the Linux kernel."
- Coordination was minimal: "Claude takes a 'lock' on a task by writing a text file to
  current_tasks/"; "If two agents try to claim the same task, git's synchronization forces the second
  agent to pick a different one."
- Roles were by job, not by persona: one agent coalesced duplicate code; others worked on performance,
  code generation, Rust code-quality critique and documentation.
- Cost: "Over nearly 2,000 Claude Code sessions and $20,000 in API costs."
- Verification carried the run: "it's important that the task verifier is nearly perfect, otherwise
  Claude will solve the wrong problem"; a CI pipeline with "stricter enforcement" was added to stop
  regressions; GCC served as a "known-good compiler oracle".
- Limits stated by the author: "New features and bugfixes frequently broke existing functionality";
  "The Rust code quality is reasonable, but is nowhere near the quality of what an expert Rust
  programmer might produce"; it "does not have its own assembler and linker"; "It's not yet a drop-in
  replacement for a real compiler."

## Limits

- Vendor-authored, one project, one run, no single-agent comparison: it shows what a parallel team can
  do with a near-perfect test oracle, not that a team beats one agent at equal cost ($20,000 buys the
  comparison too).
