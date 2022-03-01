from dataclasses import dataclass
from typing import List

from pydantic import BaseModel
from rich.console import Group, group
from rich.pretty import Pretty

from .lint import PathLevelLint, ProjectLevelLint, RepoLint
from .lint_register import enabled_path_level_lints, enabled_project_level_lints
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

    @group()
    def get_renderable_linting_results(self):
        for lint in self.lints:
            if lint.result:
                yield lint

    def __rich__(self) -> Group:
        rendered_results = Group(
            Pretty(self.repository_metadata),
            Pretty(self.repository_stats),
            self.get_renderable_linting_results(),
        )
        return rendered_results
