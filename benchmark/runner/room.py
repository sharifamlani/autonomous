"""The clean room: a fresh folder per run at C:\\abench\\<run-id>, holding task.md and the inputs only.

Why C:\\abench (D23, spike 2026-11-22): Claude Code finds CLAUDE.md files by walking up from the
working folder, so any folder under the user's home picks up the personal ~/.claude/CLAUDE.md. A room
outside the home folder, the repo and Dropbox starts as stock Claude Code and keeps the answer keys
out of the agent's neighbourhood.
"""
import os
import re
import shutil
from pathlib import Path

ROOM_ROOT = Path(os.environ.get("AUTONOMOUS_ROOM_ROOT", "C:/abench"))


def _assert_outside_home(p):
    home = str(Path.home().resolve()).lower()
    if str(p.resolve()).lower().startswith(home):
        raise SystemExit(f"room {p} is under {home}: the personal CLAUDE.md would load (D23)")


def build(task, run_id):
    room = ROOM_ROOT / run_id
    _assert_outside_home(ROOM_ROOT)
    if room.exists():
        raise SystemExit(f"room {room} already exists")
    room.mkdir(parents=True)
    shutil.copyfile(task["dir"] / task.get("prompt", "task.md"), room / "task.md")
    if task.get("inputs"):
        shutil.copytree(task["dir"] / task["inputs"], room, dirs_exist_ok=True)
    return room


def probe():
    """An empty room for the clean-room check; recreated each time."""
    room = ROOM_ROOT / "_probe"
    _assert_outside_home(ROOM_ROOT)
    shutil.rmtree(room, ignore_errors=True)
    room.mkdir(parents=True)
    return room


def collect(task, room, dest):
    """Copy what the agent made (everything not copied in as an input) to dest; return the names."""
    given = {"task.md"}
    if task.get("inputs"):
        src = task["dir"] / task["inputs"]
        given |= {str(p.relative_to(src)) for p in src.rglob("*") if p.is_file()}
    made = []
    for p in room.rglob("*"):
        rel = str(p.relative_to(room))
        if p.is_file() and rel not in given:
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest / rel)
            made.append(rel.replace("\\", "/"))
    return sorted(made)


def remove(room):
    shutil.rmtree(room, ignore_errors=True)


def clean_check(context_text):
    """Problems found in a /context report from the room; [] means stock Claude Code."""
    problems = [f"memory file loaded: {l.strip()}" for l in context_text.splitlines() if "CLAUDE.md" in l]
    problems += [f"MCP loaded: {l.strip()}" for l in context_text.splitlines() if re.match(r"\| MCP ", l)]
    skills = context_text.split("### Skills", 1)[1] if "### Skills" in context_text else ""
    for l in skills.splitlines():
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0] not in ("Skill", "") and not cells[0].startswith("-") and cells[1] != "Built-in":
            problems.append(f"non-built-in skill: {cells[0]} ({cells[1]})")
    return problems
