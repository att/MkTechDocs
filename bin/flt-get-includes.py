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
# Outputs all files referenced in any include blocks in
# a file to stderr. Used internally by MkTechDocs to
# build dependency lists.
# 

import os
import sys

from pandocfilters import toJSONFilter

def get_includes(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "include" in classes:
            for line in code.splitlines():
                sys.stderr.write(line + "\n")

if __name__ == "__main__":
    toJSONFilter(get_includes)
