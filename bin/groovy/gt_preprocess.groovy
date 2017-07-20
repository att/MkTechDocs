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

import groovy.text.SimpleTemplateEngine

/**
 * This script passes a groovy template through the
 * StreamingTemplateEngine whether presented as input
 * on stdin or as a file
 */
def engine = new groovy.text.SimpleTemplateEngine()
def tmplt

if (args.length == 1) {
	tmplt = engine.createTemplate(new File(args[0])).make()
	//System.err << "Processing Groovy template ${args[0]}\n"
}
else {
	tmplt = engine.createTemplate(new BufferedReader(new InputStreamReader(System.in))).make()
	//System.err << "Processing Groovy template on STDIN\n"
}


println tmplt.toString()

