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

import os
import sys
import struct
from optparse import OptionParser

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

(options, args) = parser.parse_args()

if not options.vfs:
    print "error: vfs file not given"
    exit(1)

def process_files(fin, dir_count, file_count):
    # process files
    for i in range(root_file_count):
        len = struct.unpack("B", fin.read(1))[0]
        dir_entry = fin.read(len) # filename
        
        unknown1 = struct.unpack("I", fin.read(4))[0]
        unknown2 = struct.unpack("I", fin.read(4))[0]
        unknown3 = struct.unpack("I", fin.read(4))[0]
        unknown4 = struct.unpack("I", fin.read(4))[0]
        unknown5 = struct.unpack("I", fin.read(4))[0]
        unknown6 = struct.unpack("I", fin.read(4))[0]

        print "File: %-55s - %6d %8d %8d - %2d %10d %10d" % (dir_entry,
                                                  unknown1, unknown2, unknown2,
                                                  unknown4, unknown5, unknown6)
        
    # process dirs
    for j in range(root_dir_count):
        len = struct.unpack("B", fin.read(1))[0]
        file_entry = fin.read(len)
        
        print "Dir:", file_entry
        
        dir_count  = struct.unpack("I", fin.read(4))[0]
        file_count = struct.unpack("I", fin.read(4))[0]
        print file_count, dir_count

        for i in range(file_count):
            len = struct.unpack("B", fin.read(1))[0]
            print len, "'%s'" % fin.read(len) # filename
            fin.read(24)   

with open(options.vfs, "rb") as fin:
    print fin.read(4)
    root_dir_count  = struct.unpack("I", fin.read(4))[0]
    root_file_count = struct.unpack("I", fin.read(4))[0]

    process_files(fin, root_dir_count, root_file_count)

# EOF #
