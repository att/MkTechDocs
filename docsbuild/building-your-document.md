# Building your document

To build your new project from scratch with the default configuration (a single CSS-styled HTML page with a navigation sidebar pinned to the left-hand side), simply do:

``` {.bash}
mktechdocs
```

If no errors occur, your new `index.html` HTML page and CSS file should appear in `./myproject/myproject_pages`.

Here is the inline help:

```
$ mktechdocs help
Usage: mtechdocs [help|clean|init]
  help : Display this help message
  clean: Remove temporary build files
  init : Create a new MkTechDocs project in the current directory

Usage: mtechdocs
  Builds the MkTechDocs project in the current directory. Assumes
  that a mktechdocs.conf file and master.md file are present.

Usage: mtechdocs <config> <directory>
  Builds the MkTechDocs project in the given directory using the
  given configuration.
$
```

## Multiple configurations

Note that a project can have as many configurations as necessary. For example, if you need to produce a PDF and styled webpage:

```bash
mktechdocs config1.conf /Users/mylogin/myproject
mktechdocs config2.conf /Users/mylogin/myproject
```

## Pre- and post-build activities

Suppose you have a set of static documents as part of your documentation. You'll need to copy these to both the build and output directories in order for the images to appear inline.

Use the `BUILD_SCRIPT` [configuration](configuration.html#advanced-configuration) variable to provide the name of a script to run pre-build and post-build. The script should accept 2 arguments:

|Argument #|Description                                     |
|----------|------------------------------------------------|
|1|The activity being performed. Possible values given by MkTechDocs are `pre` and `post`. These indicate that any pre- or post-build activies should take place.|
|2|The full path to the output directory.|

Here's an example build script:

```bash
#!/bin/bash

ACTIVITY=$1
OUT_DIR=$2

if [[ "$ACTIVITY" == "pre" ]] ; then
	echo "Creating some new stuff in ./mystuff..."
elif [[ "$ACTIVITY" == "post" ]] ; then
	echo "Copying ./mystuff to $OUT_DIR..."
	cp -r ./mystuff $OUT_DIR/.
fi
```

You don't need to worry about copying images to your output directory. Because images are often associated with documentation, MkTechDocs provides a [configuration option](configuration-options.html#simple-configuration) where you can specify the path to your the directory that holds your images.
