from pathlib import Path

import pymupdf
import pytest

from pdforge._utils import parse_pages
from tests.conftest import run_cli


@pytest.mark.parametrize("page_range", ["1", "1,2,3", "1-3", "1,2,4-6"])
def test_rm(sample_pdf: Path, capsys: pytest.CaptureFixture, page_range: str):
    input_pdf = str(sample_pdf)
    output_pdf = str(sample_pdf.parent / "output.pdf")

    error_code = run_cli(["rm", input_pdf, page_range, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Removed pages" in out

    src = pymupdf.open(input_pdf)
    dest = pymupdf.open(output_pdf)
    pages = parse_pages(src, page_range)
    page_count = src.page_count - len(pages)
    assert dest.page_count == page_count
    
    src.close()
    dest.close()


@pytest.mark.parametrize("page_range", ["a", "-", "1-", "0-1", "1-1000", "1000-1", "1-1-1"])
def test_rm_invalid_range(sample_pdf: Path, capsys: pytest.CaptureFixture, page_range: str):
    input_pdf = str(sample_pdf)
    output_pdf = str(sample_pdf.parent / "output.pdf")

    error_code = run_cli(["rm", input_pdf, page_range, "-o", output_pdf])
    assert error_code == 2
    assert not Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not out
    assert "Invalid page range" in err
