"""Build the agent-visible inputs for benchmark task S2 (replicate from the paper, no code).

S2 gives the agent only the Methodology section of Amlani & Collitt (2022) and the replication data,
never the code, results, tables 2-3, figures or abstract (they all state the answer). The paper is a
publisher PDF ("For personal use only"), so the extracted text stays local:

  input : benchmark/keys/papers/amlani_collitt_2022.pdf      (local, gitignored)
          benchmark/keys/s1/vbm_data.rda                      (CC0 data, fetched by build_key_s1.R)
  output: benchmark/tasks/study_s2_replicate/inputs_local/    (gitignored)
            methods.md      Methodology section, pp. 4-7 up to RESULTS, equations re-typeset
            vbm_data.rda    the data, unchanged

Run from the repo root:  python scripts/benchmark/build_inputs_s2.py
Then check for leaks:   python benchmark/run.py --check-inputs --task study_s2_replicate
"""
import re
import shutil
import sys
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "benchmark/keys/papers/amlani_collitt_2022.pdf"
DATA = ROOT / "benchmark/keys/s1/vbm_data.rda"
OUT = ROOT / "benchmark/tasks/study_s2_replicate/inputs_local"

EQ_TURNOUT = ("We estimate our DID model using the equation:\n\n"
              "    VAP Turnout = a + b1(Vote by Mail Conditions) + b2(Year)\n"
              "                  + b3(Vote by Mail Conditions x Year) + bi(Xi) + sigma_c + e\n\n")
EQ_SHARE = ("    Republican Presidential Vote Share = a + b1(Vote by Mail Conditions) + b2(Year)\n"
            "                  + b3(Vote by Mail Conditions x Year) + bi(Xi) + sigma_c + e\n\n")


def page_text(doc, i):
    t = doc[i].get_text()
    t = t.replace("For personal use only.", "")
    t = re.sub(r"^\s*(\d{1,2}\s+)?(AMLANI AND COLLITT|VOTE-BY-MAIL POLICY AND THE 2020 ELECTION)(\s+\d{1,2})?\s*$", "", t, flags=re.M)
    return t


def main():
    if not PDF.exists() or not DATA.exists():
        sys.exit(f"missing input: {PDF if not PDF.exists() else DATA}")
    doc = fitz.open(PDF)
    p4, p5, p6, p7 = (page_text(doc, i) for i in (3, 4, 5, 6))
    text = p4[p4.index("METHODOLOGY"):] + "\n" + p5 + "\n" + p6 + "\n" + p7[:p7.index("RESULTS")]
    # re-typeset the two equations (the PDF encodes their symbols as private glyphs)
    text = re.sub(r"We estimate our DID model using the equation:.*?(?=The interaction term)", EQ_TURNOUT, text, count=1, flags=re.S)
    text = re.sub(r"(Republican Presidential Vote Share)\s*\n.*?(?=The interaction term)", EQ_SHARE, text, count=1, flags=re.S)
    text = re.sub(r"-\n(?=[a-z])", "", text)          # hyphenated line breaks
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)      # join wrapped lines
    text = re.sub(r"[ \t]+", " ", text).strip()
    header = ("# Task material: methodology section\n\n"
              "Source: Amlani, Sharif, and Samuel Collitt. 2022. \"The Impact of Vote-By-Mail Policy on Turnout "
              "and Vote Share in the 2020 Election.\" Election Law Journal. Methodology section only "
              "(results, tables of estimates, figures and abstract withheld).\n\n")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "methods.md").write_text(header + text + "\n", encoding="utf-8", newline="\n")
    shutil.copyfile(DATA, OUT / "vbm_data.rda")
    print(f"wrote {OUT.relative_to(ROOT)}/methods.md ({len(text.split())} words) and vbm_data.rda")


if __name__ == "__main__":
    main()
