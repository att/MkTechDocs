# Running filters

Running MkTechDocs Pandoc filters outside of the normal build environment is easy if you've [set up your environment](#setting-up-your-environment) properly:

```bash
pandoc --filter <flt-filtername.py> -f markdown -t some-other-format inputfile.md >outputfile.fmt
```

In some cases, MkTechDocs filters produce artifacts on STDERR. In these cases use something like the following:

```bash
pandoc --filter <flt-filtername.py> -f markdown -t some-other-format inputfile.md >outputfile.fmt 2>artifacts.out
```

The following Pandoc python filters come with MkTechDocs. Groovy versions are available as well in `$MKTECHDOCSHOME/bin/groovy`. They are run in the same way (but have a .groovy extension).

{% for d in docs %}
## `{{ d.file }}`

{{ d.doc }}

{% endfor %}
