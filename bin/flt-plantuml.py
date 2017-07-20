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
# Adapted from: [https://github.com/jgm/pandocfilters/blob/master/examples/plantuml.py](https://github.com/jgm/pandocfilters/blob/master/examples/plantuml.py)
#
# Turns PlantUML, e.g.:
#
#     ```plantuml
#     actor Foo1
#     boundary Foo2
#     control Foo3
#     entity Foo4
#     database Foo5
#     Foo1 -> Foo2 : To boundary
#     Foo1 -> Foo3 : To control
#     Foo1 -> Foo4 : To entity
#     Foo1 -> Foo5 : To database
#     ````
# 
# Into an image for inclusion in HTML documents.
#
# To affect the output format, provide a metadata variable on the command line:
# 
#     pandoc -M umlformat=[eps,svg] . . .
#
# If no umlformat is indicated, the filter will default to svg.
#
# Needs `plantuml.jar` from http://plantuml.com/.
#

import os
import sys
import md5

from subprocess import call
from pandocfilters import toJSONFilter, Para, Image, Str, get_filename4code, get_value, get_extension

def get_md5(s):
	m = md5.new()
	m.update(s)
	return m.hexdigest()

def get_title(kv):
	title = []
	typef = ""
	value, res = get_value(kv, u"title")
	if value is not None:
		title = [Str(value)]
		typef = "Fig:"
	
	return title, typef, res

def plantuml(key, value, format, meta):
	if key == 'CodeBlock':
		[[ident, classes, keyvals], code] = value

		if "plantuml" in classes:
			title, typef, keyvals = get_title(keyvals)
			
			filename = "plantuml-" + get_md5(code)

			if 'umlformat' in meta:
				filetype = meta['umlformat']['c']
			else:
				filetype = 'svg'

			#if filetype != "eps" and filetype != "svg":
			#	sys.stderr.write("Unsupported plantuml format: " + filetype + ". Defaulting to svg.")
			#	filetype = "svg"

			src = filename + '.uml'
			dest = filename + '.' + filetype
			
			if not os.path.isfile(dest):
				txt = code.encode(sys.getfilesystemencoding())
				if not txt.startswith("@start"):
					txt = "@startuml\n" + txt + "\n@enduml\n"
				
				with open(src, "w") as f:
					f.write(txt)

			call(["plantuml", "-t"+filetype, src])
			sys.stderr.write('Created image ' + dest + '\n')
			
			return Para([Image([ident, [], keyvals], title, [dest, typef])])

if __name__ == "__main__":
	toJSONFilter(plantuml)
