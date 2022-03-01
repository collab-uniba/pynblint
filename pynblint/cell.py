from enum import Enum

import rich
from nbformat.notebooknode import NotebookNode
from rich.abc import RichRenderable
from rich.columns import Columns
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax

from .config import CellRenderingMode, settings
from .rich_extensions import NotebookMarkdown


class CellType(str, Enum):
    MARKDOWN = "markdown"
    CODE = "code"
    RAW = "raw"
    OTHER = "other"


class Cell(RichRenderable):
    def __init__(self, cell_index: int, cell_dict: NotebookNode) -> None:
        """Pynblint's representation of a notebook cell."""

        self.cell_index: int = cell_index
        self._cell_dict: NotebookNode = cell_dict

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
            self.exec_count: int = self._cell_dict["execution_count"]

        # Cell source and source excerpt (for cell visualization with Rich)
        self.cell_source = self._cell_dict["source"]
        self._source_excerpt: str = ""

        if settings.cell_rendering_mode == CellRenderingMode.COMPACT:
            cell_source_array = self.cell_source.split("\n")
            if len(cell_source_array) > 2:
                self._source_excerpt = "\n".join(
                    [cell_source_array[0], "\n[...]\n", cell_source_array[-1]]
                )
            else:
                self._source_excerpt = self.cell_source
        else:
            self._source_excerpt = self.cell_source

    @property
    def empty(self) -> bool:
        """``True`` if the code cell is empty."""
        if self.cell_type == CellType.CODE:
            return (self.exec_count is None) and (len(self.cell_source) == 0)
        else:
            raise Exception("The `empty` property is defined only for code cells.")

    @property
    def non_executed(self) -> bool:
        """``True`` if the non-empty code cell has not been executed."""
        if self.cell_type == CellType.CODE:
            return (self.exec_count is None) and (len(self.cell_source) > 0)
        else:
            raise Exception(
                "The `non_executed` property is defined only for code cells."
            )

    def __rich__(self) -> Columns:

        if self.cell_type == CellType.CODE:
            if settings.display_cell_index:
                panel_title = f"Index: {self.cell_index}"
            else:
                panel_title = None
            rendered_cell = Columns(
                [
                    f"\nIn [{self.exec_count}]:",
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
