"""Cheat flags (D23): a tool call that reaches for the original package, the repo or another run fails the run.

Checked on every tool_use block as it streams, before the tool's result comes back. The fence is a
seatbelt, not a vault: the agent's shell could still read a path we don't list. Anything flagged is
scored FAIL.
"""
import json
import re

# fragments of the repo's path: the answer keys live there
REPO_MARKERS = ["dropbox (personal)", "genai company", "benchmark/keys", "/autonomous/benchmark"]


def flags(block, run_id, watch):
    text = json.dumps(block.get("input", {})).lower().replace("\\\\", "/").replace("\\", "/")
    out = [f"watch:{w}" for w in watch if w.lower() in text]
    out += [f"repo:{m}" for m in REPO_MARKERS if m in text]
    for other in re.findall(r"abench/([^/\"' ]+)", text):          # another run's room
        if other != run_id.lower():
            out.append(f"room:{other}")
    return out
