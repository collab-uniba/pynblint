from typing import List

import pynblint.lint_register as register
from pynblint.lint import LintDefinition, LintLevel
from pynblint.notebook import Notebook


def example_plugin_lint(notebook: Notebook) -> bool:
    """Check whether the notebook has at least one executed cell."""
    return any([cell.exec_count is not None for cell in notebook.code_cells])


notebook_level_lints: List[LintDefinition] = [
    LintDefinition(
        slug="example-plugin-lint",
        description="This is just an example.",
        recommendation="Nothing to recommend",
        linting_function=example_plugin_lint,
    )
]


def initialize() -> None:
    register.register_lints(LintLevel.NOTEBOOK, notebook_level_lints)
