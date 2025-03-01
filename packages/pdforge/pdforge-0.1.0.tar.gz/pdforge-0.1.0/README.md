# pdforge: iLovePDF made in home.

I'm too lazy to go to iLovePDF so i wrote this. Blessings!

## Install
```console
pip install -U pdforge
```
`pdforge` is an application, you might want to install it with [`pipx`](https://pypi.org/project/pipx/).

## Usage
```console
$ pdforge -h

usage: pdforge [-h] [-v]
             {cat,rm,secure,meta,rotate,extract-text,extract-images,watermark}
             ...

pdforge: iLovePDF made in home.

options:
  -h, --help            show this help message and exit
  -v, --version         display the current version

commands:
  {cat,rm,secure,meta,rotate,extract-text,extract-images,watermark}
                        PDF Utilities
    cat                 Merge multiple PDF files into a single PDF document
    rm                  Remove specified pages from a PDF and create a new
                        file with the remaining pages
    secure              Encrypt or decrypt a PDF file
    meta                Retrieve metadata from a PDF file
    rotate              Rotate page horizontally or vertically
    extract-text        Extract text from PDF file
    extract-images      Extract images from PDF file
    watermark           Add a watermark to every page in a PDF file

For help with a specific command, see: `pdforge <command> -h`.
```

To view detailed help for each subcommand, use the `-h` or `--help` flag:
```console
$ pdforge cat -h

usage: pdforge cat [-h] [-o [OUTPUT]] FILE[:PAGES]] [FILE[:PAGES]] ...]

positional arguments:
  FILE[:PAGES]]         Path to the input PDF files to merge. Optionally
                        specify a page or page range in the format
                        'file.pdf:page' or 'file.pdf:start-end'

options:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        Output filename. Defaults to 'output.pdf'
```
