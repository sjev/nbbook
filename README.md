# nb-book

Tools to write a book using Jupyter notebooks

## Why this toolset

I love writing in markdown and Jupyter notebooks, but managing material that spans multiple notebooks
can be a bit challenging sometimes.

This toolset helps a little by providing a way to generate

- Table of Contents notebook
- Cross-reference notebook

## How it works

### Table of contents
(or index notebook)
The tool can create an index notebook linking to all referenced notebooks. For an example
see `index.ipynb` in `example` folder.



### References
A reference is defined as

    [ref]: # (topic - description)

The tool wil scan for these and create a link to the *last header* before the reference tag.
An entry will be made in generated `_reference.ipynb` linking to the original notebook.
For an example see `reference.ipynb` in `example` folder





### Configuration
In the directory containing your notebooks, create a yaml config file, like this:

```
notebooks:
    - notebook_one.ipynb
    - notebook_two.ipynb

index:
    name : _index.ipynb
    indent: 2
    max_depth: 2

reference:
    name : _reference.ipynb
```

the `notebooks` section defines which notebooks will be indexed

### Running make script

create a build file like `make.py` in examples folder
run with

`python make.py index`  (or other command that you define)
