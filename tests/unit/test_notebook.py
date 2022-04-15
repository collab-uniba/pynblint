from pathlib import Path
from typing import Dict

import pytest

from pynblint.notebook import Notebook


@pytest.fixture(scope="module")
def notebooks() -> Dict[str, Notebook]:
    nb1 = Notebook(Path("tests/fixtures", "FullNotebook2.ipynb"))
    nb2 = Notebook(Path("tests/fixtures", "FullNotebookFullNotebookFullNotebook.ipynb"))
    return {
        "FullNotebook2.ipynb": nb1,
        "FullNotebookFullNotebookFullNotebook.ipynb": nb2,
    }


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "FullNotebook2.ipynb",
            [
                '13:convention:C0413:wrong-import-position:Import "import os" should '
                "be placed at the top of the module",
                "14:convention:C0115:missing-class-docstring:Missing class docstring",
                "14:refactor:R0903:too-few-public-methods:Too few public methods (0/2)",
                "13:warning:W0611:unused-import:Unused import os",
            ],
        ),
        (
            "FullNotebookFullNotebookFullNotebook.ipynb",
            [
                '8:convention:C0413:wrong-import-position:Import "import os" should be '
                "placed at the top of the module",
                "14:convention:C0116:missing-function-docstring:Missing function or "
                "method docstring",
                "15:warning:W0612:unused-variable:Unused variable 'x'",
                "8:warning:W0611:unused-import:Unused import os",
            ],
        ),
    ],
)
def test_lint_notebook_code_with_pylint(test_input, expected, notebooks):
    assert notebooks[test_input].lint_notebook_code_with_pylint() == expected
