#!/usr/bin/env python3
"""Copy the pre-rendered entry image to the output directory.

Reads MAKEFUN_OUTPUT_DIR (default "out") and copies entry.png from the
repository root into it as entry.png. The image itself is drawn by
render.py (PIL, stdlib-free of the entrypoint: this file only copies bytes,
so both graded runs produce byte-identical output).

Validation: the source must exist, be a PNG (first 8 bytes), and be at
most 1 MiB, matching the competition gate; anything else fails loudly
instead of shipping a bad entry.
"""
import os
import shutil
import sys

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    if not os.path.isfile(SRC):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    with open(SRC, "rb") as fh:
        head = fh.read(8)
    if head != PNG_MAGIC:
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print("entry.png is %d bytes, over the 1 MiB limit" % size,
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
