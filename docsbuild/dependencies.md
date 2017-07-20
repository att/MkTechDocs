# Dependencies

MkTechDocs requires the following:

| Package | Version    | Description                                      |
|---------|------------|--------------------------------------------------|
|Bash     | any recent | A shell.|
|Git      | any recent | A distributed version-control system.|
|Pandoc   | >= 1.18    | Pandoc is a powerful document conversion tool and is at the heart of MkTechDocs.|
|Make     | any recent | A tool to help manage document dependencies during the build process.|
|Graphviz | any recent | A collection of open-source tools for drawing graphs in the DOT language.|
|Plantuml | any recent | A tool for creating UML diagrams that uses Graphviz underneath.|
|XeTeX    | any recent | A suite of tools for building PDF documents.|
|Python   | 2.7        | MkTechDocs is currently compatible with Python 2.7.|
|Jinja2   | 2+         | A Python templating library.|
|homebrew\*\*| any recent | A package manager for macOS.|

\*\* *homebew*: macOS only

**Groovy/Java**\*

| Package | Version    | Description                                      |
|---------|------------|--------------------------------------------------|
|Java\*   | >= 1.8     | MkTechDocs is currently compatible with Java 1.8 |
|Groovy\* | > 2.0      | A Java-like scripting language that extends Java.|
|groovy-pandoc\*| >= 0.8 | A Groovy library used to build Pandoc filters for document transformation.|
|Gradle\* | > 3.0      | A build automation system that is friendly to the Groovy language.|

\*: Java/Groovy dependencies are optional but ideal for interfacing MkTechDocs with existing Java libraries. Note that Groovy pandoc filters are orders of magnitude slower than their Python counterparts. To shorten build time, you might want to try [GroovyServ](https://kobo.github.io/groovyserv/userguide.html).

