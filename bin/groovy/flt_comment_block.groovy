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
// This filter allows you to create comment blocks that are
// ignored:
//
// ```comment
// Some text here
// ```
//

Pandoc.toJSONFilter(CodeBlock) { CodeBlock cb ->
	if ("comment" in cb.attr.classes) {
		return []
	}
	
	return cb
}
