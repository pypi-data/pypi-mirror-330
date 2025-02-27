
# Usage - NavTree

```rst
..  toctree::
    :caption: Index
    :maxdepth: 1
    :titlesonly:
    :numbered:

    page1.md
    page2.md
    page3.md
```

## Directives

`.. toctree::` is a directive to build a toctree-cache and render toc in the page. The contents of sidebar navtree is generated from this toctree. It is advised to understand this directive.

**caption (Text)**

Sets the title of the toctree. The title is printed above the toc (effective for both page and navtree). The title of nested toctree is ignored in the sidebar navigation. 

**numbered**

Add chapter numbers to each section.

**titlesonly**

For each subdocuments, only the top level header is included in the toctree, and all subsections are ignored. 

Set this flag if you prefer simpler navtree. (No subsections listed, effective for both page and navtree). Do not set this flag if you want a complete list of headers.

The nested toctrees inside the subsections are still discovered and merged to the parent. 

**maxdepth (N)**

Limits the toctree depth printed in the page. This value is ignored in the navtree. Check theme variable `shiratama_navtree_maxdepth` for that purpose.

**hidden**

Hides this toctree from the page. This flag is ignored in the navtree.


**etc**

See [official documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree) for more. 


```{note}
Multiple toctrees are all included in the sidebar navtrees. However multiple toctree results in strage output when you use non-HTML output. 
```