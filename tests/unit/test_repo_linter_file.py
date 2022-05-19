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
    nb5 = Repository(Path("pynblint", "poetry.lock"))
    nb6 = Repository(Path("pynblint", "pyproject.toml"))
    return {
        "requirement.txt": nb1,
        "enviroment.yaml": nb2,
        "Pipfile": nb3,
        "setup.py": nb4,
        "poetry.lock": nb5,
        "pyproject.toml": nb6,
    }


@pytest.mark.parametrize(
    "test_input,expected",
    [("pyproject.toml", set())],
)
def test__get_toml_dependencies(test_input, expected, repo_linters):
    assert Repository._get_toml_dependencies(repo_linters[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("requirement.txt", set())],
)
def test__get_txt_dependencies(test_input, expected, repo_linters):
    assert Repository._get_txt_dependencies(repo_linters[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("enviroment.yaml", set())],
)
def test__get_yaml_dependencies(test_input, expected, repo_linters):
    assert Repository._get_yaml_dependencies(repo_linters[test_input]) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("Pipfile", set())],
)
def test__get_Pipfile_dependencies(test_input, expected, repo_linters):
    assert Repository._get_Pipfile_dependencies == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("setup.py", set())],
)
def test__get_Setup_dependencies(test_input, expected, repo_linters):
    assert Repository._get_Setup_dependencies(repo_linters[test_input]) == expected
