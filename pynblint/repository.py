import os
import re
import sys
import tempfile
import zipfile
from abc import ABC
from pathlib import Path
from typing import List, Optional, Pattern

import git

from .config import settings
from .notebook import Notebook


class Repository(ABC):
    """
    This class stores data about a code repository.
    """

    def __init__(self, path: Path):

        # Repository info
        self.path = path
        self.dependencies_module: set

        # Extracted content
        self.notebooks: List[Notebook] = []  # List of Notebook objects
        self.dependencies_module = self._get_dependencies()
        self.core_library: set = self._get_core_dependecies()

    def retrieve_notebooks(self):

        # Directories to ignore while traversing the tree
        dirs_ignore = [".ipynb_checkpoints"]

        for root, dirs, files in os.walk(self.path):
            # `dirs[:] = value` modifies dirs in-place
            dirs[:] = [d for d in dirs if d not in dirs_ignore]
            for f in files:
                if f.endswith(".ipynb"):
                    nb = Notebook(Path(root) / Path(f))
                    self.notebooks.append(nb)

    @property
    def is_git_repository(self):
        # Directories to ignore while traversing the tree
        dirs_ignore = [".ipynb_checkpoints"]
        versioned = False
        for _, dirs, _ in os.walk(self.path):
            # `dirs[:] = value` modifies dirs in-place
            dirs[:] = [d for d in dirs if d not in dirs_ignore]
            for d in dirs:
                if d == ".git":
                    versioned = True
        return versioned

    @property
    def large_file_paths(self) -> List[Path]:
        """Return the list of files whose size is above the fixed threshold.

        The threshold size for data files is defined in the settings.

        Returns:
            List[Path]: the list of large files.
        """
        large_files: List[Path] = []
        for dirpath, _, filenames in os.walk(self.path):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                if os.path.getsize(file_path) > settings.max_data_file_size:
                    large_files.append(file_path)
        return large_files

    def _get_dependencies(self) -> set:
        dependencies = set()
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.dirname(path)
        # siccome il file di requirement si toverà nella root di
        # progetto ho creato un file fittizio con le stesse
        # informazioni per non spostare quello pre-esistente
        file = "kk.txt"
        final_path = os.path.join(path, file)
        with open(final_path, "r") as fi:
            file_row = fi.read()
            tmp = file_row.split("\n")
            for item in tmp:
                item.strip()
                dependencies.add(tuple(item.split("==")))

        # print(dependencies)

        return dependencies

    # momentaneamente la lascio qui ma quando ma dovo la sposterò
    # perchè ovviamente non è una funzione che riguarda il repository
    def _get_core_dependecies(self) -> set:
        coredependecies = set()
        modules = sys.modules
        pattern: Pattern[str] = re.compile(r".*\\\\Python\\\\Python37\\\\lib\\\\.*.py")
        for i in modules.items():
            # print(" PPOSIZIONE 0:" + i[0])
            # print(" PPOSIZIONE 1:" + str(i))
            if pattern.match(str(i)):
                coredependecies.add(i[0])
        print(coredependecies)

        return coredependecies


class LocalRepository(Repository):
    """
    This class stores data about a local code repository.
    The `source_path` can point either to a local directory or a zip archive
    """

    def __init__(self, source_path: Path):

        self.source_path = source_path
        tmp_dir: Optional[tempfile.TemporaryDirectory] = None

        # Handle .zip archives
        if self.source_path.suffix == ".zip":

            # Create temp directory
            tmp_dir = tempfile.TemporaryDirectory()
            repo_path: Path = Path(tmp_dir.name)

            # Extract the zip file into the temp folder
            with zipfile.ZipFile(self.source_path, "r") as zip_file:
                zip_file.extractall(repo_path)

        # Handle local folders
        elif self.source_path.is_dir():
            repo_path = self.source_path

        else:
            raise ValueError(
                "The file at the specified path is neither a notebook (.ipynb) "
                "nor a compressed archive."
            )

        super().__init__(repo_path)
        self.retrieve_notebooks()

        # Clean up the temp directory if one was created
        if tmp_dir is not None:
            tmp_dir.cleanup()


class GitHubRepository(Repository):
    """
    This class stores data about a GitHub repository
    """

    def __init__(self, github_url: str):
        self.url = github_url

        # Clone the repo in a temp directory
        tmp_dir = tempfile.TemporaryDirectory()
        git.Repo.clone_from(  # type: ignore
            url=github_url, to_path=tmp_dir.name, depth=1
        )
        super().__init__(Path(tmp_dir.name) / github_url.split("/")[-1])

        # Analyze the repo
        self.retrieve_notebooks()

        # Clean up the temp directory
        tmp_dir.cleanup()
