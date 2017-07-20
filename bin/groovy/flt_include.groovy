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
import com.att.mktechdocs.MarkdownUtils

// This filter allows you to include other markdown files in
// your markdown. It supports an arbitrary level of inclusions, which means
// your includes can include markdown.
// The replaced text is interpreted as markdown.
// If the filename has 'gt' extension, the content is processed as Groovy template.

def converter = Pandoc.factory.converter

toJSONFilter(CodeBlock) { CodeBlock cb, meta ->
  def result = [cb]

  while (result.any {isIncludeBlock(it)}) {
    result = result.collectMany { isIncludeBlock(it) ? converter.mdToDocument(includeFiles(it.code, it.attr.properties['heading-level']))['blocks'] : [it] }
  }

  result
}

boolean isIncludeBlock(element) {
  element in CodeBlock && "include" in element.attr.classes
}

String includeFiles(lines, headingLevel) {
  lines.readLines().
    collect{ it.trim() }.findAll { it && !it.startsWith('#') }. // ignore empty and commented lines
    collect{ includeFile(it, headingLevel) }.
    join("\n")
}

String includeFile(filename, headingLevel) {
	def f = new File(filename)
	def content = f.text

	// ???TBD???:
	//
	// In the future, may want to enable putting .gt templates into
	// include blocks. We don't now because it isn't necessary? .gt
	// templates are converted to markdown in the preprocessing
	// step, so you "include" them like this:
	//
	// 1. Create foo.gt
	// 2. Add to include blocks in other files as foo.md
	//
	// The makefile will generate the correct dependencies in this
	// case. Like, if you add include blocks programatically, you'll
	// wind up with a .md file that the makefile will generate
	// dependencies for. I think.
	//
	// Agreed that it's confusing to have foo.gt file and then
	// include it as foo.md.
	//
	/*if (filename.endsWith('.gt')) {
		return new SimpleTemplateEngine().createTemplate(content).make()
	}*/
  
	// If we see a heading-level, we'll need to increase the
  // the headings in the included file by the amount
  // indicated by the heading-level
  if (headingLevel != null) {
  	def baseHeadingLevel = headingLevel as int
  	def altMarkdown = MarkdownUtils.getMarkdownFileAndChangeHeader(f, baseHeadingLevel)
  	content = MarkdownUtils.getMarkdownFileAndChangeHeader(f, baseHeadingLevel) + "\n"  
  }

	content
}
