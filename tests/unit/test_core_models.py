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
def test_get_yaml_dependencies(
    test_input, expected, environment_yaml, environment_yaml_keys
):
    assert (
        Repository._get_requirements_from_yaml(environment_yaml[test_input])
        == environment_yaml_keys[expected]
    )
