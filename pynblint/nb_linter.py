import ast
import dataclasses
from dataclasses import dataclass
from typing import Dict, List

from rich.columns import Columns
from rich.console import Console, ConsoleOptions, RenderResult, group
from rich.panel import Panel
from rich.rule import Rule

from .config import settings
from .lint import CellLevelLint, NotebookLevelLint, NotebookLint
from .lint_register import enabled_cell_level_lints, enabled_notebook_level_lints
from .notebook import Notebook


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
                    lint.show_details,
                )
                for lint in enabled_cell_level_lints
            ]
        )

        self.has_linting_results = any([lint.result for lint in self.lints])

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

    def as_dict(self) -> Dict:
        results_dict = {
            "notebook_metadata": dataclasses.asdict(self.notebook_metadata),
            "notebook_stats": dataclasses.asdict(self.notebook_stats),
            "lints": [lint.as_dict() for lint in self.lints if lint.result],
        }
        return results_dict

    @group()
    def get_renderable_linting_results(self):
        for lint in self.lints:
            if lint.result:
                yield lint

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        # Notebook name and path
        notebook_name = "\n"
        notebook_name += "[blue bold underline]NOTEBOOK[/blue bold underline]"
        notebook_name += "[blue bold]:[/blue bold] "
        notebook_name += f"[green]{self.notebook_metadata.notebook_name}[/green]\n"
        notebook_name += "[blue bold]    PATH:[/blue bold] "
        notebook_name += f"[grey50]{self.notebook.path.parent}/"
        notebook_name += f"[bold]{self.notebook.path.name}[bold][/grey50]\n"
        yield notebook_name

        if not settings.hide_stats:
            # Statistics panels
            yield "\n[blue bold]STATISTICS[/blue bold]\n"

            # Cells stats
            cells_stats = "\n"
            cells_stats += "[green]Total cells[/green]: "
            cells_stats += f"{self.notebook_stats.number_of_cells}\n"
            cells_stats += "[green]Code cells[/green]: "
            cells_stats += f"{self.notebook_stats.number_of_code_cells}\n"
            cells_stats += "[green]Markdown cells[/green]: "
            cells_stats += f"{self.notebook_stats.number_of_MD_cells}\n"
            cells_stats += "[green]Raw cells[/green]: "
            cells_stats += f"{self.notebook_stats.number_of_raw_cells}\n"

            # Markdown stats
            md_stats = "\n"
            md_stats += "[green]Markdown titles[/green]: "
            md_stats += f"{self.notebook_stats.number_of_md_titles}\n"
            md_stats += "[green]Markdown lines[/green]: "
            md_stats += f"{self.notebook_stats.number_of_md_lines}\n"

            # Modularization stats
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
            yield Columns(
                metadata_panels,
                equal=True,
            )

        # Linting results
        if self.has_linting_results:
            yield "\n[blue bold]LINTING RESULTS[/blue bold]\n"
            yield self.get_renderable_linting_results()

        yield Rule()
