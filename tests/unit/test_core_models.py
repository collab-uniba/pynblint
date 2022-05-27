from pathlib import Path
from typing import Dict, Set

import pytest

from pynblint.core_models import LocalRepository, Notebook, Repository

if __name__ == "__main__":
    pytest.main()


# ************* #
# TEST NOTEBOOK #
# ************* #


@pytest.fixture(scope="module")
def notebooks() -> Dict[str, Notebook]:
    nb1 = Notebook(Path("tests/fixtures", "FullNotebook2.ipynb"))
    nb2 = Notebook(Path("tests/fixtures", "Untitled2.ipynb"))
    return {"FullNotebook2.ipynb": nb1, "Untitled2.ipynb": nb2}


def test_standalone_notebook_constructor():
    """Tests the contruction of a standalone ``Notebook`` object."""

    notebook_path: Path = Path("tests", "fixtures", "FullNotebook2.ipynb")
    notebook: Notebook = Notebook(notebook_path)

    assert notebook.repository is None


def test_notebook_from_repo_constructor():
    """Tests the construction of a ``Notebook`` object extracted from a repository."""

    repo_path: Path = Path("tests", "fixtures", "test_repo", "UntitledNoDuplicates")
    repository: LocalRepository = LocalRepository(repo_path)
    notebook: Notebook = repository.notebooks[0]

    assert notebook.repository is not None
    assert notebook.repository.path == repo_path


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("FullNotebook2.ipynb", {"os"}),
        ("Untitled2.ipynb", set()),
    ],
)
def test_get_imported_packages(test_input, expected, notebooks):
    assert Notebook._get_imported_packages(notebooks[test_input]) == expected


# *************** #
# TEST REPOSITORY #
# *************** #

# Parsing project requirements from:
# environment.yaml


@pytest.fixture()
def environment_yaml() -> Dict[str, Path]:

    BASE_PATH = Path("tests/fixtures/requirement_files/conda/")
    environment_yaml_1: Path = BASE_PATH / "environment_1.yaml"
    environment_yaml_2: Path = BASE_PATH / "environment_2.yaml"
    environment_yaml_3: Path = BASE_PATH / "environment_3.yaml"

    return {
        "environment_1.yaml": environment_yaml_1,
        "environment_2.yaml": environment_yaml_2,
        "environment_3.yaml": environment_yaml_3,
    }


@pytest.fixture()
def environment_yaml_keys() -> Dict[str, Set[str]]:
    BASE_PATH = Path("tests/fixtures/requirement_files/conda/")
    environment_yaml_1_keys_file_path: Path = BASE_PATH / "environment_1_yaml.txt"
    with open(environment_yaml_1_keys_file_path, "r") as f:
        environment_yaml_1_keys = {line.rstrip() for line in f.readlines()}

    environment_yaml_2_keys_file_path: Path = BASE_PATH / "environment_2_yaml.txt"
    with open(environment_yaml_2_keys_file_path, "r") as f:
        environment_yaml_2_keys = {line.rstrip() for line in f.readlines()}

    environment_yaml_3_keys_file_path: Path = BASE_PATH / "environment_3_yaml.txt"
    with open(environment_yaml_3_keys_file_path, "r") as f:
        environment_yaml_3_keys = {line.rstrip() for line in f.readlines()}

    return {
        "environment_1.yaml": environment_yaml_1_keys,
        "environment_2.yaml": environment_yaml_2_keys,
        "environment_3.yaml": environment_yaml_3_keys,
    }


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("environment_1.yaml", "environment_1.yaml"),
        ("environment_2.yaml", "environment_2.yaml"),
        ("environment_3.yaml", "environment_3.yaml"),
    ],
)
def test_get_requirements_from_yaml(
    test_input, expected, environment_yaml, environment_yaml_keys
):
    assert (
        Repository._get_requirements_from_yaml(environment_yaml[test_input])
        == environment_yaml_keys[expected]
    )


# Parsing project requirements from:
# requirements.txt


@pytest.fixture()
def requirements_txt() -> Dict[str, Path]:

    BASE_PATH = Path("tests/fixtures/requirement_files/pip/")
    requirements_txt_1: Path = BASE_PATH / "requirements_1.txt"
    requirements_txt_2: Path = BASE_PATH / "requirements_2.txt"
    requirements_txt_3: Path = BASE_PATH / "requirements_3.txt"

    return {
        "requirements_1.txt": requirements_txt_1,
        "requirements_2.txt": requirements_txt_2,
        "requirements_3.txt": requirements_txt_3,
    }


@pytest.fixture()
def requirements_txt_keys() -> Dict[str, Set[str]]:
    BASE_PATH = Path("tests/fixtures/requirement_files/pip/")
    requirements_txt_1_keys_file_path: Path = BASE_PATH / "requirements_1_txt.txt"
    with open(requirements_txt_1_keys_file_path, "r") as f:
        requirements_txt_1_keys = {line.rstrip() for line in f.readlines()}

    requirements_txt_2_keys_file_path: Path = BASE_PATH / "requirements_2_txt.txt"
    with open(requirements_txt_2_keys_file_path, "r") as f:
        requirements_txt_2_keys = {line.rstrip() for line in f.readlines()}

    requirements_txt_3_keys_file_path: Path = BASE_PATH / "requirements_3_txt.txt"
    with open(requirements_txt_3_keys_file_path, "r") as f:
        requirements_txt_3_keys = {line.rstrip() for line in f.readlines()}

    return {
        "requirements_1.txt": requirements_txt_1_keys,
        "requirements_2.txt": requirements_txt_2_keys,
        "requirements_3.txt": requirements_txt_3_keys,
    }


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("requirements_1.txt", "requirements_1.txt"),
        ("requirements_2.txt", "requirements_2.txt"),
        ("requirements_3.txt", "requirements_3.txt"),
    ],
)
def test_get_requirements_from_txt(
    test_input, expected, requirements_txt, requirements_txt_keys
):
    assert (
        Repository._get_requirements_from_txt(requirements_txt[test_input])
        == requirements_txt_keys[expected]
    )


# Parsing project requirements from:
# pyproject.toml


@pytest.fixture()
def pyproject_toml() -> Dict[str, Path]:

    BASE_PATH = Path("tests/fixtures/requirement_files/poetry/")
    pyproject_toml_1: Path = BASE_PATH / "pyproject_1.toml"
    pyproject_toml_2: Path = BASE_PATH / "pyproject_2.toml"

    return {
        "pyproject_1.toml": pyproject_toml_1,
        "pyproject_2.toml": pyproject_toml_2,
    }


@pytest.fixture()
def pyproject_toml_keys() -> Dict[str, Set[str]]:
    BASE_PATH = Path("tests/fixtures/requirement_files/poetry/")
    pyproject_toml_1_keys_file_path: Path = BASE_PATH / "pyproject_1_toml.txt"
    with open(pyproject_toml_1_keys_file_path, "r") as f:
        pyproject_toml_1_keys = {line.rstrip() for line in f.readlines()}

    pyproject_toml_2_keys_file_path: Path = BASE_PATH / "pyproject_2_toml.txt"
    with open(pyproject_toml_2_keys_file_path, "r") as f:
        pyproject_toml_2_keys = {line.rstrip() for line in f.readlines()}

    return {
        "pyproject_1.toml": pyproject_toml_1_keys,
        "pyproject_2.toml": pyproject_toml_2_keys,
    }


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("pyproject_1.toml", "pyproject_1.toml"),
        ("pyproject_2.toml", "pyproject_2.toml"),
    ],
)
def test_get_requirements_from_toml(
    test_input, expected, pyproject_toml, pyproject_toml_keys
):
    assert (
        Repository._get_requirements_from_toml(pyproject_toml[test_input])
        == pyproject_toml_keys[expected]
    )
