#!/usr/bin/env groovy

/*
 Copyright (c) 2017 AT&T Intellectual Property. All rights reserved.
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/

import com.github.dfrommi.pandoc.Pandoc
import com.github.dfrommi.pandoc.convert.PandocConverter
import com.github.dfrommi.pandoc.convert.JsonToPandocTypeConverter
import com.github.dfrommi.pandoc.types.*

//
// This filter throughputs a document and outputs to stderr the 
// file names of the files that are included within. The purpose
// is to safely discover included files for building dependency
// lists in Makefiles.
//

Pandoc.toJSONFilter() { 
	if (it in CodeBlock) {	
		def cb = it
		if ("include" in cb.attr.classes) {
			cb.code.eachLine { l ->
				l = l.trim()	
				if (l[0] != '&') {
					System.err << l << " "
				}
			}	
		}
	}

	it
}
