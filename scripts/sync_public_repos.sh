#!/usr/bin/env bash
#
# Sync the third-party reference repos listed in public/manifest.tsv.
#
# These are upstream projects we read, evaluate, and borrow from. They are
# deliberately NOT vendored into this repo: each stays a real clone with its own
# history and remote, so it can be pulled and diffed against upstream. The
# manifest pins the commit we actually evaluated, so a fresh checkout of this
# repo can reproduce the exact state the notes in _README.md describe.
#
# Usage:
#   scripts/sync_public_repos.sh            ensure every repo is present at its pinned commit
#   scripts/sync_public_repos.sh --latest   fast-forward each repo to upstream tip, rewrite pins
#   scripts/sync_public_repos.sh --verify   assert every repo is present at its pinned commit
#
# Exits non-zero if any repo fails to sync or fails verification.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$REPO_ROOT/public"
MANIFEST="$DEST/manifest.tsv"
MODE="${1:-sync}"

case "$MODE" in
  sync|--sync) MODE=sync ;;
  --latest)    MODE=latest ;;
  --verify)    MODE=verify ;;
  -h|--help)   sed -n '2,20p' "$0"; exit 0 ;;
  *) echo "unknown argument: $MODE (try --help)" >&2; exit 2 ;;
esac

[ -f "$MANIFEST" ] || { echo "FATAL: manifest not found at $MANIFEST" >&2; exit 1; }

fail=0
count=0

# Columns: name <TAB> url <TAB> pinned_commit    ('#' comments and blank lines skipped)
while IFS=$'\t' read -r name url pin; do
  case "${name:-}" in ''|'#'*) continue ;; esac
  count=$((count + 1))
  path="$DEST/$name"

  if [ "$MODE" = verify ]; then
    if [ ! -d "$path/.git" ]; then
      echo "MISSING  $name  (run scripts/sync_public_repos.sh)"; fail=1; continue
    fi
    have="$(git -C "$path" rev-parse HEAD)"
    if [ "$have" = "$pin" ]; then
      echo "OK       $name  @ ${pin:0:7}"
    else
      echo "DRIFT    $name  pinned ${pin:0:7} but HEAD is ${have:0:7}"; fail=1
    fi
    continue
  fi

  if [ ! -d "$path/.git" ]; then
    echo "CLONE    $name  <- $url"
    git clone --quiet --filter=blob:none "$url" "$path" || { echo "FAILED to clone $name" >&2; fail=1; continue; }
  fi

  if [ "$MODE" = latest ]; then
    git -C "$path" fetch --quiet origin || { echo "FAILED to fetch $name" >&2; fail=1; continue; }
    head_ref="$(git -C "$path" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || echo origin/main)"
    git -C "$path" checkout --quiet --detach "$head_ref" || { echo "FAILED to check out $head_ref in $name" >&2; fail=1; continue; }
    new="$(git -C "$path" rev-parse HEAD)"
    if [ "$new" != "$pin" ]; then
      echo "UPDATE   $name  ${pin:0:7} -> ${new:0:7}  ($head_ref)"
      # rewrite this row's pin in place
      tmp="$MANIFEST.tmp.$$"
      awk -v n="$name" -v p="$new" 'BEGIN{FS=OFS="\t"} $1==n{$3=p} {print}' "$MANIFEST" > "$tmp" && mv "$tmp" "$MANIFEST"
    else
      echo "CURRENT  $name  @ ${new:0:7}  (already at upstream tip)"
    fi
  else
    have="$(git -C "$path" rev-parse HEAD)"
    if [ "$have" = "$pin" ]; then
      echo "OK       $name  @ ${pin:0:7}"
    else
      git -C "$path" fetch --quiet origin || true
      if git -C "$path" checkout --quiet --detach "$pin" 2>/dev/null; then
        echo "PINNED   $name  ${have:0:7} -> ${pin:0:7}"
      else
        echo "FAILED to check out pin $pin in $name" >&2; fail=1
      fi
    fi
  fi
done < "$MANIFEST"

echo "---"
if [ "$fail" -ne 0 ]; then
  echo "$count repo(s) processed, with failures." >&2
  exit 1
fi
echo "$count repo(s) processed, all good."
