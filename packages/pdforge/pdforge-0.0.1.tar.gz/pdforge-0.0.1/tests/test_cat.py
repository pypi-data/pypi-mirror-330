from pathlib import Path

import pymupdf
import pytest

from pdforge._utils import parse_pages

from .conftest import run_cli


@pytest.mark.parametrize("page_range", [":", ":1", ":1-5", ":2-8"])
def test_cat(sample_pdf: Path, capsys: pytest.CaptureFixture, page_range: str):
    output_pdf = str(sample_pdf.parent / "output.pdf")
    input_pdf = str(sample_pdf) + page_range

    error_code = run_cli(["cat", input_pdf, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Merged PDF files" in out

    src = pymupdf.open(sample_pdf)
    dest = pymupdf.open(output_pdf)

    _, pages = input_pdf.split(":")
    parsed_pages = parse_pages(src, pages) if pages else []
    total_pages = len(parsed_pages) if parsed_pages else src.page_count
    assert total_pages == dest.page_count

    src.close()
    dest.close()


@pytest.mark.parametrize("page_range", ["a", "-", "1-", "0-1", "1-1000", "1000-1", "1-1-1"])
def test_cat_invalid_range(sample_pdf: Path, capsys: pytest.CaptureFixture, page_range: str):
    input_pdf = f"{sample_pdf}:{page_range}"
    output_pdf = str(sample_pdf.parent / "output.pdf")

    error_code = run_cli(["cat", input_pdf, "-o", output_pdf])
    assert error_code == 2
    assert not Path(output_pdf).exists()

    out, err = capsys.readouterr()
    assert not out
    assert "Invalid page range" in err


def test_cat_multiple_files(sample_pdf: Path, capsys: pytest.CaptureFixture):
    page_range = [":1-4", ":2-4", ":4-8"]
    output_pdf = str(sample_pdf.parent / "output.pdf")
    input_files = [f"{sample_pdf}{p}" for p in page_range]

    error_code = run_cli(["cat", *input_files, "-o", output_pdf])
    assert error_code == 0
    assert Path(output_pdf).is_file()

    out, err = capsys.readouterr()
    assert not err
    assert "Merged PDF files" in out

    total_pages = 0
    for i, f in enumerate(input_files):
        path, pages = f.split(":")
        src = pymupdf.open(path)
        parsed_pages = parse_pages(src, pages)
        total_pages += len(parsed_pages)
        src.close()

    dest = pymupdf.open(output_pdf)
    assert total_pages == dest.page_count
    dest.close()
