from dataclasses import dataclass
from pathlib import Path

from pdforge._utils import open_pdf, parse_pages


@dataclass
class PdfRemoveArgs:
    input: Path
    pages: str
    output: Path


def main(args: PdfRemoveArgs) -> None:
    input = args.input
    pages = args.pages
    output = args.output

    src = open_pdf(input)
    pages_parsed = parse_pages(src, pages)

    src.delete_pages(list(pages_parsed))
    src.save(output, garbage=4, deflate=True)

    src.close()
    print(f"Removed pages and saved to '{output}'")
