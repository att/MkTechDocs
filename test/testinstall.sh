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

function exit_ok {
	[[ "$?" == "0" ]]
}

# This simple test can usually track down installation problems

pandoc -F flt-include.py -F flt-plantuml.py -f markdown -t markdown test_install.md

if ! exit_ok ; then
	echo "Something went wrong. Please check the output of the installation script. Also, make sure"
	echo "that $MKTECHDOCSHOME/bin is in your PATH."
	exit
fi

echo "Pandoc seems ok."

echo
echo 
echo "Checking python..."
echo 

printf "import mktechdocslib\n\nprint 'If this prints with no error, you are good to go!'" | python

if ! exit_ok ; then
	echo "Something went wrong. Please check the output of the installation script."
	exit
fi

echo "Python seems ok."
