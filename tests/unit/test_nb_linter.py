from pathlib import Path
from typing import Dict

import pytest

from pynblint.core_models import Notebook
from pynblint.nb_linter import NotebookLinter

if __name__ == "__main__":
    pytest.main()


@pytest.fixture(scope="module")
def nb_linters() -> Dict[str, NotebookLinter]:
    nb1 = Notebook(Path("tests", "fixtures", "FullNotebook2.ipynb"))
    nb2 = Notebook(
        Path("tests", "fixtures", "FullNotebookFullNotebookFullNotebook.ipynb")
    )
    nb3 = Notebook(Path("tests", "fixtures", "acs,.-e+.ipynb"))
    nb4 = Notebook(Path("tests", "fixtures", "Untitled.ipynb"))
    return {
        "FullNotebook2.ipynb": NotebookLinter(nb1),
        "FullNotebookFullNotebookFullNotebook.ipynb": NotebookLinter(nb2),
        "acs,.-e+.ipynb": NotebookLinter(nb3),
        "Untitled.ipynb": NotebookLinter(nb4),
    }


@pytest.mark.parametrize(
    "test_input,expected",
    [("FullNotebook2.ipynb", 3), ("FullNotebookFullNotebookFullNotebook.ipynb", 15)],
)
def test_count_cells(test_input, expected, nb_linters):
    nb_linter: NotebookLinter = nb_linters[test_input]
    assert nb_linter.count_cells() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("FullNotebook2.ipynb", 0), ("FullNotebookFullNotebookFullNotebook.ipynb", 5)],
)
def test_count_md_cells(test_input, expected, nb_linters):
    nb_linter: NotebookLinter = nb_linters[test_input]
    assert nb_linter.count_md_cells() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("acs,.-e+.ipynb", 0), ("FullNotebookFullNotebookFullNotebook.ipynb", 9)],
)
def test_count_code_cells(test_input, expected, nb_linters):
    nb_linter: NotebookLinter = nb_linters[test_input]
    assert nb_linter.count_code_cells() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("FullNotebook2.ipynb", 0), ("FullNotebookFullNotebookFullNotebook.ipynb", 1)],
)
def test_count_raw_cells(test_input, expected, nb_linters):
    nb_linter: NotebookLinter = nb_linters[test_input]
    assert nb_linter.count_raw_cells() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("FullNotebook2.ipynb", 1), ("FullNotebookFullNotebookFullNotebook.ipynb", 0)],
)
def test_count_class_defs(test_input, expected, nb_linters):
    nb_linter: NotebookLinter = nb_linters[test_input]
    assert nb_linter.count_class_defs() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("FullNotebook2.ipynb", 0), ("FullNotebookFullNotebookFullNotebook.ipynb", 1)],
)
def test_count_func_defs(test_input, expected, nb_linters):
    nb_linter: NotebookLinter = nb_linters[test_input]
    assert nb_linter.count_func_defs() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("FullNotebook2.ipynb", 0), ("FullNotebookFullNotebookFullNotebook.ipynb", 8)],
)
def test_count_md_lines(test_input, expected, nb_linters):
    nb_linter: NotebookLinter = nb_linters[test_input]
    assert nb_linter.count_md_lines() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("FullNotebook2.ipynb", 0), ("FullNotebookFullNotebookFullNotebook.ipynb", 1)],
)
def test_count_md_titles(test_input, expected, nb_linters):
    nb_linter: NotebookLinter = nb_linters[test_input]
    assert nb_linter.count_md_titles() == expected
