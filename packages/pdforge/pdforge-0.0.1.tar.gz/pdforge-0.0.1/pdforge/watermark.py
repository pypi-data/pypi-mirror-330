from dataclasses import dataclass
from pathlib import Path

from pdforge._utils import error_args, open_pdf


@dataclass
class PdfWatermarkArgs:
    input: Path
    image: Path
    output: Path


def main(args: PdfWatermarkArgs) -> None:
    input = args.input
    image_path = args.image
    output = args.output

    src = open_pdf(input)
    try:
        img = open(image_path, "rb").read()
        img_xref = 0
        for page in src:
            page.insert_image(
                rect=page.bound(), stream=img, xref=img_xref, overlay=False
            )

        src.save(output, garbage=4, deflate=True)
        print(f"Watermarked PDF file saved to '{output}'")
    except (FileNotFoundError, PermissionError) as e:
        error_args(e)
    except Exception as e:
        error_args(e)
    finally:
        src.close()
