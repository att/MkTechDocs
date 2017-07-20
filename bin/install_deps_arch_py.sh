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
# This script will install all MkTechDocs dependencies in an Arch
# environment. It is not currently suited for using in a
# docker container or vagrantfile, although it would be easy enough
# to adapt it for such use.
#
# --------------------- -------------------------------------------------
# Example usage         `install_deps_arch_py.sh`
#
# Arguments             None
#
# Special exit values   None
# --------------------- -------------------------------------------------
#

# #####################################
# The following commands will install
# all of the necessary MkTechDocs
# dependencies on an Arch system.
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
sudo pacman -S git \
							 pandoc \
               make \
							 python-pip2 \
						   graphviz \
						   texlive-most \
							 groovy \
							 gradle

if ! exit_ok ; then
	echo "The installation failed. Bailing out."
	exit
fi

# PlantUML
PUML=`sudo pacman -Q | grep plantuml`
if [[ "$PUML" == "" ]] ; then
	git clone https://aur.archlinux.org/plantuml
	if ! exit_ok ; then
		echo "Couldn't get plantuml from AUR."
		exit
	fi
	
	cd plantuml
	
	makepkg -sri

	if ! exit_ok ; then
		echo "Couldn't install plantuml from AUR"
		exit
	fi
fi

# Install pandocfilters

sudo pip2 install pandocfilters

if ! exit_ok ; then
	echo "Installation of pandocfilters failed. Bailing out."
	exit
fi

# Install Jinja2 for python templates

sudo pip2 install Jinja2

if ! exit_ok ; then
	echo "Installation of Jinja2 failed. Bailing out."
	exit
fi

echo "Finished without error."
echo
echo "NOTE 1: You might need to change #!/usr/bin/env python to #!/usr/bin/env python2 for the bin/flt-*py filters to work correctly depending on whether python3 is the default, which is common on newer arch installations."
echo
echo "NOTE 2: You might want to install groovy (2+) and gradle (3+) if you want to use Groovy templates."

