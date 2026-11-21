# Sharif Amlani
# Python 3.13
# Fall 2026

######################## Code Summary ##################
# ********************* v1 **********************
# Turn final_report/key_numbers.json into numbers.tex (one \newcommand per number) so the paper
# quotes saved results through macros, never hand-typed digits.
# Usage: python numbers_to_tex.py research/NNN_slug/final_report

######################### Library #####################
import json
import re
import sys
from pathlib import Path


######################### Functions ###################
def tex_escape(v: str) -> str:
    return (str(v).replace("\\", r"\textbackslash{}").replace("%", r"\%").replace("$", r"\$")
            .replace("&", r"\&").replace("#", r"\#").replace("_", r"\_"))


def main(folder: str) -> int:
    d = Path(folder)
    nums = json.loads((d / "key_numbers.json").read_text(encoding="utf-8"))
    bad = [k for k in nums if not re.fullmatch(r"[A-Za-z]+", k)]
    if bad:
        print(f"FAIL: macro names must be letters only: {bad}")
        return 1
    lines = ["% Generated from key_numbers.json by numbers_to_tex.py. Do not edit."]
    lines += [f"\\newcommand{{\\{k}}}{{{tex_escape(v)}}}" for k, v in sorted(nums.items())]
    (d / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(nums)} macros to {d / 'numbers.tex'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
