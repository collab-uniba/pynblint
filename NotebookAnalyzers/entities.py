import config
import git
import json
import os
from os import path
import stat
import zipfile
import shutil
import pynblint
from notebooktoall.transform import transform_notebook


class Notebook:
    """
    This class stores the representations of a notebook
    on which pynblint functions are called
    """

    def __init__(self, notebook_path: str):
        # Importing the notebook as a Python dictionary
        with open(notebook_path) as f:
            self.nb_dict = json.load(f)

        # Importing the notebook as a Python script
        transform_notebook(ipynb_file=notebook_path, export_list=["py"])
        notebook_path = notebook_path.split("/")[-1]
        self.path = notebook_path
        with open(notebook_path.replace(".ipynb", ".py")) as f:
            self.script = f.read()

    def get_pynblint_results(self, bottom_size=4):
        results = {
            "notebookName": self.path,
            #"notebookStats":
            #    {
                    "numberOfCells": pynblint.count_cells(self),
                    "numberOfMDCells": pynblint.count_md_cells(self),
                    "numberOfCodeCells": pynblint.count_code_cells(self),
                    "numberOfRawCells": pynblint.count_raw_cells(self),
            #    },
            #"lintingResults":
            #    {
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
            #    }
        }
        return results


class Repository:
    """
    This class stores data about a code repository
    """

    notebooks = []  # List of Notebook objects

    def retrieve_notebooks(self):
        for root, dirs, files in os.walk(self.path):
            for dir in dirs:
                os.chmod(path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(path.join(root, file), stat.S_IRWXU)
                if file.endswith(".ipynb"):
                    file_path = os.path.join(root, file).replace('\\', '/')
                    nb = Notebook(file_path)
                    nb.path = file_path[8:]
                    self.notebooks.append(nb)
                    os.remove(file[:-5] + "py")
        shutil.rmtree(self.path)


class LocalRepository(Repository):
    """
    This class stores data about a local code repository
    """

    def __init__(self, local_path: str):
        self.path = local_path
        if local_path.endswith('.zip'):
            with zipfile.ZipFile(local_path, 'r') as zip_ref:
                zip_ref.extractall(config.data_path)
                self.path = config.data_path + (local_path.split("/")[-1])[:-4]
            self.retrieve_notebooks()
        elif path.isdir(local_path):
            self.retrieve_notebooks()
        else:
            raise Exception


class GitHubRepository(Repository):
    """
    This class stores data about a GitHub repository
    """

    def __init__(self, github_url: str):
        git.Git(config.data_path).clone(github_url, depth=1)
        self.path = config.data_path + (github_url.split("/")[-1])
        self.retrieve_notebooks()
