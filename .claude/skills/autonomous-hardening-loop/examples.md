# Examples

## Example A — Job Market apply canary (source instance)

**Goal:** Multi-platform apply canaries submit (or document human gates).

**Runner:**
```powershell
$env:PYTHONPATH="Scripts"
python Scripts/run_apply_batch.py --canary --platforms workday --reset-friction --report Scripts/data/canary_workday_report.json
```

**Loop highlights:**
1. Extracted shared helpers + thin CLI so notebook ≠ source of truth.
2. Workday stuck on My Information → DOM smoke → exact Apply click / LinkedIn source pick → Gemini canary submitted.
3. Greenhouse email OTP → failing parser tests → Gmail scrape via signed-in profile → mid-loop heal + autoheal retry.
4. Moody’s reCAPTCHA → human gate with opt-in `JOB_APPLY_CAPTCHA_WAIT_S`; other lanes continued.
5. Commit per green milestone (`Workday fill`, `Gmail OTP`, `canary selection`, …).

**Status shape:**
| Lane | Result | Notes |
|------|--------|-------|
| workday | submitted | DOM fill |
| linkedin→greenhouse | submitted | handoff |
| moodys_sf | captcha | human gate |

## Example B — Generic HTTP API / CLI

**Goal:** `mycli sync --canary` exits 0 against staging.

**Contract:**
```markdown
# Hardening: mycli sync
Goal: canary sync writes 1 record and exits 0
Runner: `mycli sync --canary --env staging`
Canaries:
- [ ] auth — token refresh — HTTP 200 from /me
- [ ] write — create fixture row — row visible in GET
- [ ] idempotent — second sync — no duplicate
Human gates: none
Evidence dir: ./tmp/canary/
```

**Loop:**
1. Run canary → capture failing lane (e.g. 401).
2. Failing test around token refresh edge case.
3. Fix client package; unit green; canary green; commit.
4. Next lane (write) → smoke against staging → fix serialization → commit.
5. Close when matrix green.

## Example C — Agent / browser flow (non–Job Market)

**Goal:** Checkout agent reaches `order_confirmed` on fixture store.

**Runner:** `python -m shop_agent.canary --sku FIXTURE-1`

**Loop:**
1. Full canary fails at payment step.
2. Isolated smoke: fill address only → proves address bug ≠ payment.
3. Deterministic `fill_address(page, answers)` helper; unit-test field mapping.
4. Re-run canary; payment captcha → human gate documented; address+cart lanes marked green.

## How to ask for this skill

- “Run the autonomous hardening loop on `<target>` until green.”
- “Canary-harden the `<CLI/feature>` the same way as the apply pipeline.”
- “Work as long as you need to get `<X>` working — use the hardening skill.”
