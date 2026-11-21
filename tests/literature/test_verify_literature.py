"""verify_literature.py catches each kind of bad literature entry, and passes a clean library.

Each test builds a repo root in tmp_path (clean fixture + one defect overlay; see fixtures/_README.md)
and runs the checker on it with --root, exactly as a user would.
"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
CHECKER = HERE.parents[1] / "scripts" / "literature" / "verify_literature.py"
README02 = Path("literature/02_Claude_Code_and_Harness_Engineering/README.md")
PAPERS = Path("literature/papers.tsv")
PDF_A1 = Path("literature/01_Agent_Architectures_and_Orchestration/A1_Yao_2022_ReAct.pdf")


def build(tmp_path, overlay=None):
    """Clean fixture tree, then the overlay on top. `*.pdf.txt` lands as `*.pdf` (no PDFs in git)."""
    root = tmp_path / "repo"
    shutil.copytree(FIX / "clean", root)
    if overlay:
        for src in (FIX / overlay).rglob("*"):
            if src.is_file():
                rel = src.relative_to(FIX / overlay)
                dst = root / (rel.with_suffix("") if src.name.endswith(".pdf.txt") else rel)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
    return root


def run(*args):
    p = subprocess.run([sys.executable, str(CHECKER), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def test_clean_fixture_passes(tmp_path):
    code, out = run("--all", "--root", build(tmp_path))
    assert code == 0, out
    assert out.strip().endswith("PASS")
    assert "stale: skipped" in out          # no reorg_map.tsv: skipped with a note, not a crash
    assert "WARN A1" in out                 # missing PDF is only a warning


@pytest.mark.parametrize("overlay, expected", [
    ("missing_section", "missing section 'The catch'"),
    ("duplicate_id", "duplicate id A1"),
    ("short_row", "short row: 9 fields, expected 10"),
    ("fake_pdf", "A1_Yao_2022_ReAct.pdf: not a PDF"),
    ("short_candidate", "short candidates row: 3 fields, expected 8"),
])
def test_planted_defect_is_caught(tmp_path, overlay, expected):
    code, out = run("--all", "--root", build(tmp_path, overlay))
    assert code != 0, out
    assert expected in out, out
    assert out.strip().endswith("FAIL")


def test_valid_local_pdf_passes(tmp_path):
    root = build(tmp_path)
    (root / PDF_A1).write_bytes(b"%PDF-1.4\n%fixture\n")
    code, out = run("--all", "--root", root)
    assert code == 0, out
    assert "WARN A1" not in out


def edit(root, rel, old, new):
    p = root / rel
    s = p.read_text(encoding="utf-8")
    assert old in s
    p.write_text(s.replace(old, new), encoding="utf-8")


@pytest.mark.parametrize("rel, old, new, expected", [
    (README02, "# 02 Claude Code and Harness Engineering", "# 03 Claude Code", "first line is '# 03 Claude Code'"),
    (PAPERS, "H1\t02_", "A7\t02_", "A7 prefix A does not match folder 02 (prefix H)"),
    (PAPERS, "\t2022\t", "\t22\t", "year '22' is not 4 digits"),
    (PAPERS, "\tyes\n", "\tmaybe\n", "verified 'maybe' is not yes/no"),
    (PAPERS, "A1_Yao_2022_ReAct.pdf", "react.pdf", "does not follow <ID>_<FirstAuthor>_<Year>_<Short_Title>.pdf"),
    (PAPERS, "A1_Yao_2022_ReAct.pdf", "A1_Smith_2022_ReAct.pdf", "author 'Smith' is not in first_author"),
    (PAPERS, "id\tfolder", "ID\tfolder", "header is"),
    (Path("public/_candidates/02.tsv"), "\t156484\t", "\t\t", "has empty field(s): stars"),
])
def test_other_rule_violations(tmp_path, rel, old, new, expected):
    root = build(tmp_path)
    edit(root, rel, old, new)
    code, out = run("--all", "--root", root)
    assert code != 0, out
    assert expected in out, out


def test_missing_note_is_an_error(tmp_path):
    root = build(tmp_path)
    next((root / "literature").rglob("*_NOTE.md")).unlink()
    code, out = run("--all", "--root", root)
    assert code != 0 and "notes are committed" in out, out


def test_agent_contract_full_prompt_passes():
    code, out = run("--agent", FIX / "scout_prompt_full.md")
    assert code == 0, out
    assert "agent contract: PASS" in out


def test_agent_contract_partial_prompt_lists_what_is_missing():
    code, out = run("--agent", FIX / "scout_prompt_partial.md")
    assert code != 0, out
    for missing in ["README section 'The catch'", "papers.tsv column 'arxiv_or_doi'", "papers.tsv column 'verified'",
                    "candidates column 'last_push'", "candidates column 'archived'", "file-name pattern",
                    "phrase 'fetched source'"]:
        assert missing in out, out
    assert "agent contract: FAIL" in out


def test_agent_missing_file_fails(tmp_path):
    code, out = run("--agent", tmp_path / "nope.md")
    assert code != 0 and "agent contract: FAIL" in out
