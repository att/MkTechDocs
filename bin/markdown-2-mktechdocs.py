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


 This standalone script imports a single markdown file, breaks it up into
 smaller markdown files by heading level, and then creates a MkTechDocs project
 from it.

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

MKTECHDOCS_CONF = """TITLE=doc
OUTPUT_FILE_NAME_BASE=doc
FORMAT=cssframes
HTML_STYLE=archwiki
# Commented out so mktechdocs will not produce a TOC
TABLE_OF_CONTENTS_MAIN_DEPTH=6
TABLE_OF_CONTENTS_SUB_DEPTH=3
SECTION_NUMBERS=true
IMAGES=./img
#BUILD_SCRIPT=postbuild.sh
#CUSTOM_CSS=my.css
#CUSTOM_TEMPLATE=mytemplate.html
KEEP_TEMP_FILES=false
#UML_OUTPUT_FORMAT=png
"""

def usage():
    """Usage output"""
    print("%s <--file=F> [--heading-level=N] [--output-dir=D]" %
          os.path.basename(__file__))
    print("  -f, --file: input markdown file")
    print("  -h, --heading-level: Heading level to split files. Default: '1'.")
    print("  -o, --output-dir: The output directory. Default: '.'.")

def is_desired_header(hline_1, hline_2, desired_level):
    """
    Analyzes line1 and line2 and desired_level (an integer) to determine if the
    two lines represent an interesting level (i.e. match desired_level).

    If true, returns the heading title as a string. If false, returns an empty
    string.
    """
    # If hline_1 starts with a '#' character, we try to extract a title from
    # it.
    match_obj = re.search("^#{%s}[\\s]+(.*)" % desired_level, hline_1.rstrip())
    if match_obj:
        return match_obj.group(1)

    # If desired level is 1 or 2, we need to do a lookahead since these can be:
    #
    #   heading 1
    #   =========
    #
    #      or
    #
    #   heading 2
    #   =========
    #

    level_indicator = "="
    if int(desired_level) == 2:
        level_indicator = "-"

    match_obj = re.search("^[%s]+$" % level_indicator, hline_2.rstrip())
    if match_obj:
        return hline_1.rstrip()

    return ""

def is_line_all_header_1_or_2(line):
    """Returns True if the given line is all '=' or all '-'."""
    match_obj = re.search("^[=]+$", line.rstrip())
    if match_obj:
        return True

    match_obj = re.search("^[\\-]+$", line.rstrip())
    if match_obj:
        return True

    return False

def heading_to_filename(heading):
    """This function replaces whitespace, ., `, and () with hyphens. It then
    lowercases the heading string and adds a markdown extension (.md)
    """
    filename = heading.lower()

    # Replace bad chars
    filename = re.sub("[\\s`\\.\\(\\)]+", "-", filename)

    # Remove leading hyphens
    filename = re.sub("^[\\-]", "", filename)

    return "%s.md" % filename

def slurp_file(file_path):
    """Reads the given file into an array and returns it"""
    return_array = []
    my_file = open(file_path, "r")
    if my_file:
        return_array = my_file.readlines()
    return return_array

def write_buffer_to_file(buffer, path):
    """Writes the given string to the file at path."""
    my_file = open(path, "w")
    if my_file:
        num_chars = my_file.write(buffer)
        if num_chars == 0:
            sys.stderr.write("WARNING: wrote 0 characters\n" % num_chars)
    else:
        sys.stderr.write("WARNING: Couldn't open %s for writing\n" % path)

def do_import(markdown_file, heading_level, output_dir):
    """Imports the given markdown_file using the heading_level as the basis
    for where to split the file and puts output files in the given output_dir.
    """
    # Read the given markdown file into an array. This is the easiest way to do
    # a 1 line lookahead.
    file_lines = slurp_file(markdown_file)

    # Open our master file to keep track of includes
    master_file = open("%s/master.md" % output_dir, "w")

    master_file.write("```include\n")

    # Set up our line indices and initial values
    max_idx = len(file_lines)
    idx = 0
    file_buffer = ""
    heading = ""
    while idx < max_idx:
        # Grab 2 lines at a time
        line_1 = file_lines[idx]
        line_2 = "EOF"
        if (idx + 1) < max_idx:
            line_2 = file_lines[idx + 1]

        title = is_desired_header(line_1, line_2, heading_level)

        # If we get a valid title or we have reached the last line, we might
        # have a stored heading to sort out
        if title != "" or line_2 == "EOF":
            # If we have a stored heading, we need to blast the collected lines
            # underneath in a new file.
            if heading != "":
                # If the second line is EOF, we need to add the last line to
                # the file buffer.
                if line_2 == "EOF":
                    file_buffer = "%s%s" % (file_buffer, line_1)

                file_to_create = heading_to_filename(heading)
                print("Creating file: %s/%s" % (output_dir, file_to_create))

                # Add the heading to the file buffer
                if heading_level in (1, 2):
                    # Create the right number of underline characters
                    underline = ""
                    if heading_level == 1:
                        underline = "=" * len(heading)
                    elif heading_level == 2:
                        underline = "-" * len(heading)

                    file_buffer = "%s\n%s\n%s" % (heading,
                                                  underline, file_buffer)
                else:
                    file_buffer = "%s\n%s" % (heading, file_buffer)

                # Blast the new file
                write_buffer_to_file(file_buffer,
                                     "%s/%s" % (output_dir, file_to_create))

                # Clear the file buffer
                file_buffer = ""

                # Record in master file
                master_file.write("%s\n" % file_to_create)

            # Save the heading we found for the next time
            heading = title

            # If line_2 is all '=' or '-', we can eat it
            if is_line_all_header_1_or_2(line_2):
                idx = idx + 1
        else:
            # We didn't find a heading, so save the line
            file_buffer = "%s%s\n" % (file_buffer, line_1.rstrip())

        # Advance the index
        idx = idx + 1

    # Close our master file include block
    master_file.write("```\n")

    # Create a new mktechdocs.conf file
    conf_file = open("%s/mktechdocs.conf" % output_dir, "w")
    conf_file.write(MKTECHDOCS_CONF)

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

    # Sanity checks
    if ARG_FILE == "":
        usage()
        sys.exit(1)

    if not os.path.isfile(ARG_FILE):
        sys.stderr.write("%s doesn't exist. Giving up.\n" % ARG_FILE)
        sys.exit(1)

    if not os.path.isdir(ARG_DIR):
        sys.stderr.write("%s doesn't exist. Giving up.\n" % ARG_DIR)
        sys.exit(1)

    do_import(ARG_FILE, int(ARG_LEVEL), ARG_DIR)
