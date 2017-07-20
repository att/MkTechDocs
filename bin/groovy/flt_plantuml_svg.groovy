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

import java.security.MessageDigest

//
// This filter allows you to include plantuml in your markdown.
//
// E.g.
//    ```plantuml
//    actor foo1
//    actor foo2
//
//    foo1 -> foo2
//    ```
//
// To use this filter, make sure "plantuml" is in your PATH
//

def md5(text) {
	def messageDigest = MessageDigest.getInstance("MD5")
	messageDigest.update( text.getBytes() );
	new BigInteger(1, messageDigest.digest()).toString(16).padLeft(32, '0')
}

Pandoc.toJSONFilter(CodeBlock) { CodeBlock cb ->
	if ("plantuml" in cb.attr.classes) {
		def plantUMLType = "svg"

		def title = "Diagram"
		if (cb.attr.properties["title"]) {
			title = cb.attr.properties["title"]
		}

		System.err << "Generating '${plantUMLType}' plantuml diagram named '${title}'\n"
		def plantuml = "plantuml -pipe -t${plantUMLType}".execute()
		
		plantuml.withWriter { w ->
			w << cb.code
		}

		// Capture the results from the pipe
		def res = plantuml.text
		def url = "./" + md5(res) + ".plantuml.${plantUMLType}"

		def f = new File(url)
		f.text = res
    
		// Now we create a paragraph containing an image and return it
		//new Para(new Image(altText: "fig: ${title}", attr: new Attributes(classes: [], identifier: "myid", properties: []), title: new Str(title), url: url))
		new Para(new Image(altText: "", attr: new Attributes(classes: [], identifier: "myid", properties: []), title: new Str(title), url: url))
	}
}
