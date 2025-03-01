import sys
from pathlib import Path

import pymupdf


def error_args(msg: str, code=2) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


def open_pdf(path: Path, password="") -> pymupdf.Document:
    try:
        doc = pymupdf.open(path)

        if not doc.is_pdf:
            error_args(f"{path}'not a pdf")
        if not doc.needs_pass:
            return doc

        if password:
            rc = doc.authenticate(password)
            if not rc:
                error_args(f"'{path.name}' authentication failed")
            return doc
        else:
            error_args(f"'{path.name}' has not been decrypted")
    except pymupdf.FileNotFoundError as e:
        error_args(e)
    except pymupdf.FileDataError as e:
        error_args(e)
    except Exception as e:
        error_args(e)


def is_valid_page_range(start: int, end: int, total: int) -> bool:
    if not (0 <= start <= end <= total):
        error_args(f"Invalid page range: {start}-{end}")
