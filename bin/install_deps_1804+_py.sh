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
# This script will install all MkTechDocs dependencies in an Ubuntu
# 16.04 environment. It is not currently suited for using in a
# docker container or vagrantfile, although it would be easy enough
# to adapt it for such use.
#
# --------------------- -------------------------------------------------
# Example usage         `install_deps_1604+_py.sh`
#
# Arguments             None
#
# Special exit values   None
# --------------------- -------------------------------------------------
#

# #####################################
# The following commands will install
# all of the necessary MkTechDocs
# dependencies on an Ubuntu 16.04 or
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
sudo apt install -y git \
                    make \
                    python3-pip \
                    graphviz \
                    plantuml \
                    texlive-xetex

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
    echo "The version of pandoc currently installed (${MAJ}.${MIN}) needs to be updated or downgraded to version 1.19"
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


# Install pandocfilters

sudo pip3 install pandocfilters

if ! exit_ok ; then
    echo "Installation of pandocfilters failed. Bailing out."
    exit
fi

# Install Jinja2 for python templates

sudo pip3 install Jinja2

if ! exit_ok ; then
    echo "Installation of Jinja2 failed. Bailing out."
    exit
fi

echo "Finished without error."
echo
echo "You might also want to install groovy (2+) and gradle (3+) to support Groovy templates."
echo 
echo "Ubuntu 16.04 LTS ships with a buggy TeX package named titlesec, consider updating it if"
echo "you plan to create PDFs with MkTechDocs. See the following:"
echo "    https://att.github.io/MkTechDocs/#a-note-about-titlesec"

