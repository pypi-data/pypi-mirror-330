from dataclasses import dataclass
from pathlib import Path

from pdforge._utils import open_pdf


@dataclass
class PdfExtractTextArgs:
    input: Path
    output: Path


def main(args: PdfExtractTextArgs) -> None:
    input = args.input
    output = args.output

    src = open_pdf(input)
    output_file = open(output, "wb")
    for p in src:
        text = p.get_text().encode("utf8")
        output_file.write(text)
        output_file.write(bytes((12,)))
    src.close()
    output_file.close

    print(f"Text extracted to {output}")
