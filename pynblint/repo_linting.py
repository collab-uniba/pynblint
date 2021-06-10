import os
from pynblint import nb_linting


def get_duplicate_notebooks(repo):
    nb_filenames = []
    duplicate_filanames = []
    paths = []
    for notebook in repo.notebooks:
        filename = os.path.basename(notebook.path)
        if filename in nb_filenames:
            duplicate_filanames.append(filename)
        else:
            nb_filenames.append(filename)
    for filename in duplicate_filanames:
        for notebook in repo.notebooks:
            if os.path.basename(notebook.path) == filename:
                paths.append(notebook.path)
    return paths


def get_untitled_paths(repo):
    untitled_notebooks = []
    for notebook in repo.notebooks:
        if nb_linting.is_untitled(notebook):
            untitled_notebooks.append(notebook.path)
    return untitled_notebooks
