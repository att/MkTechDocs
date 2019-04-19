# Building your document with Docker

MkTechDocs is a complex set of code and dependencies, so it can be difficult to
set up to run locally. Fortunately, MkTechDocs is available as a Docker image on
[Docker Hub](https://hub.docker.com/r/jsseidel/mktechdocs/):
`jsseidel/mktechdocs`.

## PDF output and docker

Please note that the Docker version of MkTechDocs does not currently support PDF
output. Adding in this support makes the Docker image unreasonably large, and
the image is already too big. 

## The build command

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

## Considerations

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


