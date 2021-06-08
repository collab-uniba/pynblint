import os
import shutil
import stat
import zipfile
from os import path
from pathlib import Path
from typing import List

import git

from pynblint.notebook import Notebook
from pynblint import config


class Repository:
    """
    This class stores data about a code repository
    """

    def __init__(self):

        # Repository info
        self.path: Path = None

        # Extracted content
        self.notebooks: List[Notebook] = []  # List of Notebook objects

    def retrieve_notebooks(self):

        # Directories to ignore while traversing the tree
        dirs_ignore = [
            '.ipynb_checkpoints'
        ]

        for root, dirs, files in os.walk(self.path):
            # `dirs[:] = value` modifies dirs in-place
            dirs[:] = [d for d in dirs if d not in dirs_ignore]
            for f in files:
                if f.endswith(".ipynb"):
                    nb = Notebook(Path(root) / Path(f))
                    self.notebooks.append(nb)

    def delete_repository(self):
        for root, dirs, files in os.walk(self.path):
            for d in dirs:
                os.chmod(path.join(root, d), stat.S_IRWXU)
            for f in files:
                os.chmod(path.join(root, f), stat.S_IRWXU)
        shutil.rmtree(self.path)

    def get_pynblint_results(self):
        """
        Returns a list of dictionaries containing the linting results for all the notebooks found in the repository
        """
        data = []
        for notebook in self.notebooks:
            data.append(notebook.get_pynblint_results())
        return data


class LocalRepository(Repository):
    """
    This class stores data about a local code repository
    """

    def __init__(self, source_path: Path):
        super().__init__()
        self.source_path = source_path

        # Handle .zip archives
        if self.source_path.suffix == '.zip':
            with zipfile.ZipFile(self.source_path, 'r') as zip_file:
                zip_file.extractall(config.temp_data_dir_path)
            self.path = config.temp_data_dir_path / self.source_path.stem
            self.retrieve_notebooks()
            self.delete_repository()

        # Handle local folders
        elif self.source_path.is_dir():
            self.path = self.source_path
            self.retrieve_notebooks()

        else:
            raise Exception  # TODO: raise a more specific exception


class GitHubRepository(Repository):
    """
    This class stores data about a GitHub repository
    """

    def __init__(self, github_url: str):
        super().__init__()
        self.url = github_url

        # Clone the repo
        git.Git(config.temp_data_dir_path).clone(github_url, depth=1)
        self.path = config.temp_data_dir_path / github_url.split("/")[-1]

        # Analyze the repo
        self.retrieve_notebooks()
        self.delete_repository()
