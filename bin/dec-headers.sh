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
# A utility script that decrements the headers in a given
# markdown file by a given number of levels.
#
# A copy of the original file is kept using the origial
# file name and a PID as the extension.
#
# --------------------- -------------------------------------------------
# Example usage         `dec-headers.sh file.md 1`
#
# Arguments             1 A file to alter.<br />
#                       2 The number of heading levels to decrement.
#
# Special exit values   None
# --------------------- -------------------------------------------------
#

if [[ "$1" == "" ]] ; then
	echo "usage: dec_headers.sh <markdown file> [n]"
	echo "    Decrements headers in a given markdown file by n levels."
	echo "    If no 'n' is supplied, 1 is used."
	echo "    Saves a copy of the modified file in <filename>.PID"
fi

FILE=$1

N=$2
if [[ "$N" == "" ]] ; then
	N=1
fi

pandoc -f markdown -t markdown --wrap=none --filter flt-decrement-header-${N}.py $FILE > $$.md
cp $FILE $FILE.$$
mv $$.md $FILE
