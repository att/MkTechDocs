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
# This script will install all MkTechDocs dependencies in a macOS
# environment. It is not currently suited for using in a
# docker container or vagrantfile, although it would be easy enough
# to adapt it for such use.
#
# --------------------- -------------------------------------------------
# Example usage         `install_deps_macos_py.sh`
#
# Arguments             None
#
# Special exit values   None
# --------------------- -------------------------------------------------
#

# #####################################
# The following commands will install
# all of the necessary MkTechDocs
# dependencies for MacOS. Please edit
# to suit your needs and system.
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

GIT=`which git`
if [[ "$GIT" == "" ]] ; then
  echo "Please install Xcode from the Mac App Store and run 'git' from the command line."
  exit
fi

MAKE=`which make`
if [[ "$MAKE" == "" ]] ; then
  echo "Please install Xcode from the Mac App Store and run 'make' from the command line."
  exit
fi

BREW=`which brew`
if [[ "$BREW" == "" ]] ; then
  echo "Please install 'homebrew.' See: http://brew.sh/"
  exit
fi

# Install all the necessary packages. Note
# that brew will simply skip over packages
# that are already installed, so there is
# no need to edit things out unless you
# don't want something installed.
brew install pandoc \
             graphviz \
             plantuml \
             Caskroom/cask/mactex

if ! exit_ok ; then
	echo "The installation failed. Bailing out."
	exit
fi

sudo easy_install pip
if ! exit_ok ; then
	echo "The installation failed. Bailing out."
	exit
fi

# Install pandocfilters and jinja2
sudo pip install pandocfilters
if ! exit_ok ; then
	echo "The installation of pandocfilters failed. Bailing out."
	exit
fi

sudo pip install Jinja2
if ! exit_ok ; then
	echo "The installation of Jinja2 failed. Bailing out."
	exit
fi

echo "Please add the following location to your PATH environment variable:"
echo "/usr/local/texlive/2016/bin/x86_64-darwin/"
echo
echo "E.g."
echo "    export PATH=$PATH:/usr/local/texlive/2016/bin/x86_64-darwin/"
echo
echo "You also might want to install groovy (2+) and gradle (3+) if you"
echo "need Groovy templates."


echo "Finished without error."
