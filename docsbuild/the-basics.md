# The basics

There are a couple of different use cases for MkTechDocs:

1. You want to build and maintain a complex documentation project.
2. You want to use MkTechDoc tools to process one-off documents for previewing or ingesting into some other documentation scheme.

In either case, the best way to start is to create a new MkTechDocs project and import existing files. This way, you automatically gain access to all the complex command-lines, CSS styling, PDF templates, Pandoc filters, and so on.

## The executive summary

The easiest way to learn how to use MkTechDocs effectively is with a tutorial project. [Here's one on GitHub](https://github.com/jsseidel/GettingStartedWithMkTechDocs).

Unlike the comprehensive usage guide, the tutorial project uses a Docker image to build and provides a good overview of a MkTechDocs project without getting too far into the weeds.

## Markdown

MkTechDocs uses Markdown exclusively, although support for additional syntaxes may be added in the future. More specifically, it uses standard Markdown syntax [with Pandoc extensions](http://pandoc.org/MANUAL.html#pandocs-markdown). In this documentation, assume that any file with a `.md` extension is a file that contains Markdown. Markdown is easy to learn, read, and edit and is easily transformable into a myriad of output formats. To use MkTechDocs effectively, take a few minutes to familiarize yourself with [Markdown syntax](https://daringfireball.net/projects/markdown/syntax).

## Creating a new project

To create a new MkTechDocs project, `cd` inside the directory where you want to create it and run `mktechdocs`. For example:

```bash
mkdir mynewproject
cd mynewproject
mktechdocs init
```

`mktechdocs` will create the following files in `mynewproject`:

| File Name       | Purpose                                                                 |
|-----------------|-------------------------------------------------------------------------|
|`footer.html`\*|Custom HTML content MkTechDocs should place in the footer area of HTML output.|
|`header.html`\*|Custom HTML content MkTechDocs should place in the header area of HTML output.|
|`landing.html`\*|Custom HTML landing-page content MkTechDocs uses in index.html when creating multi-html-page output.|
|`master.md`|A stub master document.|
|`subdocument.md`|An example subdocument that's included inside the master.|
|`mktechdocs.conf`|Project configuration.|

\* NOTE 1: Optional. If you don't need this HTML content, for example, if you're producing PDF content only, you can safely delete these files.

\* NOTE 2: If you need more dynamic content in your header, footer, or main content, dates, database information, etc., please read the [`footer.html`, `header.html`, and `landing.html` as templates section](templates.html#footer.html-header.html-and-landing.html-as-templates)

## MkTechDocs projects

### Master document

MkTechDocs projects consist of a "master" document &mdash; a single markdown document that defines your project, always named `master.md`&mdash; and any number of sub documents. Building a master document is simple:

    ```comment
    Define one or more include blocks to include all the major subdocuments that
    make up your project.
    ```
    ```{.include heading-level=0}
    introduction.md
    getting-started.md
    more-things.md
    the-end.md
    ```

Note the `heading-level=0` attribute. This tells MkTechDocs that the current heading level at the point of the include block is '0'. This will result in each included document starting with heading level of 1, or &lt;H1&gt; in HTML parlance. If you want to keep all your heading-level ones in the master document, that's okay, too. Simply use `heading-level=1` when including subdocuments. More information on this follows.

### Sub documents

Every sub document you include should start with a heading level of 1 (i.e. &lt;H1&gt;). MkTechDocs automatically increases the heading level of included documents (even multi-level recursive includes, where a document includes another document that includes another document, and so on). The heading-level adjustments will work provided that you give MkTechDocs a hint about the current heading level at the point of inclusion, as we have already seen:

    ### A level three header
    
    ```{.include heading-level=3}
    myincludeddoc.md
    ```

Now, regardless of how many included documents appear in `myincludedoc.md` and in documents included in *those* documents, the heading levels should be consistent, provided you remember that all sub documents should start with a heading level of 1, as if they were a standalone document.

```tip
Creating every sub document such that it can exist on its own has the added benefit of allowing you to assemble different combinations of documents for different audiences. For example, you might want to build a small section of a much larger document as a standalone PDF.
```

#### Images

If you want to include images in your project document, include them inline using standard Markdown:

E.g.

    ```
    Please click to [the following link](images/smiley.png) to see a smiley.
        
    Or let's include it inline with a title underneath:
     
    ![Smiley](images/smiley.png)
    ```

And here's what the code above looks like after rendering:

<hr />

Please refer to [the following link](images/smiley.png) to see a smiley.

Or let's include it inline with a title underneath:

![Smiley](images/smiley.png)

<hr />


Then, tell MkTechDocs where your images directory is in the [configuration section](configuration-options.html#simple-configuration) of your project makefile.

