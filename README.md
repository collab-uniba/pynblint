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

Pynblint currently implements 22 linting rules based on empirically-validated best practices for collaborative Jupyter notebook usage:
- 17 rules applicable to standalone notebooks
- 5 rules applicable to entire data science repositories

These rules are derived from our comprehensive catalog of best practices collaborative notebook development [\[1\]](#references). Below is the current implementation state of linting rules associated with each best practice:

- :white_check_mark: Complete: Fully implemented
- :puzzle_piece: Partial: Partially implemented with planned improvements
- :hourglass_flowing_sand: In Progress: Implementation planned for future releases
- :x: Not Planned: No implementation planned

| Best Practice from [\[1\]](#references)                       | **Status**                            | Details                                                                                                                                                     |
| ------------------------------------------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. *Use version control*                                      | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
| 2. *Manage project dependencies*                              | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
| 3. *Use self-contained environments*                          | :hourglass_flowing_sand: In Progress: | *Planned*: detection of<br>- Python virtual environments (e.g., created with `venv`, `pyenv`, or `conda`)<br>- containerized environments (e.g., Docker).   |
| 4. *Put imports at the beginning*                             | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
| 5. *Ensure re-executability (re-run notebooks top to bottom)* | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
| 6. *Modularize your code*                                     | :puzzle_piece: Partial                | *Current*: detection of modularization constructs in notebooks.<br>*Planned*: modularization-focused refactoring recommendations based on detected patterns |
| 7. *Test your code*                                           | :puzzle_piece: Partial                | *Current*: repository-level detection of coverage data.<br>*Planned*: detection of test modules/functions independent of coverage tools                     |
| 8. *Name your notebooks consistently*                         | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
| 9. *Stick to coding standards*                                | :puzzle_piece: Partial                | *Current*: detection of cells with invalid Python syntax.<br>*Planned*: Integration of Python linters such as pylint, flake8, and ruff                      |
| 10. *Use relative paths*                                      | :hourglass_flowing_sand: In Progress: | *Planned*: identification of absolute paths instances in notebooks and recommendation of corresponding relative paths                                       |
| 11. *Document your analysis*                                  | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
| 12. *Leverage Markdown headings to structure your notebook*   | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
| 13. *Keep your notebook clean*                                | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
| 14. *Keep your notebook concise*                              | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
| 15. *Distinguish production and development artifacts*        | :x: Not Planned                       | Implementation deemed infeasible (see the note below)                                                                                                       |
| 16. *Make your notebooks available*                           | :hourglass_flowing_sand: In Progress: | *Planned*: Pynblint will ensure that notebooks marked as published in its configuration are available online                                                |
| 17. *Make your data available*                                | :white_check_mark: Complete           | Fully implemented                                                                                                                                           |
**Note**: Best practice #15 (Distinguishing Production/Development Artifacts) will not be implemented as there are no objective criteria for determining this distinction through static analysis of notebooks or repositories.

## License

This project is licensed under the terms of the MIT license.

## References

[1] Luigi Quaranta, Fabio Calefato, and Filippo Lanubile. 2022. [Eliciting Best Practices for Collaboration with Computational Notebooks.](https://arxiv.org/abs/2202.07233) _Proc. ACM Hum.-Comput. Interact. 6_, CSCW1, Article 87 (April 2022), 41 pages. <https://doi.org/10.1145/3512934>
