import json
import os
import shutil
import stat
import zipfile
from os import path
from pathlib import Path

import git
import nbformat
from nbconvert import PythonExporter

import config
import pynblint


class Notebook:
    """
    This class stores the representations of a notebook
    on which pynblint functions are called
    """

    # Notebook info
    path: Path

    # Notebook representations
    nb_dict: dict
    script: str

    def __init__(self, notebook_path: Path):
        self.path = notebook_path

        # Read the raw notebook file
        with open(self.path) as f:
            _nb_raw = f.read()

        # Convert the notebook to a Python dictionary
        self.nb_dict = json.loads(_nb_raw)

        # Convert the notebook to a Python script
        _nb_node = nbformat.reads(_nb_raw, as_version=self.nb_dict['nbformat'])
        python_exporter = PythonExporter()
        self.script, _ = python_exporter.from_notebook_node(_nb_node)

    @classmethod
    def from_string(cls, path_string: str):
        """
        Create a Notebook object from a string representing a valid path
        """
        p = Path(path_string)
        return cls(p)

    def get_pynblint_results(self, bottom_size: int = 4):
        """
        Organize the linting results from all the repo notebooks
        """

        try:
            nb_path = str(self.path.relative_to(config.data_path))
        except ValueError:
            nb_path = str(self.path)

        results = {
            "notebookName": nb_path,
            "notebookStats": {
                "numberOfCells": pynblint.count_cells(self),
                "numberOfMDCells": pynblint.count_md_cells(self),
                "numberOfCodeCells": pynblint.count_code_cells(self),
                "numberOfRawCells": pynblint.count_raw_cells(self),
            },
            "lintingResults": {
                "linearExecutionOrder": pynblint.has_linear_execution_order(self),
                "numberOfClassDefinitions": pynblint.count_class_defs(self),
                "numberOfFunctionDefinitions": pynblint.count_func_defs(self),
                "allImportsInFirstCell": pynblint.are_imports_in_first_cell(self),
                "numberOfMarkdownLines": pynblint.count_md_lines(self),
                "numberOfMarkdownTitles": pynblint.count_md_titles(self),
                "bottomMarkdownLinesRatio": pynblint.get_bottom_md_lines_ratio(self),
                "nonExecutedCells": pynblint.count_non_executed_cells(self),
                "emptyCells": pynblint.count_empty_cells(self),
                "bottomNonExecutedCells": pynblint.count_bottom_non_executed_cells(self, bottom_size),
                "bottomEmptyCells": pynblint.count_bottom_empty_cells(self, bottom_size)
            }
        }
        return results


class Repository:
    """
    This class stores data about a code repository
    """

    # Repository info
    path: Path

    # Extracted content
    notebooks: list[Notebook] = []  # List of Notebook objects

    def get_pynblint_results(self):
        """Function takes a list of notebook objects and returns a list of dictionaries containg the linting results"""
        data = []
        for notebook in self.notebooks:
            data.append(notebook.get_pynblint_results())
        return data


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


class LocalRepository(Repository):
    """
    This class stores data about a local code repository
    """

    # Repository info
    source_path: Path

    def __init__(self, source_path: Path):
        self.source_path = source_path

        # Handle .zip archives
        if self.source_path.suffix == '.zip':
            with zipfile.ZipFile(self.source_path, 'r') as zip_file:
                zip_file.extractall(config.data_path)
            self.path = config.data_path / self.source_path.stem
            self.retrieve_notebooks()
            self.delete_repository()

        # Handle local folders
        elif self.source_path.is_dir():
            self.path = self.source_path
            self.retrieve_notebooks()

        else:
            raise Exception  # TODO: raise a more specific exception

    @classmethod
    def from_string(cls, path_string: str):
        """
        Create a LocalRepository object from a string representing a valid path
        """
        p = Path(path_string)
        return cls(p)


class GitHubRepository(Repository):
    """
    This class stores data about a GitHub repository
    """

    # Repository info
    url: str

    def __init__(self, github_url: str):
        self.url = github_url

        # Clone the repo
        git.Git(config.data_path).clone(github_url, depth=1)
        self.path = config.data_path / github_url.split("/")[-1]

        # Analyze the repo
        self.retrieve_notebooks()
        self.delete_repository()