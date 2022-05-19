import os
import re
import tempfile
import zipfile
from abc import ABC
from pathlib import Path
from typing import List, Optional

import git
from isort.stdlibs.py39 import stdlib
from pipfile import Pipfile
from toml import dumps, loads
from yaml import dump, safe_load

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
        self.dependencies_module = self._get_txt_dependencies()
        self.core_library: set = self._get_core_dependecies()
        self.toml_dependencies: set = self._get_toml_dependencies()
        self.yaml_dependencies: set = self._get_yaml_dependencies()
        self.Pipfile_dependencies: set = self._get_Pipfile_dependencies()
        self.setup_dependencies: set = self._get_Setup_dependencies()

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

    def _get_txt_dependencies(self) -> set:
        txt_dependencies = set()
        final_path = os.path.join(self.path, "reqirement.txt")
        if os.path.exists(final_path):
            with open(final_path, "r") as fi:
                file_row = fi.read()
                tmp = file_row.split("\n")
                for item in tmp:
                    item.strip()
                    txt_dependencies.add(item.split("==")[0])
            # print("TXT DEPENDENCIES: \n")
            # print(txt_dependencies)

        return txt_dependencies

    def _get_yaml_dependencies(self) -> set:
        yaml_config = set()
        final_path = os.path.join(self.path, "enviroment.yaml")
        if os.path.exists(final_path):
            with open(final_path, "r") as fi:
                file_row = fi.read()
                data = safe_load(file_row)
                data_sorted = dump(data, sort_keys=True)
                data_line = data_sorted.split("\n")
                pattern = re.compile(r".*(-)\s(\w*){1}(\d)*(==).*$")
                for i in data_line:
                    if pattern.match(i):
                        tmp = i.replace("-", "")
                        tmp = tmp.split("==")[0]
                        yaml_config.add(tmp)
                # print("\n after add:\n")
                # for i in yaml_config:
                # print(i)

        return yaml_config

    def _get_toml_dependencies(self) -> set:
        toml_config = set()
        final_path = os.path.join(self.path, "pyproject.toml")
        if os.path.exists(final_path):
            with open(final_path, "r") as fi:
                file_row = fi.read()
                tmp = loads(file_row)
                new_toml_string = dumps(tmp)
                tmp_str = new_toml_string.split("\n")
                # print("\n\ntoml file: \n")
                pattern = re.compile(r".*(\w){1}(\d)*\s(=)\s\"\^(\d.)+$")
                for item in tmp_str:
                    if pattern.match(item):
                        item = item.replace("^", " ")
                        item = item.split("=")[0]
                        toml_config.add(item)
                """print("\nafter add\n\n")
                for i in toml_config:
                    print(i)"""

        return toml_config

    def _get_Pipfile_dependencies(self) -> set:
        pip_dependencies = set()
        tmp = str()
        pattern = re.compile(r"^(\w)*(\d)*")
        final_path = os.path.join(self.path, "Pipfile")

        if os.path.exists(final_path):
            parsed = Pipfile.load(filename=final_path)
            row_data = parsed.contents
            # il motivo per cui ho svolto in questo modo i successivi
            # 2 passaggi vorrei spiegarglielo durante il prossimo meeting
            low = row_data.find("[dev-packages]") + len("[dev-packages]")
            high = row_data.find("[scripts]")
            row3 = row_data[low:high]
            row3.strip()

            for i in row3.split("\n"):
                tmp2 = re.search(pattern, i)
                if tmp2 is not None:
                    tmp = tmp2.group()
                    if len(tmp) > 0:
                        pip_dependencies.add(tmp.strip())
        # print(pip_dependencies)

        return pip_dependencies

    def _get_Setup_dependencies(self) -> set:
        setup_dependencies = set()
        final_path = os.path.join(self.path, "setup.py")
        if os.path.exists(final_path):
            with open(final_path, "r") as fi:
                file_row = fi.read()
                tmp_str = file_row.split("\n")
                pattern = re.compile(r".*\"(\w)*\s(>)*(<)*(=)*\s(\d.)*(.\d)*\"")
                for item in tmp_str:
                    if pattern.match(item):
                        item.strip()
                        item = item.replace("    install_requires=[", "")
                        item = item.replace("]", "")
                        item = item.replace('"', "")
                        item = item.replace("<", "")
                        item = item.replace(">", "")
                        item_split = item.split(",")
                        for i in item_split:
                            setup_dependencies.add(i.split("=")[0].strip())
                        # for k in setup_dependencies:
                        # print(k)
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
