from pathlib import Path

import pytest

from pynblint import nb_linting, repo_linting
from pynblint.core_models import LocalRepository, Notebook

if __name__ == "__main__":
    pytest.main()


@pytest.fixture(scope="module")
def notebooks():
    nb1 = Notebook(Path("tests/fixtures", "FullNotebook2.ipynb"))
    nb2 = Notebook(Path("tests/fixtures", "FullNotebookFullNotebookFullNotebook.ipynb"))
    nb3 = Notebook(Path("tests/fixtures", "acs,.-e+.ipynb"))
    nb4 = Notebook(Path("tests/fixtures", "Untitled.ipynb"))
    return {
        "FullNotebook2.ipynb": nb1,
        "FullNotebookFullNotebookFullNotebook.ipynb": nb2,
        "acs,.-e+.ipynb": nb3,
        "Untitled.ipynb": nb4,
    }


@pytest.fixture(scope="module")
def repos():
    folder1 = LocalRepository(
        Path("tests/fixtures", "test_repo", "UntitledNoDuplicates")
    )
    folder2 = LocalRepository(
        Path("tests/fixtures", "test_repo", "DuplicatesNoUntitled")
    )
    return {"UntitledNoDuplicates": folder1, "DuplicatesNoUntitled": folder2}


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("FullNotebook2.ipynb", None),
        ("FullNotebookFullNotebookFullNotebook.ipynb", 0.375),
    ],
)
def test_get_bottom_md_lines_ratio(test_input, expected, notebooks):
    assert nb_linting.get_bottom_md_lines_ratio(notebooks[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected", [("FullNotebook2.ipynb", None), ("Untitled.ipynb", 1)]
)
def test_count_bottom_non_executed_cells(test_input, expected, notebooks):
    assert nb_linting.count_bottom_non_executed_cells(notebooks[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected", [("FullNotebook2.ipynb", None), ("Untitled.ipynb", 1)]
)
def test_count_bottom_empty_cells(test_input, expected, notebooks):
    assert nb_linting.count_bottom_empty_cells(notebooks[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("UntitledNoDuplicates", []),
        (
            "DuplicatesNoUntitled",
            [
                Path(
                    "tests/fixtures", "test_repo", "DuplicatesNoUntitled", "Test.ipynb"
                ),
                Path(
                    "tests/fixtures",
                    "test_repo",
                    "DuplicatesNoUntitled",
                    "prova",
                    "Test.ipynb",
                ),
            ],
        ),
    ],
)
def test_get_duplicate_notebooks(test_input, expected, repos):
    assert repo_linting.get_duplicate_notebooks(repos[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("DuplicatesNoUntitled", []),
        (
            "UntitledNoDuplicates",
            [
                Path(
                    "tests/fixtures",
                    "test_repo",
                    "UntitledNoDuplicates",
                    "Untitled.ipynb",
                )
            ],
        ),
    ],
)
def test_get_untitled_notebooks(test_input, expected, repos):
    assert repo_linting.get_untitled_notebooks(repos[test_input]) == expected


@pytest.mark.parametrize("test_input,expected", [("UntitledNoDuplicates", False)])
def test_is_versioned(test_input, expected, repos):
    assert repos[test_input].versioned == expected
