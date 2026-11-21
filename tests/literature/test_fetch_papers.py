"""fetch_papers.py: URL resolution, %PDF check, deletion of non-PDFs, idempotence. Offline (fake HTTP);
the live arXiv fetch is smoke S6 in docs/plans/04_research_tooling_and_pilot.md.
"""
import sys
from pathlib import Path

import pytest
import requests

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts" / "literature"))
import fetch_papers as fp  # noqa: E402

FIX = HERE / "fixtures"
PDF_BYTES = b"%PDF-1.5\n%fake paper\n"


class FakeResponse:
    def __init__(self, status, body, ctype):
        self.status_code, self.body, self.headers = status, body, {"Content-Type": ctype}

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def iter_content(self, n):
        yield self.body


class FakeSession:
    """arxiv.org -> a PDF; example.com -> an HTML page; *.invalid -> connection error."""

    def __init__(self):
        self.calls = []

    def get(self, url, headers=None, **kw):
        self.calls.append((url, headers))
        if ".invalid" in url:
            raise requests.ConnectionError("no such host")
        if "arxiv.org/pdf/" in url:
            return FakeResponse(200, PDF_BYTES, "application/pdf")
        return FakeResponse(200, b"<!doctype html><html></html>", "text/html")


@pytest.fixture(autouse=True)
def no_wait(monkeypatch):
    monkeypatch.setattr(fp, "ARXIV_GAP_S", 0)


@pytest.mark.parametrize("url, ident, want", [
    ("https://arxiv.org/abs/2210.03629", "", "https://arxiv.org/pdf/2210.03629"),
    ("https://arxiv.org/abs/2210.03629v3", "", "https://arxiv.org/pdf/2210.03629v3"),
    ("http://www.arxiv.org/abs/2210.03629/", "", "https://arxiv.org/pdf/2210.03629"),
    ("https://arxiv.org/pdf/2210.03629.pdf", "", "https://arxiv.org/pdf/2210.03629"),
    ("https://arxiv.org/html/2210.03629v2", "", "https://arxiv.org/pdf/2210.03629v2"),
    ("", "2210.03629", "https://arxiv.org/pdf/2210.03629"),
    ("https://example.org/paper.pdf", "10.1000/xyz", "https://example.org/paper.pdf"),
])
def test_resolve_url(url, ident, want):
    assert fp.resolve_url(url, ident) == want


def test_fetch_then_skip(tmp_path, capsys):
    s = FakeSession()
    first = fp.fetch(FIX / "one_paper.tsv", tmp_path, s)
    assert first == {"fetched": 1, "skipped": 0, "failed": 0}
    pdf = tmp_path / "01_Agent_Architectures_and_Orchestration" / "A1_Yao_2022_ReAct.pdf"
    assert pdf.read_bytes().startswith(b"%PDF")
    assert s.calls[0][0] == "https://arxiv.org/pdf/2210.03629"
    assert "User-Agent" in s.calls[0][1]
    second = fp.fetch(FIX / "one_paper.tsv", tmp_path, s)
    assert second == {"fetched": 0, "skipped": 1, "failed": 0}
    assert len(s.calls) == 1                       # idempotent: no second request
    assert "fetched 0, skipped 1, failed 0" in capsys.readouterr().out


def test_bad_urls_fail_and_leave_no_file(tmp_path, capsys):
    counts = fp.fetch(FIX / "bad_url.tsv", tmp_path, FakeSession())
    assert counts == {"fetched": 0, "skipped": 0, "failed": 2}
    out = capsys.readouterr().out
    assert "not a PDF (Content-Type text/html); deleted" in out
    assert "request failed: ConnectionError" in out
    assert not list(tmp_path.rglob("*.pdf")) and not list(tmp_path.rglob("*.part"))


def test_existing_non_pdf_is_replaced(tmp_path):
    bad = tmp_path / "01_Agent_Architectures_and_Orchestration" / "A1_Yao_2022_ReAct.pdf"
    bad.parent.mkdir(parents=True)
    bad.write_text("<html>captcha</html>")
    counts = fp.fetch(FIX / "one_paper.tsv", tmp_path, FakeSession())
    assert counts["fetched"] == 1 and bad.read_bytes().startswith(b"%PDF")


def test_cli_exits_nonzero_on_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(fp.requests, "Session", FakeSession)
    monkeypatch.setattr(sys, "argv", ["fetch_papers.py", "--tsv", str(FIX / "bad_url.tsv"), "--dest", str(tmp_path)])
    assert fp.main() == 1
    monkeypatch.setattr(sys, "argv", ["fetch_papers.py", "--tsv", str(FIX / "one_paper.tsv"), "--dest", str(tmp_path)])
    assert fp.main() == 0
