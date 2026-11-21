# playwright-form-driving — field manual for Playwright MCP form work

You are driving ANY web form via `mcp__playwright__browser_*` tools — job applications, outreach forms, login flows, verification pages. This skill is the general-purpose field manual for Playwright MCP; it is agnostic to the specific ATS. For per-ATS gotchas (Workday spinbuttons, iCIMS iframes, LinkedIn shadow DOM, Oracle HCM postal-code race, specific selector rotations), load [`ats-playwright-quirks`](../ats-playwright-quirks/SKILL.md). For the full apply pipeline, load [`job-apply`](../job-apply/SKILL.md).

## The two biggest unit-of-time wins (reach for these FIRST, not last)

Both proven 2026-10-08 — 30 submits in one session. The pattern is: **minimize round-trips, maximize per-call surface**.

1. **Batch identity + text fields into ONE `browser_evaluate` call, not one per field.** 7 React-safe `.value` writes in a single JS block replaces 7 `browser_type` tool calls. Also fits well with discovery: use `discoverFields()` from the shared `greenhouse_diag.js` to map the form first, THEN compose one batched setter call that hits everything named. Only use `browser_type slowly=true` for the fields that *require* keystroke events (react-select comboboxes + Workday date spinbuttons).

2. **Reuse identity across the SAME company's forms.** A Greenhouse validityToken is company-scoped — resolve once, apply to N roles on that company's board by rotating only the `token=` parameter. A Workday "Use My Last Application" dialog carries ALL prior data forward within a tenant. Pinterest batch: 7 submits in ~15 min on one validityToken. Zillow batch: 6 Workday submits in ~15 min on one "Use My Last Application" chain. Always ask "is this an N-of-many at the same company?" and resolve the shared-state once before the first submit.

## When to fire

- You are about to drive a form, modal, or multi-step flow via Playwright MCP and the specific ATS is NOT already covered by `ats-playwright-quirks`.
- A `browser_type` / `browser_click` silently no-oped and you can't tell why.
- A react-select / typeahead / autocomplete combo rejected your input.
- A submit button bounced the form with an opaque "This field is required" error.
- A `.value` setter looked correct but the framework still rejected the field.

## The two-mode mental model

Every input you touch is either (a) **React-managed** or (b) **native-browser**. The tool call that works for one mode is often the exact call that silently fails on the other. Keep this split in mind at all times.

| Field kind | Tool / pattern that works |
|---|---|
| Native `<input type="text">`, no React state | `browser_fill_form`, or JS `.value =` setter |
| React-managed `<input>` | JS **React-safe setter** (prototype `.value` setter + `input`/`change` events) |
| React-managed Workday `[role="spinbutton"]` (dates) | **Playwright real `browser_type`** (JS setter does NOT sync React state) |
| react-select combobox | `browser_type` with `slowly: true` (pressSequentially) + Enter |
| Native `<select>` | `browser_select_option` |
| Radio in `<fieldset><legend>` | Click the `<label>`, not the `<input>` (clicking input toggles) |
| Checkbox (standalone consent) | `<input>.click()` is fine; JS .click or Playwright click both work |
| Hidden `<input type="file">` | Never click directly. Click the visible Attach `<button>`; `setFiles` via `browser_file_upload` |
| Shadow-DOM content (LinkedIn SDUI) | `document.querySelector('#interop-outlet').shadowRoot.querySelector(...)` |
| iframe content (iCIMS, some careers wrappers) | Route through `iframe[name=...].contentDocument` |

## The React-safe setter (memorize this pattern)

React maintains a shadow value separate from the DOM `.value`. Setting `.value =` directly updates the DOM but React's next render blows your value away. **Call the prototype setter and dispatch `input` + `change` manually**:

```javascript
const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set
            || Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
setter.call(el, val);
el.dispatchEvent(new Event('input',  { bubbles: true, composed: true }));
el.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
```

Use `{ composed: true }` so the event crosses the shadow DOM boundary (LinkedIn Easy Apply). Works for: Ashby text inputs, Greenhouse text inputs, LinkedIn Easy Apply text inputs, iCIMS text inputs, Pinpoint, all non-Workday-date Workday text inputs.

**Does NOT work for:** Workday `[role="spinbutton"]` date fields (use real `browser_type`), react-select comboboxes (use `pressSequentially`), `<select>` elements (use `browser_select_option`).

## The react-select combobox cookbook

React-select is used by Greenhouse, many Lever installs, Ashby location typeaheads, Pinterest's Country/State/EEO fields, Anthropic's screening questions. It has three failure modes, each with a specific fix.

### The 4 moves

1. **Simple typeahead with Enter commit** — the happy path.
   ```
   browser_type target=#combo-id text="California" slowly=true
   browser_press_key key=Enter
   ```

2. **No results on typed value** — the option doesn't exist OR the input had leftover text.
   ```
   browser_evaluate: setter.call(el, '')  → dispatch input
   browser_click target=#combo-id
   browser_press_key key=ArrowDown         # force menu open with FULL list
   browser_evaluate: Array.from(document.querySelectorAll('[role="option"]'))
                     .filter(o => o.offsetParent).map(o => o.innerText)
   ```
   Inspect what's actually offered before guessing. If your target isn't there, pick the honest fallback (e.g. "I don't wish to answer") — don't fabricate.

3. **Menu doesn't open at all after typing** — react-select requires keystroke-level events.
   ```
   # browser_fill() does NOT work — it bypasses pressSequentially events
   # Use browser_type slowly=true instead
   browser_type target=#combo-id text="Asian" slowly=true
   # Options now visible; press Enter to commit
   ```

4. **Hidden cascading combo appears after a prior answer** — common on authorization/sponsorship/location-cascade forms.
   ```
   # Fill combo A → press Enter → wait for DOM update
   # Re-poll input[role="combobox"] to find combo B's new id
   # Fill combo B
   ```

### The "singleValue lie" after a submit bounce

**After the form bounces on a required-field error, every react-select combo clears its DOM `.value` to `""` — even the ones you filled correctly.** The visible `[class*="singleValue"]` text still shows the previous selection, so visually the form looks filled. It is not.

```javascript
// Truth check:
const check = (id) => {
  const el = document.getElementById(id);
  const parent = el.closest('div[class*="field"]') || el.closest('[class*="question"]');
  const sv = parent?.querySelector('[class*="singleValue"], [class*="single-value"]')?.innerText || '';
  return { id, value: el.value, singleValue: sv };
};
// value === "" AND singleValue === "<expected>" ⇒ bounce lie, refill
```

**Rule: on any submit bounce, re-fill every open combo in order before resubmitting.** Trusting the visible singleValue text and only re-filling the "obvious" failed field will fail again on the exact same error.

## Numeric-ID retagging (CSS can't match pure-digit IDs)

Greenhouse's EEO comboboxes have IDs like `29783` / `29784` / `29785`. `document.querySelector('#29783')` throws a parse error. **Rename them first**:

```javascript
['29783','29784','29785'].forEach(id => {
  const el = document.getElementById(id);
  if (el) el.id = `eeo-${id}`;
});
```

Then `#eeo-29784` works with every Playwright tool. Also useful: tagging ambiguous Attach buttons with sequential IDs so you can target "the second one" cleanly.

```javascript
const btns = Array.from(document.querySelectorAll('button'))
  .filter(b => b.textContent.trim() === 'Attach' && b.offsetParent);
btns.forEach((b, i) => b.id = `attach-btn-${i}`);
```

## File uploads — the one rule that matters

**NEVER cancel an open file chooser with `browser_file_upload paths=[]`.** Doing it to a Greenhouse upload wedges the field into a permanent "uploading at 0%" state that `localStorage` persists across reloads. Recovery requires `localStorage.clear() + sessionStorage.clear() + navigate` and refilling the entire form. See `ats-playwright-quirks` §8.

**If you opened the wrong Attach button:** upload something valid (anything), then use the UI's "Remove" button after. Do NOT cancel.

**Resume path:** always resolve via `job_apply.resume.canonical_resume_pdf()` — never hardcode. Default is `Private Market/Resume/Experience/Amlani_Resume_Experience.pdf`.

**Cover letter:** compressed `.pdf` from `Scripts/cover_letter/` output, Ghostscript `/screen`-reduced if the target has an upload size cap (LinkedIn 512KB, Oracle HCM stalls above ~500KB).

## Shadow DOM: when the DOM "doesn't exist"

LinkedIn Easy Apply, LinkedIn Invite modal, and some newer SDUI widgets render inside `#interop-outlet.shadowRoot`. `document.querySelector('[role="dialog"]')` returns null. `browser_snapshot` won't see the modal.

**Dig into the shadow root:**
```javascript
const sr = document.querySelector('#interop-outlet').shadowRoot;
const modal = sr.querySelector('[role="dialog"]');
const nextBtn = Array.from(modal.querySelectorAll('button'))
  .find(b => /^Next$/.test((b.innerText || '').trim()));
```

Event dispatches must use `{ bubbles: true, composed: true }` to cross the shadow boundary. Playwright's `browser_wait_for text=...` pierces shadow DOM natively; use it to wait for modal content.

## iframe routing (iCIMS and some careers wrappers)

iCIMS forms live inside `iframe[name="icims_content_iframe"]`. Direct top-level queries return nothing.

**Two routing styles:**
```javascript
// In browser_evaluate:
const doc = document.querySelector('iframe[name="icims_content_iframe"]').contentDocument;
const el = doc.querySelector('#some-id');
```
Or pass the iframe ref as `target` to Playwright tools — Playwright auto-resolves refs inside iframes.

## Workday-specific: date spinbuttons and overlay clicks

Workday renders dates as three `[role="spinbutton"]` inputs (Month/Day/Year). JS `.value =` setters appear to work (aria-valuenow updates) but React state never receives the change and the form rejects on submit. **Use Playwright real `browser_type` with the input ID:**

```
browser_type target=#workExperience-9--startDate-dateSectionMonth-input text=05
browser_type target=#workExperience-9--startDate-dateSectionYear-input text=2025
```

Workday "Select One" buttons are often covered by a `<div data-automation-id="click_filter">` overlay. If `browser_click` throws "subtree intercepts pointer events", click the overlay instead:
```
browser_click target='div[data-automation-id="click_filter"][aria-label="Create Account"]'
```

## "Why isn't my submit going through?" — the diagnostic ladder

Run these in order. The first positive result tells you what to fix.

1. **Error banner probe:**
   ```javascript
   Array.from(document.querySelectorAll('[class*="error"], [role="alert"], [class*="invalid"]'))
     .filter(e => e.offsetParent).map(e => e.innerText.trim().slice(0, 200));
   ```
   Returns `[field label, "This field is required.", ...]`. Scope the fix to those fields.

2. **Combo singleValue lie check** — see above. If any `value === ""` with populated `singleValue`, state-reset bounce; refill all combos.

3. **Unchecked consent checkboxes:**
   ```javascript
   Array.from(document.querySelectorAll('input[type="checkbox"]'))
     .filter(c => c.offsetParent && !c.checked).map(c => c.id);
   ```
   Mass-tick: `.forEach(c => c.click())`.

4. **Hidden cascading field appeared:**
   ```javascript
   Array.from(document.querySelectorAll('input[id^="question_"]'))
     .filter(el => el.offsetParent && !el.value).map(el => el.id);
   ```
   If a question_id you didn't fill is visible, it appeared mid-flow.

5. **Submit button disabled:** inspect `button[type="submit"].disabled`. If true, a required field hasn't passed validation yet.

6. **Validation runs on blur, not Enter:** some forms require focus to leave the field. Fire `change` + `blur` after setting value:
   ```javascript
   el.dispatchEvent(new Event('change', {bubbles: true}));
   el.dispatchEvent(new Event('blur',   {bubbles: true}));
   ```

7. **The `pressSequentially` vs `fill` trap:** if a react-select failed to open its menu, you probably used `fill` or `type` without `slowly: true`. Redo with `slowly: true`.

## Discovery patterns — what fields does this form have?

Before filling anything, map the form. **Batched discovery call:**

```javascript
() => {
  const openQ = Array.from(document.querySelectorAll('input[id^="question_"], textarea[id^="question_"]'))
    .filter(el => el.offsetParent)
    .map(el => ({
      id: el.id,
      tag: el.tagName,
      role: el.getAttribute('role') || '',
      label: document.querySelector(`label[for="${el.id}"]`)?.innerText?.trim().slice(0, 100) || ''
    }));
  const combos = Array.from(document.querySelectorAll('input[role="combobox"]'))
    .filter(el => el.offsetParent)
    .map(el => ({
      id: el.id,
      label: document.querySelector(`label[for="${el.id}"]`)?.innerText?.trim().slice(0, 100) || ''
    }));
  return { openQ, combos };
}
```

This one call tells you: every text/textarea question (`openQ`), every combobox (`combos`), every label, every current value. Enough to plan the fill order.

**Visible-option enumeration (any combo):**
```javascript
Array.from(document.querySelectorAll('[role="option"]'))
  .filter(o => o.offsetParent).map(o => o.innerText.trim());
```

Also check `offsetParent` to distinguish rendered-but-hidden options (e.g. the phone-country-code list is always in the DOM but offscreen when you want the race list).

**Scrollable-menu detection** — some long option lists get truncated by viewport:
```javascript
const menu = document.querySelector('[class*="menu-list"]');
menu ? { height: menu.scrollHeight, client: menu.clientHeight } : null;
// scrollHeight > clientHeight ⇒ options exist below the fold
```

## API discovery — company careers pages often ship open JSON

Many ATS vendors expose unauthenticated listing APIs that enumerate all open roles. Hitting these lets you filter in-browser instead of scraping each careers page.

| Vendor | API |
|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/<company>/jobs` |
| Lever | `https://api.lever.co/v0/postings/<company>?mode=json` |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/<company>` |
| SmartRecruiters | `https://api.smartrecruiters.com/v1/companies/<company>/postings` |

**CORS matters:** Greenhouse-origin pages can `fetch()` the Greenhouse API freely. From any other origin (an iframe apply page, a different ATS), direct `fetch` throws. **Fallback: navigate directly to the API URL and parse `document.body.innerText` as JSON.**

```javascript
// On the API page itself:
const j = JSON.parse(document.body.innerText);
// Filter in-browser, pick role IDs, compose embed URLs
```

**The reusable-token trick (Greenhouse):** a careers wrapper's embed iframe URL contains `?for=<company>&validityToken=<T>&token=<job_id>`. The `validityToken` is COMPANY-scoped; rotate only `token=` to visit any other role on that board without re-resolving. Verified on Pinterest 2026-10-08 — one validityToken, 7 submits.

## Timing — pressSequentially, waits, and the "I think it's done" trap

- **`browser_type slowly=true`** translates to `pressSequentially`, which fires keystroke-level events. Required for react-select autocompletes.
- **`browser_type slowly=false` (default)** fires one bulk `input` event — faster, but typeahead menus won't open.
- **`browser_press_key`** is a single keyboard event; use for Enter, ArrowDown, Tab, Escape.
- **Explicit waits:** `browser_wait_for text="Thank you for applying"` is more reliable than `wait_for timeout=2000`. Prefer content assertions over sleeps.
- **The "snapshot before next action" habit** — `browser_snapshot` is cheap. When uncertain whether a prior action committed, snapshot first. The returned YAML tells you current form state in one call.

## When to call it and HALT

- **Captcha / Turnstile / hCaptcha / reCAPTCHA image challenge:** no automation. Fire Windows toast (per `job-apply` §6) with company + "captcha needed", log friction, move on.
- **2FA / OTP email code required for a flow Sharif can't retrieve async:** toast, keep browser open, move on.
- **8+ digit security code (not Gmail OTP):** Hard halt. Flip `ready_for_review`.
- **Unknown form section after 3 fill-and-retry cycles:** flip `friction_kind='other'` with a precise `friction_detail`.
- **Session expired mid-batch (LinkedIn / any logged-in ATS):** toast, keep browser, do not auto-close. Pivot to no-login ATS targets.

## When to NOT fire this skill

- Pure JD scrape (no form interaction) — just use `browser_navigate` + `browser_snapshot`.
- A specific ATS you've already loaded `ats-playwright-quirks` for — those recipes are more specific.
- LinkedIn Easy Apply — load `linkedin-easy-apply-autoloop` instead (shadow-DOM autoloop, not the techniques here).
- Login provisioning — load `create-account` + `account-recovery`.

## Shared assets — stop re-typing the same JS every submit

Three files codify the patterns in this skill so you don't retype them inline:

- [`Scripts/playwright/greenhouse_diag.js`](../../../Scripts/playwright/greenhouse_diag.js) — the probes memorized. `errorsVisible()`, `errorMap()`, `checkComboLie(id)`, `checkAllComboLies()`, `uncheckedConsents({tick:true})`, `discoverFields()`, `visibleOptions()`, `unfilledRequired()`, `retagNumericIds([...])`, `tagAttachButtons()`, `reactSafeSet(selector, value)`. Load the file verbatim into a `browser_evaluate` function body, then call what you need. One source of truth; no inline drift.
- [`Scripts/job_search/greenhouse_rapid_apply.py`](../../../Scripts/job_search/greenhouse_rapid_apply.py) — CLI resolver. One call → ranked apply URLs filtered to Sharif's whitelist. `python -m job_search.greenhouse_rapid_apply <slug> [--title REGEX] [--exclude IDS] [--embed VALIDITYTOKEN] [--json]`. Exit 0 on hits, 2 on none, 1 on API failure.
- [`Scripts/data/race_list_variants.yaml`](../../../Scripts/data/race_list_variants.yaml) — six documented EEO race taxonomies (standard Greenhouse, Pinterest-Marketing-no-Asian, Lever, Workday federal, Oracle HCM, Ashby) with the honest fallback for each. When `visibleOptions()` shows a race list, match against this file and pick the variant's `pick:` field. **Never fabricate.** If Asian isn't offered, pick the neutral opt-out. If no variant matches, add a new one before picking.

## Cross-references

- [`job-apply`](../job-apply/SKILL.md) §7 — per-ATS playbook, §10 Playwright recipes
- [`ats-playwright-quirks`](../ats-playwright-quirks/SKILL.md) — vendor-specific DOM traps + the Common Mistakes table
- [`linkedin-easy-apply-autoloop`](../linkedin-easy-apply-autoloop/SKILL.md) — SDUI shadow-DOM mega-loop
- `Scripts/data/application_answers.yaml` — canonical answer values (never invent)

## Session battle record (2026-10-08)

- 30 submits in one day across Workable / Workday / Ashby / Greenhouse (Pinterest × 7, Anthropic × 2, Zillow × 6, Doximity, ZoomInfo, Typeform, Life360, Grafana, Omada, Mercury, Descript, You.com, Arize, Kard, Cohere, GameChanger, TLDR, Murmuration).
- 7 Pinterest Greenhouse submits in ~15 min using the reusable-validityToken trick + the 7-step fill pattern.
- 2 Anthropic Greenhouse submits with per-role "Why Anthropic?" textareas + 7 custom screening combos each.
- Discovered + patched: Pinterest Sr DS Marketing EEO race list omits "Asian" → honest fallback "I don't wish to answer."
- Discovered + patched: cascading sponsor combo appears mid-form on auth=Yes answer → re-poll required.
- Discovered + patched: react-select state resets on submit bounce → refill rule.
