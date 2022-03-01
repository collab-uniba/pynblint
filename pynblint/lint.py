from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Callable, List, NamedTuple, Optional, Union

from .notebook import Cell, Notebook
from .repository import Repository


class LintLevel(str, Enum):
    CELL = "cell"
    NOTEBOOK = "notebook"
    PATH = "path"
    PROJECT = "project"


class LintDefinition(NamedTuple):
    slug: str
    description: str
    recommendation: str
    linting_function: Callable


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

    @abstractmethod
    def __rich__(self):
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

    def __rich__(self) -> str:
        render = f"[orange3 bold]({self.slug})[/orange3 bold]: {self.description}"
        if len(self.recommendation):
            render += f"\n\t[italic]Recommendation[/italic]: {self.recommendation}"

        render += "\n"
        return render


class CellLevelLint(NotebookLint):
    def __init__(
        self,
        slug: str,
        description: str,
        recommendation: str,
        linting_function: Callable[[Notebook], List[Cell]],
        notebook: Notebook,
    ) -> None:
        super().__init__(slug, description, recommendation)
        self.linting_function: Callable[[Notebook], List[Cell]] = linting_function
        self.result: List[Cell] = self.lint(notebook)

    def lint(self, notebook: Notebook) -> List[Cell]:
        """
        Execute the cell-level lint represented by the class.

        Returns:
            The index list of affected cells in case of a positive result,
            an empty list otherwise.
        """
        return self.linting_function(notebook)

    def __rich__(self):
        render = f"[orange3 bold]({self.slug})[/orange3 bold]: {self.description}"
        if len(self.recommendation):
            render += f"\n\t[italic]Recommendation[/italic]: {self.recommendation}"

        render += "\n\t[italic]Cells affected[/italic]: [grey50]indexes[/grey50]" + str(
            [cell.cell_index for cell in self.result]
        )
        render += "\n"
        return render


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

    @abstractmethod
    def __rich__(self):
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

    def __rich__(self) -> str:
        render = f"[blue bold]({self.slug})[/blue bold]: {self.description}"
        if len(self.recommendation):
            render += f"\n\t[italic]Recommendation[/italic]: {self.recommendation}"
        return render


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

    def __rich__(self) -> str:
        render = f"[blue bold]({self.slug})[/blue bold]: {self.description}"
        if len(self.recommendation):
            render += f"\n\t[italic]Recommendation[/italic]: {self.recommendation}"
            render += f"\n\t[italic]Affected paths[/italic]: {self.result}"
        return render
