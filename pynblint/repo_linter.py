from dataclasses import dataclass
from typing import List

from pydantic import BaseModel
from rich.columns import Columns
from rich.console import Group, group
from rich.panel import Panel
from rich.rule import Rule

from .lint import PathLevelLint, ProjectLevelLint, RepoLint
from .lint_register import enabled_path_level_lints, enabled_project_level_lints
from .nb_linter import NotebookLinter
from .repository import Repository


class RepoLinterOptions(BaseModel):
    pass


@dataclass
class RepositoryMetadata:
    repository_name: str


@dataclass
class RepositoryStats:
    number_of_notebooks: int


class RepoLinter:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo
        self.options: RepoLinterOptions = RepoLinterOptions()
        self.repository_metadata: RepositoryMetadata = RepositoryMetadata(
            repository_name=repo.path.name
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

        self.notebook_level_lints = [
            NotebookLinter(notebook) for notebook in self.repo.notebooks
        ]

    @group()
    def get_renderable_linting_results(self):
        for lint in self.lints:
            if lint.result:
                yield lint

    @group()
    def get_renderable_nblevel_linting_results(self):
        for lint in self.notebook_level_lints:
            yield lint

    def __rich__(self) -> Group:

        # Stats
        repo_stats = "\n"
        repo_stats += "[green]Number of notebooks[/green]: "
        repo_stats += f"{self.repository_stats.number_of_notebooks}\n"

        metadata_panels = [Panel(repo_stats, title="Stats")]

        rendered_results = Group(
            f"\n[blue bold underline]REPOSITORY:[/blue bold underline] "
            f"[green]{self.repository_metadata.repository_name}[/green]\n",
            Columns(metadata_panels, equal=True),
            "\n\n",
            Rule(
                "[turquoise2 bold]REPOSITORY-LEVEL RESULTS[/turquoise2 bold]",
                align="left",
                style="",
            ),
            "\n",
            self.get_renderable_linting_results(),
            "\n\n\n",
            Rule(
                "[turquoise2 bold]NOTEBOOK-LEVEL RESULTS[/turquoise2 bold]",
                align="left",
                style="",
            ),
            "\n",
            self.get_renderable_nblevel_linting_results(),
            "\n",
        )
        return rendered_results
