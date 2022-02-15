import json
from enum import Enum, auto
from pathlib import Path
from typing import Dict

import nbformat
import rich
from nbconvert import PythonExporter
from rich.abc import RichRenderable
from rich.columns import Columns
from rich.console import Console, ConsoleOptions, RenderResult
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax

from pynblint import nb_linting

from .rich_extensions import NotebookMarkdown


class Notebook(RichRenderable):
    """
    This class stores the representations of a notebook
    on which pynblint functions are called
    """

    def __init__(
        self,
        notebook_path: Path,
        repository_path: Path = None,
        notebook_name: str = None,
    ):
        self.path = notebook_path
        self.repository_path = repository_path
        self.notebook_name = notebook_name

        # Read the raw notebook file
        with open(self.path) as f:
            _nb_raw = f.read()

        # Convert the notebook to a Python dictionary
        self.nb_dict = json.loads(_nb_raw)

        # Convert the notebook to a Python script
        _nb_node = nbformat.reads(_nb_raw, as_version=self.nb_dict["nbformat"])
        python_exporter = PythonExporter()
        self.script, _ = python_exporter.from_notebook_node(_nb_node)

    def get_pynblint_results(self, bottom_size: int = 4, filename_max_length=None):

        if self.notebook_name is not None:
            nb_name = self.notebook_name
        elif self.repository_path is not None:
            nb_name = str(self.path.relative_to(self.repository_path))
        else:
            nb_name = str(self.path)

        results: Dict = {
            "notebookName": nb_name,
            "notebookStats": {
                "numberOfCells": nb_linting.count_cells(self),
                "numberOfMDCells": nb_linting.count_md_cells(self),
                "numberOfCodeCells": nb_linting.count_code_cells(self),
                "numberOfRawCells": nb_linting.count_raw_cells(self),
            },
            "lintingResults": {
                "linearExecutionOrder": nb_linting.has_linear_execution_order(self),
                "numberOfClassDefinitions": nb_linting.count_class_defs(self),
                "numberOfFunctionDefinitions": nb_linting.count_func_defs(self),
                "allImportsInFirstCell": nb_linting.are_imports_in_first_cell(self),
                "numberOfMarkdownLines": nb_linting.count_md_lines(self),
                "numberOfMarkdownTitles": nb_linting.count_md_titles(self),
                "bottomMarkdownLinesRatio": nb_linting.get_bottom_md_lines_ratio(
                    self, bottom_size
                ),
                "nonExecutedCells": nb_linting.count_non_executed_cells(self),
                "emptyCells": nb_linting.count_empty_cells(self),
                "bottomNonExecutedCells": nb_linting.count_bottom_non_executed_cells(
                    self, bottom_size
                ),
                "bottomEmptyCells": nb_linting.count_bottom_empty_cells(
                    self, bottom_size
                ),
                "isTitled": nb_linting.is_titled(self),
                "isFilenameCharsetRestr": nb_linting.is_filename_charset_restricted(
                    self
                ),
            },
        }
        # if filename_max_length is not None:
        #     results["lintingResults"]["isFilenameShort"] =
        #                                                  nb_linting.is_filename_short(
        #         self, filename_max_length
        #     )
        return results

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        return [Cell(cell) for cell in self.nb_dict["cells"]]


class CellType(Enum):
    MARKDOWN = auto()
    CODE = auto()
    RAW = auto()
    OTHER = auto()


class Cell(RichRenderable):
    def __init__(self, cell_dict: Dict) -> None:
        """Pynblint's representation of a notebook cell."""

        self._cell_dict = cell_dict

        # Cell type
        if self._cell_dict["cell_type"] == "markdown":
            self.cell_type = CellType.MARKDOWN
        elif self._cell_dict["cell_type"] == "code":
            self.cell_type = CellType.CODE
        elif self._cell_dict["cell_type"] == "raw":
            self.cell_type = CellType.RAW
        else:
            self.cell_type = CellType.OTHER

        # Cell source
        self.cell_source: str = "".join(self._cell_dict["source"])

        # Execution count
        if self.cell_type == CellType.CODE:
            self.cell_exec_count: int = self._cell_dict["execution_count"]

    def __rich__(self) -> Columns:

        if self.cell_type == CellType.CODE:
            rendered_cell = Columns(
                [
                    f"\nIn [{self.cell_exec_count}]:",
                    Panel(
                        Syntax(self.cell_source, "python"),
                        width=int(rich.get_console().size[0] * 0.90),
                    ),
                ]
            )
        else:
            rendered_cell = Columns(
                [
                    "        ",
                    Padding(NotebookMarkdown(self.cell_source), (1, 0, 1, 8)),
                ]
            )

        return rendered_cell
