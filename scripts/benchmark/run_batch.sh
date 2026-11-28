#!/usr/bin/env bash
# Run a benchmark batch: every arm x task, k runs each, one after another, logged to one file.
#
#   bash scripts/benchmark/run_batch.sh "<arms>" "<tasks>" <k> <log> [extra run.py args]
#   bash scripts/benchmark/run_batch.sh "baseline kit" "app_a5_missing_doc app_a6_wrong_test" 5 "$TEMP/claude/traps.log"
#
# On Windows the runner runs under pythonw.exe, not python.exe. An agent that stops its own server with
# `taskkill /F /IM python.exe` kills every python.exe on the machine, and that took the runner with it
# (2026-11-27: 6 of 8 trap batches died mid-run). taskkill /IM matches the exact image name, so pythonw.exe
# survives. Prints one line per finished run and a final count; exits 1 if any run.py exited non-zero.
set -u
arms=$1; tasks=$2; k=$3; log=$4; shift 4
cd "$(dirname "$0")/../.."
py=python
if command -v pythonw >/dev/null 2>&1; then py=pythonw; fi
fail=0
: > "$log"
for arm in $arms; do
  for t in $tasks; do
    "$py" benchmark/run.py --arm "$arm" --task "$t" --runs "$k" "$@" >> "$log" 2>&1 || { fail=1; echo "run.py exited non-zero: $arm $t" >> "$log"; }
  done
done
grep -E '\] (DONE|CAP|STUCK|FLAGGED|ERROR)' "$log"
echo "finished runs: $(grep -cE '\] (DONE|CAP|STUCK|FLAGGED|ERROR)' "$log")"
exit $fail
