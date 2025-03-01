from dataclasses import dataclass
from pathlib import Path

from pdforge._utils import open_pdf
from pdforge.parsing import parse_date


@dataclass
class PdfMetaArgs:
    input: Path


def main(args: PdfMetaArgs) -> None:
    input = args.input

    src = open_pdf(input)
    data = src.metadata
    data["pageCount"] = src.page_count

    print(f"Metadata for: {input.name}\n{'-' * 50}")
    for key, value in data.items():
        if key == "creationDate" or key == "modDate":
            value = parse_date(value)
        print(f"{key:<20} : {value if value else 'None'}")

    src.close()
