from dataclasses import dataclass
from pathlib import Path

import pymupdf

from pdforge._utils import is_valid_page_range, open_pdf
from pdforge.parsing import parse_filename_pages


@dataclass
class PdfCatArgs:
    input: list[str]
    output: Path


def main(args: PdfCatArgs) -> None:
    input = args.input
    output = args.output
    doc = pymupdf.open()

    parsed_args = parse_filename_pages(input)
    for filepath, pages in parsed_args:
        src = open_pdf(filepath)
        start = 0
        end = src.page_count - 1

        if pages:
            start, end = min(pages), max(pages)
            is_valid_page_range(start, end, src.page_count)

        doc.insert_pdf(src, from_page=start, to_page=end)
        src.close()

    doc.save(output, garbage=4, deflate=True)
    doc.close()
    print(f"Merged PDF files into '{output}'")
