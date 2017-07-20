# Useful Blocks

MkTechDocs contains built-in blocks that are useful when creating documentation.

## Comment

Comment blocks are ignored by MkTechDocs.

E.g.

    ```comment
    This text will be ignored.
    ```

## Include

The `include` block was introduced in the [basics](the-basics.html#master-document) section.

|Parameter|Description|
|----------------------|------------------------------------------------|
|heading-level         |Provides a hint to MkTechDocs about the current heading level. In order for MkTechDocs to produce nested headings, this parameter should always be used.|

E.g.

    # My header
    
    ```{.include heading-level=1}
    myinclude.md
    mysecondinclude.md
    ```

`include` blocks support infinte recursion, so included documents can contain included documents and so on.

## Include-code

The `include-code` block is used to include source-code files with syntax highlighting.

|Parameter|Description|
|----------------------|------------------------------------------------|
|language              |Optional parameter that tells MkTechDocs what language the source code is. If no language is provided, MkTechDocs will use the file's extension. E.g. file.c -> language=c|

E.g.

    ```{.include-code language=c}
    /home/mylogin/MkTechDocs/docs/file1.h
    /home/mylogin/MkTechDocs/docs/file1.c
    ```

Produces:

```{.include-code language=c}
../file1.h
../file1.c
```

```note
Paths are an issue here. Remember that MkTechDocs projects are built inside the `./build` directory relative to your project directory. Therefore, for files to be included correctly, a full path or a path relative to the build directory must be given.
```

## Note

`note` blocks are used to create documentation "notes" that appear highlighted in documentation text for HTML output formats. For PDF output, the content of the `note` block is prepended with "Note:".

E.g.

    ```note
    This text will appear inside its own highlighted block and be prepended with "Note:".
    ```

Produces:

```note
This text will appear inside its own highlighted block and be prepended with "Note:".
```

## Plantuml

`plantuml` blocks let you include [PlantUML](http://plantuml.com) diagramming UML directly in your documentation.

|Parameter|Description|
|----------------------|------------------------------------------------|
|title                 | The title of the diagram. Used for a caption that appears beneath the diagram.|

E.g.

    # My Diagram
    
    ```{.plantuml title="My Diagram"}
    A->B    
    ```

Produces:

```{.plantuml title="My Diagram"}
A->B    
```

## Tip

`tip` blocks are used to create documentation "tips" that appear highlighted in documentation text for HTML output formats. For PDF output, the content of the `tip` block is prepended with "Tip:".

E.g.

    ```tip
    This text will appear inside its own highlighted block and be prepended with "Tip:".
    ```

Produces:

```tip
This text will appear inside its own highlighted block and be prepended with "Tip:".
```
