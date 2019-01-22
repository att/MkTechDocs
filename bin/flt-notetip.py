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
# This filter replaces 'note' and 'tip' blocks with
# div tags of either a note or tip class
#
# E.g.
#
#     ```tip
#     My tip
#     ```
#
# Becomes:
#
#     <div class='tip'>**Tip**: My tip</div>
#
# for markdown and html. For other output formats:
#
# TIP: My tip
#

import os
import sys

from pandocfilters import toJSONFilter, RawBlock, Str, Para

def note_tip(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "note" in classes or "tip" in classes:
            blockType = ""    
            if "note" in classes:
                blockType = "note"
            elif "tip" in classes:
                blockType = "tip"

            if format == "html" or format == "markdown":    
                return RawBlock("html", "<p class=\"" + blockType + "\"><b>" + blockType.title() + "</b>: " + code + "</p>\n")
            else:
                return Para([Str(blockType.upper() + ":" + code)])

if __name__ == "__main__":
    toJSONFilter(note_tip)
