# Addendum

## How MkTechDocs evolved

MkTechDocs was inspired by a complex, ad-hoc build script for a large (300+
pages) PDF deployment guide. That proof of concept used a variety of tools,
such as LaTeX, DocBook and Textile. The content was contained in an enormous
Groovy template master document. In addition, it had non-negotiable
dependencies on several proprietary Java and Groovy classes.

There were a couple of problems. First, the system was fragile. Subtle
changes broke the build and debugging build issues was difficult.
Second, the build system and content were tightly coupled. Third, there
was no easy way for developers to contribute to the documentation. 

A new system was clearly needed, but which one? Any new system had to
duplicate the existing document exactly, down to the section numbers,
for one thing. The new system would have to use Groovy and/or Java
because of the dependencies. Finally, and most importantly, an urgent
need was arising for developers to contribute documentation about their
own components.

Although there are many technical documentation systems out there, none
of them were a good fit. The biggest hurdles were:

1. The need for a robust templating system -- much of the deployment
  guide was generated programatically by enumerating dependencies,
  including bits of configuration YAML, code, etc.
2. Incorporating existing Groovy and Java libraries in order to do
  the above.
3. Letting developers contribute documentation
4. The system needed to be completely open to any and all configuration
  changes we might need to make that affected how the output was styled.

The first version of MkTechDocs solved theses problems by:

1. Using Groovy pandoc filters
2. Using Groovy templates
3. Modularizing the build so that:
    a. errors would be easier to identify and fix
    b. developers who contributed documentation would edit only their
      modules
4. Using CodeCloud (Gerrit would work as well) to allow a single
  repository master (i.e. editor) monitor changes and subsequent
	merges

There remained an issue. Groovy was s-l-o-w. Builds took upwards of
twenty minutes.

To solve this problem, MkTechDocs migrated to Python filters and
templates (via Jinja2). This decreased build times by an order of
magnitude.  Now, MkTechDocs supports both.

## Understanding the build process

The MkTechDocs build process is complex. The following is a step-by-step guide towards understanding how it works.

1. Lists of files are created. Every A.md file has a corresponding build/A.pmd, build/A.md, and build/A.pmd.d file. Every B.pyt file has either a corresponding B.renderer file or a generic renderer supplied in a `makefile` variable, as well as a corresponding build/B.pmd, build/B.md, and build/B.pmd.d file. Every C.gt file has a corresponding build/C.pmd, build/C.md, and build/C.pmd.d file. Every D.htmlt has a corresponding build/D.html file.
1. For every file in every list, there is a corresponding `make` rule:
	1. \*.pyt, \*.gt -> build/\*.pmd, build/\*.pmd.d:
	1. \*.md -> build/\*.pmd, build/\*.pmd.d: To build a build/\*.pmd file, we run the markdown through pandoc, searching for include blocks which are used to build the dependency list stored in build/\*.pmd.d. In the case of templates, `make` first renders the templates before searching for include blocks.
	1. \*.htmlt -> build/\*.html: To build a build/\*.html file, `make` renders the template using a corresponding renderer or a generic renderer specified in the `makefile`.
1. For PDF output, produce a final PDF by passing the master document through pandoc with an array of filters applied (see the "-F" arguments in `makefile`). 
1. For HTML outputs that produce a single page:
	1. Produce a Jinja2 template by passing the master document through pandoc with an array of filters (see the "-F" arguments in `makefile`). We also use the --template argument to tell pandoc to produce a file from a template.
	1. Strip any reference to pages in links.
	1. Render the final output by using `page.renderer`.
1. For HTML outputs that produce multiple pages:
	1. Create a jinja2 template for each page and render using `page.renderer` in order to include header and footer content.
	1. Massage the output of pandoc to produce links that look like: page.html#section.
	1. Create a jinja2 template for the main page and render using `page.renderer` in order to include header, footer, and landing content.
1. Copy all output files and CSS (if any) to the output directory.

