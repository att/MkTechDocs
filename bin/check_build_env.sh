#!/bin/bash

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
# This script does a simplistic check on your build environment
# to make sure that a MkTechDocs project can build.
#
# --------------------- -------------------------------------------------
# Example usage         `check_build_env.sh`
#
# Arguments             None
#
# Special exit values   1 Problem with build environment<br />
#                       0 No problems with build environment
# --------------------- -------------------------------------------------
#

if [[ "$MKTECHDOCSHOME" == "" ]] ; then
	echo "Please point MKTECHDOCSHOME to your MkTechDocs installation directory and try again."
	echo "E.g."
	echo "        export MKTECHDOCSHOME=~/MkTechDocs"
	exit
fi

# Java 8

if [[ $(java -version 2>&1 | grep 1.8) == "" ]] ; then
	echo "Can't find Java 8 (1.8)."
	exit 1
fi

# Executables

#for exe in pandoc pd groovyc cg gtp flt_get_includes.groovy plantuml xelatex ; do
for exe in foo pandoc flt-get-includes.py plantuml xelatex ; do
	if [[ $(which $exe) == "" ]] ; then
		cat <<EOF
Can't find $exe. Did you add $MKTECHDOCSHOME/bin to your PATH? Did you install all the
dependencies?
EOF
		exit 1
	fi
done

# Libs

#for lib in GroovyPandoc-*jar ; do
#	if ! ls $MKTECHDOCSHOME/lib/$lib 1>/dev/null 2>&1 ; then
#		echo "ls $MKTECHDOCSHOME/lib/$lib 1>/dev/null 2>&1"
#		cat <<EOF
#Can't find $lib. Please install all the dependencies as outlined in the doc directory.
#EOF
#		exit 1
#	fi
#done

echo "Build environment looks good."
