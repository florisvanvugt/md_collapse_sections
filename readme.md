# MD-collapse-sections

A cheap-and-cheerful way to turn markdown documents into HTML documents with collapsable section headers. I didn't find a satisfactory solution elsewhere so I coded this up in Python. It works under Python 3 and you need markdown (`pip install markdown`).

I hope this will be of use to others too!


## Usage

```python md_collapse_sections.py infile.md outfile.html```

where

* `infile.md` is the input file name (a normal Markdown document)
* `outfile.html` is the file that the output HTML will be written to


## Requirements

* Markdown



## Details

To get collapsable sections in HTML this function uses the `<details>`/`<summary>` tag structure, e.g.

```
<details>
<summary>Summary: click here to see the details</summary>
These are the details that are hidden by default.
</details>
```

From what I gather the cross-browser support for this is reasonably good. I chose to use this because it is a pure HTML solution not requiring Javascript.

Also, note that the headers are no longer coded as header tags (e.g. `<h1>`, `<h2>`, `<h3>` etc.) but as `<span>` tags. This is because if I used the header tags then the header appears on a separate line after the triangle used to collapse the section.

