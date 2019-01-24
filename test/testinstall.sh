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

# Default test is master_no_groovy.md
PASSFAIL=PASSED
cp master_no_groovy.md master.md
mktechdocs
diff test_pages/test.md successful_render.md
if ! exit_ok ; then
    PASSFAIL=FAILED
fi

echo "========================================"
echo "basic python functionality $PASSFAIL"
echo "========================================"

if [[ "$1" == "groovy" ]] ; then
    PASSFAIL=PASSED
    cp master_w_groovy.md master.md
    cp test_template.groovy test_template_groovy.gt
    mktechdocs
    diff test_pages/test.md successful_render_w_groovy.md
    if ! exit_ok ; then
        PASSFAIL=FAILED
    fi

    echo "========================================"
    echo "basic groovy functionality $PASSFAIL"
    echo "========================================"
    rm -f test_template_groovy.gt
fi

rm -rf master.md test_pages
