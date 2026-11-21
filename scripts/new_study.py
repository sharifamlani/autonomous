#!/usr/bin/env python3
# Sharif Amlani
# Python 3.13
# Fall 2026

######################## Code Summary ##################
# ********************* v1 **********************
# Scaffold research/NNN_slug/ from research/_templates (CLAUDE.md §5).
#   - NNN is the next free study number (highest existing + 1) unless --number is given.
#   - Copies PREREG.md and RESULT.md; refuses to overwrite an existing study folder.
#   - Does NOT commit: fill in PREREG.md, then commit it BEFORE any trial (the commit is the
#     pre-registration).
#
# Usage:  python scripts/new_study.py <slug> --title "End-of-day momentum" [--number 1]

######################### Library #####################
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STUDY_RE = re.compile(r"^\d{3}_[a-z0-9_]+$")

######################### Functions ###################
def next_number(research: Path) -> int:
    nums = [int(m.group(1)) for p in research.iterdir() if p.is_dir()
            for m in [re.match(r"^(\d{3})_", p.name)] if m]
    return max(nums, default=0) + 1


def scaffold(slug: str, title: str, research: Path, number: int | None = None) -> Path:
    slug = slug.lower().replace("-", "_")
    n = number if number is not None else next_number(research)
    name = f"{n:03d}_{slug}"
    if not STUDY_RE.match(name):
        raise SystemExit(f"bad study name {name!r}: slug must be lowercase letters, digits, underscores")
    dest = research / name
    if dest.exists():
        raise SystemExit(f"{dest} already exists: refusing to overwrite")
    templates = research / "_templates"
    dest.mkdir(parents=True)
    for fname in ("PREREG.md", "RESULT.md"):
        text = (templates / fname).read_text(encoding="utf-8")
        text = text.replace("Study NNN — <title>", f"Study {n:03d} — {title}")
        text = text.replace("Study NNN — Result", f"Study {n:03d} — Result: {title}")
        (dest / fname).write_text(text, encoding="utf-8")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold a research study from the templates")
    ap.add_argument("slug")
    ap.add_argument("--title", default=None)
    ap.add_argument("--number", type=int, default=None)
    ap.add_argument("--research-dir", default=str(ROOT / "research"))
    args = ap.parse_args()
    research = Path(args.research_dir)
    dest = scaffold(args.slug, args.title or args.slug.replace("_", " "), research, args.number)
    print(f"created {dest}")
    print("next: fill in PREREG.md, then commit it before running any trial:")
    print(f'  git add research/{dest.name}/PREREG.md && git commit -m "research: pre-register {dest.name}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
