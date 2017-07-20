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
import com.github.dfrommi.pandoc.types.*
import java.util.regex.Pattern
import java.util.regex.Matcher

//
// This filter ignores all text between 2 specially-formated
// comment indicators. This filter is probably better for
// large-scale comments, like for commenting-out entire sections
//
// E.g.
//
// <!-- /* -->
//
// This text will be ignored.
//
// <!-- */ -->
//

def inComment = false
def Pattern beginCommentPattern = Pattern.compile("<!--[\\s]*\\/\\*[\\s]*-->")
def Pattern endCommentPattern = Pattern.compile("<!--[\\s]*\\*\\/[\\s]*-->")

Pandoc.toJSONFilter() {
	
	if (it in RawBlock) {
		def rb = it as RawBlock
		
		if (inComment) {
			def Matcher m = endCommentPattern.matcher(rb.content)
			if (m.find()) {
				inComment = false
			}

			return []
		}
		else {
			def Matcher m = beginCommentPattern.matcher(rb.content)
			if (m.find()) {
				inComment = true
				return []
			}
		}
	}
	
	if (inComment) {
		return []
	}
	
	it
}
