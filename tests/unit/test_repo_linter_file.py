from pathlib import Path
from typing import Dict

import pytest

from pynblint.repository import Repository

if __name__ == "__main__":
    pytest.main()


@pytest.fixture(scope="module")
def repo_linters() -> Dict[str, Repository]:
    nb1 = Repository(Path("tests/fixtures", "requirement.txt"))
    nb2 = Repository(Path("tests/fixtures", "enviroment.yaml"))
    nb3 = Repository(Path("tests/fixtures", "Pipfile"))
    nb4 = Repository(Path("tests/fixtures", "setup.py"))
    nb5 = Repository(Path("pynblint", "pyproject.toml"))
    return {
        "requirement.txt": nb1,
        "enviroment.yaml": nb2,
        "Pipfile": nb3,
        "setup.py": nb4,
        "pyproject.toml": nb5,
    }


# these test fail because of PermissionError: [Errno 13] Permission denied: '.'
# i'm trying to fix it
def test__get_txt_dependencies(repo_linters):
    expected = {
        "",
        "rich",
        "defusedxml",
        "pyparsing",
        "pyrsistent",
        "traitlets",
        "certifi",
        "commonmark",
        "mistune",
        "smmap",
        "urllib3",
        "jupyter-core",
        "nbclient",
        "Babel",
        "nbconvert",
        "Sphinx",
        "typing_extensions",
        "sphinxcontrib-qthelp",
        "imagesize",
        "jupyter-client",
        "ipython-genutils",
        "webencodings",
        "packaging",
        "sphinxcontrib-htmlhelp",
        "sphinxcontrib-devhelp",
        "zipp",
        "Pygments",
        "sphinxcontrib-applehelp",
        "importlib-metadata",
        "bleach",
        "Jinja2",
        "MarkupSafe",
        "tornado",
        "nbformat",
        "attrs",
        "pyzmq",
        "gitdb",
        "six",
        "idna",
        "importlib-resources",
        "python-dateutil",
        "jupyterlab-pygments",
        "pydantic",
        "GitPython",
        "entrypoints",
        "requests",
        "testpath",
        "docutils",
        "sphinx-rtd-theme",
        "alabaster",
        "nest-asyncio",
        "charset-normalizer",
        "sphinxcontrib-jsmath",
        "sphinxcontrib-serializinghtml",
        "snowballstemmer",
        "pytz",
        "pandocfilters",
        "jsonschema",
    }
    txt_dependecies = Repository._get_dependencies_from_txt(
        repo_linters["requirement.txt"]
    )
    assert txt_dependecies.issubset(expected)


def test__get_yaml_dependencies(repo_linters):
    expected = {"Flask", "PyYAML", "psycopg2"}
    assert (
        Repository._get_dependencies_from_yaml(repo_linters["enviroment.yaml"])
        == expected
    )


def test__get_pipfile_dependencies(repo_linters):
    expected = {
        "invoke",
        "sphinx-rtd-theme",
        "wheel",
        "parver",
        "twine",
        "pytest-cov",
        "pytest-xdist",
        "sphinx",
        "pytest",
        "towncrier",
    }
    assert (
        Repository._get_dependencies_from_pipfile(repo_linters["Pipfile"]) == expected
    )


def test__get_setup_dependencies(repo_linters):
    expected = {"", "matplotlib", "numpy"}
    assert Repository._get_dependencies_from_setup(repo_linters["setup.py"]) == expected


def test__get_toml_dependencies(repo_linters):
    expected = {
        "pytest",
        "mypy",
        "bandit",
        "pytest-cov",
        "coverage",
        "isort",
        "black",
        "flake8",
        "pylint",
        "pydocstyle",
        "pre-commit",
        "jupyterlab",
    }
    assert (
        Repository._get_dependencies_from_toml(repo_linters["pyproject.toml"])
        == expected
    )
