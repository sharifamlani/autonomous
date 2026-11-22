"""Build the agent-visible inputs for benchmark task S1 (reproduce Tables 2-3 with the replication package).

S1 gives the agent the Amlani & Collitt replication package as published on Dataverse (CC0,
doi:10.7910/DVN/TKBWOC): the four R scripts, the README and the data. The county shapefile (3 MB, only
for the map in Figure 1) is left out. Kept local like every task input (gitignored).

  output: benchmark/tasks/study_s1_reproduce/inputs_local/   (original file names)

Run from the repo root:  python scripts/benchmark/build_inputs_s1.py
Then check for leaks:   python benchmark/run.py --check-inputs --task study_s1_reproduce
"""
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "benchmark/keys/s1/vbm_data.rda"                       # fetched by build_key_s1.R
OUT = ROOT / "benchmark/tasks/study_s1_reproduce/inputs_local"
API = "https://dataverse.harvard.edu/api/access/datafile/{}"
FILES = {                                                             # Dataverse file id -> published name
    5616200: "Table1.R",
    5616203: "Table2_Figure3_Table3_Figure5.R",
    5721996: "Figure1.R",
    5721997: "Figure2_Figure4.R",
    5616205: "README - Replication - Amlani & Collitt 2021 - Election Law Journal.docx",
}


def main():
    if not DATA.exists():
        sys.exit(f"missing {DATA}; run scripts/benchmark/build_key_s1.R first")
    OUT.mkdir(parents=True, exist_ok=True)
    for fid, name in FILES.items():
        req = urllib.request.Request(API.format(fid), headers={"User-Agent": "autonomous-benchmark/0.1"})  # default UA gets 403
        with urllib.request.urlopen(req, timeout=60) as r:
            (OUT / name).write_bytes(r.read())
        print(f"  {name}")
    shutil.copyfile(DATA, OUT / "Replication Data - Amlani & Collitt 2021.rda")
    print(f"wrote {len(FILES) + 1} files to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
