"""Linting functions for repositories containing notebooks"""

from typing import Dict, List

from pydantic import BaseModel

from pynblint import nb_linting
from pynblint.nb_linting import NotebookLinter
from pynblint.repository import Repository


class RepoLinterOptions(BaseModel):
    pass


class RepoLinter:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo
        self.options: RepoLinterOptions = RepoLinterOptions()

        self.results: Dict = {
            "repositoryName": repo.path.name,
            "lintingResults": {
                "duplicateFilenames": get_duplicate_notebooks(repo),
                "untitledNotebooks": get_untitled_notebooks(repo),
                "isVersioned": repo.versioned,
            },
            "notebookLintingResults": self._get_notebooks_results(),
        }

    def _get_notebooks_results(self) -> List[Dict]:
        """This function takes the list of notebook objects from the current repository
        and returns a list of dictionaries containing the related linting results."""
        data = []
        for notebook in self.repo.notebooks:
            nb_linter: NotebookLinter = NotebookLinter(notebook)
            data.append(nb_linter.get_linting_results())
        return data

    def get_linting_results(self):
        return self.results


def get_duplicate_notebooks(repo):
    """
    The function takes a repository and checks whether two or more notebooks
    with the same filename are present.

        Args:
            repo(Repository): python object representing the repository
        Returns:
            paths: list containing paths to notebooks with duplicate filenames

        A way you might use me is

        duplicate_nb_in_repo = get_duplicate_notebooks(repo)
    """
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
