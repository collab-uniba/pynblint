import re
from typing import Dict, Optional, Union

import rich
from nbformat.notebooknode import NotebookNode
from rich.abc import RichRenderable
from rich.columns import Columns
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax

from .config import CellRenderingMode, settings
from .rich_extensions import NotebookMarkdown


class Cell(RichRenderable):
    def __init__(
        self,
        cell_index: int,
        cell_dict: NotebookNode,
    ) -> None:
        """Pynblint's representation of a notebook cell."""

        self.cell_index: int = cell_index
        self._cell_dict: NotebookNode = cell_dict
        self.cell_source: str = self._cell_dict["source"]

        if settings.cell_rendering_mode == CellRenderingMode.COMPACT:
            self._source_excerpt = self.get_cell_excerpt()
        else:
            self._source_excerpt = self.cell_source

    def get_cell_excerpt(self) -> str:
        cell_source_array = self.cell_source.split("\n")
        if len(cell_source_array) > 2:
            return "\n".join([cell_source_array[0], "\n[...]\n", cell_source_array[-1]])
        else:
            return self.cell_source

    def as_dict(self, source: bool = True) -> Dict:
        cell_dict: Dict[str, Union[int, str]] = {
            "index": self.cell_index,
        }
        if source:
            cell_dict["source"] = self._source_excerpt
        return cell_dict


class MarkdownCell(Cell):
    @property
    def is_heading(self) -> bool:
        """Return ``True`` if the cell is an MD cell containing only MD headings."""
        pattern = re.compile(r"^\s*#{1,6}\s*[^#\n]*$")
        return all(
            pattern.match(line)
            for line in self.cell_source.splitlines()
            if line and (not line.isspace())
        )

    def as_dict(self, source: bool = True) -> Dict:
        cell_dict = super().as_dict(source)
        cell_dict["type"] = "markdown"
        return cell_dict

    def __rich__(self) -> Columns:
        rendered_cell = Columns(
            [
                "        ",
                Padding(NotebookMarkdown(self._source_excerpt), (1, 0, 1, 8)),
            ]
        )
        return rendered_cell


class CodeCell(Cell):
    def __init__(
        self,
        cell_index: int,
        cell_dict: NotebookNode,
        cell_offset: Optional[int] = None,
    ) -> None:
        super().__init__(cell_index, cell_dict)

        # Cell offset in script
        self.cell_offset: Optional[int] = cell_offset

        # Execution count
        self.exec_count: int = self._cell_dict["execution_count"]

    @property
    def empty(self) -> bool:
        """Return ``True`` if the code cell is empty."""
        return (self.exec_count is None) and (len(self.cell_source) == 0)

    @property
    def non_executed(self) -> bool:
        """Return ``True`` if the code cell is not empty and has not been executed."""
        return (self.exec_count is None) and (len(self.cell_source) > 0)

    def as_dict(self, source: bool = True) -> Dict:
        cell_dict = super().as_dict(source)
        cell_dict["type"] = "code"
        cell_dict["execution_count"] = self.exec_count
        return cell_dict

    def __rich__(self) -> Columns:

        counter = self.exec_count or " "
        if settings.display_cell_index:
            panel_title = f"Index: {self.cell_index}"
        else:
            panel_title = None
        rendered_cell = Columns(
            [
                f"\nIn [{counter}]:",
                Panel(
                    Syntax(self._source_excerpt, "python", background_color="default"),
                    width=int(rich.get_console().size[0] * 0.85),
                    title=panel_title,
                ),
            ]
        )

        return rendered_cell


class RawCell(Cell):
    def as_dict(self, source: bool = True) -> Dict:
        cell_dict = super().as_dict(source)
        cell_dict["type"] = self._cell_dict["cell_type"]
        return cell_dict

    def __rich__(self) -> str:
        rendered_cell = ""
        return rendered_cell
