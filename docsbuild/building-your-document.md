# Building your document

To build your new project from scratch with the default configuration (a single CSS-styled HTML page with a navigation sidebar pinned to the left-hand side), simply do:

``` {.bash}
make deps
make
```

This will first build dependency lists (because none exist yet) and then build the documents.

If no errors occur, your new `index.html` HTML page and CSS file should appear in `./mynewproject/mynewproject_pages`.


Normally, when editing text, you can simply run:

``` bash
make
```

This is much faster, since `make` will only rebuild the parts of the document that have changed and the documents which those changes have affected. For example, suppose you have a document that includes another document, and you've already run `make deps`:

document1.md:

    ```{.include heading-level=1}
    myincludeddoc.md
    ```

myincludeddoc.md

    # Here is some text
    
    Suppose I just edited this text.

Now, if you make changes only in `myincludeddoc.md`, a `make` command will rebuild `myincludeddoc.md` and `document1.md` only, since these are the only files that affected the output. This drastically speeds up build times for large documents.

## Multiple makefiles

Note that a project can have as many makefiles as necessary. For example, if you have a large project and would like to produce a stripped-down version for a particular audience, you can simply create a different master document file and an additional makefile. Then:

```bash
make -f myothermakefile.mk deps
make -f myothermakefile.mk
```

## When to build dependencies

Run `make deps` only when you add a new file or add (or remove) an include block from an existing file.

Common sense applies here. If you change your document in such a way that the dependencies would be affected, you should rebuild `deps`. This command doesn't hurt anything, so when in doubt, run it.

## How to reset your build

Often, such as in the case of the "make deps loop" problem described below, you'll want to reset your build to remove any output produced, dependency lists, intermediate files, and so on. To do this:

``` {.bash}
make distclean
```

If MkTechDocs seems confused about something, try a reset.

## Pre- and post-build activities

Suppose you have a set of static images as part of your documentation. You'll need to copy these to both the build and output directories in order for the images to appear inline.

Use the `BUILD_SCRIPT` [configuration](configuration.html#advanced-configuration) variable to provide the name of a script to run pre-build and post-build. The script should accept 3 arguments:

|Argument #|Description                                     |
|----------|------------------------------------------------|
|1|The activity being performed. Possible values given by MkTechDocs are `pre` and `post`. These indicate that any pre- or post-build activies should take place.|
|2|The full path to the build directory.|
|3|The full path to the output directory.|

Here's an example build script that copies a directory of images into the build and output directories when appropriate:

```bash
#!/bin/bash

ACTIVITY=$1
BUILD_DIR=$2
OUT_DIR=$3

if [[ "$1" == "pre" ]] ; then
	echo "Copying ./img to $BUILD_DIR..."
	cp -r ./img $BUILD_DIR/.
elif [[ "$1" == "post" ]] ; then
	echo "Copying ./img to $OUT_DIR..."
	cp -r ./img $OUT_DIR/.
fi
```

## Troubleshooting build problems

### The make deps loop

Sometimes, particularly if there is an error during a `make deps` command, you will find yourself trapped in the "make deps loop," where `make` tells you to `make deps` even though you've just issued the command. The solution is fortunately easily solved: `make distclean deps`. This forces `make` to clear the `build` directory and start from the beginning.

### Mysterious make error numbers

If you see a mysterious "make error 83" or similar, this usually means that `make` has encountered an error trying to running a Bash command.  Try running the test installation script in the \$MKTECHDOCSHOME/test directory.

## Detailed build-process information

For more detailed information, please see the [understanding the build process](advanced.html#understanding-the-build-process) section.
