"""Cheat flags (D23): a tool call that reaches for the original package, the repo or another run fails the run.

Checked on every tool_use block as it streams, before the tool's result comes back. The fence is a
seatbelt, not a vault: the agent's shell could still read a path we don't list. Anything flagged is
scored FAIL.
"""
import json
import re

# fragments of the repo's path: the answer keys live there
REPO_MARKERS = ["dropbox (personal)", "genai company", "benchmark/keys", "/autonomous/benchmark"]


# tools that reach outside the room; `watch_net` strings count only here, so a notebook may name a
# famous study in its prose (S4a: "LaLonde") while a web search for its answer is still a cheat
NET_TOOLS = {"WebSearch", "WebFetch", "Bash"}


def flags(block, own_room, watch, watch_net=()):
    text = json.dumps(block.get("input", {})).lower().replace("\\\\", "/").replace("\\", "/")
    out = [f"watch:{w}" for w in watch if w.lower() in text]
    if block.get("name") in NET_TOOLS:
        out += [f"watch_net:{w}" for w in watch_net if w.lower() in text]
    out += [f"repo:{m}" for m in REPO_MARKERS if m in text]
    # another run's room: only names shaped like a room name (r + 10 hex, room.name). Two honest S1 runs were
    # failed by looser rules (`cd C:/abench/<own>; ls` read as "<own>;", then the agent's own
    # C:/abench/_scratch_b1). Leftovers between runs are handled by room.sweep(), not here.
    for other in re.findall(r"abench/(r[0-9a-f]{10})(?![0-9a-f])", text):
        if other != own_room.lower():
            out.append(f"room:{other}")
    return out
