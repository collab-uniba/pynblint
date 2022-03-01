import ast
from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel

from .lint import CellLevelLint, NotebookLevelLint, NotebookLint
from .lint_register import enabled_cell_level_lints, enabled_notebook_level_lints
from .notebook import Notebook


class NotebookLinterOptions(BaseModel):
    bottom_size: int = 4
    filename_max_length: Optional[int] = None


@dataclass
class NotebookMetadata:
    notebook_name: str


@dataclass
class NotebookStats:
    # Cells
    number_of_cells: int
    number_of_MD_cells: int
    number_of_code_cells: int
    number_of_raw_cells: int

    # Modularization
    number_of_functions: int
    number_of_classes: int


class NotebookLinter:
    def __init__(self, notebook: Notebook) -> None:
        self.notebook = notebook
        self.options: NotebookLinterOptions = NotebookLinterOptions()
        self.notebook_metadata: NotebookMetadata = NotebookMetadata(
            notebook_name=notebook.path.name
        )
        self.notebook_stats: NotebookStats = NotebookStats(
            number_of_cells=self.count_cells(),
            number_of_MD_cells=self.count_md_cells(),
            number_of_code_cells=self.count_code_cells(),
            number_of_raw_cells=self.count_raw_cells(),
            number_of_functions=self.count_func_defs(),
            number_of_classes=self.count_class_defs(),
        )

        self.lints: List[NotebookLint] = []

        self.lints.extend(
            [
                NotebookLevelLint(
                    lint.slug,
                    lint.description,
                    lint.recommendation,
                    lint.linting_function,
                    self.notebook,
                )
                for lint in enabled_notebook_level_lints
            ]
        )

        self.lints.extend(
            [
                CellLevelLint(
                    lint.slug,
                    lint.description,
                    lint.recommendation,
                    lint.linting_function,
                    self.notebook,
                )
                for lint in enabled_cell_level_lints
            ]
        )

        # self.results: Dict = {
        #     "lintingResults": {
        #         "linearExecutionOrder": has_linear_execution_order(notebook),
        #         "numberOfClassDefinitions": count_class_defs(notebook),
        #         "numberOfFunctionDefinitions": count_func_defs(notebook),
        #         "allImportsInFirstCell": are_imports_in_first_cell(notebook),
        #         "numberOfMarkdownLines": count_md_lines(notebook),
        #         "numberOfMarkdownTitles": count_md_titles(notebook),
        #         "bottomMarkdownLinesRatio": get_bottom_md_lines_ratio(
        #             notebook, self.options.bottom_size
        #         ),
        #         "nonExecutedCells": count_non_executed_cells(notebook),
        #         "emptyCells": count_empty_cells(notebook),
        #         "bottomNonExecutedCells": count_bottom_non_executed_cells(
        #             notebook, self.options.bottom_size
        #         ),
        #         "bottomEmptyCells": count_bottom_empty_cells(
        #             notebook, self.options.bottom_size
        #         ),
        #         "isTitled": is_titled(notebook),
        #         "isFilenameCharsetRestr": is_filename_charset_restricted(notebook),
        #     },
        # }
        # # if filename_max_length is not None:
        # #     results["lintingResults"]["isFilenameShort"] =
        # #                                                  is_filename_short(
        # #         self, filename_max_length
        # #     )

    # def get_linting_results(self):
    #     return self.results

    def count_cells(self) -> int:
        """Computes the total number of cells within a notebook."""

        nb_dict = self.notebook.nb_dict
        return len(nb_dict["cells"])

    def count_md_cells(self) -> int:
        """Computes the total number of Markdown cells within a notebook."""

        nb_dict = self.notebook.nb_dict
        counter = 0
        for cell in nb_dict["cells"]:
            if cell["cell_type"] == "markdown":
                counter = counter + 1
        return counter

    def count_code_cells(self) -> int:
        """Computes the total number of code cells within a notebook."""

        nb_dict = self.notebook.nb_dict
        counter = 0
        for cell in nb_dict["cells"]:
            if cell["cell_type"] == "code":
                counter = counter + 1
        return counter

    def count_raw_cells(self) -> int:
        """Computes the total number of raw cells within a notebook."""

        nb_dict = self.notebook.nb_dict
        counter = 0
        for cell in nb_dict["cells"]:
            if cell["cell_type"] == "raw":
                counter = counter + 1
        return counter

    def count_func_defs(self):
        """Computes the total number of function definitions within a notebook."""
        code = self.notebook.script
        tree = ast.parse(code)
        f_num = sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
        return f_num

    def count_class_defs(self):
        """Computes the total number of class definitions within a notebook."""
        code = self.notebook.script
        tree = ast.parse(code)
        class_def_num = sum(isinstance(exp, ast.ClassDef) for exp in tree.body)
        return class_def_num
