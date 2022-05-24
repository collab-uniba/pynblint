from pathlib import Path
from typing import Dict

import pytest

from pynblint.notebook import Notebook

if __name__ == "__main__":
    pytest.main()


@pytest.fixture(scope="module")
def notebooks() -> Dict[str, Notebook]:
    nb1 = Notebook(Path("tests/fixtures", "FullNotebook2.ipynb"))
    nb2 = Notebook(Path("tests/fixtures", "Untitled2.ipynb"))
    return {"FullNotebook2.ipynb": nb1, "Untitled2.ipynb": nb2}


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("FullNotebook2.ipynb", {"os"}),
        ("Untitled2.ipynb", set()),
    ],
)
def test_get_imported_packages(test_input, expected, notebooks):
    assert Notebook.get_imported_packages(notebooks[test_input]) == expected
