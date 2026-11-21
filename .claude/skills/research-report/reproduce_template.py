# Sharif Amlani
# Python 3.13
# Fall 2026

######################## Code Summary ##################
# ********************* v1 **********************
# Replication helper copied into each study's final_report/replication/ as reproduce.py.
#   python reproduce.py --verify   check research/<study>/output/* against MANIFEST.json checksums
#   python reproduce.py --run      run every step in MANIFEST.json (from the repo root), then verify
# ********************* v2 **********************
# Replication notebook standard (Sharif 2026-10-27): when MANIFEST.json has a "notebook" entry, --run executes
# research/<study>/replicate.ipynb headless (nbclient, kernel "trading" if registered else "python3", saved
# in place) instead of the shell steps, then verifies. --verify is unchanged.
# Exit code 0 on a full match, 1 otherwise.

######################### Library #####################
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDY = HERE.parents[1]
ROOT = STUDY.parents[1]


######################### Functions ###################
def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(m: dict) -> int:
    bad, missing = [], []
    base = ROOT if m.get("output_root") == "repo" else STUDY   # v2: wave packages hash repo-relative paths
    for rel, digest in m["output_sha256"].items():
        p = base / rel
        if not p.exists():
            missing.append(rel)
        elif sha256(p) != digest:
            bad.append(rel)
    ok = len(m["output_sha256"]) - len(bad) - len(missing)
    print(f"outputs matching manifest: {ok}/{len(m['output_sha256'])}")
    for r in missing:
        print(f"MISSING {r}")
    for r in bad:
        print(f"DIFFERS {r}")
    print("PASS" if not bad and not missing else "FAIL")
    return 0 if not bad and not missing else 1


def run_notebook(m: dict) -> int:
    import nbformat
    from nbclient import NotebookClient
    nbp = STUDY / m["notebook"]["path"]
    nb = nbformat.read(nbp, as_version=4)
    kernel = nb.metadata.get("kernelspec", {}).get("name", "python3")
    try:
        from jupyter_client.kernelspec import KernelSpecManager
        if kernel not in KernelSpecManager().find_kernel_specs():
            kernel = "python3"
    except Exception:
        kernel = "python3"
    print(f"$ run {nbp.name} headless (kernel {kernel})")
    try:
        NotebookClient(nb, timeout=14400, kernel_name=kernel, resources={"metadata": {"path": str(STUDY)}}).execute()
    except Exception as e:
        print(f"FAIL: notebook run failed: {type(e).__name__}: {str(e).strip().splitlines()[-1][:300]}")
        return 1
    nbformat.write(nb, nbp)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--verify", action="store_true")
    g.add_argument("--run", action="store_true")
    a = ap.parse_args()
    m = json.loads((HERE / "MANIFEST.json").read_text(encoding="utf-8"))
    if a.run and m.get("notebook"):
        if run_notebook(m) != 0:
            return 1
    elif a.run:
        for step in m["steps"]:
            print(f"$ {step}")
            if subprocess.run(step, shell=True, cwd=ROOT).returncode != 0:
                print(f"FAIL at step: {step}")
                return 1
    return verify(m)


if __name__ == "__main__":
    sys.exit(main())
