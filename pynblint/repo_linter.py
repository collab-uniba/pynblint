import dataclasses
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from rich.columns import Columns
from rich.console import Console, ConsoleOptions, RenderResult, group
from rich.panel import Panel
from rich.rule import Rule

from .config import settings
from .lint import PathLevelLint, ProjectLevelLint, RepoLint
from .lint_register import enabled_path_level_lints, enabled_project_level_lints
from .nb_linter import NotebookLinter
from .repository import Repository


@dataclass
class RepositoryMetadata:
    repository_name: str


@dataclass
class RepositoryStats:
    number_of_notebooks: int


class RepoLinter:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo
        self.repository_metadata: RepositoryMetadata = RepositoryMetadata(
            repository_name=repo.path.name or Path.cwd().name
        )
        self.repository_stats: RepositoryStats = RepositoryStats(
            number_of_notebooks=len(repo.notebooks)
        )

        self.lints: List[RepoLint] = []

        self.lints.extend(
            [
                ProjectLevelLint(
                    lint.slug,
                    lint.description,
                    lint.recommendation,
                    lint.linting_function,
                    self.repo,
                )
                for lint in enabled_project_level_lints
            ]
        )

        self.lints.extend(
            [
                PathLevelLint(
                    lint.slug,
                    lint.description,
                    lint.recommendation,
                    lint.linting_function,
                    self.repo,
                )
                for lint in enabled_path_level_lints
            ]
        )

        self.has_linting_results = any([lint.result for lint in self.lints])

        self.notebook_linters = [
            NotebookLinter(notebook) for notebook in self.repo.notebooks
        ]

        self.has_notebook_level_linting_results = any(
            [linter.has_linting_results for linter in self.notebook_linters]
        )

    @group()
    def get_renderable_linting_results(self):
        for lint in self.lints:
            if lint.result:
                yield lint

    def as_dict(self) -> Dict:
        results_dict = {
            "repository_metadata": dataclasses.asdict(self.repository_metadata),
            "repository_stats": dataclasses.asdict(self.repository_stats),
            "lints": [lint.as_dict() for lint in self.lints if lint.result],
            "notebook_level_lints": [
                nb_linter.as_dict() for nb_linter in self.notebook_linters
            ],
        }
        return results_dict

    @group()
    def get_renderable_nblevel_linting_results(self):
        for linter in self.notebook_linters:
            yield linter

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        # Repository name
        repo_name = "\n"
        repo_name += "[blue bold underline]REPOSITORY[/blue bold underline]"
        repo_name += "[blue bold]:[/blue bold] "
        repo_name += f"[green]{self.repository_metadata.repository_name}[/green]\n"
        repo_name += "[blue bold]      PATH:[/blue bold] "
        repo_name += f"[grey50]{self.repo.path.resolve().parent}/"
        repo_name += f"[bold]{self.repo.path.resolve().name}[bold][/grey50]\n"
        yield repo_name

        if not settings.hide_stats:

            # Statistics panels
            yield "\n[blue bold]STATISTICS[/blue bold]\n"

            # Stats
            repo_stats = "\n"
            repo_stats += "[green]Analyzed notebooks[/green]: "
            repo_stats += f"{self.repository_stats.number_of_notebooks}\n"

            metadata_panels = [Panel(repo_stats, title="Stats")]
            yield Columns(metadata_panels, equal=True)
            yield "\n\n"

        # Repo-level linting results
        if self.has_linting_results:
            yield Rule(
                "[turquoise2 bold]REPOSITORY-LEVEL RESULTS[/turquoise2 bold]",
                align="left",
                style="",
            )
            yield "\n"
            yield self.get_renderable_linting_results()
            yield "\n\n\n"

        # Notebook-level linting results
        if self.has_notebook_level_linting_results:
            yield Rule(
                "[turquoise2 bold]NOTEBOOK-LEVEL RESULTS[/turquoise2 bold]",
                align="left",
                style="",
            )
            yield "\n"
            yield self.get_renderable_nblevel_linting_results()
        yield "\n"
