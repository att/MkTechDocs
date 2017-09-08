# How MkTechDocs evolved

MkTechDocs was inspired by a complex, ad-hoc build script for the DCAE
deployment guide (a component of AT&T's OpenECOMP/ONAP initiative). That
proof of concept used a variety of tools, such as DocBook and Textile,
and consisted of a large Textile master document. In addition, it had
non-negotiable dependencies on several Java and Groovy classes.

There were a couple of problems. First, the system was fragile. Subtle
changes broke the build and debugging build issues was difficult.
Second, the build system and content were tighly coupled. Third, there
was no easy way for developers to contribute to the documentation. 

A new system was clearly needed, but which one? Any new system had to
duplicate the existing document exactly, down to the section numbers,
for one thing. The new system would have to be use Groovy and/or Java.
And what about Textile? The majority of the document was written in that
syntax. Finally, and most importantly, an urgent need was arising for
developers to contribute documentation about their own components.

Although there are many technical documentation systems out there, none
of them were a good fit. The biggest hurdles were:

1. The need for a robust templating system -- much of the deployment
guide was generated programatically by enumerating dependencies,
including bits of configuration YAML, code, etc.
2. Incorporating existing Groovy and Java libraries in order to do
(1)
3. Letting developers contribute documentation

The first version of MkTechDocs solved theses problems by:

1. Using 100% Groovy pandoc filters
2. Using Groovy templates
3. Modularizing the build so that developers who contributed
documentation would edit only their modules
4. Using CodeCloud (Gerrit would work as well) to allow a single repo
master to monitor changes and subsequent merges

There remained an issue. Groovy was s-l-o-w. Builds took upwards of
twenty minutes.

To solve this problem, MkTechDocs migrated to Python filters and
templates (via Jinja2) and speeded up builds by orders of magnitude.
Now, MkTechDocs supports both.

