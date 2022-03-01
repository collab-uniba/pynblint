from dataclasses import dataclass
from typing import List

from pydantic import BaseModel

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

        # self.results: Dict = {
        #     "lintingResults": {
        #         "duplicateFilenames": get_duplicate_notebooks(repo),
        #         "untitledNotebooks": get_untitled_notebooks(repo),
        #         "isVersioned": repo.versioned,
        #     },
        #     "notebookLintingResults": self._get_notebooks_results(),
        # }

    # def _get_notebooks_results(self) -> List[Dict]:
    #     """This function takes the list of notebook objects from the current
    #       repository
    #     and returns a list of dictionaries containing the related linting results."""
    #     data = []
    #     for notebook in self.repo.notebooks:
    #         nb_linter: NotebookLinter = NotebookLinter(notebook)
    #         data.append(nb_linter.get_linting_results())
    #     return data

    def get_linting_results(self):
        # return self.results
        pass
