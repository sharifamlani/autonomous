# H15 Anthropic (2026): Run Claude Code programmatically (headless `claude -p`)

- **Citation:** Anthropic. (2026). *Run Claude Code programmatically.* Claude Code documentation.
- **Link:** https://code.claude.com/docs/en/headless
- **Fetched:** 2026-11-21. Living documentation with no publication date; the year is the fetch year.
  Version notes on the page go up to v2.1.302.
- **Why no PDF:** official product documentation; there is no PDF version.

## What it says (quoted from the page), for unattended runs

- Permissions: "With Claude Code v2.1.302 or later, `claude -p` runs start in Manual mode when
  nothing sets a permission mode", and in Manual mode "a call that needs approval is denied unless
  something approves it, such as a `PermissionRequest` hook or a `--permission-prompt-tool`."
- `--permission-mode` takes `auto` ("a classifier review[s] most actions"), `dontAsk` ("denies every
  call that would otherwise prompt") or `acceptEdits`.
- "Pass `--permission-prompts none` when nobody is available to answer permission prompts"; then
  "Claude is told that nobody can approve the request and not to retry it, and the run continues."
- Background work: "Claude Code stops whatever is still running after 10 minutes of continuous idle
  waiting by default and drops its partial result"; `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` waits
  without a cap.
- A subagent's long command that moves to the background can let "a `claude -p` run ... exit with
  code 0 before the command finishes" (raise `BASH_DEFAULT_TIMEOUT_MS`).
- `--bare` skips hooks, skills, subagents, plugins, MCP servers, auto memory and CLAUDE.md, and "is
  the recommended mode for scripted and SDK calls"; hooks do not run in bare mode even from a plugin
  loaded by flag.
- Cost: `--output-format json` includes `total_cost_usd`, described as "client-side estimates".
- Load checks: the `system/init` event's `plugin_errors` and `mcp_server_errors` fields let CI fail
  when a plugin or MCP server did not load.

## Limits

- Documentation states what the product does, not whether a configuration succeeds; flags and
  defaults change between versions (several statements are version-gated).
