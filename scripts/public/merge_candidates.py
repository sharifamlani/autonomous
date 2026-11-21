"""Merge public/_candidates/*.tsv into one de-duplicated list with fresh GitHub metadata.

Reads every per-theme candidate file, merges rows that name the same repo (case-insensitive,
following GitHub renames), re-pulls stars / last push / license / archived from `gh api`, and
writes:

  public/candidates.tsv   one row per repo (the survey's data)
  PUBLIC_REPOS.md         the tables between the GENERATED markers (hand-written parts kept)

Usage:
  python scripts/public/merge_candidates.py            # refresh metadata from GitHub, write both
  python scripts/public/merge_candidates.py --offline  # merge only, keep the scouts' metadata
  python scripts/public/merge_candidates.py --check    # exit 1 if candidates.tsv is incomplete

Exits non-zero if a repo cannot be fetched (it is kept, flagged `missing`) or on --check failure.
"""
import argparse
import csv
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "public" / "_candidates"
OUT = ROOT / "public" / "candidates.tsv"
SURVEY = ROOT / "PUBLIC_REPOS.md"
IN_COLS = ["name", "url", "stars", "last_push", "license", "archived", "theme", "why"]
OUT_COLS = ["name", "url", "stars", "last_push", "license", "archived", "themes", "papers", "status", "description", "why"]
THEMES = {
    "01": "Agent architectures and orchestration",
    "02": "Harnesses, Claude Code and autonomy",
    "03": "Coding agents and SWE benchmarks",
    "04": "Multi-agent software teams",
    "05": "Verification, testing and QA",
    "06": "AI scientists and research agents",
    "07": "Data science agents and benchmarks",
    "08": "Reproducibility and research integrity",
    "09": "Evaluation, reliability and cost",
}
SURVEY_DATE = datetime(2026, 11, 21, tzinfo=timezone.utc)
PAPER_ID = re.compile(r"\b[AHCTVSDRF]\d{1,2}\b")
START, END = "<!-- GENERATED: tables start -->", "<!-- GENERATED: tables end -->"


def read_candidates():
    merged = {}
    for f in sorted(CAND.glob("*.tsv")):
        lines = f.read_text(encoding="utf-8").splitlines()
        if lines[0].split("\t") != IN_COLS:
            sys.exit(f"FATAL: {f.name} header is not {IN_COLS}")
        for n, line in enumerate(lines[1:], 2):
            if not line.strip():
                continue
            c = line.split("\t")
            if len(c) != len(IN_COLS):
                sys.exit(f"FATAL: {f.name}:{n} has {len(c)} columns")
            row = dict(zip(IN_COLS, c))
            key = row["name"].strip().lower()
            if key in merged:
                m = merged[key]
                m["themes"].add(row["theme"])
                m["whys"].append(f"[{row['theme']}] {row['why']}")
            else:
                row["themes"] = {row["theme"]}
                row["whys"] = [f"[{row['theme']}] {row['why']}"]
                merged[key] = row
    return list(merged.values())


def gh(name):
    try:
        p = subprocess.run(["gh", "api", f"repos/{name}"], capture_output=True, text=True, timeout=60, encoding="utf-8")
    except subprocess.TimeoutExpired:
        return None
    return json.loads(p.stdout) if p.returncode == 0 else None


def refresh(row):
    d = gh(row["name"])
    if d is None:
        row["status"] = "missing"
        row["description"] = ""
        return row
    full = d["full_name"]
    row["status"] = "renamed" if full.lower() != row["name"].lower() else "ok"
    row["name"], row["url"] = full, d["html_url"]
    row["stars"] = str(d["stargazers_count"])
    row["last_push"] = d["pushed_at"] or ""
    lic = (d.get("license") or {}).get("spdx_id") or "NONE"
    row["license"] = "NONE" if lic in ("NOASSERTION", "NONE") and not d.get("license") else lic
    row["archived"] = str(d["archived"]).lower()
    row["description"] = (d.get("description") or "").replace("\t", " ").replace("\n", " ")
    return row


def normalise_offline(row):
    row["status"] = "offline"
    row["description"] = ""
    if row["license"].strip().lower() in ("none", ""):
        row["license"] = "NONE"
    return row


def finish(rows):
    # renames can make two candidate rows the same repo: merge again on the canonical name
    out = {}
    for r in rows:
        k = r["name"].lower()
        if k in out:
            out[k]["themes"] |= r["themes"]
            out[k]["whys"] += r["whys"]
        else:
            out[k] = r
    for r in out.values():
        r["papers"] = ",".join(sorted(set(PAPER_ID.findall(" ".join(r["whys"]))), key=lambda s: (s[0], int(s[1:]))))
        r["themes"] = ",".join(sorted(r["themes"]))
        r["why"] = " || ".join(w.replace("\t", " ") for w in r["whys"])
    return sorted(out.values(), key=lambda r: (r["themes"].split(",")[0], -int(r["stars"] or 0)))


def stale(push):
    if not push:
        return True
    t = datetime.fromisoformat(push.replace("Z", "+00:00"))
    return (SURVEY_DATE - t).days > 365


def tables(rows):
    out = []
    for code, title in THEMES.items():
        mine = [r for r in rows if r["themes"].split(",")[0] == code]
        out += [f"### {code}. {title} ({len(mine)})", "",
                "| Repo | Stars | Last push | License | Flags | Papers | What it is |", "|---|---:|---|---|---|---|---|"]
        for r in mine:
            flags = []
            if r["archived"] == "true":
                flags.append("archived")
            if stale(r["last_push"]):
                flags.append("stale")
            if r["license"] == "NONE":
                flags.append("no license")
            if r["status"] in ("renamed", "missing"):
                flags.append(r["status"])
            also = [t for t in r["themes"].split(",")[1:]]
            if also:
                flags.append("also " + "/".join(also))
            desc = (r["description"] or r["why"].split(" || ")[0].split("] ", 1)[-1])[:140].replace("|", "/")
            out.append(f"| [{r['name']}]({r['url']}) | {r['stars']} | {r['last_push'][:10]} | {r['license']} | "
                       f"{', '.join(flags)} | {r['papers'].replace(',', ', ')} | {desc} |")
        out.append("")
    return "\n".join(out)


def write_survey(rows):
    body = f"{START}\n\n{tables(rows)}\n{END}"
    if SURVEY.exists():
        s = SURVEY.read_text(encoding="utf-8")
        if START in s and END in s:
            s = s[: s.index(START)] + body + s[s.index(END) + len(END):]
        else:
            s = s.rstrip() + "\n\n" + body + "\n"
    else:
        s = "# Public Repos: GitHub survey\n\n" + body + "\n"
    SURVEY.write_text(s, encoding="utf-8", newline="\n")


def check():
    if not OUT.exists():
        print("FAIL: public/candidates.tsv missing")
        return 1
    rows = list(csv.DictReader(OUT.open(encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))
    bad = [r["name"] for r in rows if r["status"] == "missing" or not all(r[k] for k in ("url", "stars", "last_push", "license", "archived"))]
    names = [r["name"].lower() for r in rows]
    dups = sorted({n for n in names if names.count(n) > 1})
    for b in bad:
        print(f"  incomplete: {b}")
    for d in dups:
        print(f"  duplicate: {d}")
    ok = not bad and not dups and len(rows) >= 60
    print(f"{'PASS' if ok else 'FAIL'}: {len(rows)} repos, {len(bad)} incomplete, {len(dups)} duplicates")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        sys.exit(check())
    rows = read_candidates()
    print(f"merged {sum(1 for _ in CAND.glob('*.tsv'))} files into {len(rows)} unique repos")
    if a.offline:
        rows = [normalise_offline(r) for r in rows]
    else:
        with ThreadPoolExecutor(8) as ex:
            rows = list(ex.map(refresh, rows))
    rows = finish(rows)
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(OUT_COLS) + "\n")
        for r in rows:
            f.write("\t".join(r[c] for c in OUT_COLS) + "\n")
    write_survey(rows)
    missing = [r["name"] for r in rows if r["status"] == "missing"]
    renamed = sum(r["status"] == "renamed" for r in rows)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} repos; {renamed} renamed, {len(missing)} missing) and {SURVEY.name}")
    for m in missing:
        print(f"  missing on GitHub: {m}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
