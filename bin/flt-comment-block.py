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

from pandocfilters import toJSONFilter
import re

##
# Adapted from https://github.com/jgm/pandocfilters/blob/master/examples/comments.py
#
# Pandoc filter that causes everything between
# '&lt;!-- BEGIN COMMENT --&gt;' and '&lt;!-- END COMMENT --&gt;'
# to be ignored.  The comment lines must appear on
# lines by themselves, with blank lines surrounding
# them.
#
# E.g.
#
#     <!-- BEGIN COMMENT -->
#
#     This text will be ignored.
#
#     <!-- END COMMENT -->
#

incomment = False

def comment(k, v, fmt, meta):
    global incomment
    if k == 'RawBlock':
        fmt, s = v
        if fmt == "html":
            if re.search("<!-- BEGIN COMMENT -->", s):
                incomment = True
                return []
            elif re.search("<!-- END COMMENT -->", s):
                incomment = False
                return []
    if incomment:
        return []  # suppress anything in a comment

if __name__ == "__main__":
    toJSONFilter(comment)
