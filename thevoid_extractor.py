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


from typing import Sequence

import fnmatch
import os
import sys
import struct
import argparse


def process_dir(fin, parent, dir_count, file_count, lst):
    # process files
    for i in range(file_count):
        len = struct.unpack("B", fin.read(1))[0]
        dir_entry = fin.read(len)  # filename

        size = struct.unpack("I", fin.read(4))[0]
        unknown3 = struct.unpack("I", fin.read(4))[0]
        offset = struct.unpack("I", fin.read(4))[0]
        zero = struct.unpack("I", fin.read(4))[0]
        unknown1 = struct.unpack("I", fin.read(4))[0]
        unknown2 = struct.unpack("I", fin.read(4))[0]

        dir_entry = os.path.join(parent, dir_entry)

        lst.append((dir_entry, offset, size))

        if False:
            print("%-55s - %6d %8d - %2d %10d %10d %10d" %
                  (dir_entry,
                   size, offset,
                   zero, unknown1, unknown2, unknown3))

    # process dirs
    for j in range(dir_count):
        len = struct.unpack("B", fin.read(1))[0]
        file_entry = fin.read(len)

        next_dir_count = struct.unpack("I", fin.read(4))[0]
        next_file_count = struct.unpack("I", fin.read(4))[0]

        process_dir(fin, os.path.join(parent, file_entry), next_dir_count, next_file_count, lst)


def extract_file(fin, outfile, offset, size, options):
    fin.seek(offset)
    data = fin.read(size)

    if options.stdout:
        sys.stdout.write(data)
    else:
        print("extracting \"%s\"" % outfile)
        outdir = os.path.dirname(outfile)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        with open(outfile, "wb") as fout:
            fout.write(data)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="'The Void' datafile extraction tool")

    parser.add_argument("FILE", nargs='*')
    parser.add_argument("-l", "--list", dest="list_files", action="store_true",
                        help="List all resource files")
    parser.add_argument("-x", "--extract", dest="extract_files", action="store_true",
                        help="Extract resource files")
    parser.add_argument("-t", "--targetdir", dest="targetdir", default=".",
                        help="The directory where files will be extracted", metavar="DIR")
    parser.add_argument("-s", "--stdout", dest="stdout", action="store_true",
                        help="Extract data to stdout")
    parser.add_argument("-g", "--glob", metavar="PATTERN", dest="glob_pattern",
                        help="Extract files by glob pattern")
    parser.add_argument("-v", "--vfs", dest="vfs",
                        help="Prefix of the resource files, can be 'resources' or 'german'")

    return parser.parse_args(argv[1:])


def main() -> None:
    opts = parse_args(sys.argv)

    if not opts.vfs:
        print("error: vfs file not given", file=sys.stderr)
        exit(1)

    with open(opts.vfs, "rb") as fin:
        magic = fin.read(4)
        if magic != b'LP2C':
            raise RuntimeError("not a VFS file, invalid file magic \"{}\"".format(magic.hex()))

        root_dir_count = struct.unpack("I", fin.read(4))[0]
        root_file_count = struct.unpack("I", fin.read(4))[0]

        (parent, ext) = os.path.splitext(os.path.basename(opts.vfs))

        lst = []
        process_dir(fin, parent.encode(), root_dir_count, root_file_count, lst)

        def extract_or_print(fin, filename, offset, size, opts):
            if opts.extract_files:
                extract_file(fin, os.path.join(opts.targetdir, filename), offset, size, opts)
            else:
                print("%10d  %10d  %-55s" % (offset, size, filename))

        if opts.glob_pattern:  # extract pattern
            for (filename, offset, size) in lst:
                if fnmatch.fnmatch(filename.decode(), opts.glob_pattern):
                    extract_or_print(fin, os.path.join(opts.targetdir, filename.decode()), offset, size, opts)

        if opts.FILE:
            for fname in opts.FILE:
                fname_enc = fname.encode()
                for (filename, offset, size) in lst:
                    if fname_enc == filename:
                        extract_or_print(fin, os.path.join(opts.targetdir, filename.decode()), offset, size, opts)
                        break
                else:
                    print("error: failed to extract {}".format(fname), file=sys.stderr)

        if not opts.glob_pattern and not opts.FILE:  # extract all
            for (filename, offset, size) in lst:
                extract_or_print(fin, os.path.join(opts.targetdir, filename.decode()), offset, size, opts)


if __name__ == "__main__":
    main()


# EOF #
