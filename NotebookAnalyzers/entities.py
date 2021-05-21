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

        # TODO: handle exceptions

    def get_pynblint_results(self, bottom_size: int = 4):
        notebook_tuple = (str(self.path.relative_to(config.data_path)),
                          pynblint.has_linear_execution_order(self),
                          pynblint.count_class_defs(self),
                          pynblint.count_func_defs(self),
                          pynblint.are_imports_in_first_cell(self),
                          pynblint.count_md_lines(self),
                          pynblint.count_md_titles(self),
                          pynblint.get_bottom_md_lines_ratio(self),
                          pynblint.count_non_executed_cells(self),
                          pynblint.count_empty_cells(self),
                          pynblint.count_bottom_non_executed_cells(self, bottom_size),
                          pynblint.count_bottom_empty_cells(self, bottom_size),
                          pynblint.count_cells(self),
                          pynblint.count_md_cells(self),
                          pynblint.count_code_cells(self),
                          pynblint.count_raw_cells(self)
                          )
        return notebook_tuple


class Repository:
    """
    This class stores data about a code repository
    """

    # Repository info
    path: Path

    # Extracted content
    notebooks: list[Notebook] = []  # List of Notebook objects

    def retrieve_notebooks(self):
        for root, dirs, files in os.walk(self.path):
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
            self.retrieve_notebooks()

        else:
            raise Exception  # TODO: raise a more specific exception


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
