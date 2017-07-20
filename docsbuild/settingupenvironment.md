# Setting up your environment

Please export the following variables. Here is an example in Bash:

```bash
# MkTechDocs libraries and scripts require the following variable:
export MKTECHDOCSHOME=/home/mylogin/MkTechDocs

# Make sure the MkTechDocs bin directory is in your path:
export PATH=$PATH:$MKTECHDOCSHOME/bin

# Let Python know where to find MkTechDocs libraries:
export PYTHONPATH=$MKTECHDOCSHOME/bin
```
## Running the dependencies installation script

Install MkTechDocs dependencies using the (admittedly imperfect) installation script. Consider the script more of a guide.

Examine the contents of the `$MKTECHDOCSHOME/bin/install_deps*sh` script appropriate for your architecture. For Groovy support, please also see the `install_deps*sh` scripts in the `bin/groovy` directory. The install script simply tries to install the various dependencies using an architecture-appropriate package manager and in some cases checks version numbers of installed binaries. You can also install the dependencies manually.

```{.include heading-level=2}
dependencies.md
```

## Testing your environment

After installing the dependencies, run this:

```bash
cd $MKTECHDOCSHOME/test
./testinstall.sh
```

You should see something like this:

```
[~/MkTechDocs/test]$ ./testinstall.sh
Created image plantuml-c6117aebb4ce8e59ba2b46950eca869f.svg
Test dependency installation
============================

First, we'll try an include:

Include test file
-----------------

This text is coming from inside test\_install\_include.md.

Now, we'll try some plantUML:

![](plantuml-c6117aebb4ce8e59ba2b46950eca869f.svg)
Pandoc seems ok.


Checking python...

If this prints with no error, you are good to go!
Python seems ok.
[~/MkTechDocs/test]$
```

If you get errors, examine the output of the installation script to see where something went wrong.
