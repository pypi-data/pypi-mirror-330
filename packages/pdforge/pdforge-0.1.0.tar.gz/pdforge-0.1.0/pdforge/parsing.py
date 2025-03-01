import re
from datetime import datetime
from typing import Optional, Set, Tuple


def parse_pages(pages: str) -> Set[int]:
    nums = set()
    pages_arr = pages.split(",")

    for p in pages_arr:
        p = p.strip()

        match_single = re.match(r"^\d+$", p)
        match_range = re.match(r"^(\d+)-(\d+)$", p)

        if match_single:
            nums.add(int(p) - 1)
        elif match_range:
            start, end = map(int, match_range.groups())
            if start > end:
                raise ValueError(f"Invalid page range: {pages}")
            nums.update(range(start - 1, end))
        else:
            raise ValueError(f"Invalid page range: {pages}")

    return nums


def parse_filename_pages(args: list[str]) -> list[Tuple[str, Set[int] | None]]:
    pairs: list[Tuple[str, Set[int] | None]] = []
    filename: Optional[str] = None
    for arg in args + [None]:
        try:
            pages = parse_pages(arg)
            pairs.append((filename, pages))
            if filename is None:
                raise ValueError("Page range must follow a filename")
            filename = None
        except Exception:
            if filename:
                pairs.append((filename, None))
            filename = arg

    return pairs


def parse_date(date_fmt: str) -> datetime:
    """
    Parses a PDF date string from the metadata in the format:
    "D:YYYYMMDDHHMMSSZ00'00'" (e.g., "D:20160319061844Z00'00'")
    """
    date = date_fmt.split(":")[1]
    date = date.replace("Z00'00'", "+00:00")
    fmt = "%Y%m%d%H%M%S%z"
    parsed_date = datetime.strptime(date, fmt)
    return parsed_date
