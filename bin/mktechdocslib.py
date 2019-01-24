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


import os
import sys
import re
import jinja2
from subprocess import Popen, PIPE

##
# Support functions/classes for MkTechDocs
#

##
# A Jinja2 template loader that loads a template
# from a given path.
#
class PathLoader(jinja2.BaseLoader):
    def __init__(self):
        self.path = ""

    def get_source(self, environment, template):
        path = template
        if not os.path.exists(path):
            raise jinja2.TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with open(path) as f:
            source = f.read()
        return source, path, lambda: mtime == os.path.getmtime(path)

##
# Build a jinja2 environment and render the
# given template
#
def render_mktechdocs_jinja2_template(path, varDictionary):
    # Create a simple loader that will simply load a template
    # from a given path.
    tmplLoader = PathLoader()

    # Set up a simple jinja2 environment
    env = jinja2.Environment(
                    loader=tmplLoader,
                    #autoescape=jinja2.select_autoescape(['html']),
                    trim_blocks=True,
                    lstrip_blocks=True
                )

    # Load a template given as the first argument
    template = env.get_template(path)

    # Render the template    
    #return template.render(varDictionary).encode('utf-8')
    return template.render(varDictionary)

##
# This is a poor man's version of the bit in pythondoc that
# picks up comments at the top of a module.
#
# We use it here simply to demonstrate the power of the
# jinja2 template in documenting live code.
#
def get_comment_from_pythondoc_desc(pyfile):
    beginPDocBlockPat = re.compile("^##[\s]*$")
    contPDocBlockPat = re.compile("^#")
    endPDocBlockPat = re.compile("^$")

    if os.path.isfile(pyfile):
        with open(pyfile, "r") as f:
            state = 0
            collectedDesc = ""
            for l in f:
                if beginPDocBlockPat.match(l):
                    state = 1 # Found the beginning of a block
                elif state == 1 and contPDocBlockPat.match(l):
                    state = 2 # Found a continuation of the block
                elif state == 2 and endPDocBlockPat.match(l):
                    return collectedDesc # End of the block, so bail. One per file.

                if state == 2:
                    add = re.sub("^#", "", l)
                    if add:
                        collectedDesc = collectedDesc + add

        return ""

##
# This is a Git commit message, meant to store individual
# Git commit messages
#
class GitCommitMessage:
    def __init__(self, id="", mergeID="", author="", date="", message=""):
        self.id = id
        self.mergeID = mergeID
        self.author = author
        self.date = date
        self.message = message
        self.mergeCommit = (mergeID != "")

##
# This is a Git commit database, meant for storing Git commit
# messages in such a way as they can be divided into versions
# of a document
#
class GitCommitDB:
    def __init__(self, fcid="", lcid="", mustNotContainList=[], mustContainList=[]):
        self.firstCommitID = fcid
        self.lastCommitID = lcid
        self.messages = []
        self.buildDB(mustNotContainList, mustContainList)

    def __str__(self):
        rv = ""
        for m in self.messages:
            rv += "Commit ID: " + m.id + "\n"
            if m.mergeCommit:
                rv += "Merge ID: " + m.mergeID + "\n"
            rv += "Author: " + m.author + "\n"
            rv += "Date: " + m.date + "\n"
            rv += "Message: " + m.message + "\n\n"

        return rv

    def _getCommitMessages(self):
        p = Popen(["git", "log"], stdout=PIPE, stderr=PIPE)
        ## TESTING ONLY
        #p = Popen(["cat", "foo"], stdout=PIPE, stderr=PIPE)
        ## END TESTING
        (stdout, stderr) = p.communicate()
        stdout = stdout.decode()

        if stderr is not None:
            stderr = stderr.decode()
            if stderr != "":
                sys.stderr.write("WARNING: reading from git log failed: " + stderr + "\n")

        return stdout

    def buildDB(self, mustNotContainList, mustContainList):
        lines = self._getCommitMessages().split('\n')
        idx = 0

        # This means we got an empty line back
        if len(lines) == 1:
            return

        keepCommits = (self.lastCommitID == "")
        while idx+6 < len(lines):
            # Commit ID
            id = lines[idx].replace("commit", "").strip()
            idx += 1

            # More recent commits are first, so we look for the last
            # commit id before we start recording
            if id == self.lastCommitID:
                keepCommits = True

            # Merge ID
            mergeID = ""
            if "Merge:" in lines[idx]:
                mergeID = lines[idx].replace("Merge:", "").strip()
                idx += 1

            # Author
            author = lines[idx].replace("Author:", "").strip()
            idx += 1

            # Date
            date = lines[idx].replace("Date:", "").strip()
            idx += 1

            # Empty line
            idx += 1

            # Message
            message = ""
            while idx < len(lines) and lines[idx] != "":
                message += (lines[idx] + "\n")
                idx += 1

            # Empty line
            idx += 1

            # Ignore commits if they contain a forbidden word, given to us
            # by mustNotContainList
            forbidden = False
            for w in mustNotContainList:
                if message.find(w) != -1:
                    forbidden = True
                    break

            if not forbidden:
                for w in mustContainList:
                    if message.find(w) == -1:
                        forbidden = True
                        break

            if keepCommits and not forbidden:
                self.messages.append(GitCommitMessage(id, mergeID, author, date, message))

            # We may have reached the first commit, at which point
            # we should stop recording commits
            if id == self.firstCommitID:
                keepCommits = False

