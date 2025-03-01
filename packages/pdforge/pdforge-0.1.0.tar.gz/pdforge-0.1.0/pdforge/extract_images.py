from dataclasses import dataclass
from pathlib import Path

import pymupdf

from pdforge._utils import open_pdf


@dataclass
class PdfExtractImagesArgs:
    input: Path
    output: Path


def main(args: PdfExtractImagesArgs) -> None:
    input = args.input
    output = args.output or Path.cwd() / f"{input.stem}-images"
    output.mkdir(parents=True, exist_ok=True)

    src = open_pdf(input)
    for page_index in range(len(src)):
        page = src[page_index]
        images = page.get_images()

        if images:
            print(f"Found {len(images)} images on page {page_index + 1}")
        else:
            print(f"No images found on page {page_index + 1}")

        for img_index, img in enumerate(images, start=1):
            xref = img[0]
            pix = pymupdf.Pixmap(src, xref)

            if pix.n - pix.alpha > 3:
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)

            pix.save("%s/page_%s-image_%s.png" % (output, page_index, img_index))
            pix = None

    src.close()
    print(f"\nImages extracted to {output}")
