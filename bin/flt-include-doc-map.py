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
# This filter is identical to the include filter, except
# that while building a document, it outputs a document
# map on stderr so that a script can figure out where each part of
# the document came from. E.g.
#
#         ```include
#         includethisfile.md
#         ```
# This filter is recursive, so you markdown can include
# other markdown to any level.
#
# This filter is used internally by MkTechDocs.
#

import os
import sys
import json
import re
from subprocess import Popen, PIPE
from pandocfilters import toJSONFilter, walk, get_value, Str, Header, Para, Space

REFFILE=""

def md_to_json(s):
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

def docmap(key, value, format, meta):
    global REFFILE

    if key == 'Header':
        [level, attr, inline] = value
        [ids, classes, keyvals] = attr

        # Change the reference file if we see a new level-1 header    
        if level == 1 and 'fromfile' in meta:
            reffile = re.sub("\.md", ".html", meta['fromfile']['c'])
            REFFILE="~~" + reffile + "~~" 
            sys.stderr.write(reffile + "\n")

        return Header(level, [REFFILE + str(ids), [], []], inline)

    elif key == 'CodeBlock':
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

                    doc = json.loads(md_to_json(contents))

                    if 'meta' in doc:
                        meta = doc['meta']
                    elif doc[0]:  # old API
                        meta = doc[0]['unMeta']
                    else:
                        meta = {}

                    # Add a file to the meta info
                    meta['fromfile']= {u'c':l, u't':'MetaString'}

                    altered = walk(doc, docmap, format, meta)

                    rv.append(altered['blocks'])
                else:
                    sys.stderr.write("WARNING: Can't read file '" + l + "'. Skipping.")

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
    toJSONFilter(docmap)
