# Document links

## Pandoc links

Pandoc automatically creates anchor names for every heading within your documents. Therefore, generating internal links is theoretically easy thanks to Pandoc's naming convention. For example, suppose you create the following header:

    # My New Header

Here's how you'd normally create a link to it using Pandoc naming conventions:

    Some markdown text that contains a [link](#my-new-header)

## MkTechDocs links

Because MkTechDocs can generate documents that require internal links that cross pages as well as documents that contain only internal relative links (as illustrated above), some thought has to be given to how links are created. When you generate internal links in your document, assume that your top-level included documents exist as HTML documents. For example, consider the following master document:

    ```{.include heading-level=0}
    introduction.md
    middle-section.md
    end.md
    ```

To create links to other parts of your document, point your links to headings in `introduction.html`, `middle-section.html`, and `end.html`. For example, suppose `introduction.md` contained:

```
# Some heading

Some text

# Some other heading

Some more interesting text.
```

To refer to a section in this file in another file:

```
# Middle section

Here is a [link](introduction.html#some-heading) that points to another file.
```

If you follow this convention, MkTechDocs will produce correct links for every available format.

