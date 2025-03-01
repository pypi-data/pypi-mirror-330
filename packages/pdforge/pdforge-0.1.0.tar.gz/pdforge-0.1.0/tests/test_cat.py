from pathlib import Path

import pymupdf
import pytest

from pdforge.parsing import parse_pages

from .conftest import run_cli


@pytest.mark.parametrize("page_range", ["1", "1,2,3", "1-5", "1,2,3,4-8"])
def test_cat(sample_pdf: Path, capsys: pytest.CaptureFixture, page_range: str):
    input_pdf = str(sample_pdf)
    output_pdf = str(sample_pdf.parent / "output.pdf")

    error_code = run_cli(["cat", input_pdf, page_range, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Merged PDF files" in out

    src = pymupdf.open(sample_pdf)
    dest = pymupdf.open(output_pdf)

    parsed_pages = parse_pages(page_range)
    total_pages = len(parsed_pages) if parsed_pages else src.page_count
    assert total_pages == dest.page_count

    src.close()
    dest.close()


@pytest.mark.parametrize("page_range", ["0-1", "1-1000"])
def test_cat_invalid_range(sample_pdf: Path, capsys: pytest.CaptureFixture, page_range: str):
    input_pdf = str(sample_pdf)
    output_pdf = str(sample_pdf.parent / "output.pdf")

    error_code = run_cli(["cat", input_pdf, page_range, "-o", output_pdf])
    assert error_code == 2
    assert not Path(output_pdf).exists()

    out, err = capsys.readouterr()
    assert not out
    assert "Invalid page range" in err


def test_cat_multiple_files(sample_pdf: Path, capsys: pytest.CaptureFixture):
    page_ranges = ["1,2,3", "1,2-8", "1-4", "2-4", "4-8"]
    output_pdf = str(sample_pdf.parent / "output.pdf")

    command = ["cat"]
    for page_range in page_ranges:
        command.extend([str(sample_pdf), page_range])
    command.extend(["-o", output_pdf])
    error_code = run_cli(command)

    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Merged PDF files" in out

    total_pages = 0
    for r in page_ranges:
        pages = parse_pages(r)
        total_pages += len(pages)

    dest = pymupdf.open(output_pdf)
    assert total_pages == dest.page_count
    dest.close()
