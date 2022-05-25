from pathlib import Path
from typing import Dict

import pytest

from pynblint.repository import Repository

if __name__ == "__main__":
    pytest.main()


@pytest.fixture(scope="module")
def repository() -> Dict[str, Repository]:
    nb1 = Repository(Path("pynblint/docs"))
    nb2 = Repository(Path("pynblint/tests/fixtures"))
    nb3 = Repository(Path("pynblint/tests/fixtures"))
    nb4 = Repository(Path("pynblint/tests/fixtures"))
    nb5 = Repository(Path("pynblint"))
    return {
        "requirements.txt": nb1,
        "enviroment.yaml": nb2,
        "Pipfile": nb3,
        "setup.py": nb4,
        "pyproject.toml": nb5,
    }


# these test fail because of PermissionError: [Errno 13] Permission denied: '.'
# i'm trying to fix it
def test__get_txt_dependencies(repository):
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

    assert Repository._get_dependencies_from_txt(
        repository["requirements.txt"]
    ).intersection(expected) == Repository._get_dependencies_from_txt(
        repository["requirements.txt"]
    )


def test__get_yaml_dependencies(repository):
    expected = {"Flask", "PyYAML", "psycopg2"}
    assert Repository._get_dependencies_from_yaml(
        repository["enviroment.yaml"]
    ).intersection(expected) == Repository._get_dependencies_from_yaml(
        repository["enviroment.yaml"]
    )


def test__get_pipfile_dependencies(repository):
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
    assert Repository._get_dependencies_from_pipfile(
        repository["Pipfile"]
    ).intersection(expected) == Repository._get_dependencies_from_pipfile(
        repository["Pipfile"]
    )


def test__get_setup_dependencies(repository):
    expected = {"", "matplotlib", "numpy"}
    assert Repository._get_dependencies_from_setup(repository["setup.py"]).intersection(
        expected
    ) == Repository._get_dependencies_from_setup(repository["setup.py"])


def test__get_toml_dependencies(repository):
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
    assert Repository._get_dependencies_from_toml(
        repository["pyproject.toml"]
    ).intersection(expected) == Repository._get_dependencies_from_toml(
        repository["pyproject.toml"]
    )
