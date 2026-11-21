#!/usr/bin/env python3
# Sharif Amlani
# Python 3.13
# Fall 2026

######################## Code Summary ##################
# ********************* v1 **********************
# Headless "Run All" for a study notebook (CLAUDE.md §5 step 7; ROADMAP row 4.1, smoke S2).
#   - Executes every cell top to bottom with nbclient, in the notebook's own folder, with the
#     kernel named in the notebook's metadata (the template uses `python3`).
#   - PASS only if no cell produced an error output AND the last code cell (the verify step)
#     printed a line that is exactly "PASS".
#   - By default the executed copy is written to a new temp dir (the source notebook is untouched);
#     --inplace overwrites the notebook with its executed version (outputs visible, for committing).
#   - Prints what it did, then exactly one final line:
#       PASS: 0 error cells, verify cell PASS        (exit 0)
#       FAIL: <reason>                               (exit 1)
#
# Usage:  python scripts/research/run_notebook.py <notebook.ipynb> [--inplace] [--timeout 600]

######################### Library #####################
import argparse
import asyncio
import sys
import tempfile
import warnings
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError, CellTimeoutError, DeadKernelError

######################### Functions ###################
def error_cells(nb) -> list[tuple[int, str]]:
    """(cell index, 'EName: evalue') for every code cell with an error output."""
    found = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                found.append((i, f"{out.get('ename', '?')}: {out.get('evalue', '')}".strip()))
                break
    return found


def verify_cell_passed(nb) -> tuple[bool, str]:
    """True if the last code cell printed a line that is exactly 'PASS'; also returns its last printed line."""
    code = [c for c in nb.cells if c.cell_type == "code" and c.source.strip()]
    if not code:
        return False, "(no code cells)"
    text = "".join(out.get("text", "") for out in code[-1].get("outputs", []) if out.get("output_type") == "stream")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "PASS" in lines, (lines[-1] if lines else "(no output)")


def run(nb_path: Path, inplace: bool, timeout: int) -> tuple[bool, str]:
    nb = nbformat.read(nb_path, as_version=4)
    kernel = nb.metadata.get("kernelspec", {}).get("name", "python3")
    print(f"notebook : {nb_path}")
    print(f"kernel   : {kernel}   cwd: {nb_path.parent}   timeout/cell: {timeout}s")
    client = NotebookClient(nb, timeout=timeout, kernel_name=kernel,
                            resources={"metadata": {"path": str(nb_path.parent)}})
    crash = None
    try:
        client.execute()
    except CellExecutionError:
        pass                                    # the error output is in the notebook; counted below
    except (CellTimeoutError, DeadKernelError) as e:
        crash = f"{type(e).__name__}: {str(e).strip().splitlines()[0] if str(e).strip() else ''}"

    if inplace:
        out_path = nb_path
    else:
        out_path = Path(tempfile.mkdtemp(prefix="run_notebook_")) / nb_path.name
    nbformat.write(nb, out_path)
    print(f"executed : {out_path}")

    errors = error_cells(nb)
    for i, msg in errors:
        print(f"error    : cell {i}: {msg}")
    if crash:
        return False, f"FAIL: {crash}"
    if errors:
        i, msg = errors[0]
        return False, f"FAIL: {len(errors)} error cell(s); first is cell {i}: {msg}"
    ok, last = verify_cell_passed(nb)
    if not ok:
        return False, f"FAIL: verify cell did not print PASS (last line: {last})"
    return True, "PASS: 0 error cells, verify cell PASS"


######################### Main #######################
def main() -> int:
    ap = argparse.ArgumentParser(description="Run a notebook headless, top to bottom, and check its verify cell")
    ap.add_argument("notebook", help="path to the .ipynb to execute")
    ap.add_argument("--inplace", action="store_true", help="overwrite the notebook with its executed version")
    ap.add_argument("--timeout", type=int, default=600, help="seconds allowed per cell (default 600)")
    args = ap.parse_args()

    if sys.platform == "win32":                 # zmq needs a selector loop; avoids the Proactor warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    nb_path = Path(args.notebook).resolve()
    if not nb_path.is_file():
        print(f"FAIL: notebook not found: {nb_path}")
        return 1
    try:
        ok, line = run(nb_path, args.inplace, args.timeout)
    except Exception as e:                      # kernel missing, unreadable notebook, ...
        ok, line = False, f"FAIL: {type(e).__name__}: {e}"
    print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
