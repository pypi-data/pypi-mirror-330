from pathlib import Path

import pymupdf
import pytest

from pdforge._utils import open_pdf


def test_open_pdf(sample_pdf: Path):
    doc = open_pdf(sample_pdf)
    assert isinstance(doc, pymupdf.Document)


def test_open_pdf_not_found():
    with pytest.raises(SystemExit):
        open_pdf("/non_existent.pdf")


def test_open_pdf_requires_password(encrypted_pdf: Path, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        open_pdf(encrypted_pdf)

    out, err = capsys.readouterr()
    assert not out
    assert "not been decrypted" in err


def test_open_pdf_password(encrypted_pdf: Path):
    doc = open_pdf(encrypted_pdf, "pepelotas")
    assert isinstance(doc, pymupdf.Document)


def test_open_pdf_invalid_password(encrypted_pdf: Path, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit):
        open_pdf(encrypted_pdf, "wrong_password")

    out, err = capsys.readouterr()
    assert not out
    assert "authentication failed" in err
