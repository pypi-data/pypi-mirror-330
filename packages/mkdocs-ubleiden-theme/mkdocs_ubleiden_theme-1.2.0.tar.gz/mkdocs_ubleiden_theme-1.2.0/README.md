# MkDocs UBL theme for documentation

MkDocs UBL is a theme for writing documentation using the Leiden University
Libraries style and colors.
MkDocs UBL template is based on [Material for MkDocs][1]; a theme for 
[MkDocs][2].
MkDocs is static site generator geared towards (technical) project
documentation.

[1]: https://squidfunk.github.io/mkdocs-material/
[2]: https://www.mkdocs.org

## Installation

The MkDocs UBL theme can be installed with `pip`:

First, make sure you have installed [Python v3.*][py] on your machine.
During the installation you will be asked if you also want to install 'pip'.
Do so, and then run the following command to install all the dependencies to
run MkDocs with the theme on your machine:

[py]: https://www.python.org/downloads/

```shell
pip install mkdocs-ubleiden-theme
```

This will automatically install compatible versions of all dependencies:
[MkDocs][2], [Material for MkDocs][1], [Markdown][5], [Pygments][6] and
[Python Markdown Extensions][7].
There's no need to install these packages separately.

[5]: https://python-markdown.github.io/
[6]: https://pygments.org/
[7]: https://facelessuser.github.io/pymdown-extensions/

## Using this theme in your project

Following the [Styling your docs guide][style], set the theme to `ubleiden` in
your `mkdocs.yml` configuration file:

```yml
theme: ubleiden
```

or:

```yml
theme:
  name: ubleiden
```

## Generating the documentation

If you have installed Python 3.* and MkDocs, you can use the command
`mkdocs serve`, or `python -m mkdocs serve` in your terminal to serve the
documentation on your development computer.
For example:

```console
C:\Users\username\Documents\my-cool-application> python -m mkdocs serve
```

When you are ready to generate the final documentation files, run
`mkdocs build` to create a static version locally, or `mkdocs gh-deploy` to
build and push the docs to a special branch in your remote git repository.

For more information about generating and publishing the documentation, see
[Deploying your Docs](https://www.mkdocs.org/user-guide/deploying-your-docs/).
