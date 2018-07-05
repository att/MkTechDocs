# Building your document with Docker

MkTechDocs is a complex set of code and dependencies, so it can be difficult to set up to run locally. Fortunately, MkTechDocs is available as a Docker image on [Docker Hub](https://hub.docker.com/r/jsseidel/mktechdocs/): `jsseidel/mktechdocs`.

To use it, you need to have Docker installed. Then, building projects is relatively simple:

```
docker run --rm -v /home/ubuntu/MyMkTechDocsProject:/project jsseidel/mktechdocs
```

Here's the breakdown of the command:

`--rm`: Remove the container after it exits. Otherwise, it will hang around in the `Exited` state, which can be useful if there were problems.

`-v`: Create a volume and map `/home/ubuntu/MyMkTechDocsProject` _outside_ the container to `/project` _inside_ the container. `/project` is where the entry script inside the container looks for a project to build.

`jsseidel/mktechdocs`: This is the docker image to use to run the container. Since no tag is specified (e.g. `jsseidel/mktechdocs:0.0.1`), docker will use the `latest` tag.

When you run it, an entry script inside the `mktechdocs` container will `cd` into `/project` and run `mktechdocs`. For this to work, your project must contain both a `mktechdocs.conf` and a `master.md` file.

