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
# This filter turns links like this:
#
#     [foo link](somepage.html#some-heading)
#
# into:
#
#     [foo link](#some-heading)
#
# This is necessary to transform documents from multi-page
# to single page
#

import os
import sys
import re

from pandocfilters import toJSONFilter, Link

def my_filter(key, value, format, _):
    if key == 'Link':
        #[u'', [], []] | [{u'c': u'link', u't': u'Str'}] | [u'index.html#some-header', u'Alt-Title']
        [attr, inline, [target, title]] = value

        if not re.search("://", target):
            m = re.search("(#.*$)", target)
            if m:
                target = m.group(0)

        return Link(attr, inline, [target, title])

if __name__ == "__main__":
    toJSONFilter(my_filter)
