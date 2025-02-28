import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

import pdforge.cat
import pdforge.extract_images
import pdforge.extract_text
import pdforge.meta
import pdforge.rm
import pdforge.rotate
import pdforge.secure
import pdforge.watermark
from pdforge.__init__ import __version__


def display_version():
    print(f"pdforge v{__version__}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pdforge",
        description="pdforge: iLovePDF made in home.",
        epilog="For help with a specific command, see: `pdforge <command> -h`.",
    )
    parser.add_argument("-v", "--version", action="store_true", help="display the current version")

    ps_commands = parser.add_subparsers(title="commands", help="PDF Utilities", dest="command")

    # ---------------------------------------------------------------------------------------------
    # 'cat' command
    # ---------------------------------------------------------------------------------------------
    ps_cat = ps_commands.add_parser(
        "cat", help="Merge multiple PDF files into a single PDF document"
    )
    ps_cat.add_argument(
        "input",
        nargs="+",
        help="Path to the input PDF files to merge. Optionally specify a page or page range in the format 'file.pdf:page' or 'file.pdf:start-end'",
        metavar="FILE[:PAGES]]",
    )
    ps_cat.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        default="output.pdf",
        help="Output filename. Defaults to 'output.pdf'",
        metavar="OUTPUT",
    )
    ps_cat.set_defaults(func=pdforge.cat.main)

    # ---------------------------------------------------------------------------------------------
    # 'rm' command
    # ---------------------------------------------------------------------------------------------
    ps_rm = ps_commands.add_parser(
        "rm",
        help="Remove specified pages from a PDF and create a new file with the remaining pages",
    )
    ps_rm.add_argument("input", type=Path, help="Path to the input PDF file", metavar="INPUT")
    ps_rm.add_argument(
        "pages",
        help="Pages to remove from the PDF file. Specify as single values (e.g., 3), ranges (e.g., 2-5), or a comma-separated list (e.g., 1,3,6-8)",
        metavar="PAGES",
    )
    ps_rm.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        default="output.pdf",
        help="Output filename. Defaults to 'output.pdf'",
        metavar="OUTPUT",
    )
    ps_rm.set_defaults(func=pdforge.rm.main)

    # ---------------------------------------------------------------------------------------------
    # 'secure' command
    # ---------------------------------------------------------------------------------------------
    ps_secure = ps_commands.add_parser("secure", help="Encrypt or decrypt a PDF file")

    ps_secure.add_argument("input", type=Path, help="Path to the input PDF file", metavar="INPUT")
    ps_secure.add_argument(
        "password", help="Password to encrypt or decrypt the PDF file", metavar="PASSWORD"
    )
    ps_secure.add_argument(
        "-m",
        "--mode",
        choices=["encrypt", "decrypt"],
        required=True,
        help="Choose whether to encrypt or decrypt the PDF file",
        metavar="MODE",
    )
    ps_secure.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        help="Output filename for the processed PDF file. If not provided, it will be named 'filename'-'mode'.pdf",
        metavar="OUTPUT",
    )
    ps_secure.set_defaults(func=pdforge.secure.main)

    # ---------------------------------------------------------------------------------------------
    # 'meta' command
    # ---------------------------------------------------------------------------------------------
    ps_meta = ps_commands.add_parser("meta", help="Retrieve metadata from a PDF file")

    ps_meta.add_argument("input", type=Path, help="Path to the input PDF file", metavar="INPUT")
    ps_meta.set_defaults(func=pdforge.meta.main)

    # ---------------------------------------------------------------------------------------------
    # 'rotate' command
    # ---------------------------------------------------------------------------------------------
    ps_rotate = ps_commands.add_parser(
        "rotate",
        help="Rotate page horizontally or vertically",
    )
    ps_rotate.add_argument("input", type=Path, help="Path to the input PDF file", metavar="INPUT")
    ps_rotate.add_argument(
        "pages",
        help="Pages to rotate",
        metavar="PAGES",
    )
    ps_rotate.add_argument(
        "-r",
        "--rotation",
        default="left",
        choices=pdforge.rotate.rotations_map.keys(),
        help="Rotation direction. Choose from: left, right, upside-down. Defaults to left",
        metavar="ROTATION",
    )
    ps_rotate.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        default="output.pdf",
        help="Output filename. Defaults to 'output.pdf'",
        metavar="OUTPUT",
    )
    ps_rotate.set_defaults(func=pdforge.rotate.main)

    # ---------------------------------------------------------------------------------------------
    # 'extract-text' command
    # ---------------------------------------------------------------------------------------------
    ps_extract_text = ps_commands.add_parser(
        "extract-text",
        help="Extract text from PDF file",
    )
    ps_extract_text.add_argument(
        "input", type=Path, help="Path to the input PDF file", metavar="INPUT"
    )
    ps_extract_text.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        default="output.txt",
        help="Output filename. Defaults to 'output.txt'",
        metavar="OUTPUT",
    )
    ps_extract_text.set_defaults(func=pdforge.extract_text.main)

    # ---------------------------------------------------------------------------------------------
    # 'extract-images' command
    # ---------------------------------------------------------------------------------------------
    ps_extract_images = ps_commands.add_parser(
        "extract-images",
        help="Extract images from PDF file",
    )
    ps_extract_images.add_argument(
        "input", type=Path, help="Path to the input PDF file", metavar="INPUT"
    )
    ps_extract_images.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        help="Output folder. Defaults to 'file'-images",
        metavar="OUTPUT",
    )
    ps_extract_images.set_defaults(func=pdforge.extract_images.main)

    # ---------------------------------------------------------------------------------------------
    # 'watermark' command
    # ---------------------------------------------------------------------------------------------
    ps_watermark = ps_commands.add_parser(
        "watermark",
        help="Add a watermark to every page in a PDF file",
    )
    ps_watermark.add_argument(
        "input", type=Path, help="Path to the input PDF file", metavar="INPUT"
    )
    ps_watermark.add_argument(
        "image",
        type=Path,
        help="Path to the image file (e.g., PNG or JPG) that will be used as the watermark",
        metavar="IMAGE",
    )
    ps_watermark.add_argument(
        "-o",
        "--output",
        type=Path,
        nargs="?",
        default="watermarked.pdf",
        help="Output filename. Defaults to 'watermarked.pdf'",
        metavar="OUTPUT",
    )
    ps_watermark.set_defaults(func=pdforge.watermark.main)

    args = parser.parse_args(argv)

    if args.version:
        display_version()
        sys.exit(0)

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    else:
        args.func(args)
        sys.exit(0)
