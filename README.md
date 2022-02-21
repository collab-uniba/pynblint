# Pynblint

[![CI](https://github.com/collab-uniba/pynblint/actions/workflows/CI.yml/badge.svg)](https://github.com/collab-uniba/pynblint/actions/workflows/CI.yml)
[![Documentation Status](https://readthedocs.org/projects/pynblint/badge/?version=latest)](https://pynblint.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/collab-uniba/pynblint/branch/master/graph/badge.svg?token=CSX10BJ1CU)](https://codecov.io/gh/collab-uniba/pynblint)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Many professional data scientists use Jupyter Notebook to accomplish their daily tasks, from preliminary data exploration to model prototyping. Notebooks' interactivity is particularly convenient for data-centric programming; moreover, their self-documenting nature greatly simplifies and enhances the communication of analytical results.

However, Jupyter Notebook has often been criticized for offering scarce native support for Software Engineering best practices and inducing bad programming habits. To really benefit from computational notebooks, practitioners need to be aware of their common pitfalls and learn how to avoid them.

In our paper ["Eliciting Best Practices for Collaboration with Computational Notebooks" [1]](https://arxiv.org/abs/2202.07233), we introduced a catalog of validated best practices for the collaborative use of notebooks in professional contexts.

To raise awareness of these best practices and promote their adoption, we have created Pynblint, a static analysis tool for Jupyter notebooks written in Python. Pynblint can be operated as a standalone CLI application or as part of a CI/CD pipeline. It reveals potential defects of Jupyter notebooks found in software repositories and recommends corrective actions.

The core linting rules that power Pynblint have been derived as operationalizations of the validated best practices from our catalog. Nonetheless, the tool is designed to be easily customized and extended with new rules.


## Installation

To use Pynblint, clone this repository and install it with [Poetry](https://python-poetry.org):

```bash
poetry install --no-dev
```

To install Pynblint for development purposes, simply omit the `--no-dev` option:

```bash
poetry install
```

At present, we are finalizing the first version of Pynblint (v0.1.0).
When released, it will become available as a Python package on PyPI and installable via `pip`.


## Usage

Once installed, Pynblint can be used to analyze:

- a single notebook:

    ```bash
    pynblint path/to/the/notebook.ipynb
    ```
- the set of notebooks found in the current working directory:

    ```bash
    pynblint .
    ```

- the set of notebooks found in the directory located at the specified path:

    ```bash
    pynblint path/to/the/project/dir/
    ```

- the set of notebooks found in a compressed `.zip` archive:

    ```bash
    pynblint path/to/the/compressed/archive.zip
    ```

- the set of notebooks found in a _public_ GitHub repository (support for private repositories is on our roadmap 🙂):

    ```bash
    pynblint --from-github https://github.com/collab-uniba/pynblint
    ```

For further information on the available options, please read Pynblint's CLI manual:

```bash
pynblint --help
```

## References

Luigi Quaranta, Fabio Calefato, and Filippo Lanubile. 2022. [Eliciting Best Practices for Collaboration with Computational Notebooks.](https://arxiv.org/abs/2202.07233) *Proc. ACM Hum.-Comput. Interact.* 6, CSCW1, Article 87 (April 2022), 41 pages. <https://doi.org/10.1145/3512934>
