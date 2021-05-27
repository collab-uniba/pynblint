import pytest
import pynblint
import config
from entities import Notebook
from pathlib import Path


def test_count_cells():
    nb = Notebook(Path(config.target_path) / "stroke-prediction-beginner-s-guide.ipynb")
    assert nb.get_pynblint_results()["notebookStats"]["numberOfCells"] == 32

def test_count_md_cells():
    nb = Notebook(Path(config.target_path) / "stroke-prediction-beginner-s-guide.ipynb")
    assert nb.get_pynblint_results()["notebookStats"]["numberOfMDCells"] == 13

def test_count_code_cells():
    nb = Notebook(Path(config.target_path) / "stroke-prediction-beginner-s-guide.ipynb")
    assert nb.get_pynblint_results()["notebookStats"]["numberOfCodeCells"] == 19

def test_count_raw_cells():
    nb = Notebook(Path(config.target_path) / "stroke-prediction-beginner-s-guide.ipynb")
    assert nb.get_pynblint_results()["notebookStats"]["numberOfRawCells"] == 0

def test_has_linear_execution_order():
    nb = Notebook(Path(config.target_path) / "stroke-prediction-beginner-s-guide.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["linearExecutionOrder"] == True

def test_count_class_defs():
    nb = Notebook(Path(config.target_path) / "stroke-prediction-beginner-s-guide.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["numberOfClassDefinitions"] == 0

def test_count_func_defs():
    nb = Notebook(Path(config.target_path) / "stroke-prediction-beginner-s-guide.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["numberOfFunctionDefinitions"] == 1

def test_are_imports_in_first_cell():
    nb = Notebook(Path(config.target_path) / "stroke-prediction-beginner-s-guide.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["allImportsInFirstCell"] == False

def test_count_md_lines():
    nb = Notebook(Path(config.target_path) / "my-attempt-at-analytics-vidhya-job-a-thon.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["numberOfMarkdownLines"] == 7

def test_count_md_titles():
    nb = Notebook(Path(config.target_path) / "my-attempt-at-analytics-vidhya-job-a-thon.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["numberOfMarkdownTitles"] == 2

def test_get_bottom_md_lines_ratio():
    nb = Notebook(Path(config.target_path) / "my-attempt-at-analytics-vidhya-job-a-thon.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["bottomMarkdownLinesRatio"] == 0

def test_count_non_executed_cells():
    nb = Notebook(Path(config.target_path) / "my-attempt-at-analytics-vidhya-job-a-thon.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["nonExecutedCells"] == 0

def test_count_empty_cells():
    nb = Notebook(Path(config.target_path) / "my-attempt-at-analytics-vidhya-job-a-thon.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["emptyCells"] == 3

def test_count_bottom_non_executed_cells():
    nb = Notebook(Path(config.target_path) / "my-attempt-at-analytics-vidhya-job-a-thon.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["bottomNonExecutedCells"] == 0

def test_count_bottom_empty_cells():
    nb = Notebook(Path(config.target_path) / "my-attempt-at-analytics-vidhya-job-a-thon.ipynb")
    assert nb.get_pynblint_results()["lintingResults"]["bottomEmptyCells"] == 2