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
# groovy dependencies on an Ubuntu 16.04 or
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

# Update the repository lists
sudo apt update

if ! exit_ok ; then
	echo "Couldn't update software repositories. Bailing out."
	exit
fi

# Install all the necessary packages. Note
# that apt will simply skip over packages
# that are already installed, so there is
# no need to edit things out unless you
# don't want something installed.
sudo apt -y install gradle \
		    groovy 

if ! exit_ok ; then
	echo "The installation failed. Bailing out."
	exit
fi

# Now we need to make sure that a decent version of pandoc is installed and
# tell the user how to upgrade if the installed version is out of date.
#
PD=$(which pandoc)
VERS=""
if [[ "$PD" != "" ]] ; then
	VERS=$($PD --version | grep "^pandoc " | awk '{print $2}' | awk -F\. '{print $1 " " $2}' | sed 's/\.//g')
fi

read -r MAJ MIN <<< "$VERS"

if [[ "$VERS" == "" ]] ; then
	echo
	echo "Please download and install pandoc. Then run this script again."
	echo "https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb"
	exit
elif ((MAJ == 2)) || (((MAJ == 1)) && ((MIN < 18))); then
	echo
	echo
	echo "The version of pandoc currently installed (${MAJ}.${MIN}) needs to be updated or downgraded to version > 1.19"
	echo "in order to run MkTechDocs. Please do the following:"
	echo
	echo "    sudo apt remove --purge pandoc"
	echo "    wget https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb"
	echo "    sudo apt install ./pandoc-1.19.2.1-1-amd64.deb" 
	echo
	echo "Then, run this script again. You can also visit the github pandoc page and install"
	echo "any other version that is appropriate, so long as the version is at least 1.18."
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
