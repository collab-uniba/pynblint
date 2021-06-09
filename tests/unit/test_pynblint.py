from pynblint.notebook import Notebook
from pathlib import Path

if __name__ == '__main__':

    @pytest.fixture(scope="module")
    def notebooks():
        nb1 = Notebook(Path(config.target_path) / "stroke-prediction-beginner-s-guide.ipynb")
        nb2 = Notebook(Path(config.target_path) / "my-attempt-at-analytics-vidhya-job-a-thon.ipynb")
        nb3 = Notebook(Path(config.target_path) / "Untitled.ipynb")
        return {
            "stroke-prediction-beginner-s-guide.ipynb": nb1,
            "my-attempt-at-analytics-vidhya-job-a-thon.ipynb": nb2,
            "Untitled.ipynb": nb3
        }


    @pytest.mark.parametrize("test_input,expected", [
        ("stroke-prediction-beginner-s-guide.ipynb", 32),
        ("Untitled.ipynb", 2)
    ])
    def test_count_cells(test_input, expected, notebooks):
        assert notebooks[test_input].get_pynblint_results()["notebookStats"]["numberOfCells"] == expected


    def test_count_md_cells(notebooks):
        assert notebooks["stroke-prediction-beginner-s-guide.ipynb"].get_pynblint_results()["notebookStats"][
                   "numberOfMDCells"] == 13


    def test_count_code_cells(notebooks):
        assert notebooks["stroke-prediction-beginner-s-guide.ipynb"].get_pynblint_results()["notebookStats"][
                   "numberOfCodeCells"] == 19


    def test_count_raw_cells(notebooks):
        assert notebooks["stroke-prediction-beginner-s-guide.ipynb"].get_pynblint_results()["notebookStats"][
                   "numberOfRawCells"] == 0


    def test_has_linear_execution_order(notebooks):
        assert notebooks["stroke-prediction-beginner-s-guide.ipynb"].get_pynblint_results()["lintingResults"][
                   "linearExecutionOrder"] == True


    def test_count_class_defs(notebooks):
        assert notebooks["stroke-prediction-beginner-s-guide.ipynb"].get_pynblint_results()["lintingResults"][
                   "numberOfClassDefinitions"] == 0


    def test_count_func_defs(notebooks):
        assert notebooks["stroke-prediction-beginner-s-guide.ipynb"].get_pynblint_results()["lintingResults"][
                   "numberOfFunctionDefinitions"] == 1


    def test_are_imports_in_first_cell(notebooks):
        assert notebooks["stroke-prediction-beginner-s-guide.ipynb"].get_pynblint_results()["lintingResults"][
                   "allImportsInFirstCell"] == False


    def test_count_md_lines(notebooks):
        assert notebooks["my-attempt-at-analytics-vidhya-job-a-thon.ipynb"].get_pynblint_results()["lintingResults"][
                   "numberOfMarkdownLines"] == 7


    def test_count_md_titles(notebooks):
        assert notebooks["my-attempt-at-analytics-vidhya-job-a-thon.ipynb"].get_pynblint_results()["lintingResults"][
                   "numberOfMarkdownTitles"] == 2


    def test_get_bottom_md_lines_ratio(notebooks):
        assert notebooks["my-attempt-at-analytics-vidhya-job-a-thon.ipynb"].get_pynblint_results()["lintingResults"][
                   "bottomMarkdownLinesRatio"] == 0


    def test_count_non_executed_cells(notebooks):
        assert notebooks["my-attempt-at-analytics-vidhya-job-a-thon.ipynb"].get_pynblint_results()["lintingResults"][
                   "nonExecutedCells"] == 0


    def test_count_empty_cells(notebooks):
        assert notebooks["my-attempt-at-analytics-vidhya-job-a-thon.ipynb"].get_pynblint_results()["lintingResults"][
                   "emptyCells"] == 3


    def test_count_bottom_non_executed_cells(notebooks):
        assert notebooks["my-attempt-at-analytics-vidhya-job-a-thon.ipynb"].get_pynblint_results()["lintingResults"][
                   "bottomNonExecutedCells"] == 0


    def test_count_bottom_empty_cells(notebooks):
        assert notebooks["my-attempt-at-analytics-vidhya-job-a-thon.ipynb"].get_pynblint_results()["lintingResults"][
                   "bottomEmptyCells"] == 2
