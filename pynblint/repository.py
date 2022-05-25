import os
import tempfile
import zipfile
from abc import ABC
from pathlib import Path
from typing import Dict, List, Optional

import git
import toml
from isort.stdlibs.py39 import stdlib
from yaml import safe_load

from .config import settings
from .notebook import Notebook


class Repository(ABC):
    """
    This class stores data about a code repository.
    """

    def __init__(self, path: Path):

        # Repository info
        self.path = path

        # Extracted content
        self.notebooks: List[Notebook] = []  # List of Notebook objects
        self.dependecies_file_found: Dict[str, Path] = self.retrieve_file()
        self.declare_dependencies: set = self.get_requirement_from_file()

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

    def get_requirement_from_file(self) -> set:
        requirement_set = set()

        requirement_set.update(self._get_dependencies_from_txt())
        requirement_set.update(self._get_dependencies_from_setup())
        requirement_set.update(self._get_dependencies_from_yaml())
        requirement_set.update(self._get_dependencies_from_toml())
        requirement_set.update(self._get_dependencies_from_pipfile())

        return requirement_set

    def retrieve_file(self) -> Dict[str, Path]:
        path = Path()
        list_of_path: Dict[str, Path] = {}
        for root, dirs, files in os.walk(self.path):
            dirs[:] = [d for d in dirs]
            for f in files:
                if f.endswith("enviroment.yaml"):
                    path = Path(root) / Path(f)
                    list_of_path["enviroment.yaml"] = path
                elif f.endswith("Pipfile"):
                    path = Path(root) / Path(f)
                    list_of_path["Pipfile"] = path
                elif f.endswith("setup.py"):
                    path = Path(root) / Path(f)
                    list_of_path["setup.py"] = path
                elif f.endswith("pyproject.toml"):
                    path = Path(root) / Path(f)
                    list_of_path["pyproject.toml"] = path
                elif f.endswith("requirements.txt"):
                    path = Path(root) / Path(f)
                    list_of_path["requirements.txt"] = path
        return list_of_path

    def _get_dependencies_from_txt(self) -> set:
        """this function after fetching the location of the
        .txt file reads it and scans it for dependencies"""
        txt_dependencies = set()
        try:
            path = self.dependecies_file_found["requirements.txt"]
            if path is not None:
                with open(path, "r") as fi:
                    row_file = fi.read()
                    tmp = row_file.split("\n")
                    for item in tmp:
                        item.strip()
                    txt_dependencies.add(item.split("==")[0])
                    fi.close()

        except KeyError:
            return txt_dependencies

        return txt_dependencies

    def _get_dependencies_from_toml(self) -> set:
        toml_dependencies = set()
        try:
            path = self.dependecies_file_found["pyproject.toml"]
            if path is not None:
                data = toml.load(path)
                tmp_list = [
                    x.split("=")[0] for x in data["tool"]["poetry"]["dev-dependencies"]
                ]
                for i in tmp_list:
                    toml_dependencies.add(i)
        except KeyError:
            return toml_dependencies

        return toml_dependencies

    def _get_dependencies_from_yaml(self) -> set:
        yaml_dependencies = set()
        try:
            path = self.dependecies_file_found["enviroment.yaml"]
            if path is not None:
                with open(path, "r") as fi:
                    row_file = fi.read()
                    data = safe_load(row_file)
                    tmp_list = [x.split("==")[0] for x in data["requirements"]]
                    for i in tmp_list:
                        yaml_dependencies.add(i)
                fi.close()

        except KeyError:
            return yaml_dependencies

        return yaml_dependencies

    def _get_dependencies_from_pipfile(self) -> set:
        pip_dependencies = set()
        try:
            path = self.dependecies_file_found["Pipfile"]
            if path is not None:
                data = toml.load(path)
                tmp_list = [x.split("=")[0] for x in data["dev-packages"]]
                for i in tmp_list:
                    pip_dependencies.add(i)
        except KeyError:
            return pip_dependencies

        return pip_dependencies

    def _get_dependencies_from_setup(self) -> set:
        setup_dependencies = set()
        try:
            path = self.dependecies_file_found["setup.py"]
            if path is not None:
                with open(path, "r") as fi:
                    row_file = fi.read()
                    point = row_file.find("install_requires")
                    if point != -1:
                        tmp = row_file[point:-2]
                        tmp = tmp.replace("install_requires=[", "")
                        tmp = tmp.replace("]", "").strip()
                        tmp = tmp.replace('"', "").strip()
                        tmp = tmp.replace("<", "").strip()
                        tmp = tmp.replace(">", "").strip()
                        tmp_split = tmp.split(",")
                        for x in tmp_split:
                            tmp = x.split("=")[0]
                            setup_dependencies.add(tmp.strip())
                fi.close()
        except KeyError:
            return setup_dependencies

        return setup_dependencies

    def _get_core_dependecies(self) -> set:
        coredependecies = set()
        for name in sorted(stdlib):
            coredependecies.add(name)
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
