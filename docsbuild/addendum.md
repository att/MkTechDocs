# Addendum


## Understanding the build process

The MkTechDocs build process is complex. The following is a step-by-step guide towards understanding how it works.

1. MkTechDocs consists of a BASH control script and a library of Python and Groovy filters.
1. The control script is responsible for importing the project configuration and calling `pandoc` with the correct arguments to build reasonably formatted documents in a variety of formats.
1. The "magic" behind it all is `pandoc` 's Abstract Syntax Tree (AST). Internally, `pandoc` converts all documents into AST, which can then be converted to JSON, which can then be manipulated by filters.
1. MkTechDocs exploits this with a couple of libraries, [GroovyPandoc](https://github.com/jsseidel/groovy-pandoc), for Groovy template integration, and [PandocFilters](https://github.com/jgm/pandocfilters), for Python integration.
1. Every time you run `mktechdocs2`, the control script calls `pandoc` on your project's master document. Some Bash scripting then takes care of some little details, which you can see for yourself by examining the script.

## Contact

MkTechDocs was built and is maintained by [Spencer Seidel](http://www.spencerseidel.com).
