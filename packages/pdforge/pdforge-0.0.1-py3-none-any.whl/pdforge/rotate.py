from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pdforge._utils import open_pdf, parse_pages

rotations_map = {
    "right": 90,
    "upside-down": 180,
    "left": 270,
}


@dataclass
class PdfRotateArgs:
    input: Path
    pages: str
    rotation: Literal["left", "right", "upside-down"]
    output: Path


def main(args: PdfRotateArgs) -> None:
    input = args.input
    pages = args.pages
    rotation = args.rotation
    output = args.output

    src = open_pdf(input)
    pages_parsed = parse_pages(src, pages)

    angle = rotations_map[rotation]
    for p in pages_parsed:
        src[p].set_rotation(angle)

    src.save(output, garbage=4, deflate=True)
    src.close()
    print(f"Rotated pages and saved to '{output}'")
