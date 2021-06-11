from pynblint.notebook import Notebook
from pynblint.repository import LocalRepository
from pathlib import Path
import pytest

if __name__ == '__main__':
    pytest.main()


@pytest.fixture(scope="module")
def notebooks():
    nb1 = Notebook(Path("../fixtures", "FullNotebook2.ipynb"))
    nb2 = Notebook(Path("../fixtures", "FullNotebookFullNotebookFullNotebook.ipynb"))
    nb3 = Notebook(Path("../fixtures", "acs,.-e+.ipynb"))
    nb4 = Notebook(Path("../fixtures", "Untitled.ipynb"))
    return {
        "FullNotebook2.ipynb": nb1,
        "FullNotebookFullNotebookFullNotebook.ipynb": nb2,
        "acs,.-e+.ipynb": nb3,
        "Untitled.ipynb": nb4
    }


@pytest.fixture(scope="module")
def repos():
    folder1 = LocalRepository(Path("../fixtures", "UntitledNoDuplicates"))
    folder2 = LocalRepository(Path("../fixtures", "DuplicatesNoUntitled"))
    return {
        "UntitledNoDuplicates": folder1,
        "DuplicatesNoUntitled": folder2
    }


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", 3),
    ("FullNotebookFullNotebookFullNotebook.ipynb", 15)
])
def test_count_cells(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["notebookStats"]["numberOfCells"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", 0),
    ("FullNotebookFullNotebookFullNotebook.ipynb", 5)
])
def test_count_md_cells(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["notebookStats"][
               "numberOfMDCells"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("acs,.-e+.ipynb", 0),
    ("FullNotebookFullNotebookFullNotebook.ipynb", 9)
])
def test_count_code_cells(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["notebookStats"][
               "numberOfCodeCells"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", 0),
    ("FullNotebookFullNotebookFullNotebook.ipynb", 1)
])
def test_count_raw_cells(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["notebookStats"][
               "numberOfRawCells"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", False),
    ("FullNotebookFullNotebookFullNotebook.ipynb", True)
])
def test_has_linear_execution_order(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "linearExecutionOrder"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", 1),
    ("FullNotebookFullNotebookFullNotebook.ipynb", 0)
])
def test_count_class_defs(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "numberOfClassDefinitions"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", 0),
    ("FullNotebookFullNotebookFullNotebook.ipynb", 1)
])
def test_count_func_defs(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "numberOfFunctionDefinitions"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", False),
    ("FullNotebookFullNotebookFullNotebook.ipynb", True)
])
def test_are_imports_in_first_cell(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "allImportsInFirstCell"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", 0),
    ("FullNotebookFullNotebookFullNotebook.ipynb", 8)
])
def test_count_md_lines(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "numberOfMarkdownLines"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", 0),
    ("FullNotebookFullNotebookFullNotebook.ipynb", 1)
])
def test_count_md_titles(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "numberOfMarkdownTitles"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", None),
    ("FullNotebookFullNotebookFullNotebook.ipynb", 0.375)
])
def test_get_bottom_md_lines_ratio(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "bottomMarkdownLinesRatio"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", 0),
    ("Untitled.ipynb", 2)
])
def test_count_non_executed_cells(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "nonExecutedCells"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", 0),
    ("Untitled.ipynb", 1)
])
def test_count_empty_cells(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "emptyCells"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", None),
    ("Untitled.ipynb", 1)
])
def test_count_bottom_non_executed_cells(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "bottomNonExecutedCells"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", None),
    ("Untitled.ipynb", 1)
])
def test_count_bottom_empty_cells(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "bottomEmptyCells"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", False),
    ("Untitled.ipynb", True)
])
def test_is_untitled(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "isUntitled"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebook2.ipynb", False),
    ("Untitled.ipynb", True)
])
def test_is_filename_charset_restricted(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
        "isFilenameCharsetRestricted"]


@pytest.mark.parametrize("test_input,expected", [
    ("FullNotebookFullNotebookFullNotebook.ipynb", False),
    ("Untitled.ipynb", True)
])
def test_is_filename_short(test_input, expected, notebooks):
    assert notebooks[test_input].get_pynblint_results()["lintingResults"][
               "isFilenameShort"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("UntitledNoDuplicates", []),
    ("DuplicatesNoUntitled", [Path("../fixtures", "DuplicatesNoUntitled", "Test.ipynb"),
                              Path("../fixtures", "DuplicatesNoUntitled", "prova", "Test.ipynb")])
])
def test_get_duplicate_notebooks(test_input, expected, repos):
    assert repos[test_input].get_repo_results()["lintingResults"][
               "duplicateFilenames"] == expected


@pytest.mark.parametrize("test_input,expected", [
    ("DuplicatesNoUntitled", []),
    ("UntitledNoDuplicates", [Path("../fixtures", "UntitledNoDuplicates", "Untitled.ipynb")])
])
def test_get_untitled_notebooks(test_input, expected, repos):
    assert repos[test_input].get_repo_results()["lintingResults"][
               "untitledNotebooks"] == expected
