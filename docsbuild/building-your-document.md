# Building your document

## From local install

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

### Multiple configurations

Note that a project can have as many configurations as necessary. For example, if you need to produce a PDF and styled webpage:

```bash
mktechdocs config1.conf /Users/mylogin/myproject
mktechdocs config2.conf /Users/mylogin/myproject
```

### Pre- and post-build activities

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

## Docker

MkTechDocs is a complex set of code and dependencies, so it can be difficult to
set up to run locally. Fortunately, MkTechDocs is available as a Docker image on
[Docker Hub](https://hub.docker.com/r/jsseidel/mktechdocs/):
`jsseidel/mktechdocs`.

### PDF output and docker

Please note that the Docker version of MkTechDocs does not currently support PDF
output. Adding in this support makes the Docker image unreasonably large, and
the image is already too big. 

### The build command

To get started, you'll need to have Docker installed. Then, building projects
is relatively simple. When you first run the command below,
`MyMkTechDocsProject` should be an empty directory. MkTechDocs will recognize
that it should create a new project there. Subsequent runs will build your
project.

```
docker run --user $(id -u):$(id -g) --rm -v /home/ubuntu/MyMkTechDocsProject:/project jsseidel/mktechdocs
```

Here's the breakdown of the command:

`--user $(id -u):$(id -g)`: This tells docker to run the command under the
current user and group id.

`--rm`: Remove the container after it exits. Otherwise, it will hang around in
the `Exited` state, which can be useful if there were problems.

`-v`: Create a volume and map `/home/ubuntu/MyMkTechDocsProject` _outside_ the
container to `/project` _inside_ the container. `/project` is where the entry
script inside the container looks for a project to build.

`jsseidel/mktechdocs`: This is the docker image to use to run the container.
Since no tag is specified (e.g. `jsseidel/mktechdocs:0.0.1`), docker will use
the `latest` tag.

When you run it, an entry script inside the `mktechdocs` container will `cd`
into `/project` and run `mktechdocs`. For this to work, your project must
contain both a `mktechdocs.conf` and a `master.md` file.

### Considerations

MkTechDocs uses a volume inside the Docker container (`/project`) and maps it to
the contents to your MkTechDoc project directory. As such, it isn't possible to
access directories outside your MkTechDoc project directory inside the
container.

If you therefore have any [pre- or post-build
scripts](https://att.github.io/MkTechDocs/#pre--and-post-build-activities),
please note that the script will only have access to the contents of your
MkTechDocs project directory.

For example, suppose you wanted to copy the contents of your output directory to
some other directory and map that to your GitHub IO website. The following
command will not work in a post-build script during a Docker build:

```bash
cp $OUTPUT_DIR/* ../docs/.
```

Inside the Docker container, when MkTechDocs is building, `../docs` doesn't
exist.

To fix this, you need `docs` inside your project directory. Then, the following
will work:

```bash
cp $OUTPUT_DIR ./docs/.
```


