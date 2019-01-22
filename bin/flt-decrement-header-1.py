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
# Decrements all headers by 1 level
#

import os
import sys

from pandocfilters import toJSONFilter, Header

LEVELS=1

def dec_header(key, value, format, _):
    if key == 'Header':
        [level, attr, inline] = value
        if level > LEVELS:
            level -= LEVELS 
        return Header(level, attr, inline)

if __name__ == "__main__":
    toJSONFilter(dec_header)
