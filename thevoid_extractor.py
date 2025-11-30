#!/usr/bin/env python

# The Void Extractor
# Copyright (C) 2011-2022 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Sequence, Tuple, BinaryIO

import argparse
import fnmatch
import os
import struct
import sys
import logging


def process_dir(fin: BinaryIO, parent: bytes, dir_count: int, file_count: int,
                lst: list[Tuple[bytes, int, int]]) -> None:
    # process files
    for _ in range(file_count):
        length = struct.unpack("B", fin.read(1))[0]
        dir_entry = fin.read(length)  # filename

        size = struct.unpack("I", fin.read(4))[0]
        unknown3 = struct.unpack("I", fin.read(4))[0]
        offset = struct.unpack("I", fin.read(4))[0]
        zero = struct.unpack("I", fin.read(4))[0]
        unknown1 = struct.unpack("I", fin.read(4))[0]
        unknown2 = struct.unpack("I", fin.read(4))[0]

        dir_entry = os.path.join(parent, dir_entry)

        lst.append((dir_entry, offset, size))

        logging.debug("%-55s - %6d %8d - %2d %10d %10d %10d" %
                      (dir_entry.decode(),
                       size, offset,
                       zero, unknown1, unknown2, unknown3))

    # process dirs
    for _ in range(dir_count):
        length = struct.unpack("B", fin.read(1))[0]
        file_entry = fin.read(length)

        next_dir_count = struct.unpack("I", fin.read(4))[0]
        next_file_count = struct.unpack("I", fin.read(4))[0]

        process_dir(fin, os.path.join(parent, file_entry), next_dir_count, next_file_count, lst)


def extract_file(fin: BinaryIO, outfile: str, offset: int, size: int, opts: argparse.Namespace) -> None:
    fin.seek(offset)
    data = fin.read(size)

    if opts.stdout:
        sys.stdout.buffer.write(data)
    else:
        print("extracting \"%s\"" % outfile)
        outdir = os.path.dirname(outfile)
        os.makedirs(outdir, exist_ok=True)
        with open(outfile, "wb") as fout:
            fout.write(data)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=argv[0],
        formatter_class=argparse.RawTextHelpFormatter,
        description="'The Void' datafile extraction tool",
        epilog=f"""
examples:
  List the VFS content:
    {argv[0]} --list "The Void/data/Sound.vfs"

  Extract the VFS content:
    {argv[0]} --extract "The Void/data/Sound.vfs" --outputdir extracted/

  Extract only `.ogg` files using a glob:
    {argv[0]} --extract "The Void/data/Sound.vfs" --outputdir extracted/ -g "*.ogg"
""")

    parser.add_argument(
        "VFSFILE",
        help=".vfs file to process (e.g. \".../The Void/data/Sound.vfs\")")
    parser.add_argument(
        "ENTRYTOEXTRACT", nargs='*',
        help="individual entry to extract, extract all by default"
    )

    action_group = parser.add_argument_group('actions').add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "-l", "--list", dest="action_list", action="store_true",
        help="List all resource files")
    action_group.add_argument(
        "-x", "--extract", dest="action_extract", action="store_true",
        help="Extract resource files")

    option_group = parser.add_argument_group('options')
    option_group.add_argument(
        "-o", "--outputdir", dest="outputdir", default=None,
        help="The directory where files will be extracted", metavar="DIR")
    option_group.add_argument(
        "-s", "--stdout", dest="stdout", action="store_true",
        help="Extract data to stdout")
    option_group.add_argument(
        "-g", "--glob", metavar="PATTERN", dest="glob_pattern",
        help="Extract entries by glob pattern")

    opts = parser.parse_args(argv[1:])

    print(f"{opts.action_extract!r} {opts.outputdir!r}")
    if opts.action_extract and not opts.outputdir:
        parser.error("--outputdir required for extraction")

    return opts


def main() -> None:
    opts = parse_args(sys.argv)

    with open(opts.VFSFILE, "rb") as fin:
        magic = fin.read(4)
        if magic != b'LP2C':
            raise RuntimeError("not a VFS file, invalid file magic \"{}\"".format(magic.hex()))

        root_dir_count = struct.unpack("I", fin.read(4))[0]
        root_file_count = struct.unpack("I", fin.read(4))[0]

        (parent, _) = os.path.splitext(os.path.basename(opts.VFSFILE))

        lst: list[Tuple[bytes, int, int]] = []
        process_dir(fin, parent.encode(), root_dir_count, root_file_count, lst)

        def extract_or_print(fin: BinaryIO, filename: str, offset: int, size: int, opts: argparse.Namespace) -> None:
            if opts.action_extract:
                extract_file(fin, os.path.join(opts.outputdir, filename), offset, size, opts)
            else:  # opts.action_list
                print("%10d  %10d  %-55s" % (offset, size, filename))

        if opts.glob_pattern:  # extract pattern
            for (filename, offset, size) in lst:
                if fnmatch.fnmatch(filename.decode(), opts.glob_pattern):
                    extract_or_print(fin, filename.decode(), offset, size, opts)

        elif opts.ENTRYTOEXTRACT:
            for entrytoextract in opts.ENTRYTOEXTRACT:
                for (entry, offset, size) in lst:
                    if entrytoextract.encode() == entry:
                        extract_or_print(fin, entry.decode(), offset, size, opts)
                        break
                else:
                    print("error: failed to extract {}".format(entrytoextract), file=sys.stderr)

        else:  # extract all
            for (filename, offset, size) in lst:
                extract_or_print(fin, filename.decode(), offset, size, opts)


if __name__ == "__main__":
    main()


# EOF #
