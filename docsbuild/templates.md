# Python templates

MkTechDocs contains built-in support for [Jinja2 templates](http://jinja.pocoo.org). Using jinja2 templates is simply a matter of creating templates (plain text files containing Jinja2 markup code) and adding a `.pyt` extension, or, in the case of your header, landing page, and footer, a `.htmlt` extension, so MkTechDocs knows how to build them.

To use templates in MkTechDocs, you'll need to create both a renderer and a template to render.

## The template

A template is nothing more than plain text with some special Jinja2 markup thrown in. For example, let's create a dynamic title page using templates. First, we'll create a template that represents a dynamic YAML title block in our project directory:

**title-page.pyt**:

```
---
title: My Title {{ openCurlyBrackets }} docVersion {{ closeCurlyBrackets }}
author:
	- John Doe
	- Jane Doe
date: Built on {{ openCurlyBrackets }} currentDateTime {{ closeCurlyBrackets }}
---
```

The Jinja2 templating engine will replace the variables in the double curly brackets with values you provide in the renderer.

## The renderer

Now, in your project directory, create a renderer with the same name as the template, but replace `.pyt` with `.renderer`. MkTechDocs will automatically use the renderer associated with the template name. Renderers are built with pure Python code. Continuing with our title-page example, here is a renderer that will properly render our title page template.

**title-page.renderer**:

```python
#!/usr/bin/env python

import sys
import datetime
from mktechdocslib import render_mktechdocs_jinja2_template

##
# Create a simple renderer function that ouputs a template passed in on the
# command line with the given variable dictionary.
#

def render():
  # Here, we hard code a document version, but in a real-world example, we'd
  # probably want to grab this from a configuration file or even a database.
  docVersion = "0.1a"

  # Now set up the date and time however you see fit
  currentDateTime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

  varDictionary = {"docVersion":docVersion, "currentDateTime":currentDateTime}

  if not os.path.isfile(sys.argv[1]):
    sys.stderr.write("Cannot find " + sys.argv[1] + "\n")
    sys.exit(1)

  print render_mktechdocs_jinja2_template(sys.argv[1], varDictionary)

if __name__ == "__main__":
  render()
```

You can add as many variables to your `varDictionary` as necessary. You can even add entire modules and functions, if you need more logic in your templates.

Next, set the `TITLE_PAGE` variable in your project makefile to `title-page.md`. Why the `.md` extension? MkTeckDocs automatically converts anything with a `.pyt` extension to markdown before building your documents. Here's a diagram that illustrates the process:

```{.plantuml title="Template Rendering"}
node mytemplate.pyt as PYT
node mytemplate.renderer as RND
cloud MkTechDocs as MTD
node mytemplate.md as MD
node "Final Document" as FD

MTD <-- PYT
MTD <-- RND
MTD --> MD
MD --> FD
```

Since title pages are only used in PDF documents (currently), you should also set `FORMAT` to `pdf` or `pdffloat`.

## Referencing templates in include blocks

MkTechDocs automatically detects `*.pyt` templates and converts them into markdown before processing include blocks. So, if you need to include the contents of a template's output in another markdown file, simply treat the template as if it were markown. For example, if your template's name is `mytemplate.pyt` reference the output in include blocks like:

    ```include
    mytemplate.md
    ```

## `footer.html`, `header.html`, and `landing.html` as templates

MkTechDocs will recognize `footer.htmlt`, `header.htmlt`, and `landing.htmlt` as templates and process into corresponding `.html` files, using similarly named renderers. E.g. `footer.renderer`.

## Escaping curly brackets

Because every MkTechDocs document is ultimately converted into a large Python Jinja2 template, if you want to include double curly brackets as curly brackets in your document, for example, if you're documenting Jinja2, you will need to escape them.

Here's how:

		{{openCurlyBracket}}% raw %{{closeCurlyBracket}}
   	{%raw%} 
		{{somevar}}
   	{%endraw%} 
		{{openCurlyBracket}}% endraw %{{closeCurlyBracket}}

If you need to escape a single curly bracket, you can use:

{%raw%}
`{{openCurlyBracket}}` and `{{closeCurlyBracket}}`
{%endraw%}

## For more information

For real-world examples of how to use Jinja2 templates with MkTechDocs, see the following files in the MkTechDocs directory:

```
docsbuild/runningfilters.pyt
docsbuild/runningfilters.renderer
docsbuild/scripts.pyt
docsbuild/scripts.renderer
```

These templates and renderers incorporate some pythondoc-like markup in the [filters](#running-filters) and [scripts](#scripts) that come with MkTechDocs.

Jinja2 templates can be powerful documentation tools. Please reference the [Jinja2 template documentation](http://jinja.pocoo.org/docs/2.9/templates/) for more information 2>$template.err.
