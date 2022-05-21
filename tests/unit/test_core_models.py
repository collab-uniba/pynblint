from pathlib import Path

import pytest

from pynblint.core_models import LocalRepository, Notebook

if __name__ == "__main__":
    pytest.main()


def test_standalone_notebook_constructor():
    """Tests the contruction of a standalone ``Notebook`` object."""

    notebook_path: Path = Path("tests", "fixtures", "FullNotebook2.ipynb")
    notebook: Notebook = Notebook(notebook_path)

    assert notebook.repository is None


def test_notebook_from_repo_constructor():
    """Tests the construction of a ``Notebook`` object extracted from a repository."""

    repo_path: Path = Path("tests", "fixtures", "test_repo", "UntitledNoDuplicates")
    repository: LocalRepository = LocalRepository(repo_path)
    notebook: Notebook = repository.notebooks[0]

    assert notebook.repository is not None
    assert notebook.repository.path == repo_path
