---
umlformat: svg
---

Test dependency installation and basic code integrity
=====================================================

recursive includes
------------------

Include test file
-----------------

This text is coming from inside test\_install\_include.md.

Include test file 2
===================

This text is coming from inside test\_install\_include2.md.

include code
------------

``` {.c}
#include <stdio.h>
#include "file1.h"

int main(int argc, char **argv)
{
	printf("Size of SOMETHING is: %lu\n", sizeof(SOMETHING));
	return 0;
}
```

notes and tips
--------------

<p class="note"><b>Note</b>: Note test</p>

<p class="tip"><b>Tip</b>: Tip test</p>

plantuml
--------

![](plantuml-c6117aebb4ce8e59ba2b46950eca869f.svg)

python template
---------------

hello, test
