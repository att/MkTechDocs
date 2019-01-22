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
# This script will install all MkTechDocs dependencies in a Fedora
# 26+ environment. It is not currently suited for using in a
# docker container or vagrantfile, although it would be easy enough
# to adapt it for such use.
#
# --------------------- -------------------------------------------------
# Example usage         `install_deps_fedora_py.sh`
#
# Arguments             None
#
# Special exit values   None
# --------------------- -------------------------------------------------
#

# #####################################
# The following commands will install
# all of the necessary MkTechDocs
# dependencies on a Fedora 26 or
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
sudo dnf install -y git \
                    make \
                    python3-pip \
                    graphviz \
                    plantuml \
                    pandoc \
                    texlive-xetex

if ! exit_ok ; then
    echo "The installation failed. Bailing out."
    exit
fi

# Install pandocfilters

sudo pip install pandocfilters

if ! exit_ok ; then
    echo "Installation of pandocfilters failed. Bailing out."
    exit
fi

# Install Jinja2 for python templates

sudo pip install Jinja2

if ! exit_ok ; then
    echo "Installation of Jinja2 failed. Bailing out."
    exit
fi

echo "Finished without error."
echo
echo "You might also want to install groovy (2+) and gradle (3+) to support Groovy templates."
echo 
