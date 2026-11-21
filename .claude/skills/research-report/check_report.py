# Sharif Amlani
# Python 3.13
# Fall 2026

######################## Code Summary ##################
# ********************* v1 **********************
# Build and verify a study's final report. Runs latexmk on final_report/report.tex, then checks:
#   1. the PDF exists and the main article ends by page 5 (\label{mainend} before \appendix)
#   2. no undefined references or citations, and every \includegraphics file exists
#   3. every value in key_numbers.json appears verbatim in RESULT.md or a saved output/*.json
# ********************* v2 **********************
#   4. every included figure has an entry in figures/manifest.json with a title, axis labels and
#      human-readable legend labels (no snake_case, pipes or bare lowercase codes); Sharif 2026-10-18
# ********************* v3 **********************
#   5. the replication package exists (README, MANIFEST, code copies, reproduce.py) and the study's
#      saved outputs match the manifest checksums (reproduce.py --verify)
# ********************* v4 **********************
# Wave reports (Sharif 2026-10-18): --max-pages N (wave report limit 20) and --studies a,b,c so key
# numbers may trace to any listed study's RESULT.md / output json.
# ********************* v5 **********************
# Replication notebook standard (Sharif 2026-10-27): research/NNN_slug/replicate.ipynb must exist, be saved
# executed (every code cell has an execution count, outputs present), contain no error outputs, and end with
# a verify cell that printed PASS. Required for studies whose PREREG is dated 2026-10-28 or later (first git
# commit of PREREG.md, else the first date in its text, else file mtime) or when --require-notebook is passed;
# finished studies 002-053 keep their .py scripts. --execute re-runs the notebook headless (nbclient, in
# memory; the committed file is not touched) and fails if the run fails or any output/ checksum changes.
# --notebook-only runs just the notebook checks (no LaTeX build), for use while the study is being built.
# Prints PASS / FAIL lines and exits non-zero on any failure.
# Usage: python check_report.py research/NNN_slug [--report-dir DIR] [--max-pages 20] [--studies research/030_x,research/031_y]
#        [--require-notebook] [--execute] [--notebook-only]

######################### Library #####################
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

MAX_MAIN_PAGES = 5
NOTEBOOK = "replicate.ipynb"
NOTEBOOK_FROM = date(2026, 10, 28)       # studies pre-registered on or after this date must have the notebook
ROOT = Path(__file__).resolve().parents[3]


def is_code_like(label: str) -> bool:
    """Same rule as make_figures.py: snake_case, pipes, or bare lowercase/digit tokens are codes."""
    s = str(label).strip()
    return (not s) or "_" in s or "|" in s or bool(re.fullmatch(r"[a-z0-9]+", s))


######################### Functions ###################
def prereg_date(study: Path) -> date | None:
    """Date of the study's PREREG: first git commit of PREREG.md, else the first ISO date in its text, else mtime."""
    p = study / "PREREG.md"
    if not p.exists():
        return None
    r = subprocess.run(["git", "log", "--diff-filter=A", "--format=%cs", "--", str(p.resolve())], cwd=ROOT,
                       capture_output=True, text=True)
    lines = [x for x in r.stdout.split() if x]
    if lines:
        return date.fromisoformat(lines[-1])          # the oldest commit that added the file
    m = re.search(r"20\d\d-\d\d-\d\d", p.read_text(encoding="utf-8", errors="replace"))
    if m:
        return date.fromisoformat(m.group(0))
    return date.fromtimestamp(p.stat().st_mtime)


def notebook_required(study: Path, require_flag: bool) -> bool:
    if require_flag:
        return True
    d = prereg_date(study)
    return d is not None and d >= NOTEBOOK_FROM


def output_checksums(study: Path) -> dict:
    out = study / "output"
    res = {}
    for f in sorted(out.rglob("*")) if out.exists() else []:
        if f.is_file() and "_cache" not in f.parts and f.name != "CHECKSUMS.json":
            h = hashlib.sha256()
            with open(f, "rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b""):
                    h.update(chunk)
            res[str(f.relative_to(study)).replace("\\", "/")] = h.hexdigest()
    return res


def check_notebook(study: Path, execute: bool = False, timeout: int = 7200) -> list:
    """Return a list of failure strings for the study's replicate.ipynb (empty list = PASS)."""
    import nbformat
    nbp = study / NOTEBOOK
    if not nbp.exists():
        return [f"{NOTEBOOK} missing: all study code lives in one notebook (Sharif 2026-10-27)"]
    fails = []
    nb = nbformat.read(nbp, as_version=4)
    codes = [c for c in nb.cells if c.cell_type == "code"]
    if not codes:
        return [f"{NOTEBOOK} has no code cells"]
    errs = [i for i, c in enumerate(codes) for o in c.get("outputs", []) if o.get("output_type") == "error"]
    if errs:
        fails.append(f"{NOTEBOOK} has error outputs in code cells {sorted(set(errs))}")
    unexec = [i for i, c in enumerate(codes) if c.get("execution_count") is None and c.source.strip()]
    n_out = sum(len(c.get("outputs", [])) for c in codes)
    if n_out == 0 or unexec:
        fails.append(f"{NOTEBOOK} was not saved executed (no outputs, or code cells never run: {unexec[:10]}); "
                     f"run it (Run All) and save with outputs")
    last = "".join(str(o.get("text", "")) for o in codes[-1].get("outputs", []))
    if "PASS" not in last:
        fails.append(f"{NOTEBOOK}: the last (verify) cell did not print PASS")
    if not any(re.search(r"^\s*RERUN\s*=", c.source, re.M) for c in codes):
        fails.append(f"{NOTEBOOK}: no RERUN flag defined (RERUN = False at the top of the first code cell)")
    if fails or not execute:
        if not fails:
            print(f"PASS: {NOTEBOOK} exists, saved executed, no error outputs, verify cell printed PASS")
        return fails

    # --execute: headless run in memory; the committed notebook file is not touched
    from nbclient import NotebookClient
    before = output_checksums(study)
    kernel = nb.metadata.get("kernelspec", {}).get("name", "python3")
    try:
        from jupyter_client.kernelspec import KernelSpecManager
        if kernel not in KernelSpecManager().find_kernel_specs():
            kernel = "python3"
    except Exception:
        kernel = "python3"
    try:
        NotebookClient(nb, timeout=timeout, kernel_name=kernel, resources={"metadata": {"path": str(study.resolve())}}).execute()
    except Exception as e:                                  # CellExecutionError, DeadKernelError, timeout
        tail = str(e).strip().splitlines()
        return [f"headless run of {NOTEBOOK} failed: {type(e).__name__}: {tail[-1][:300] if tail else ''}"]
    after = output_checksums(study)
    changed = sorted(k for k in before if k in after and before[k] != after[k])
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    if changed or added or removed:
        fails.append(f"headless run changed output checksums: changed {changed[:8]}, added {added[:8]}, removed {removed[:8]}")
    else:
        print(f"PASS: headless run of {NOTEBOOK} succeeded and {len(after)} output checksums are unchanged")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("study")
    ap.add_argument("--report-dir", default=None, help="defaults to <study>/final_report")
    ap.add_argument("--max-pages", type=int, default=MAX_MAIN_PAGES, help="main-article page limit (wave reports: 20)")
    ap.add_argument("--studies", default="", help="comma list of extra study dirs whose RESULT.md/output json count as sources")
    ap.add_argument("--require-notebook", action="store_true", help="fail if replicate.ipynb is missing or invalid (automatic for PREREG dated 2026-10-28+)")
    ap.add_argument("--execute", action="store_true", help="also run replicate.ipynb headless and require unchanged output checksums")
    ap.add_argument("--notebook-only", action="store_true", help="run only the notebook checks (no LaTeX build)")
    a = ap.parse_args()
    max_pages = a.max_pages
    study = Path(a.study)
    rep = Path(a.report_dir) if a.report_dir else study / "final_report"
    fails = []

    # 0. Replication notebook (Sharif 2026-10-27): required for new studies; checked when present for older ones
    if notebook_required(study, a.require_notebook or a.execute or a.notebook_only):
        fails += check_notebook(study, execute=a.execute)
    elif (study / NOTEBOOK).exists():
        fails += check_notebook(study, execute=False)
    else:
        print(f"SKIP: {NOTEBOOK} not required (PREREG before {NOTEBOOK_FROM}; use --require-notebook to enforce)")
    if a.notebook_only:
        for f in fails:
            print(f"FAIL: {f}")
        print("PASS" if not fails else "FAIL")
        return 0 if not fails else 1

    if not shutil.which("latexmk"):
        print("FAIL: latexmk not found on PATH (TinyTeX expected)")
        return 1
    r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "report.tex"],
                       cwd=rep, capture_output=True, text=True, encoding="utf-8", errors="replace")
    pdf = rep / "report.pdf"
    if r.returncode != 0 or not pdf.exists():
        print(f"FAIL: latexmk exit {r.returncode}\n{r.stdout[-2000:]}")
        return 1
    print("PASS: built report.pdf")

    log = (rep / "report.log").read_text(encoding="utf-8", errors="replace")
    if re.search(r"undefined (references|citations)|Citation .* undefined|Reference .* undefined", log):
        fails.append("undefined references or citations in report.log")

    aux = (rep / "report.aux").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\\newlabel\{mainend\}\{\{[^}]*\}\{(\d+)\}", aux)
    if not m:
        fails.append("\\label{mainend} not found before the appendix")
    else:
        page = int(m.group(1))
        (print if page <= max_pages else lambda s: fails.append(s))(
            f"{'PASS' if page <= max_pages else 'FAIL'}: main article ends on page {page} (limit {max_pages})")

    tex = (rep / "report.tex").read_text(encoding="utf-8")
    for g in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex):
        if not any((rep / d / g).exists() for d in ("", "figures")):
            fails.append(f"missing figure {g}")

    manifest_path = rep / "figures" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    for g in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex):
        name = Path(g).name if Path(g).suffix else Path(g).name + ".pdf"
        entry = manifest.get(name)
        if not entry:
            fails.append(f"figure {name} has no entry in figures/manifest.json (title, axis labels, legend)")
            continue
        for key in ("title", "xlabel", "ylabel"):
            if not str(entry.get(key, "")).strip():
                fails.append(f"figure {name}: missing {key}")
        codes = [lab for lab in entry.get("legend", []) if is_code_like(lab)]
        if codes:
            fails.append(f"figure {name}: code-like legend labels {codes}; use plain English")
        else:
            print(f"PASS: figure {name} has a title, axis labels and readable legend labels")

    nums_path = rep / "key_numbers.json"
    if nums_path.exists():
        nums = json.loads(nums_path.read_text(encoding="utf-8"))
        corpus = ""
        for sd in [study] + [Path(x) for x in a.studies.split(",") if x.strip()]:
            if (sd / "RESULT.md").exists():
                corpus += "\n" + (sd / "RESULT.md").read_text(encoding="utf-8")
            for j in (sd / "output").glob("*.json") if (sd / "output").exists() else []:
                corpus += "\n" + j.read_text(encoding="utf-8", errors="replace")
        missing = [f"{k}={v}" for k, v in nums.items() if str(v) not in corpus]
        if missing:
            fails.append(f"{len(missing)} key numbers not found verbatim in RESULT.md/output json: {missing[:10]}")
        else:
            print(f"PASS: all {len(nums)} key numbers trace to saved outputs")
    else:
        fails.append("key_numbers.json missing")

    # 5. Replication package (Sharif 2026-10-18): README, MANIFEST, code copies, outputs verify
    repl = rep / "replication"
    need = [repl / "README.md", repl / "MANIFEST.json", repl / "reproduce.py", repl / "code"]
    absent = [str(p.relative_to(rep)) for p in need if not p.exists()]
    if absent:
        fails.append(f"replication package incomplete: missing {absent} (run make_replication.py)")
    else:
        man = json.loads((repl / "MANIFEST.json").read_text(encoding="utf-8"))
        if not man.get("code_sha256"):
            fails.append("replication MANIFEST lists no code files")
        if not man.get("steps") or not man.get("datasets"):
            fails.append("replication MANIFEST needs steps and datasets")
        v = subprocess.run([sys.executable, str(repl / "reproduce.py"), "--verify"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        if v.returncode != 0:
            fails.append(f"replication verify failed: {v.stdout.strip().splitlines()[-3:]}")
        else:
            print(f"PASS: replication package complete; {len(man['code_sha256'])} code files, "
                  f"saved outputs match manifest checksums")

    for f in fails:
        print(f"FAIL: {f}")
    print("PASS" if not fails else "FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
