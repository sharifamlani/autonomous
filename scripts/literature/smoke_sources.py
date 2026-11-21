"""Smoke-test the two sources a research scout depends on, before any scout runs.

  python scripts/literature/smoke_sources.py

1. arXiv: download one PDF (ReAct, 2210.03629) into a temp dir and check it starts with %PDF.
2. GitHub: `gh api repos/anthropics/claude-code` returns stargazers_count, license.spdx_id, archived
   and pushed_at (license.spdx_id may be null: GitHub detected no license, which itself is the answer).

Prints `arxiv: %PDF ok` and `gh: stars=... license=... archived=... pushed_at=...`.
Exit 0 only when both pass. Nothing is written outside the temp dir.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_papers import download_pdf, is_pdf, resolve_url  # noqa: E402

ARXIV_URL = "https://arxiv.org/abs/2210.03629"
GH_REPO = "anthropics/claude-code"


def smoke_arxiv():
    url = resolve_url(ARXIV_URL)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "smoke.pdf"
        err = download_pdf(url, out)
        if err or not is_pdf(out):
            print(f"arxiv: FAIL {url}: {err or 'file does not start with %PDF'}")
            return False
        print(f"arxiv: %PDF ok ({url}, {out.stat().st_size} bytes)")
    return True


def smoke_gh():
    env = dict(os.environ, GCM_INTERACTIVE="never", GH_PROMPT_DISABLED="1")
    try:
        p = subprocess.run(["gh", "api", f"repos/{GH_REPO}"], capture_output=True, text=True,
                           encoding="utf-8", timeout=60, env=env)
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"gh: FAIL could not run gh ({type(e).__name__}); check it is installed and `gh auth status`")
        return False
    if p.returncode != 0:
        print(f"gh: FAIL exit {p.returncode}: {p.stderr.strip()[:200]}")
        return False
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        print("gh: FAIL response is not JSON")
        return False
    missing = [k for k in ("stargazers_count", "license", "archived", "pushed_at") if k not in d]
    if missing:
        print(f"gh: FAIL fields missing from the response: {', '.join(missing)}")
        return False
    lic = (d["license"] or {}).get("spdx_id")
    print(f"gh: stars={d['stargazers_count']} license={lic} archived={d['archived']} pushed_at={d['pushed_at']}")
    return True


def main() -> int:
    sys.stdout.reconfigure(errors="replace")
    ok = smoke_arxiv()
    ok &= smoke_gh()
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
