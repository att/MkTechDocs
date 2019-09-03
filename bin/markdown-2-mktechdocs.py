#!/usr/bin/env python3

"""
 Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 This script imports a single markdown file, breaks it up into smaller
 markdown files by heading level, and then creates a MkTechDocs project from
 it.

 Example runs:

   markdown-2-mktechdocs.py --file=foo.md --output-dir=./mydir

   This is the intended use. Every level-1 heading becomes a new file in
   `./mydir` where the heading title is used as the basis for the name of the
   new file.

   The next two examples demonstrate the case where you have a single big
   markdown file that consists of a level-1 heading and all subsequent major
   headings are level-2. Specifying the heading level as an argument should
   hopefully cover all other cases where there are a couple of heading levels
   used for front matter followed by major sections are level-N.

   markdown-2-mktechdocs.py --file=foo.md --heading-level=2 --output-dir=./mydir

   For every heading level of '2' or lower (e.g. 1, in this case), the script
   would create a file in `./mydir` using the heading title as the basis for
   the name of the new file.

   cat foo.md | markdown-2-mktechdocs.py --heading-level=2 --output-dir=./mydir

   Same as the last example, except input is read from stdin.
"""

import getopt
import os
import re
import sys

def usage():
    """ Usage output """
    print("%s <--file=F> [--heading-level=N] [--output-dir=D]" %
          os.path.basename(__file__))
    print("  -f, --file: input markdown file")
    print("  -h, --heading-level: Heading level to split files. Default: '1'.")
    print("  -o, --output-dir: The output directory. Default: '.'.")

def do_import(markdown_file, heading_level, output_dir):
    """ Imports the given markdown_file using the heading_level as the basis
    for where to split the file and puts output files in the given output_dir.
    """
    file_lines = []

    # Read the given markdown file into an array. This is the easiest way to do
    # a 1 line lookahead.
    if not os.path.isfile(markdown_file):
        sys.stderr.write("%s doesn't exist. Giving up.\n" % markdown_file)
        sys.exit(1)

    with open(markdown_file, "r") as my_file:
        file_lines = my_file.readlines()

    max_idx = len(file_lines) - 1
    idx = 0

    while idx < max_idx:
        # Grab 2 lines at a time
        line_1 = file_lines[idx]
        line_2 = "EOF"
        if (idx + 1) < max_idx:
            line_2 = file_lines[idx + 1]

if __name__ == "__main__":
    ARGV = sys.argv[1:]
    GET_OPT_LONG_ARGS = [
        "file=",
        "heading-level=",
        "output-dir="
    ]

    try:
        OPTS, ARGS = getopt.getopt(ARGV, "f:h:o:", GET_OPT_LONG_ARGS)
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    ARG_FILE = ""
    ARG_LEVEL = 1
    ARG_DIR = "."
    for opt, arg in OPTS:
        if opt in ("-h", "-?"):
            usage()
            sys.exit(0)
        elif opt in ("-f", "--file"):
            ARG_FILE = arg
        elif opt in ("-h", "--heading-level"):
            ARG_LEVEL = arg
        elif opt in ("-o", "--output-dir"):
            ARG_DIR = arg

    if ARG_FILE == "":
        usage()
        sys.exit(1)

    do_import(ARG_FILE, ARG_LEVEL, ARG_DIR)
