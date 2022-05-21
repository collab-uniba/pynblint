from pathlib import Path
from typing import Dict

import pytest

from pynblint import repo_linting
from pynblint.core_models import Repository


@pytest.fixture(scope="module")
def repositories() -> Dict[str, Repository]:

    repo_fixtures_base_path: Path = Path("tests/fixtures/test_repo")

    repo1 = Repository(repo_fixtures_base_path / "UntitledNoDuplicates")
    repo2 = Repository(repo_fixtures_base_path / "versioned_repo_with_coverage")
    return {
        "UntitledNoDuplicates": repo1,
        "versioned_repo_with_coverage": repo2,
    }


@pytest.mark.parametrize(
    "test_input, expected",
    [("UntitledNoDuplicates", True), ("versioned_repo_with_coverage", False)],
)
def test_coverage_data_not_available(test_input, expected, repositories):
    assert (
        repo_linting.coverage_data_not_available(repositories[test_input]) == expected
    )
