#!/bin/bash

# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.
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

function normal_exit {
    [[ "$?" == "0" ]]
}

# For color output
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export NC='\033[0m'

# Default test is master_no_groovy.md
PASSFAIL="${GREEN}PASSED${NC}"
cp master_no_groovy.md master.md
mktechdocs
diff test_pages/test.md successful_render.md
if ! normal_exit ; then
    PASSFAIL="${RED}FAILED${NC}"
fi

echo -e "========================================"
echo -e "basic python functionality $PASSFAIL"
echo -e "========================================"

if [[ "$1" == "groovy" ]] ; then
    PASSFAIL="${GREEN}PASSED${NC}"
    cp master_w_groovy.md master.md
    cp test_template.groovy test_template_groovy.gt
    mktechdocs
    diff test_pages/test.md successful_render_w_groovy.md
    if ! normal_exit ; then
        PASSFAIL="${RED}FAILED${NC}"
    fi

    echo -e "========================================"
    echo -e "basic groovy functionality $PASSFAIL"
    echo -e "========================================"
    rm -f test_template_groovy.gt
fi

rm -rf master.md test_pages

# Build the PDF version of the MkTechDocs usage_guide and check to make
# sure MkTechDocs actually produced a PDF.
mkdir tmp
(
cd tmp
cp -r ../../docsbuild/* .
perl -i -p -e 's/^FORMAT=cssframes/FORMAT=pdf/' mktechdocs.conf
cat << EOF > build.sh
#!/bin/bash
# nop
EOF
chmod 755 build.sh
PASSFAIL="${GREEN}PASSED${NC}: output in ./usage_guide.pdf"
mktechdocs
if [[ ! -s usage_guide_pages/usage_guide.pdf ]] ; then
    PASSFAIL="${RED}FAILED${NC}"
else
    cp usage_guide_pages/usage_guide.pdf ../.
fi

echo -e "========================================"
echo -e "usage_guide.pdf test $PASSFAIL"
echo -e "========================================"
)
rm -rf tmp

