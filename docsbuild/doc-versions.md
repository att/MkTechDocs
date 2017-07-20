# Managing document versions

For some documentation projects, managing document versions is vital. It is helpful if you define your document version in one place, so that any sub-documents that reference the version number get it from the same place.

The following is one reasonable way of doing this.

## `global_vars`

Whether you're using Python or Groovy, it's probably a good idea to create a module (file) called `global_vars.py` to hold any static variables or functions you need to build your project, such as a version string. Here are the steps:

1. Add your project's directory to `PYTHONPATH`.
1. For any documents that need access to information stored in global\_vars, you simply convert the document into a template (by renaming it from `.md` to `.pyt`, for example).
1. `import global_vars` as a module in your renderer and include it in your variable dictionary.
1. Now, you can access global variables and functions in glob.py in your templates that have imported it: e.g. `version=global_vars.VERS`.

