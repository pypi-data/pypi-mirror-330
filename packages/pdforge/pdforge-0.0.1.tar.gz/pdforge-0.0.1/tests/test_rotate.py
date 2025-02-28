from pathlib import Path

import pymupdf
import pytest

from pdforge._utils import parse_pages
from pdforge.rotate import rotations_map
from tests.conftest import run_cli


@pytest.mark.parametrize("page_range", ["1", "1,2,3", "1-3", "1,2,4-6"])
@pytest.mark.parametrize("rotation", ["left", "right", "upside-down"])
def test_rotate(sample_pdf: Path, capsys: pytest.CaptureFixture, rotation: str, page_range: str):
    input_pdf = str(sample_pdf)
    output_pdf = str(sample_pdf.parent / "output.pdf")

    error_code = run_cli(["rotate", input_pdf, page_range, "-r", rotation, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Rotated pages" in out

    # Check if outfile has correct rotation for each page
    dest = pymupdf.open(output_pdf)
    for p in parse_pages(dest, page_range):
        angle = rotations_map[rotation]
        assert angle == dest[p].rotation
    dest.close()
