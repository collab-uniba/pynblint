from pathlib import Path
from typing import List

import nbconvert
import nbformat
from nbformat.notebooknode import NotebookNode
from rich.abc import RichRenderable
from rich.console import Console, ConsoleOptions, RenderResult

from .cell import Cell, CellType
from .config import settings


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

        # Convert the notebook to a Python script
        python_exporter = nbconvert.PythonExporter()
        self.script, _ = python_exporter.from_notebook_node(self.nb_dict)

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
