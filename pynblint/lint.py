from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

from rich.console import Console, ConsoleOptions, RenderResult, group
from rich.padding import Padding

from .config import settings
from .notebook import Cell, Notebook
from .repository import Repository


class LintLevel(str, Enum):
    CELL = "cell"
    NOTEBOOK = "notebook"
    PATH = "path"
    PROJECT = "project"


@dataclass
class LintDefinition:
    slug: str
    description: str
    recommendation: str
    linting_function: Callable
    show_details: bool = True


# ============== #
# NOTEBOOK LINTS #
# ============== #


class NotebookLint(ABC):
    def __init__(self, slug: str, description: str, recommendation: str) -> None:
        super().__init__()
        self.slug: str = slug
        self.description: str = description
        self.recommendation: str = recommendation
        self.result: Optional[Union[bool, List[Cell]]] = None

    @abstractmethod
    def lint(self, notebook: Notebook) -> Union[bool, List[Cell]]:
        pass

    def as_dict(self, description: bool = True, recommendation: bool = True) -> Dict:
        lint_dict = {
            "slug": self.slug,
        }
        if description:
            lint_dict["description"] = self.description
        if recommendation:
            lint_dict["recommendation"] = self.recommendation
        return lint_dict

    @abstractmethod
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        pass


class NotebookLevelLint(NotebookLint):
    def __init__(
        self,
        slug: str,
        description: str,
        recommendation: str,
        linting_function: Callable[[Notebook], bool],
        notebook: Notebook,
    ) -> None:
        super().__init__(slug, description, recommendation)
        self.linting_function: Callable[[Notebook], bool] = linting_function
        self.result: bool = self.lint(notebook)

    def lint(self, notebook: Notebook) -> bool:
        return self.linting_function(notebook)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield f"[orange3 bold]({self.slug})[/orange3 bold]"
        yield Padding(
            f"{self.description}", (0, 0, 0, settings.result_details_indentation)
        )
        if not settings.hide_recommendations and len(self.recommendation):
            yield Padding(
                "[bold underline]Recommendation[/bold underline]: "
                f"{self.recommendation}",
                (0, 0, 0, settings.result_details_indentation),
            )
        yield "\n"


class CellLevelLint(NotebookLint):
    def __init__(
        self,
        slug: str,
        description: str,
        recommendation: str,
        linting_function: Callable[[Notebook], List[Cell]],
        notebook: Notebook,
        show_details: bool = True,
    ) -> None:
        super().__init__(slug, description, recommendation)
        self.linting_function: Callable[[Notebook], List[Cell]] = linting_function
        self.show_details = show_details
        self.result: List[Cell] = self.lint(notebook)

    def lint(self, notebook: Notebook) -> List[Cell]:
        """
        Execute the cell-level lint represented by the class.

        Returns:
            The index list of affected cells in case of a positive result,
            an empty list otherwise.
        """
        return self.linting_function(notebook)

    def as_dict(self, description: bool = True, recommendation: bool = True) -> Dict:
        lint_dict = super().as_dict(description, recommendation)
        lint_dict["cells"] = [cell.as_dict(source=False) for cell in self.result]
        return lint_dict

    @group()
    def get_renderable_affected_cells(self):
        for cell in self.result:
            yield Padding(cell, (0, 0, 0, settings.result_details_indentation))

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield f"[orange3 bold]({self.slug})[/orange3 bold]"
        yield Padding(
            f"{self.description}", (0, 0, 0, settings.result_details_indentation)
        )
        if not settings.hide_recommendations and len(self.recommendation):
            yield Padding(
                "[bold underline]Recommendation[/bold underline]: "
                f"{self.recommendation}",
                (0, 0, 0, settings.result_details_indentation),
            )

        yield Padding(
            "[bold underline]Affected cells[/bold underline]: [grey50]indexes[/grey50]"
            + str([cell.cell_index for cell in self.result]),
            (0, 0, 0, settings.result_details_indentation),
        )
        if self.show_details:
            yield self.get_renderable_affected_cells()
        yield "\n"


# ================ #
# REPOSITORY LINTS #
# ================ #


class RepoLint(ABC):
    def __init__(self, slug: str, description: str, recommendation: str) -> None:
        super().__init__()
        self.slug: str = slug
        self.description: str = description
        self.recommendation: str = recommendation
        self.result: Optional[Union[bool, List[Path]]] = None

    @abstractmethod
    def lint(self, repository: Repository) -> Union[bool, List[Path]]:
        pass

    def as_dict(self, description: bool = True, recommendation: bool = True) -> Dict:
        lint_dict = {
            "slug": self.slug,
        }
        if description:
            lint_dict["description"] = self.description
        if recommendation:
            lint_dict["recommendation"] = self.recommendation
        return lint_dict

    @abstractmethod
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        pass


class ProjectLevelLint(RepoLint):
    def __init__(
        self,
        slug: str,
        description: str,
        recommendation: str,
        linting_function: Callable[[Repository], bool],
        repository: Repository,
    ) -> None:
        super().__init__(slug, description, recommendation)
        self.linting_function: Callable[[Repository], bool] = linting_function
        self.result: bool = self.lint(repository)

    def lint(self, repository: Repository) -> bool:
        return self.linting_function(repository)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield f"[blue bold]({self.slug})[/blue bold]"
        yield Padding(
            f"{self.description}", (0, 0, 0, settings.result_details_indentation)
        )
        if not settings.hide_recommendations and len(self.recommendation):
            yield Padding(
                "[bold underline]Recommendation[/bold underline]: "
                f"{self.recommendation}",
                (0, 0, 0, settings.result_details_indentation),
            )
        yield "\n"


class PathLevelLint(RepoLint):
    def __init__(
        self,
        slug: str,
        description: str,
        recommendation: str,
        linting_function: Callable[[Repository], List[Path]],
        repository: Repository,
    ) -> None:
        super().__init__(slug, description, recommendation)
        self.linting_function: Callable[[Repository], List[Path]] = linting_function
        self.result: List[Path] = self.lint(repository)

    def lint(self, repository: Repository) -> List[Path]:
        return self.linting_function(repository)

    def as_dict(self, description: bool = True, recommendation: bool = True) -> Dict:
        lint_dict = super().as_dict(description, recommendation)
        lint_dict["paths"] = [str(path) for path in self.result]
        return lint_dict

    @group()
    def get_renderable_affected_cells(self):
        for path in self.result:
            yield Padding(
                "  •  [yellow]" + str(path) + "[/yellow]",
                (0, 0, 0, settings.result_details_indentation),
            )

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield f"[blue bold]({self.slug})[/blue bold]"
        yield Padding(
            f"{self.description}", (0, 0, 0, settings.result_details_indentation)
        )
        if not settings.hide_recommendations and len(self.recommendation):
            yield Padding(
                "[bold underline]Recommendation[/bold underline]: "
                f"{self.recommendation}",
                (0, 0, 0, settings.result_details_indentation),
            )

        yield Padding(
            "[bold underline]Affected paths[/bold underline]:",
            (0, 0, 0, settings.result_details_indentation),
        )
        yield self.get_renderable_affected_cells()
        yield "\n"
