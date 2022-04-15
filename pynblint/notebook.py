import ast
import tempfile
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import List, Optional, Tuple

import nbconvert
import nbformat
from nbformat.notebooknode import NotebookNode
from pylint import epylint
from rich.abc import RichRenderable
from rich.console import Console, ConsoleOptions, RenderResult

from .cell import Cell, CellType
from .config import settings


@dataclass
class PylintResult:
    line: int
    category: str
    msg_id: str
    symbol: str
    msg: str


class Notebook(RichRenderable):
    """
    This class stores the representations of a notebook
    on which pynblint functions are called
    """

    def __init__(self, path: Path):
        self.path: Path = path

        # Read the notebook with nbformat
        with open(self.path) as f:
            nb_raw = f.read()
        self.nb_dict: NotebookNode = nbformat.reads(nb_raw, as_version=4)

        # Populate the list of Cells
        SCRIPT_HEADER_OFFSET: int = 4
        CELL_PADDING: int = 5
        CELL_TOP_PADDING: int = 3
        code_cells_so_far: int = 0
        code_lines_so_far = 0

        self.cells: List[Cell] = []
        for cell_index, cell_dict in enumerate(self.nb_dict.cells):
            if cell_dict["cell_type"] == "code":
                cell_offset = (
                    SCRIPT_HEADER_OFFSET
                    + (CELL_PADDING * code_cells_so_far)
                    + code_lines_so_far
                    + CELL_TOP_PADDING
                )
                code_cells_so_far += 1
                code_lines_so_far += len(cell_dict["source"].splitlines())
                self.cells.append(Cell(cell_index, cell_dict, cell_offset))
            else:
                self.cells.append(Cell(cell_index, cell_dict))
        # self.cells: List[Cell] = [
        #     Cell(cell_index, cell_dict)
        #     for cell_index, cell_dict in enumerate(self.nb_dict.cells)
        # ]
        self.non_executed = all([cell.non_executed for cell in self.code_cells])

        # Convert the notebook to a Python script (excluding Markdown cells)
        python_exporter = nbconvert.PythonExporter()
        python_exporter.exclude_markdown = True
        script, _ = python_exporter.from_notebook_node(self.nb_dict)
        self.script = script.rstrip("\n")

        # Lint notebook code with Pylint
        pylint_results: Optional[List[str]] = self.lint_notebook_code_with_pylint()
        self.pylint_result_list: Optional[List[PylintResult]] = (
            self.parse_pylint_results(pylint_results) if pylint_results else None
        )

        # Extract the Python abstract syntax tree
        # (or set `has_invalid_python_syntax` to True)
        self.has_invalid_python_syntax: bool = False
        try:
            self.ast = ast.parse(self.script)
        except SyntaxError:
            self.has_invalid_python_syntax = True

    @property
    def code_cells(self) -> List[Cell]:
        code_cells = [cell for cell in self.cells if cell.cell_type == CellType.CODE]
        return code_cells

    @property
    def markdown_cells(self) -> List[Cell]:
        md_cells = [cell for cell in self.cells if cell.cell_type == CellType.MARKDOWN]
        return md_cells

    @property
    def initial_cells(self) -> List[Cell]:
        return self.cells[: settings.initial_cells]

    @property
    def final_cells(self) -> List[Cell]:
        return self.cells[-settings.final_cells :]  # noqa: E203

    def lint_notebook_code_with_pylint(self) -> Optional[List[str]]:
        pylint_opts: str = '--msg-template="{line}:{category}:{msg_id}:{symbol}:{msg}"'
        pylint_opts += (
            " --disable=missing-module-docstring,missing-final-newline,invalid-name"
        )

        with tempfile.NamedTemporaryFile(mode="r+") as fp:
            fp.write(self.script)
            fp.seek(0)

            pylint_result: Optional[Tuple[StringIO, StringIO]] = epylint.py_run(
                fp.name + " " + pylint_opts, return_std=True
            )

            if pylint_result is None:
                return None
            else:
                pylint_stdout, pylint_stderr = pylint_result

                if pylint_stderr.getvalue() != "":
                    return None
                else:
                    res: List[str] = [
                        line.lstrip()
                        for line in pylint_stdout.getvalue().splitlines()[1:-5]
                    ]
                    return res

    def parse_pylint_results(self, pylint_results: List[str]) -> List[PylintResult]:
        self.pylint_result_list = []
        for row in pylint_results:
            line, category, msg_id, symbol, msg = row.split(":")
            self.pylint_result_list.append(
                PylintResult(int(line), category, msg_id, symbol, msg)
            )
        return self.pylint_result_list

    def __len__(self) -> int:
        return len(self.cells)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        return self.cells
