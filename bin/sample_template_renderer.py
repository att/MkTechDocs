#!/usr/bin/env python3

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

import sys

from mktechdocslib import render_mktechdocs_jinja2_template

##
# This is a sample MkTechDocs renderer that creates a list
# of navigation links and then sends it to a simple
# jinja2 template renderer.
#

def render():
    navlinks = {"Location 1":"#loc1", "Location 2":"#loc2", "Location 3":"#loc3"}

    varDictionary = {"title":"A sample jinja2 python template", # <--- A simple variable
                     "navlinks": navlinks,                      # <--- Another dictionary
                     "sortit": sorted}                          # <--- We can even add functions

    # Always use sys.argv[1] here since our makefile will
    # always provide the name of the template that needs
    # rendering.
    print(render_mktechdocs_jinja2_template(sys.argv[1], varDictionary))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: sample_template_renderer.py <template.pyt)\n")
        sys.exit(1)
    render()
