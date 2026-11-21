---
name: autonomous-hardening-loop
description: >-
  Run an autonomous write→test→debug→improve loop until a defined canary or
  acceptance suite is green. Use when the user says work until it works, harden
  this, canary loop, fix loop, get it green, debug until passing, or asks to
  apply the job-market canary process to any other codebase or feature.
---

# Autonomous Hardening Loop

Generalize the “work as long as you need to get it working” process: define a
canary, fail for real, fix from evidence, commit green milestones, repeat.

This skill is **domain-agnostic**. The Job Market apply pipeline is only one
instance. The same loop applies to APIs, CLIs, agents, UI flows, scrapers, etc.

## Iron laws

1. **Success is measured by a canary, not by “code looks right.”**
2. **No production fix without a failing test or a reproducible smoke first.**
3. **Fix the shared library / package — not the notebook, one-off script, or UI glue.**
4. **Commit after each green milestone** (when the repo allows; ask if unclear).
5. **Stop only on: all canaries green, or a documented human gate** (CAPTCHA, paid API, missing secret). Never stop on the first flake.
6. **False positives count as bugs** (e.g. “logged in” when only the landing page loaded).

## When to invoke

User intents like:
- “work until it works” / “get it green”
- “canary / harden / fix loop”
- “apply that autonomous process to X”

If the user names a target (feature, CLI, lane, endpoint), that target becomes
the canary matrix.

## Phase 0 — Contract (do this first)

Write down (in todos or a short status file under the project’s data/docs area):

| Field | What to capture |
|-------|-----------------|
| **Goal** | One sentence outcome (“canary submits”, “tests pass”, “endpoint returns 200”) |
| **Canary matrix** | 1 row per lane/platform/path that must pass |
| **Runner** | Exact command(s) to exercise the canary (CLI preferred over GUI) |
| **Evidence** | Logs, screenshots, DB rows, HAR, test output paths |
| **Out of scope** | Explicit skips (quota walls, third-party blocks) |
| **Human gates** | Things the agent must not fake (CAPTCHA, 2FA, payments) |

Prefer a **shared helper + thin CLI** over notebook cells or ad-hoc scripts so
the same path is used by humans and automation.

```
extract helpers → CLI/canary runner → notebook/UI calls helpers (optional)
```

## Phase 1 — Red: prove failure

1. Run the canary / acceptance command for real (not only unit tests).
2. Capture **one** primary failure per lane (status, error, screenshot, log snippet).
3. Classify:
   - **Logic bug** → unit/integration test + fix
   - **Integration/DOM/API drift** → isolated smoke script, then promote fix into package
   - **Env/config** → pin override rules (don’t silently clobber user env)
   - **Human gate** → document unblock command; do not invent a bypass

Do not “fix” by skipping the failing lane unless the user marks it out of scope.

## Phase 2 — Green: smallest fix that clears the canary

For each failure:

```
observe evidence
  → write failing test OR minimal smoke that reproduces
  → watch it fail
  → implement minimal fix in the owning package
  → re-run unit/smoke
  → re-run the full canary for that lane
  → commit milestone (no secrets)
```

Rules of engagement:
- **TDD when the bug is pure logic** (parsers, detectors, ranking, URL classify).
- **DOM/browser/API smokes when the bug is environmental** — then keep a regression test if cheap.
- **One root cause per loop.** Don’t stack speculative fixes.
- Prefer **deterministic helpers** (DOM fill, OTP fetch, URL resolve) over hoping the LLM retries correctly.
- If a “fix” works in smoke but fails in the batch runner, debug **wiring** (env bootstrap, stealth flags, profile locks, path imports) next — not the helper again.

## Phase 3 — Expand coverage

After one lane is green:
1. Run the next canary lane.
2. Seed missing fixtures/materials only as needed (covers, deeplinks, test data).
3. Keep a living status table (markdown or JSON report) with lane → result → notes.
4. When selection logic picks a bad canary target, fix **selection/preference**, not just the one row.

## Phase 4 — Human gates (allowed exits)

If blocked by something the agent must not solve:

1. Leave a clear unblock recipe (env var, command, what to click).
2. Optionally implement **opt-in wait + retry** (toast + poll + one retry).
3. Mark the lane `blocked: human_gate` in the status table.
4. Continue other lanes; don’t freeze the whole matrix.

Default waits that hang unattended batches must be **opt-in** (env flag), not always-on.

## Phase 5 — Close out

- [ ] Every in-scope canary green **or** documented human gate
- [ ] Unit/smoke tests for each root-cause fix still pass
- [ ] Status report updated
- [ ] Commits are milestone-sized; no secrets / credentials / `data/` dumps
- [ ] Throwaway `_tmp_*` debug scripts left untracked or deleted

## Anti-patterns

| Don’t | Do instead |
|-------|------------|
| Edit notebook JSON to “fix” the batch | Fix `Scripts/` / package code; notebook calls helpers |
| Declare victory after unit tests only | Re-run the real canary command |
| Infinite LLM retries on the same stuck UI | Deterministic helper + coach nudge once |
| Treat “page loaded” as success | Assert the **post-condition** (submitted, 200, file written) |
| Commit secrets or live DB | Reports + code only |
| Block all lanes on one captcha | Document gate; finish other lanes |

## Instantiation template

Copy and fill when starting a new target:

```markdown
# Hardening: <name>
Goal: <one sentence>
Runner: `<exact command>`
Canaries:
- [ ] lane_a — <target> — <pass criteria>
- [ ] lane_b — <target> — <pass criteria>
Human gates: <none | list>
Out of scope: <list>
Evidence dir: <path>
```

## Related skills

- Use **test-driven-development** for pure logic fixes inside the loop.
- Use **systematic-debugging** when a canary fails for unclear reasons — root cause before the next patch.
- Use **verification-before-completion** before claiming the matrix is done.

## Examples

See [examples.md](examples.md) for a Job Market apply-pipeline instantiation and a generic API/CLI instantiation.
