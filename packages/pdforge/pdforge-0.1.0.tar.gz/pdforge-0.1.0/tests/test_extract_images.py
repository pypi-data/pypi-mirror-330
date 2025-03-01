from pathlib import Path

import pymupdf
import pytest

from tests.conftest import SAMPLES_ROOT, run_cli


def test_extract_images(sample_pdf: Path, capsys: pytest.CaptureFixture):
    input_pdf = str(SAMPLES_ROOT / "images.pdf")
    output_images = str(sample_pdf.parent / "output-images")

    error_code = run_cli(["extract-images", input_pdf, "-o", output_images])
    assert error_code == 0
    assert Path(output_images).exists()

    out, err = capsys.readouterr()
    assert not err
    assert "Images extracted" in out

    src = pymupdf.open(input_pdf)
    img_count = sum(len(p.get_images()) for p in src)
    img_output_count = sum(1 for f in Path(output_images).iterdir() if f.is_file())
    assert img_count == img_output_count

    src.close()
