# Advanced information

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

