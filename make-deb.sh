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

mkdir -p ./install_files/opt/mktechdocs
cp -r ./bin ./test ./lib ./docs ./install_files/opt/mktechdocs/.

git clone https://github.com/jsseidel/groovy-pandoc.git /tmp/groovy-pandoc
(
    cd /tmp/groovy-pandoc
    gradle build
)

cp /tmp/groovy-pandoc/build/libs/GroovyPandoc-0.*.jar ./install_files/opt/mktechdocs/lib/.
if [[ "$?" != "0" ]] ; then
    echo "Something went wrong. Giving up."
    exit 1
fi

rm -rf /tmp/groovy-pandoc

dpkg-buildpackage

