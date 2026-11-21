---
name: shipping-flywheel
description: Use when shipping changes to a live web app under a deadline or at high frequency — hackathon, demo day, launch day, a string of small UI fixes going straight to production, or several Claude Code instances committing to one repo at once. Triggers on "ship it", "commit and ship", "deploy", "we have N minutes", "make sure it's live", "check production", a manual deploy command with no CI, or a risky change requested close to a deadline.
---

# Shipping flywheel

Every change goes round the same loop, and production is part of the loop from the first hour.
The loop is cheap enough to run for a one-line change, so it is never skipped.

## The loop

1. **Fallback first.** Before any change that could break the main path: `git tag <name> && git push origin <name>`. Say the tag name out loud to the human.
2. **Smallest shippable slice.** Order work so each slice is live-able by itself (see Staging).
3. **Type-check.** `npx tsc --noEmit` (or the project's equivalent). Seconds, catches most breakage.
4. **Walk it locally** with a scripted browser: the real user path, start to finish, on the dev server.
5. **Commit only your own paths, push.** Never `git add -A` when other instances share the repo.
6. **Deploy.**
7. **Walk the same script against the production URL.**
8. **Record it** in the roadmap or changelog: what shipped, the commit, what is still unverified.

A walk script prints numbers a reader can check: how many of the thing appeared, console errors, failed requests. "It loaded" is not a result.

## Staging: ship the look before the layout

When one request touches every screen, do not batch it into one deploy near the deadline.

| Stage | Change | Why first |
|---|---|---|
| 1 | Global tokens, fonts, shared button and card classes | Minutes of work, restyles every screen, safe alone |
| 2 | The shell every screen sits in | One file, visible everywhere |
| 3 | Each screen's layout, in parallel on disjoint files | Any screen can be dropped without hurting the rest |
| 4 | Flow or state changes | Riskiest, so last, behind a fresh tag |

Deploy after each stage. If the clock wins, the last stage that shipped is the product.

## Deploy on day one

Put an empty app on a public URL before building features. First-deploy problems (auth, env vars, build config) cost minutes at hour one and the demo at hour four.

## Several instances, one repo

- One concern per instance, on files no other instance edits.
- Each instance commits its own paths and pushes often; the git log becomes the shared timeline.
- One shared roadmap file is the only place status lives.
- **A deploy CLI uploads the working directory, not the last commit.** Another instance's half-finished, uncommitted files go live with your deploy. Run `git status` before deploying and say what else is in the tree.

## Gotchas that cost real minutes

| Symptom | Cause | Do this |
|---|---|---|
| Production check fails seconds after a deploy | The alias has not switched yet | Re-run once before debugging |
| Deploy reports a build error | Previous version is still serving | Safe. Fix forward, do not panic-rollback |
| "Browser is already in use" from the browser MCP | Another instance holds it | Drive your own headless browser from a script |
| Walk passes but the screenshot shows the previous screen | `waitFor` text also exists on the screen you left | Wait for a control unique to the target screen |
| Edit lands in the wrong place, or accents turn to gibberish | A shell one-liner (`sed`, `perl`) rewriting a UTF-8 file | Edit with a script that asserts the anchor text exists, reads and writes UTF-8 |
| `unable to write new_index file` | A sync client (Dropbox) holding the git index | Re-run the commit |
| Old deployment URLs ask for a login | Preview protection | Rebuild that commit in a worktree outside the synced folder |

## When to stop

Set a freeze time before starting, and keep it. After it: reverts only. Tell the human plainly which version is live and which tag is the fallback.
