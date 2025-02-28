from pathlib import Path

import pymupdf
import pytest

from tests.conftest import SAMPLES_ROOT, run_cli


def test_watermak(sample_pdf: Path, capsys: pytest.CaptureFixture):
    input_pdf = str(sample_pdf)
    image = str(SAMPLES_ROOT / "watermark.png")
    output_pdf = str(sample_pdf.parent / "watermark.pdf")

    error_code = run_cli(["watermark", input_pdf, image, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Watermarked PDF" in out

    dest = pymupdf.open(output_pdf)
    img_count = sum(len(p.get_images()) for p in dest)
    assert img_count == dest.page_count
