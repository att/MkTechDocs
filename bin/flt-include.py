#!/usr/bin/env python3

# Copyright (c) 2017 AT&T Intellectual Property. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

##
# This filter allows you to include other markdown in
# your markdown. E.g.
# 
#         ```include
#         includethisfile.md
#         ```
# This filter is recursive, so your markdown can include
# other markdown to any level.
#
# Header levels are automatically adjusted to the correct
# heading level if you use the "heading-level" attribute:
#
#     # Heading One
# 
#     Some text
#
#     ## Heading Two
#
#     ```{.include heading-level=2}
#     somefiletoinclude.md
#     ````
# "heading-level" represents the heading level where the
# include happens. On subsequent inclusion, the heading levels
# in the included file will be increased by two. Of course, you
# can always leave out the heading-level if you don't want
# to alter the heading level of the included file.
#
# Even multiple levels of include recursion will result in
# headers of the correct level. The reason this works is by
# virtue of that depth-first recursion.
#
# The lowest level pages (i.e. the last file included in a
# recursive string of includes), are processed and stored
# to disk first.
#
# When the next outer level is processed, those headers are
# adjusted and the previously adjusted levels in the included file
# are in effect adjusted again. Then, the next level is adjusted,
# and so are all the inclusions.
#
# This results in the innermost include's headers being
# adjusted upwards by however many levels of recursion
# there are.
#

import os
import sys
import json
from subprocess import Popen, PIPE
from pandocfilters import toJSONFilter, walk, get_value

def str_to_json(s):
    p = Popen(["pandoc", "-f", "markdown", "-t", "json"], stdin=PIPE, stdout=PIPE)
    p.stdin.write(s.encode())
    (stdout, stderr) = p.communicate()
    if str(stderr) != "None":
        sys.stderr.write("WARNING: Conversion to json had results in stderr: " + str(stderr))

    return stdout.decode()

def get_contents_of_file(f, levels=u"0"):
    numLevels = int(levels)

    # Return the contents of file unchanged if no change in level is needed
    if numLevels == 0:
        if os.path.isfile(f):
            with open(f, "r") as myFile:
                return myFile.read()
        else:
            sys.stderr.write("WARNING: cannot read " + f)
            return "FILE NOT FOUND: " + f

    # Alter the level
    alterLevelBy = abs(numLevels)
    pre = "in" if numLevels > 0 else "de"

    if alterLevelBy > 5:
        sys.stderr.write("WARNING: Header change out of bounds. Will stick at a maximum of 6 or minimum of 0\n")
        alterLevelBy = 5

    p = Popen(["pandoc", "-f", "markdown", "-t", "markdown", "-F", "flt-" + pre + "crement-header-" + str(alterLevelBy) + ".py", f], stdout=PIPE)
    (stdout, stderr) = p.communicate()
    stdout = stdout.decode()
    if stderr is not None:
        stderr = stderr.decode()
        if stderr != "None":
            sys.stderr.write("WARNING: Conversion to json had results in stderr: " + stderr)

    return stdout

def include(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "include" in classes:
            rv = []

            for l in code.splitlines():
                l = l.strip()
                if os.path.isfile(l):
                    (headingLevel, dummy) = get_value(keyvals, "heading-level")
                    if not headingLevel:
                        headingLevel = 0

                    contents = get_contents_of_file(l, headingLevel)

                    doc = json.loads(str_to_json(contents))

                    if 'meta' in doc:
                        meta = doc['meta']
                    elif doc[0]:  # old API
                        meta = doc[0]['unMeta']
                    else:
                        meta = {}

                    altered = walk(doc, include, format, meta)

                    rv.append(altered['blocks'])
                else:
                    sys.stderr.write("WARNING: Can't read file '" + l + "'. Skipping.\n")

            # Return a flattened list using nested list comprehension
            #
            # The following is equivalent to:
            #
            # flattened = []
            # for sublist in rv:
            #    for item in sublist:
            #        flattened.append(item)
            # return flattened

            return [item for sublist in rv for item in sublist]

if __name__ == "__main__":
    toJSONFilter(include)
