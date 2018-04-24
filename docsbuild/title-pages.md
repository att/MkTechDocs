# Title pages

There are three ways to create a title page for your `pdf` or `pdffloat` document. In all three cases, you must create a standalone file and assign that filename to the `TITLE_PAGE` variable in your project's configuration.

## Title metadata block

    % My Document Title
    % John Doe; Jane Doe
    % January 1, 2000

For more information about this syntax: `man pandoc` and search for "Metadata block."

## YAML metadata block

    ---
    title: My Document Title
    author:
      - John Doe
      - Jane Doe
    date: January 1, 2001
    ---

## Templates

If your title page requires dynamic content (e.g. non-static date, version number) you can create a Python template to output information as in the above two exmaples. Follow along with the example in [Python templates](templates.html#python-templates) section.


