import ast
from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel
from rich.columns import Columns
from rich.console import Group, group
from rich.panel import Panel
from rich.rule import Rule

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

    # Markdown usage
    number_of_md_lines: int
    number_of_md_titles: int


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
            number_of_md_lines=self.count_md_lines(),
            number_of_md_titles=self.count_md_titles(),
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

    def count_md_lines(self) -> int:
        """Count the total number of markdown rows within a notebook."""
        nb_dict = self.notebook.nb_dict
        markdown_lines = 0
        for cell in nb_dict["cells"]:
            if cell["cell_type"] == "markdown":
                rows = len(cell["source"].split("\n"))
                markdown_lines += rows
        return markdown_lines

    def count_md_titles(self) -> int:
        """Count the total number of markdown titles within a notebook."""
        nb_dict = self.notebook.nb_dict
        titles = 0
        for cell in nb_dict["cells"]:
            if cell["cell_type"] == "markdown":
                for row in cell["source"]:
                    if row.lstrip().startswith("#"):
                        titles = titles + 1
        return titles

    @group()
    def get_renderable_linting_results(self):
        for lint in self.lints:
            if lint.result:
                yield lint

    def __rich__(self) -> Group:

        # Stats
        cells_stats = "\n"
        cells_stats += "[green]Total cells[/green]: "
        cells_stats += f"{self.notebook_stats.number_of_cells}\n"
        cells_stats += "[green]Code cells[/green]: "
        cells_stats += f"{self.notebook_stats.number_of_code_cells}\n"
        cells_stats += "[green]Markdown cells[/green]: "
        cells_stats += f"{self.notebook_stats.number_of_MD_cells}\n"
        cells_stats += "[green]Raw cells[/green]: "
        cells_stats += f"{self.notebook_stats.number_of_raw_cells}\n"

        md_stats = "\n"
        md_stats += "[green]Markdown titles[/green]: "
        md_stats += f"{self.notebook_stats.number_of_md_titles}\n"
        md_stats += "[green]Markdown lines[/green]: "
        md_stats += f"{self.notebook_stats.number_of_md_lines}\n"

        modularization_stats = "\n"
        modularization_stats += "[green]Number of functions[/green]: "
        modularization_stats += f"{self.notebook_stats.number_of_functions}\n"
        modularization_stats += "[green]Number of classes[/green]: "
        modularization_stats += f"{self.notebook_stats.number_of_classes}\n"

        metadata_panels = [
            Panel(cells_stats, title="Cells"),
            Panel(md_stats, title="Markdown usage"),
            Panel(modularization_stats, title="Code modularization"),
        ]

        rendered_results = Group(
            f"\n[blue bold]NOTEBOOK:[/blue bold] "
            f"[green]{self.notebook_metadata.notebook_name}[/green]\n"
            f"[blue]    PATH:[/blue] "
            f"[grey50]{self.notebook.path.parent}/"
            f"[bold]{self.notebook.path.name}[bold][/grey50]\n",
            Columns(
                metadata_panels,
                equal=True,
            ),
            "\n[blue bold]RESULTS[/blue bold]\n",
            self.get_renderable_linting_results(),
            Rule(),
        )
        return rendered_results
