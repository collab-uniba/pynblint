import config
import git
import json
import os
from os import path
import stat
import zipfile
import shutil
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
        with open(notebook_path.replace(".ipynb", ".py")) as f:
            self.script = f.read()


class Repository:
    """
    This class stores data about a code repository
    """

    notebooks = []  # List of Notebook objects

    def retrieve_notebooks(self, repo_path):
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".ipynb"):
                    file_path = os.path.join(root, file).replace('\\', '/')
                    nb = Notebook(file_path)
                    nb.path = file_path[8:]
                    self.notebooks.append(nb)
                    os.remove(file[:-5] + "py")
        for root, dirs, files in os.walk(repo_path):
            for dir in dirs:
                os.chmod(path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(path.join(root, file), stat.S_IRWXU)
        shutil.rmtree(repo_path)


class LocalRepository(Repository):
    """
    This class stores data about a local code repository
    """

    def __init__(self, path: str):
        project_path = path
        if path.endswith('.zip'):
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(config.data_path)
                project_path = config.data_path+(path.split("/")[-1])[:-4]
        self.retrieve_notebooks(project_path)


class GitHubRepository(Repository):
    """
    This class stores data about a GitHub repository
    """

    def __init__(self, github_url: str):
        git.Git(config.data_path).clone(github_url)
        repo_path = config.data_path+(github_url.split("/")[-1])
        self.retrieve_notebooks(repo_path)