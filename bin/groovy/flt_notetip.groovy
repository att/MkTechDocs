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

//
// This filter replaces 'note' and 'tip' blocks with
// div tags of either a note or tip class
//
// E.g.
//    ```tip
//    My tip
//    ```
// 
// Becomes:
//
// <div class='tip'>**Tip**: My tip</div>
//


Pandoc.toJSONFilter(CodeBlock) { CodeBlock cb ->
	if ("tip" in cb.attr.classes) {
		new RawBlock(format: "html", content:"<p class=\"tip\"><b>Tip</b>: ${cb.code}</p>\n")
	}
	else if ("note" in cb.attr.classes) {
		new RawBlock(format: "html", content:"<p class=\"note\"><b>Note</b>: ${cb.code}</p>\n")
	}
}
