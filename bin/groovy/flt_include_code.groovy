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
import groovy.text.SimpleTemplateEngine
import static com.github.dfrommi.pandoc.Pandoc.*
import java.lang.Math as JavaMath

// This filter allows you to include source-code files in
// your markdown.
// 
// You can provide one file per line. If you include the
// "language" property:
//
//  ```{.include-code language="java"}
//  myfile.java
//  myfile.sh
//  ```
// The filter will use whatever language you specify in
// the property regardless of what the file extensions are,
// which you may or may not want.
//
// If you provide something like the following:
//
// ```include
// myfile.java
// myfile.bash
// myfile.c
// ```
// The filter will produce 3 code blocks with the
// language property set based on the extension of
// the files within.
//

def converter = Pandoc.factory.converter

toJSONFilter(CodeBlock) { CodeBlock cb, meta ->
  def result = [cb]

  if (isIncludeBlock(cb)) {
    result = includeFiles(cb.code, cb.attr.properties['language'])
  }

  result
}

boolean isIncludeBlock(element) {
  element in CodeBlock && "include-code" in element.attr.classes
}

String getExtension(filename) {
	def char ch
	def int len
	
	if(filename==null || (len = filename.length())==0 || (ch = filename.charAt(len-1))=='/' || ch=='\\' || ch=='.' ) {
		return ""
	}

	def int dotInd = filename.lastIndexOf('.')
	def int	sepInd = JavaMath.max(filename.lastIndexOf('/'), filename.lastIndexOf('\\'))
	
	if (dotInd<=sepInd) {
		return ""
	}
	
	filename.substring(dotInd+1).toLowerCase()
}

CodeBlock[] includeFiles(filenames, language) {
	filenames.readLines().collect { f ->
		def code = new File(f.trim()).text

		// If the user specifies a language, we'll use that.
		// Otherwise, we'll strip off the file extension and try that.
		def type = language
		if (language == null) {
			def ext = getExtension(f.trim())
			type = (ext == "" ? "plaintext" : ext)
		}

		new CodeBlock(code: code, attr: new Attributes(classes: [type], identifier: "", properties: []))
	}.collect {it}
}

