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
# This filter allows you to include source-code files in
# your markdown.
# 
# You can provide one file per line. If you include the
# "language" property:
# 
#     ```{.include-code language="java"}
#     myfile.java
#     myfile.sh
#     ```
# The filter will use whatever language you specify in
# the property regardless of what the file extensions are,
# which you may or may not want.
# 
# If you provide something like the following:
# 
#     ```include-code
#     myfile.java
#     myfile.bash
#     myfile.c
#     ```
# The filter will produce 3 code blocks with the
# language property automatically set based on the extension
# of the files within.
#

import os
import sys

from pandocfilters import toJSONFilter, CodeBlock, get_value

def include_code(key, value, format, _):
	if key == 'CodeBlock':
		[[ident, classes, keyvals], code] = value

		if "include-code" in classes:
			rv = []
			
			for l in code.splitlines():
				l = l.strip()
				(filename, ext) = os.path.splitext(l)
				ext = ext.replace(".", "")

				# Overide the file extension if we are given
				# a language keyval
				(givenExt, value) = get_value(keyvals, u"language")
				if str(givenExt) != "None":
					ext = str(givenExt)

				if os.path.isfile(l):
					with open(l, "r") as f:
						contents = f.read()
					rv.append(CodeBlock(["", [ext], []], contents))
				else:
					sys.stderr.write("WARNING: Can't read file '" + l + "'. Skipping.")

			return rv

if __name__ == "__main__":
	toJSONFilter(include_code)
