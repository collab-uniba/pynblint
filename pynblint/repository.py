import git
import os
import tempfile
import zipfile
from pathlib import Path
from typing import List

from pynblint.notebook import Notebook


class Repository:
    """
    This class stores data about a code repository
    """

    def __init__(self):

        # Repository info
        self.path = None

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
                    nb = Notebook(Path(root) / Path(f), repository_path=self.path)
                    self.notebooks.append(nb)

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

            # Create temp directory
            tmp_dir = tempfile.TemporaryDirectory()

            # Extract the zip file into the temp folder
            with zipfile.ZipFile(self.source_path, 'r') as zip_file:
                zip_file.extractall(tmp_dir.name)
            self.path = Path(tmp_dir.name) / self.source_path.stem
            self.retrieve_notebooks()

            # Clean up the temp directory
            tmp_dir.cleanup()

        # Handle local folders
        elif self.source_path.is_dir():
            self.path = self.source_path
            self.retrieve_notebooks()

        else:
            raise Exception  # TODO: raise a more meaningful exception


class GitHubRepository(Repository):
    """
    This class stores data about a GitHub repository
    """

    def __init__(self, github_url: str):
        super().__init__()
        self.url = github_url

        # Create temp directory
        tmp_dir = tempfile.TemporaryDirectory()

        # Clone the repo into the temp directory
        git.Git(tmp_dir.name).clone(github_url, depth=1)
        self.path = Path(tmp_dir.name) / github_url.split("/")[-1]

        # Analyze the repo
        self.retrieve_notebooks()

        # Clean up the temp directory
        tmp_dir.cleanup()
