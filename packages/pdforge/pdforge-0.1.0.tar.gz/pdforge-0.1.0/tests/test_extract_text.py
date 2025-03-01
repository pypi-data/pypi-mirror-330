from pathlib import Path

import pytest

from tests.conftest import run_cli


def test_extract_text(sample_pdf: Path, capsys: pytest.CaptureFixture):
    input_pdf = str(sample_pdf)
    output_pdf = str(sample_pdf.parent / "output.txt")

    error_code = run_cli(["extract-text", input_pdf, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Text extracted" in out
