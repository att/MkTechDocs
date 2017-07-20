package com.att.mktechdocs

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

class MarkdownUtils {
	static private def MAXLEVEL=5
	
	static def getMarkdownFileAndChangeHeader(f, incrementHeaderBy=0) {
		if (incrementHeaderBy==0) {
			return f.text
		}

		def changeAmount = incrementHeaderBy.abs()
		def pre = (incrementHeaderBy > 0 ? "in" : "de")
		def sout = new StringBuilder()
		def serr = new StringBuilder()
		
		if (changeAmount > MAXLEVEL) {
			System.err << "WARNING: maximum header level of $MAXLEVEL exceeded: $changeAmount. Using $MAXLEVEL instead.\n"
			changeAmount = MAXLEVEL
		}
		
		def proc = "pd -f markdown -t markdown --filter flt_${pre}crement_header_${changeAmount}.groovy ${f.toString()}".execute()
		proc.consumeProcessOutput(sout, serr)
		proc.waitForOrKill(60000) // 60 seconds
		//proc.waitForProcessOutput(sout, serr)

		if (sout.toString() == "") {
			System.err << "WARNING: pandoc produced no output\n"
		}

		if (serr.toString() != "") {
			System.err << "WARNING: pandoc produced stderr: $serr"
		}

		return sout.toString()
	}
}
