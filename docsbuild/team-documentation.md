# Team documentation

MkTechDocs is ideal for incorporating team-contributed documentation. Because MkTechDocs documentation is simple Markdown, team members can contribute or edit documents via Git (for example) and let a single technical writer manage the pull requests to keep things as simple and as clear as possible.

This makes scaling documentation easier because the technical writer is no longer limited to his or her own domain knowledge or learned knowledge.

That's a simple case. The following describes a different scenario that lets agile developers contribute to documentation in a more specific and controlled way.

## Case study

In this study, a number of different agile development teams are responsible for individual components of a larger system. A configuration repository maintained by the larger system consists of a number of YAML files that describe the general deployment of each component.

Here, components could be Docker containers, VMs, micro-services, or whatever. Each component could have a different but similar set of deployment instructions for each category below, or it could simply conform to some generic set of instructions and require no extra documentation.

1. Overview
1. Environmental-setup
1. Pre-deployment
1. Deployment
1. Undeployment
1. Upgrading
1. Jenkins integration

Agile team members in this scenario are encouraged to contribute documentation in support of their respective components with those steps in mind. If they feel that specialized instructions for any of the above areas applies to their component, they should create a file in a provided directory within the documention tree that matches their component name in the configuration YAML. This file should contain a standalone Markdown document containing instructions specific for their component for that particular step. E.g. `overview/mycomponent.md`, `upgrading/mycomponent.md`.

For example, suppose a VM named `vm-inventory` exists in some YAML configuration file:

```yaml
location:
  description: >
	This is a sample description of a particular location
  vm-deployments:
         .
         .
         .
    vm-inventory:
      vm-config: vmi.cfg
      release: 1.234
      notes: Some notes about this particular VM
        .
        .
        .
```

Now, we can create a template that loads the YAML containing the list of components, and  looks for files with the same name in the directories listed above. If we find specialized instructions, we output them for a particular stage (e.g. Overview, Undeployment). If we find no specialized instructions, we output some generic ones.

## Managing git commit messages

Often, it is useful for your document's audience to understand what has changed from version to version. Rather than keeping track of this manually, in a "change log," for example, you can leverage Git's commit system.

The `git log` command shows a list of all commits to a respository. Each commit has a unique ID associated with it (SHA1 collisions not withstanding). This means that you can create "versions" by recording specific commit messages that represent the beginning and ending of a document version, pulling out all relevant commit messages dynamically when the document is built.

MkTechDocs includes this functionality in the `mktechdocslib.py` module. Here's an example of how to use it.

### GitCommitDB

What we'd like to do is create a simple database of Git messages that exist between two arbitrary Git commit IDs. First, we examine the output of `git log` to determine the first and last commit IDs that frame the version of the document we're interested in creating. Note that the output of `git log` is ordered by commit date, so the most recent dates appear first.

Here is a sample Git log:

```
commit 20de5c8bf2a53efe54a71ae06e5b0b2a813d5176
Author: Seidel, Joseph (js2589) <spence@research.att.com>
Date:   Tue Mar 7 08:04:25 2017 -0500

    Fixed several formatting issues

commit 3523b7f36d928519bba9568852babd793e783a7c
Merge: cd6c4bc f9b3edf
Author: Seidel, Joseph (js2589) <spence@research.att.com>
Date:   Tue Mar 7 06:50:53 2017 -0600

    Merge pull request #71 in FOO_BAR/foo.bar.documentation from feature/FOOBAR/FOOBAR to master

    * commit 'f9b3edfb5194a2be0456d26d742043677948d5ea':
      Added some notes about documentation formats

commit f9b3edfb5194a2be0456d26d742043677948d5ea
Author: Seidel, Joseph (js2589) <spence@research.att.com>
Date:   Mon Mar 6 16:21:17 2017 -0500

    Added some notes about documentation formats
```

From this, we determine that the first commit ID is `f9b3edfb5194a2be0456d26d742043677948d5ea` and the last commit ID is `20de5c8bf2a53efe54a71ae06e5b0b2a813d5176`.

Now, in a template.renderer, we can do something like this:

```python
#!/usr/bin/env python

import os
import sys
import datetime
import global_vars
from mktechdocslib import GitCommitDB, render_mktechdocs_jinja2_template

##
# Create a simple renderer function that ouputs a template passed in on the
# command line with the given variable dictionary.
#

def render():
	messages = GitCommitDB("f9b3edfb5194a2be0456d26d742043677948d5ea", "20de5c8bf2a53efe54a71ae06e5b0b2a813d5176").messages
	varDictionary = {"gitMessages":messages,
	                 "numCommits":len(messages)}
	
	if not os.path.isfile(sys.argv[1]):
		sys.stderr.write("Cannot find " + sys.argv[1] + "\n")
		sys.exit(1)

	print render_mktechdocs_jinja2_template(sys.argv[1], varDictionary)

if __name__ == "__main__":
	render()
```

Here, we import `GitCommitDB` from `mktechdocslib` and add the `GitCommitDB.messages` list object to our variable dictionary. `messages` contains a list of `GitCommitMessage` objects, which have the following properties:

| Property | Type | Description |
|-----------------|-----------|---------------------------------------------------|
| id              | String    | Commit ID |
| mergeID         | String    | Merge commit ID|
| author          | String    | Author of the commit|
| date            | String    | Commit date|
| message         | String    | Commit message|
| mergeCommit     | boolean   | True if the commit is a merge |

Finally, here's our template that displays the information we're interested in:

```
# Document change log

{{ openCurlyBracket }}% if numCommits == 0 %{{ closeCurlyBracket }}
Looks like no changes have been committed.
{{ openCurlyBracket }}% endif %{{ closeCurlyBracket }}

{{ openCurlyBracket }}% for m in gitMessages %{{ closeCurlyBracket }}

{{ openCurlyBracket }}% if not m.mergeCommit %{{ closeCurlyBracket }}
**Date**: {{ openCurlyBrackets }} m.date {{ closeCurlyBrackets }}<br />
**Author**: {{ openCurlyBrackets }} m.author {{ closeCurlyBrackets }}<br />
**Message**: {{ openCurlyBrackets }} m.message {{ closeCurlyBrackets }}<br />
{{ openCurlyBracket }}% endif %{{ closeCurlyBracket }}

{{ openCurlyBracket }}% endfor %{{ closeCurlyBracket }}
```

The version in the example above was hard coded. In reality, it would be better to keep track of version information in a list of tuples. For example:

**versions.py**:

```python
gVersions = [("1.0", "2017-04-06", "f9b3edfb5194a2be0456d26d742043677948d5ea", "20de5c8bf2a53efe54a71ae06e5b0b2a813d5176"),
             ("0.9", "2017-03-25", "d453519c024a49806fbd3a6740a9f0f586aaafbc", "57831131f186a60b864af27e53e06d2772a6d1ef")]
```

In this scheme, the latest version tuple would always be `gVersions[0]`. Or, if you prefer to store the versions in reverse order: `gVersions[len(gVersions)-1]`. Then, our renderer would look like this:

```python
#!/usr/bin/env python

import os
import sys
import datetime
import global_vars
from versions import gVersions
from mktechdocslib import GitCommitDB, render_mktechdocs_jinja2_template

##
# Create a simple renderer function that ouputs a template passed in on the
# command line with the given variable dictionary.
#

def render():
	(versString, date, fcid, lcid) = gVersions[0]
	
	messages = GitCommitDB(fcid, lcid).messages
	
	varDictionary = {"gitMessages":messages,
                     "numCommits":len(messages),
                     "versString":versString,
                     "date":date}
	
	if not os.path.isfile(sys.argv[1]):
		sys.stderr.write("Cannot find " + sys.argv[1] + "\n")
		sys.exit(1)

	print render_mktechdocs_jinja2_template(sys.argv[1], varDictionary)

if __name__ == "__main__":
	render()
```
