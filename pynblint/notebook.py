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
        self.cells: List[Cell] = [
            Cell(cell_index, cell_dict)
            for cell_index, cell_dict in enumerate(self.nb_dict.cells)
        ]
        self.non_executed = all([cell.non_executed for cell in self.code_cells])

        # Convert the notebook to a Python script (excluding Markdown cells)
        python_exporter = nbconvert.PythonExporter()
        python_exporter.exclude_markdown
        self.script, _ = python_exporter.from_notebook_node(self.nb_dict)

        # Lint notebook code with Pylint
        pylint_opts = '--msg-template="{line}:{category}:{msg_id}:{symbol}:{msg}"'
        pylint_opts += " --disable=missing-module-docstring,missing-final-newline"

        with tempfile.NamedTemporaryFile(mode="r+") as fp:
            fp.write(self.script)
            fp.seek(0)

            pylint_result: Optional[Tuple[StringIO, StringIO]] = epylint.py_run(
                fp.name + " " + pylint_opts, return_std=True
            )

            if pylint_result is not None:
                pylint_stdout, pylint_stderr = pylint_result

                if pylint_stderr.getvalue() == "":
                    self.pylint_result_list: List[PylintResult] = []
                    for row in pylint_stdout.getvalue().splitlines()[1:-5]:
                        line, category, msg_id, symbol, msg = row.split(":")
                        self.pylint_result_list.append(
                            PylintResult(int(line), category, msg_id, symbol, msg)
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

    def __len__(self) -> int:
        return len(self.cells)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        return self.cells
