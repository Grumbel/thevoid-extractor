#!/usr/bin/env python
##  Downtown Extractor
##  Copyright (C) 2011 Ingo Ruhnke <grumbel@gmx.de>
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import fnmatch
import os
import sys
import struct
from optparse import OptionParser


def process_dir(fin, parent, dir_count, file_count, lst):
    # process files
    for i in range(file_count):
        len = struct.unpack("B", fin.read(1))[0]
        dir_entry = fin.read(len) # filename

        size = struct.unpack("I", fin.read(4))[0]
        unknown3 = struct.unpack("I", fin.read(4))[0]
        offset = struct.unpack("I", fin.read(4))[0]
        zero = struct.unpack("I", fin.read(4))[0]
        unknown1 = struct.unpack("I", fin.read(4))[0]
        unknown2 = struct.unpack("I", fin.read(4))[0]

        dir_entry = os.path.join(parent, dir_entry)

        lst.append((dir_entry, offset, size))

        #print "%-55s - %6d %8d %8d - %2d %10d %10d" % (dir_entry,
        #                                                     size, dummy, offset,
        #                                                     zero, unknown1, unknown2)

    # process dirs
    for j in range(dir_count):
        len = struct.unpack("B", fin.read(1))[0]
        file_entry = fin.read(len)

        next_dir_count  = struct.unpack("I", fin.read(4))[0]
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


def parse_args():
    parser = OptionParser("Usage: %prog [OPTIONS] [FILES]")

    parser.add_option("-l", "--list",
                      dest="list_files", action="store_true",
                      help="List all resource files")

    parser.add_option("-e", "--extract",
                      dest="extract_files", action="store_true",
                      help="Extract resource files")

    parser.add_option("-t", "--targetdir", dest="targetdir", default=".",
                      help="The directory where files will be extracted", metavar="DIR")

    parser.add_option("-a", "--extract-all", metavar="DIR",
                      dest="extract_all", action="store_true",
                      help="Extract all resource files")
    parser.add_option("-s", "--stdout",
                      dest="stdout", action="store_true",
                      help="Extract data to stdout")
    parser.add_option("-g", "--glob", metavar="PATTERN",
                      dest="glob_pattern",
                      help="Select files by glob pattern")

    parser.add_option("-v", "--vfs",
                      dest="vfs",
                      help="Prefix of the resource files, can be 'resources' or 'german'")

    return parser.parse_args()


def main():
    (options, args) = parse_args()

    if not options.vfs:
        print("error: vfs file not given")
        exit(1)

    with open(options.vfs, "rb") as fin:
        magic = fin.read(4)
        root_dir_count  = struct.unpack("I", fin.read(4))[0]
        root_file_count = struct.unpack("I", fin.read(4))[0]

        (parent, ext) = os.path.splitext(os.path.basename(options.vfs))

        lst = []
        process_dir(fin, parent, root_dir_count, root_file_count, lst)

        if options.extract_files:
            for (filename, offset, size) in lst:
                if options.extract_all or \
                   (options.glob_pattern and fnmatch.fnmatch(filename, options.glob_pattern) ) or \
                   filename in args:
                    extract_file(fin, os.path.join(options.targetdir, filename), offset, size, options)
        else:
            for (filename, offset, size) in lst:
                print("%6d %6d %-55s" % (offset, size, filename))


if __name__ == "__main__":
    main()


# EOF #
