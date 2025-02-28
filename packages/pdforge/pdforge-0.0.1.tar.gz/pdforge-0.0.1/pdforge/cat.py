from dataclasses import dataclass
from pathlib import Path

import pymupdf

from pdforge._utils import open_pdf, parse_pages


@dataclass
class PdfCatArgs:
    input: list[str]
    output: Path


def main(args: PdfCatArgs) -> None:
    files = args.input
    output = args.output

    doc = pymupdf.open()
    for f in files:
        input = f.split(":", 1)
        path = Path(input[0])
        pages = input[1] if len(input) > 1 else ""
        src = open_pdf(path)

        start, end = 0, src.page_count - 1
        if pages:
            pages_parsed = parse_pages(src, pages)
            start, end = min(pages_parsed), max(pages_parsed)

        doc.insert_pdf(src, from_page=start, to_page=end)
        src.close()

    doc.save(output, garbage=4, deflate=True)
    doc.close()
    print(f"Merged PDF files into '{output}'")
