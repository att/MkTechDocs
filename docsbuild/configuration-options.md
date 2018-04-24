# Configuration

You configure MkTechDocs projects with variables contained in a configuration file in your project directory. By default, the name of this file is `mktechdocs.conf`, and if you choose to use this name, you won't have to provide the configuration file and directory when you run MkTechDocs.

## Simple configuration

For the majority of relatively simple documents and websites, the simple configuration options should suffice.

|Variable Name   |Possible Values                 |Effects                                                  |
|----------------|--------------------------------|---------------------------------------------------------|
|`TITLE`         | Any                            |The natural-language title of your project.|
|`OUTPUT_FILE_NAME`|Any. No spaces or punctuation.|Certain outputs will produce a file of this name.|
|`FORMAT`        |pdf, pdffloat, html, htmlsimple, cssframes, htmlmulti, markdown, docx|_Output format_<br /><br />**pdf**: A PDF file with section numbers and a title page. Diagrams are positioned near where they are included.<br />**pdffloat**: A PDF file with section numbers and a title page. Diagrams are "floated" within the document.<br />**html**: A single CSS-styled HTML page with a hideable table of contents at the top.<br />**htmlsimple**: A single unstyled HTML page with no table of contents.<br />**cssframes**: A single CSS-styled HTML page with a CSS-locked navigation sidebar on the left-hand side and locked content on the right-hand side. A customizable header and footer (in header.html and footer.html) are used to frame the page.<br />**htmlmulti**: Multi-page CSS-styled HTML with a CSS-locked navigation bar on the left-hand side and content on the right-hand side. A customizable header and footer (in header.html and footer.html) are used to frame the page. In addition, landing.html is used as a landing page with the CSS-locked navigation sidebar on the left-hand side. Best for large projects.<br />**markdown**: A single markdown document.<br />**docx**: A single Microsoft Word document.|
|`HTML_STYLE`|archwiki, github, custom|CSS styles that loosely mimic the Arch Linux Wiki and GitHub documentation. See `CUSTOM_CSS` for more information about applying custom CSS styles.|
|`PDF_MAIN_FONT`|Any installed font name.|MkTechDocs will apply this font to the main "default" text of output if `FORMAT` is `pdf` or `pdffloat`.|
|`PDF_MONO_FONT`|Any installed font name.|MkTechDocs will apply this font to any sections of the PDF document that require a fixed-width font, such as code sections. Applies only to output if `FORMAT` is `pdf` or `pdffloat`.|
|`TABLE_OF_CONTENTS_MAIN_DEPTH`|1-6|The maximum number heading-level depth to count as a section number in the "main" document (not sub documents in `htmlmulti` format). For example, if `TABLE_OF_CONTENTS_MAIN_DEPTH` is 2, all level-three headings and greater will _not_ appear in the table of contents.|
|`TABLE_OF_CONTENTS_SUB_DEPTH`|1-6|The maximum number heading-level depth to count as a section number in sub documents for the `htmlmulti` format.|
|`SECTION_NUMBERS`|true,false|Include section numbers in headings and tables of content.|
|`TITLE_PAGE`|Any. No spaces or puncutation.|See the [title pages](title-pages.html#title-pages) section for more information. Applies only to `pdf` and `pdffloat` output formats.|
|`IMAGES`|Path to directory relative to project.|See the [Images](the-basics.html#images) section for more information. Applies to all formats.|

## Advanced configuration

More complex documents may require finer-grain control over how documents are rendered and stylized.

|Variable Name   |Possible Values                 |Effects                                                  |
|----------------|--------------------------------|---------------------------------------------------------|
|`BUILD_SCRIPT`  |Any                             |See the [Pre- and post-build activities](building-your-document.html#pre--and-post-build-activities) section for for information.|
|`CUSTOM_CSS`|Relative path to CSS file|If you provide a file path here to a CSS file, MkTechDocs will copy that file into your \*\_pages output directory. To understand MkTechDocs CSS, see the `$MKTECHDOCSHOME/lib/*.css` files.|
|`CUSTOM_TEMPLATE`|Relative path to pandoc template|If you provide a file path here to a template file, MkTechDocs will use that template instead of one of the defaults. To understand MkTechDocs template files, see the `$MKTECHDOCSHOME/*_template.html` files. In addition, please see `man pandoc` -> "Variables set by pandoc" for a listing of pandoc variables available to template files. For more complex use of variables, see the [Python Templates](templates.html#python-templates) section.|
|`KEEP_TEMP_FILES`|true,false|If true, mktechdocs will delete all temporary build files after completing a build.|

