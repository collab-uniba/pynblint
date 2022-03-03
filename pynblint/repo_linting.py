"""Linting functions for repositories containing notebooks"""


from pathlib import Path
from typing import List

from . import lint_register as register
from .lint import LintDefinition, LintLevel
from .repository import Repository

# ============= #
# PROJECT LEVEL #
# ============= #


def repository_not_versioned(repo: Repository) -> bool:
    """Check the absence of the ``.git`` folder."""

    return not repo.is_git_repository


def dependencies_unmanaged(repo: Repository) -> bool:
    """Check the absence of configuration files for dependency management tools.

    All configuration files are searched in the root of the repository.
    """

    paths = [
        repo.path / "requirements.txt",
        repo.path / "pyproject.toml",
        repo.path / "environment.yml",
        repo.path / "setup.py",
        repo.path / "Pipfile",
    ]

    return not any(map(lambda x: x.exists(), paths))


# ========== #
# PATH LEVEL #
# ========== #


def duplicate_notebook_filename(repo: Repository) -> List[Path]:
    """Check the existence of notebooks with the same filename within a repository"""

    nb_filenames = []
    duplicate_filanames = []
    paths = []
    for notebook in repo.notebooks:
        filename = notebook.path.name
        if filename in nb_filenames:
            duplicate_filanames.append(filename)
        else:
            nb_filenames.append(filename)
    for filename in duplicate_filanames:
        for notebook in repo.notebooks:
            if notebook.path.name == filename:
                paths.append(notebook.path)
    return paths


# ================= #
# LINT REGISTRATION #
# ================= #


project_level_lints: List[LintDefinition] = [
    LintDefinition(
        slug="repository-not-versioned",
        description="This repository is not version controlled.",
        recommendation="Put the repository under version control using a VCS like git.",
        linting_function=repository_not_versioned,
    ),
    LintDefinition(
        slug="dependencies-unmanaged",
        description="No dependency-management tools appear to be used in this project.",
        recommendation="If you are using `pip`, declare your dependencies in a "
        "`requirements.txt` file. You can do so by running the following command: "
        "`pip freeze > requirements.txt`.",
        linting_function=dependencies_unmanaged,
    ),
]

path_level_lints: List[LintDefinition] = [
    LintDefinition(
        slug="duplicate-notebook-filename",
        description="Two or more notebooks with the same filename exist in this "
        "repository.",
        recommendation="Use different filenames to make notebooks easy to recognize; "
        "possibly stick to a naming convention.",
        linting_function=duplicate_notebook_filename,
    )
]


def initialize() -> None:
    register.register_lints(LintLevel.PROJECT, project_level_lints)
    register.register_lints(LintLevel.PATH, path_level_lints)
