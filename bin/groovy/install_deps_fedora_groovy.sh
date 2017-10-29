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

# #####################################
# The following commands will install
# all of the necessary MkTechDocs
# groovy dependencies on a Fedora 26 or
# greater system. Please edit to suit
# your needs and system.
#

# #####################################
# Functions
function exit_ok {
	[[ "$?" == "0" ]]
}

# #####################################
# INSTALL

if [[ "$MKTECHDOCSHOME" == "" ]] ; then
	echo "Please add the MkTechDocs installation directory to your environment and try again."
	echo "E.g."
	echo "        export MKTECHDOCSHOME=~/MkTechDocs"
	exit
fi

# Install all the necessary packages. Note
# that apt will simply skip over packages
# that are already installed, so there is
# no need to edit things out unless you
# don't want something installed.
sudo dnf -y install gradle \
		                groovy 

if ! exit_ok ; then
	echo "The installation failed. Bailing out."
	exit
fi

# Now install the groovy-pandoc library
(cd $MKTECHDOCSHOME/lib

git clone https://github.com/jsseidel/groovy-pandoc

if ! exit_ok ; then
	echo "Couldn't clone the groovy-pandoc repository. Bailing out."
	exit
fi
)

(cd $MKTECHDOCSHOME/lib/groovy-pandoc

gradle build

if ! exit_ok ; then
	echo "The gradle build failed. Bailing out."
	exit
fi)

cp $MKTECHDOCSHOME/lib/groovy-pandoc/build/libs/GroovyPandoc-0.*.jar $MKTECHDOCSHOME/lib/.

if ! exit_ok ; then
	echo "Couldn't copy GroovyPandoc*jar. Is MKTECHDOCSHOME set correctly? Bailing out."
	exit
fi

echo "Finished without error."
echo "You might want to remove the $MKTECHDOCSHOME/lib/groovy-pandoc directory."
