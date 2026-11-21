# Sharif Amlani
# Python 3.13
# Fall 2026

######################## Code Summary ##################
# ********************* v1 **********************
# Build a study's replication package in final_report/replication/ (Sharif 2026-10-18), like an
# academic replication archive:
#   code/            copies of the study's own code, PREREG.md and RESULT.md (the study stays frozen)
#   MANIFEST.json    git commit, Python and poetry.lock fingerprints, sha256 of every copied code file
#                    and every saved output, plus the datasets and steps from replication.json
#   README.md        how to reproduce: environment, data access (licensed data is NOT included),
#                    the exact commands, expected outputs
#   reproduce.py     `--verify` checks saved outputs against the manifest checksums;
#                    `--run` re-executes the documented steps, then verifies
# Inputs: final_report/replication.json written by the report agent:
#   {"datasets": [{"name": "tiingo_eod", "vendor": "Tiingo", "as_of": "...", "filter": "SPY 1993-2026"}],
#    "steps": ["poetry run python research/NNN_slug/run.py register", "..."],
#    "runtime_note": "about 20 minutes on a laptop CPU"}
# ********************* v2 **********************
# Wave reports: --studies research/030_x,research/031_y copies each study's code to code/<study>/ and
# hashes every study's outputs relative to the repo root (MANIFEST output_root = "repo").
# ********************* v3 **********************
# Replication notebook standard (Sharif 2026-10-27): when the study has replicate.ipynb it is the single
# entry point. The package copies it to replication/replicate.ipynb (and code/), hashes it (MANIFEST
# "notebook"), supplies the default step (headless nbconvert --execute) when replication.json lists none, and
# writes a README that says: open replicate.ipynb, select the Trading (Poetry) kernel, Run All.
# Usage: python make_replication.py research/NNN_slug [--studies research/030_x,research/031_y]

######################### Library #####################
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CODE_SUFFIXES = {".py", ".md", ".yaml", ".yml", ".toml", ".sql", ".R", ".ipynb"}
LICENCES = {
    "sharadar": "Sharadar (Nasdaq Data Link) Personal Use License: redistribution not permitted; subscribe to reproduce.",
    "tiingo": "Tiingo terms: individual, internal use; fetch with your own key.",
    "fred": "FRED/ALFRED (St. Louis Fed): public; attribute the series sources.",
    "coinbase": "Coinbase Exchange public market data API.",
    "kalshi": "Kalshi API terms; read-only market data with your own key.",
    "french": "Kenneth R. French Data Library: public, free.",
    "kenneth": "Kenneth R. French Data Library: public, free.",
    "sharadar_funds": "Sharadar (Nasdaq Data Link) Personal Use License: redistribution not permitted; subscribe to reproduce.",
    "aqr": "AQR datasets: public downloads, see AQR terms.",
    "jkp": "JKP factors: CC BY-NC.",
    "chen_zimmermann": "Open Source Asset Pricing (Chen-Zimmermann): public downloads.",
    "noaa": "NOAA NCEI GHCN-Daily: public.",
    "gdelt": "GDELT Project: public.",
}


######################### Functions ###################
def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def copy_code(study: Path, dst_dir: Path, prefix: str) -> dict:
    copied = {}
    for f in sorted(study.rglob("*")):
        rel = f.relative_to(study)
        if (f.is_file() and f.suffix in CODE_SUFFIXES and rel.parts[0] not in ("final_report", "output")
                and "__pycache__" not in rel.parts):
            dst = dst_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)
            copied[prefix + str(rel).replace("\\", "/")] = sha256(f)
    return copied


def main(study_arg: str, studies: list | None = None) -> int:
    study = (ROOT / study_arg).resolve() if not Path(study_arg).is_absolute() else Path(study_arg)
    rep = study / "final_report" / "replication"
    spec_path = study / "final_report" / "replication.json"
    if not spec_path.exists():
        print(f"FAIL: {spec_path} missing (datasets, steps, runtime_note)")
        return 1
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    nb_path = study / "replicate.ipynb"
    has_nb = nb_path.exists()
    nb_step = f"poetry run jupyter nbconvert --to notebook --execute --inplace research/{study.name}/replicate.ipynb"
    if has_nb and not spec.get("steps"):
        spec["steps"] = [nb_step]            # the notebook is the whole pipeline
    if not spec.get("steps") or not spec.get("datasets"):
        print("FAIL: replication.json needs non-empty 'datasets' and 'steps' (steps may be omitted when replicate.ipynb exists)")
        return 1

    code_dir = rep / "code"
    code_dir.mkdir(parents=True, exist_ok=True)
    if studies:
        # v2 wave package: code/<study>/..., outputs hashed relative to the repo root
        copied, outputs = {}, {}
        for sa in [study_arg] + studies:
            sd = (ROOT / sa).resolve()
            copied.update(copy_code(sd, code_dir / sd.name, sd.name + "/"))
            if (sd / "output").exists():
                outputs.update({str(f.relative_to(ROOT)).replace("\\", "/"): sha256(f)
                                for f in sorted((sd / "output").rglob("*")) if f.is_file() and "_cache" not in f.parts})
    else:
        copied = copy_code(study, code_dir, "")
        outputs = {str(f.relative_to(study)).replace("\\", "/"): sha256(f)
                   for f in sorted((study / "output").rglob("*")) if f.is_file() and "_cache" not in f.parts} \
            if (study / "output").exists() else {}

    manifest = {
        "study": study.name,
        "git_commit": git("rev-parse", "HEAD"),
        "repository": "private: sharifamlani/trading (code copied here so the package stands alone)",
        "python": platform.python_version(),
        "poetry_lock_sha256": sha256(ROOT / "poetry.lock") if (ROOT / "poetry.lock").exists() else None,
        "shared_library": "packages/trading (the repo's trading package at the commit above)",
        "datasets": spec["datasets"],
        "steps": spec["steps"],
        "runtime_note": spec.get("runtime_note", ""),
        "code_sha256": copied,
        "output_sha256": outputs,
    }
    if has_nb:
        shutil.copy2(nb_path, rep / "replicate.ipynb")
        manifest["notebook"] = {"path": "replicate.ipynb", "sha256": sha256(nb_path), "kernel": "trading (Trading (Poetry))",
                                "run": "open replicate.ipynb, select the Trading (Poetry) kernel, Run All; RERUN = False reuses cached outputs"}
    if studies:
        manifest["output_root"] = "repo"
        manifest["studies"] = [Path(x).name for x in [study_arg] + studies]
    (rep / "MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    vendors = sorted({d.get("vendor", d.get("name", "")).lower().split()[0] for d in spec["datasets"]})
    lic = [f"- **{v}**: {LICENCES.get(v, 'see the vendor terms')}" for v in vendors]
    run_block = (f"""## Run it (one notebook)
All of the study's code is `replicate.ipynb` (also in `../../replicate.ipynb`, the study folder). To reproduce:
1. Install the environment (below) and register the kernel once: `poetry run python scripts/dev/register_kernel.py`.
2. **Open `replicate.ipynb`, select the "Trading (Poetry)" kernel, press Run All.** It loads the data from the
   store, computes every result, writes `output/`, builds the figures and `final_report/key_numbers.json`, prints
   the headline table and ends with a checksum PASS / FAIL.
3. `RERUN = False` (top of the first code cell, the default) reuses the cached outputs; set `RERUN = True` to
   recompute everything from the data.
4. Headless: `{nb_step}`.

Equivalent command list (what `reproduce.py --run` executes):""" if has_nb else "## Steps")
    readme = f"""# Replication package: {study.name}

This folder lets a reader reproduce the results in `../report.pdf`.

## What is included
- `code/`: the study's own code, `PREREG.md` (pre-registration) and `RESULT.md`, copied at commit
  `{manifest['git_commit'][:12]}`.
- `MANIFEST.json`: environment fingerprints and the SHA-256 of every code file and saved output.
- `reproduce.py`: `--verify` checks your outputs against the manifest; `--run` re-executes the steps
  (for a notebook study: runs `replicate.ipynb` headless, then verifies).

## What is NOT included, and why
The underlying market data is licensed and cannot be redistributed. Pull it yourself:
{chr(10).join(lic)}

Datasets used (point-in-time store, `as_of` = knowledge cut-off used by the study):
{chr(10).join(f"- `{d.get('name')}` ({d.get('vendor', '')}): {d.get('filter', '')}; as_of {d.get('as_of', 'n/a')}" for d in spec['datasets'])}

## Environment
- Python {manifest['python']}; dependencies pinned by `poetry.lock` (sha256 `{str(manifest['poetry_lock_sha256'])[:16]}...`).
- The shared `trading` library (data store, simulator, cost model, factory gate) at the commit above.
- `poetry install --with research,models`, then set `TRADING_DATA_DIR` to your data store.

{run_block}
{chr(10).join(f"{i+1}. `{s}`" for i, s in enumerate(spec['steps']))}

Expected runtime: {(manifest['runtime_note'] or 'see RESULT.md').rstrip('.')}.

## Verify
`python reproduce.py --verify` compares the outputs in `research/{study.name}/output/` with the checksums
in `MANIFEST.json`. Exact byte equality needs the same data snapshot and library versions; if your data
was pulled later (vendor revisions), compare the key numbers in `../key_numbers.json` instead.

## Integrity notes
The study was pre-registered (see `code/PREREG.md` and its commit) and its holdout was opened once.
Numbers in the paper are generated from the saved outputs listed in the manifest.
"""
    (rep / "README.md").write_text(readme, encoding="utf-8")
    shutil.copy2(Path(__file__).with_name("reproduce_template.py"), rep / "reproduce.py")
    print(f"PASS: replication package in {rep} ({len(copied)} code files, {len(outputs)} outputs hashed)")
    return 0


if __name__ == "__main__":
    extra = sys.argv[sys.argv.index("--studies") + 1].split(",") if "--studies" in sys.argv else []
    sys.exit(main(sys.argv[1], [x for x in extra if x.strip()] or None))
