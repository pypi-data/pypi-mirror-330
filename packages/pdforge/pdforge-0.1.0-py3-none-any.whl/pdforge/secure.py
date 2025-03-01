from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pymupdf

from pdforge._utils import open_pdf


@dataclass
class PdfSecureArgs:
    input: Path
    password: str
    mode: Literal["encrypt", "decrypt"]
    output: Path


def main(args: PdfSecureArgs) -> None:
    input = args.input
    mode = args.mode
    password = args.password
    output = args.output

    src = pymupdf.open()
    if mode == "encrypt":
        src = open_pdf(input)
        output_file = output or f"{input.stem}-encrypted.pdf"
        src.save(
            output_file,
            encryption=pymupdf.PDF_ENCRYPT_AES_256,
            user_pw=password,
            garbage=4,
            deflate=True,
        )
        print(f"Encrypted PDF file saved to '{output_file}'")
    else:
        src = open_pdf(input, password)
        output_file = output or f"{input.stem}-decrypted.pdf"
        src.save(output_file, encryption=pymupdf.PDF_ENCRYPT_NONE, garbage=4, deflate=True)
        print(f"Decrypted PDF file saved to '{output_file}'")

    src.close()
