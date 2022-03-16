![Logo](https://user-images.githubusercontent.com/13979989/158653487-149633b8-ba85-4a11-976a-70eabc7d0df0.svg)

<div align="center">

[![PyPI version](https://badge.fury.io/py/pynblint.svg)](https://badge.fury.io/py/pynblint)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pynblint)

[![CI](https://github.com/collab-uniba/pynblint/actions/workflows/CI.yml/badge.svg)](https://github.com/collab-uniba/pynblint/actions/workflows/CI.yml)
[![Documentation Status](https://readthedocs.org/projects/pynblint/badge/?version=latest)](https://pynblint.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/collab-uniba/pynblint/branch/master/graph/badge.svg?token=CSX10BJ1CU)](https://codecov.io/gh/collab-uniba/pynblint)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

Many professional data scientists use Jupyter Notebook to accomplish their daily tasks, from preliminary data exploration to model prototyping. Notebooks' interactivity is particularly convenient for data-centric programming and their self-documenting nature provides excellent support for the communication of analytical results.

Nevertheless, Jupyter Notebook has been often criticized for inducing bad programming habits and scarcely supporting Software Engineering best practices. To really benefit from notebooks, users should be aware of their common pitfalls and learn how to prevent them.

In previous work (see ["Eliciting Best Practices for Collaboration with Computational Notebooks"](https://arxiv.org/abs/2202.07233) [\[1\]](#references)), we introduced a catalog of 17 empirically-validated guidelines for the collaborative use of notebooks in a professional context.

To foster the adoption of these best practices, we have created Pynblint, a static analysis tool for Jupyter notebooks written in Python. Pynblint reveals potential notebook defects and recommends corrective actions. It can be operated either as a standalone CLI application or as part of a CI/CD pipeline.

![Pynblint screens](https://user-images.githubusercontent.com/13979989/158661765-7a71e646-cde7-4e69-957d-a8f3af440101.svg)

The core linting rules of Pynblint have been derived as operationalizations of the best practices from our catalog. Nonetheless, the plug-in architecture of Pynblint enables its users to easily extend the core set of checks with their own linting rules.

## Requirements

Python 3.7+.

## Installation

Pynblint can be installed with `pip` or another PyPI package manager:

```bash
pip install pynblint
```

After installation, we recommend exploring the command-line interface of the tool:

```bash
pynblint --help
```

<!-- To use Pynblint, clone this repository and install it with [Poetry](https://python-poetry.org):

```bash
poetry install --no-dev
```

To install Pynblint for development purposes, simply omit the `--no-dev` option:

```bash
poetry install
``` -->

## Usage

Pynblint can be used to analyze:

- a standalone notebook:

    ```bash
    pynblint path/to/the/notebook.ipynb
    ```

- a code repository containing notebooks:

    ```bash
    pynblint path/to/the/project/dir/
    ```

  - (possibly also compressed as a `.zip` archive):

      ```bash
      pynblint path/to/the/compressed/archive.zip
      ```

- a _public_ GitHub repository containing notebooks
  (support for private repositories is on our roadmap 🙂):

    ```bash
    pynblint --from-github https://github.com/collab-uniba/pynblint
    ```

For further information on the available options, please refer to the project [documentation](https://pynblint.readthedocs.io/en/latest/?badge=latest).

## Catalog of best practices

In the following, we report the catalog of empirically-validated best practices on which Pynblint is based [\[1\]](#references).

For each guideline, we specify the current state of implementation within Pynblint:

- :white_check_mark: = "implemented"
- :hourglass_flowing_sand: = "partially implemented / work in progress"
- :x: = "not on our roadmap"

| State                    | Best Practice from [\[1\]](#references)                  |
| ------------------------ | -------------------------------------------------------- |
| :white_check_mark:       | Use version control                                      |
| :white_check_mark:       | Manage project dependencies                              |
| :hourglass_flowing_sand: | Use self-contained environments                          |
| :white_check_mark:       | Put imports at the beginning                             |
| :white_check_mark:       | Ensure re-executability (re-run notebooks top to bottom) |
| :hourglass_flowing_sand: | Modularize your code                                     |
| :hourglass_flowing_sand: | Test your code                                           |
| :white_check_mark:       | Name your notebooks consistently                         |
| :hourglass_flowing_sand: | Stick to coding standards                                |
| :hourglass_flowing_sand: | Use relative paths                                       |
| :white_check_mark:       | Document your analysis                                   |
| :white_check_mark:       | Leverage Markdown headings to structure your notebook    |
| :white_check_mark:       | Keep your notebook clean                                 |
| :white_check_mark:       | Keep your notebook concise                               |
| :x:                      | Distinguish production and development artifacts         |
| :hourglass_flowing_sand: | Make your notebooks available                            |
| :white_check_mark:       | Make your data available                                 |

## License

This project is licensed under the terms of the MIT license.

## References

[1] Luigi Quaranta, Fabio Calefato, and Filippo Lanubile. 2022. [Eliciting Best Practices for Collaboration with Computational Notebooks.](https://arxiv.org/abs/2202.07233) _Proc. ACM Hum.-Comput. Interact. 6_, CSCW1, Article 87 (April 2022), 41 pages. <https://doi.org/10.1145/3512934>
