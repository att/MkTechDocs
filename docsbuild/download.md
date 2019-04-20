# Install MkTechDocs

## Docker

The easiest way to use MkTechDocs is via Docker.

```
docker run --rm --user $(id -u):$(id -g) -v $PROJECTDIR:/project jsseidel/mktechdocs
```

If `$PROJECTDIR` is an empty directory, MkTechDocs will create a new project.
If `$PROJECTDIR` already contains a MkTechDocs project, MkTechDocs will build
it.

```note
The Docker version of MkTechDocs does not support PDFs.
```

## PPA

Add and install the Launchpad PPA in Ubuntu 18.04+:

```bash
sudo add-apt-repository -y ppa:jsseidel/mktechdocs
sudo apt update
sudo apt install -y mktechdocs
```

Then:

```bash
. /opt/mktechdocs/bin/mktechdocs.env
```

## Deb package

Download the latest deb package from the MkTechDocs GitHub releases
page:
[https://github.com/att/MkTechDocs/releases](https://github.com/att/MkTechDocs/releases).

```bash
sudo apt install -y ./mktechdocs_18.04_1.0.8_amd64.deb
```

Then:

```bash
. /opt/mktechdocs/bin/mktechdocs.env
```

## Source

To download the MkTechDocs source tree, clone the repo:

```bash
git clone https://github.com/att/MkTechDocs
```

Then, [set up your environment](#setting-up-your-environment).

