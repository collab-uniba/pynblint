"""Linting functions for repositories containing notebooks"""


from pathlib import Path
from typing import List

from . import lint_register as register
from . import nb_linting
from .lint import LintDefinition, LintLevel
from .repository import Repository


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


def get_untitled_notebooks(repo):
    """
    The function takes a repository and checks whether there is any untitled notebook

        Args:
            repo(Repository): python object representing the repository
        Returns:
            untitled_notebooks: list containing paths to untitled notebooks

        A way you might use me is

        untitled_nb_in_repo = get_untitled_notebooks(repo)
    """
    untitled_notebooks = []
    for notebook in repo.notebooks:
        if not nb_linting.is_titled(notebook):
            untitled_notebooks.append(notebook.path)
    return untitled_notebooks


project_level_lints: List[LintDefinition] = []

path_level_lints: List[LintDefinition] = [
    LintDefinition(
        slug="duplicate-notebook-filename",
        description="Two or more notebooks with the same filename exist in this \
            repository",
        recommendation="Use different filenames and possibly stick to a \
            naming confention to make notebooks easily identifiable.",
        linting_function=duplicate_notebook_filename,
    )
]


def initialize() -> None:
    register.register_lints(LintLevel.PROJECT, project_level_lints)
    register.register_lints(LintLevel.PATH, path_level_lints)
