# public/: third-party GitHub repos

Upstream open-source projects we read, evaluate, and borrow from. **Nothing here is ours** and
nothing here ships in the kit unless it is copied in deliberately, license-checked, with attribution.

## How this folder works

The clones are **gitignored**: each stays a real clone with its own history and remote, so it can be
pulled and diffed against upstream rather than frozen into our history. What *is* committed:

| File | What it is |
|---|---|
| `manifest.tsv` | `name, url, pinned_commit` for every clone: the exact state our notes describe |
| `_README.md` | This file: one evaluation section per clone (what it is, license, what we take from it) |
| `_candidates/<NN>.tsv` | Repos the literature scouts flagged, per literature folder, before the survey |

```
bash scripts/sync_public_repos.sh           # ensure every repo is present at its pinned commit
bash scripts/sync_public_repos.sh --latest  # fast-forward to upstream tip, rewrite the pins
bash scripts/sync_public_repos.sh --verify  # assert pins match; non-zero exit on drift
```

A fresh checkout has an empty `public/`; one command refills it at the exact state these notes
describe. The full survey (stars, last push, license, archived, evidence labels) is
`PUBLIC_REPOS.md` at the repo root, written in ROADMAP Phase 6.

## Rules

- **Untrusted code.** Clones are read, not executed or installed, until a deliberate sandboxed run.
- **License first.** Check `license.spdx_id` from the GitHub API and the raw `LICENSE` file before
  copying anything. No license means no copying.
- **Claims are claims.** A README's numbers are UNVERIFIED until one of our studies re-runs them.

## Clones

None yet.
