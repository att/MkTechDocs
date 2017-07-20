#!/usr/bin/env python

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
# A starting point for building new filters.
#

import os
import sys

from pandocfilters import toJSONFilter, Para, Str

def my_filter(key, value, format, _):
	if key == 'CodeBlock':
		[[ident, classes, keyvals], code] = value

		if "mytype" in classes:
			return Para([Str("Found mytype!")])

if __name__ == "__main__":
	toJSONFilter(my_filter)
