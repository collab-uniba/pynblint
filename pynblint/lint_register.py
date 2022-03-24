from typing import List, Set

from .config import settings
from .lint import LintDefinition, LintLevel

enabled_cell_level_lints: List[LintDefinition] = []
enabled_notebook_level_lints: List[LintDefinition] = []
enabled_path_level_lints: List[LintDefinition] = []
enabled_project_level_lints: List[LintDefinition] = []


def exclude_lints(
    available_lints: List[LintDefinition], lints_to_exclude: Set[str]
) -> List[LintDefinition]:
    """Filter the list of lint definitions based on the setting ``exclude``."""
    return [lint for lint in available_lints if lint.slug not in lints_to_exclude]


def include_lints(
    available_lints: List[LintDefinition], lints_to_include: Set[str]
) -> List[LintDefinition]:
    """Filter the list of lint definitions based on the setting ``include``."""

    return [lint for lint in available_lints if lint.slug in lints_to_include]


def register_lints(lint_level: LintLevel, lint_defs: List[LintDefinition]) -> None:

    # filter the list of lint definitions based on the settings
    if settings.exclude:
        filtered_lint_defs = exclude_lints(lint_defs, settings.exclude)
    elif settings.include:
        filtered_lint_defs = include_lints(lint_defs, settings.include)
    else:
        filtered_lint_defs = lint_defs

    # Add the filtered list of lints to the global list
    if lint_level == LintLevel.CELL:
        enabled_cell_level_lints.extend(filtered_lint_defs)
    elif lint_level == LintLevel.NOTEBOOK:
        enabled_notebook_level_lints.extend(filtered_lint_defs)
    elif lint_level == LintLevel.PATH:
        enabled_path_level_lints.extend(filtered_lint_defs)
    elif lint_level == LintLevel.PROJECT:
        enabled_project_level_lints.extend(filtered_lint_defs)
