# Incorporating Groovy code and templates

Groovy integration is an optional step and only necessary if you want to access existing Java libraries.

## Installation of groovy components

First, start by examining and then running whichever `install_deps_*_groovy.sh` script in `$MKTECHDOCSHOME/bin/groovy` is appropriate for your architecture.

They install two packages, groovy and gradle. Then, they download a Groovy library called `groovy-pandoc` from GitHub and install the resulting jar file in `$MKTECHDOCSHOME/lib`.

### Environment

Next, add `$MKTECHDOCSHOME/bin/groovy` to your `PATH` environment variable. Here's an example in Bash:

```bash
export PATH=$PATH:$MKTECHDOCSHOME/bin/groovy
```

### Testing the integration

Finally, run `$MKTECHDOCSHOME/test/testgroovyintegration.sh`. Your output should look something like this:

```
[~/MkTechDocs/test]$ testgroovyintegration.sh
Generating 'svg' plantuml diagram named 'Diagram'
Test dependency installation
============================

First, we'll try an include:

Include test file
-----------------

This text is coming from inside test\_install\_include.md.

Now, we'll try some plantUML:

![Diagram](./8410b9ad92ce7f3e2d564faff2b834b1.plantuml.svg){{ openCurlyBracket }}#myid{{ closeCurlyBracket }}
Pandoc seems ok.


Checking groovy...

If this prints with no error, you are good to go
Groovy seems ok.
[~/MkTechDocs/test]$
```

## Groovy templates

You can use Groovy templates (`*.gt`) as you would Jinja2 Python templates, except that Groovy templates do not require a renderer, which makes them somewhat more convenient. However, this comes at a price. Groovy templates are far slower than Jinja2 to generate, even with [GroovyServ](https://kobo.github.io/groovyserv/) installed.

Groovy templates work like PHP or JSP files. You can include plain text markdown and Groovy clode blocks. Here's an example:

```groovy
# An example Groovy template

Let's count to 10:

<%
(1..10).each { n ->
	out.println(n)
}
%>
```

Here's the output:

```
$ gtp testtemplate.gt
# An example Groovy template

Let's count to 10:

1
2
3
4
5
6
7
8
9
10


$
```

Notice that `gtp` is a standalone template renderer that MkTechDocs uses to render `*.gt` files.

## Groovy classes

You might need standalone classes for your Groovy templates. To do this, create \*.groovy files in your documentation directory. MkTechDocs will automatically detect and compile these into \*.class files.

For example, MkTechDocs includes a class called `MarkdownUtils`, a utility class. Even though you wouldn't likely use it in a real project, the following demonstrates the concept.

test.md:

```
# This is a level-one header

## This is a level-two header
```

mytempl.gt:

```groovy
# Some heading

<%
import MarkdownUtils

def f = new File("./test.md")

out << MarkdownUtils.getMarkdownFileAndChangeHeader(f, 2)
%>
```

And here is the output:

```
[~/MkTechDocs/docs]$ gtp mytempl.gt
# Some heading

### This is a level-one header

#### This is a level-two header


[~/MkTechDocs/docs]$
```

Note how the heading levels were increased by two levels, which is exactly what the `getMarkdownFileAndChangeHeader` function does.

## `CLASSPATH`

MkTechDocs creates a `CLASSPATH` automatically in order to process templates. However, if you need to add jars or directories to your CLASSPATH outside of MkTechDocs, simply create an environment variable. Here is an example in Bash:

```bash
export CLASSPATH=/path/to/my.jar
```

Now, when MkTechDocs runs, it will build a `CLASSPATH` that includes any existing `CLASSPATH`.
