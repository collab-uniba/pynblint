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
    """Filter the list of lint definitions based on the setting ``excluded_lints``."""
    return [lint for lint in available_lints if lint.slug not in lints_to_exclude]


def include_lints(
    available_lints: List[LintDefinition], lints_to_include: Set[str]
) -> List[LintDefinition]:
    """Filter the list of lint definitions based on the setting ``included_lints``."""

    return [lint for lint in available_lints if lint.slug in lints_to_include]


def register_lints(lint_level: LintLevel, lint_defs: List[LintDefinition]) -> None:

    # filter the list of lint definitions based on the settings
    if settings.excluded_lints:
        filtered_lint_defs = exclude_lints(lint_defs, settings.excluded_lints)
    elif settings.included_lints:
        filtered_lint_defs = include_lints(lint_defs, settings.included_lints)
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


# class LintFactory:
#     """Register of the active lints."""

#     # TODO: implement this class as a singleton.

#     def __init__(self, settings: Settings) -> None:
#         self.lint_constructors: Dict[str, Callable[..., Lint]] = {}
#         self.included_lints: Optional[Set[str]] = settings.included_lints
#         self.excluded_lints: Optional[Set[str]] = settings.excluded_lints

#         # Register lint classes
#         self.register(
#           nb_linting.NonLinearExecution.slug, nb_linting.NonLinearExecution
#         )

#     def register(self, slug: str, creation_func: Callable[..., Lint]):
#         """Register a new lint."""
#         self.lint_constructors[slug] = creation_func

#     def unregister(self, slug: str):
#         """Unregister a registered lint."""
#         self.lint_constructors.pop(slug, None)

#     def create(self, arguments: Dict[str, Any]) -> Lint:
#         """Create a lint of a specific type, given a dictionary of arguments.

#         The first item in the dictionary of arguments should represent
#         the slug of the lint to be created.
#         """
#         args_copy = arguments.copy()
#         lint_slug = args_copy.pop("slug")

#         try:
#             creation_func = self.lint_constructors[lint_slug]
#             return creation_func(**args_copy)
#         except KeyError:
#             raise ValueError(f"Unknown lint slug {lint_slug!r}")
