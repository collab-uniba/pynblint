from enum import Enum
from pathlib import Path
from typing import Dict

import nbconvert
import nbformat
import rich
from nbformat.notebooknode import NotebookNode
from rich.abc import RichRenderable
from rich.columns import Columns
from rich.console import Console, ConsoleOptions, RenderResult
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax

from .config import CellRenderingMode, settings
from .rich_extensions import NotebookMarkdown


class Notebook(RichRenderable):
    """
    This class stores the representations of a notebook
    on which pynblint functions are called
    """

    def __init__(self, path: Path):
        self.path = path

        # Read the raw notebook file
        with open(self.path) as f:
            _nb_raw = f.read()
        self.nb_dict: NotebookNode = nbformat.reads(_nb_raw, as_version=4)

        # # Convert the notebook to a Python dictionary
        # self.nb_dict = json.loads(_nb_raw)

        # Convert the notebook to a Python script
        python_exporter = nbconvert.PythonExporter()
        self.script, _ = python_exporter.from_notebook_node(self.nb_dict)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        return [Cell(index, cell) for index, cell in enumerate(self.nb_dict["cells"])]


class CellType(str, Enum):
    MARKDOWN = "markdown"
    CODE = "code"
    RAW = "raw"
    OTHER = "other"


class Cell(RichRenderable):
    def __init__(self, cell_index: int, cell_dict: Dict) -> None:
        """Pynblint's representation of a notebook cell."""

        self._cell_dict: Dict = cell_dict
        self.cell_index: int = cell_index

        # Cell type
        self.cell_type: CellType
        if self._cell_dict["cell_type"] == "markdown":
            self.cell_type = CellType.MARKDOWN
        elif self._cell_dict["cell_type"] == "code":
            self.cell_type = CellType.CODE
        elif self._cell_dict["cell_type"] == "raw":
            self.cell_type = CellType.RAW
        else:
            self.cell_type = CellType.OTHER

        # Execution count
        if self.cell_type == CellType.CODE:
            self.cell_exec_count: int = self._cell_dict["execution_count"]

        # Cell source and source excerpt (for cell visualization with Rich)
        self._cell_source = self._cell_dict["source"]
        self._source_excerpt: str = ""

        if settings.cell_rendering_mode == CellRenderingMode.COMPACT:
            cell_source_array = self._cell_source.split("\n")
            if len(cell_source_array) > 2:
                self._source_excerpt = "\n".join(
                    [cell_source_array[0], "\n[...]\n", cell_source_array[-1]]
                )
            else:
                self._source_excerpt = self._cell_source
        else:
            self._source_excerpt = self._cell_source

    def __rich__(self) -> Columns:

        if self.cell_type == CellType.CODE:
            if settings.display_cell_index:
                panel_title = f"Index: {self.cell_index}"
            else:
                panel_title = None
            rendered_cell = Columns(
                [
                    f"\nIn [{self.cell_exec_count}]:",
                    Panel(
                        Syntax(self._source_excerpt, "python"),
                        width=int(rich.get_console().size[0] * 0.90),
                        title=panel_title,
                    ),
                ]
            )
        else:
            rendered_cell = Columns(
                [
                    "        ",
                    Padding(NotebookMarkdown(self._source_excerpt), (1, 0, 1, 8)),
                ]
            )

        return rendered_cell
