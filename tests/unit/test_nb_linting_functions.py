from pathlib import Path
from typing import Dict, List

import pytest

from pynblint import nb_linting
from pynblint.cell import Cell
from pynblint.config import settings
from pynblint.notebook import Notebook


@pytest.fixture(scope="module")
def notebooks() -> Dict[str, Notebook]:
    nb1 = Notebook(Path("tests/fixtures", "FullNotebook2.ipynb"))
    nb2 = Notebook(Path("tests/fixtures", "FullNotebookFullNotebookFullNotebook.ipynb"))
    nb3 = Notebook(Path("tests/fixtures", "acs,.-e+.ipynb"))
    nb4 = Notebook(Path("tests/fixtures", "Untitled.ipynb"))
    nb5 = Notebook(Path("tests/fixtures", "notebook-Copy1.ipynb"))
    nb6 = Notebook(Path("tests/fixtures", "NotebookBackupCopy.ipynb"))
    return {
        "FullNotebook2.ipynb": nb1,
        "FullNotebookFullNotebookFullNotebook.ipynb": nb2,
        "acs,.-e+.ipynb": nb3,
        "Untitled.ipynb": nb4,
        "notebook-Copy1.ipynb": nb5,
        "NotebookBackupCopy.ipynb": nb6,
    }


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("FullNotebook2.ipynb", True),
        ("FullNotebookFullNotebookFullNotebook.ipynb", False),
    ],
)
def test_non_linear_execution(test_input, expected, notebooks):
    assert nb_linting.non_linear_execution(notebooks[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("FullNotebook2.ipynb", True),
        ("FullNotebookFullNotebookFullNotebook.ipynb", False),
    ],
)
def test_imports_beyond_first_cell(test_input, expected, notebooks):
    assert nb_linting.imports_beyond_first_cell(notebooks[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected", [("FullNotebook2.ipynb", 0), ("Untitled.ipynb", 2)]
)
def test_non_executed_cells(test_input, expected, notebooks):
    non_executed_cells_list: List[Cell] = nb_linting.non_executed_cells(
        notebooks[test_input]
    )
    assert len(non_executed_cells_list) == expected


@pytest.mark.parametrize(
    "test_input,expected", [("FullNotebook2.ipynb", 0), ("Untitled.ipynb", 1)]
)
def test_empty_cells(test_input, expected, notebooks):
    empty_cells_list: List[Cell] = nb_linting.empty_cells(notebooks[test_input])
    assert len(empty_cells_list) == expected


@pytest.mark.parametrize(
    "test_input,expected", [("FullNotebook2.ipynb", False), ("Untitled.ipynb", True)]
)
def test_untitled_notebook(test_input, expected, notebooks):
    assert nb_linting.untitled_notebook(notebooks[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected", [("acs,.-e+.ipynb", True), ("Untitled.ipynb", False)]
)
def test_notebook_named_with_unrestricted_charset(test_input, expected, notebooks):
    assert (
        nb_linting.notebook_named_with_unrestricted_charset(notebooks[test_input])
        == expected
    )


@pytest.mark.parametrize(
    "test_input,expected",
    [("FullNotebookFullNotebookFullNotebook.ipynb", True), ("Untitled.ipynb", False)],
)
def test_long_filename(test_input, expected, notebooks):
    settings.filename_max_length = 20
    assert nb_linting.long_filename(notebooks[test_input]) == expected
