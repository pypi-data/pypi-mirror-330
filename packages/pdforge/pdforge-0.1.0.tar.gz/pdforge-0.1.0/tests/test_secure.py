from pathlib import Path

import pymupdf
import pytest

from tests.conftest import run_cli


def test_secure_encrypt(sample_pdf: Path, capsys: pytest.CaptureFixture):
    input_pdf = str(sample_pdf)
    output_pdf = str(sample_pdf.parent / "encrypted.pdf")
    password = "password"

    error_code = run_cli(["secure", input_pdf, password, "-m", "encrypt", "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Encrypted" in out

    dest = pymupdf.open(output_pdf)
    assert dest.is_encrypted
    assert dest.needs_pass
    assert dest.authenticate(password) > 0

    dest.close()


def test_secure_decrypt(sample_pdf: Path, capsys: pytest.CaptureFixture):
    input_pdf = str(sample_pdf)
    output_pdf = str(sample_pdf.parent / "encrypted.pdf")
    password = "password"

    error_code = run_cli(["secure", input_pdf, password, "-m", "decrypt", "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Decrypted" in out

    dest = pymupdf.open(output_pdf)
    assert not dest.is_encrypted
    assert not dest.needs_pass

    dest.close()
