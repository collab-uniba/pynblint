from enum import Enum
from typing import List, Optional, Set

from pydantic import BaseSettings


class CellRenderingMode(str, Enum):
    FULL = "full"
    COMPACT = "compact"


class Settings(BaseSettings):

    plugins: List[str] = []
    included_lints: Optional[Set[str]] = None
    excluded_lints: Optional[Set[str]] = None
    cell_rendering_mode: CellRenderingMode = CellRenderingMode.COMPACT
    display_cell_index: bool = False

    # TODO: custom validation: included_lints OR excluded lints must be None
    #       I.e., something like:
    #
    # if (excluded_lints is not None) and (included_lints is not None):
    #     raise ValueError(
    #         "The arguments `excluded_lints` and `included_lints` cannot be used \
    #             at the same time. \
    #         Please, choose whether you need to specify the lints to be exluded \
    #             or those to be included."
    #     )

    class Config:
        env_file = ".pynblint"
        env_file_encoding = "utf-8"


settings = Settings()


# class LintRegister:
#     """Register of the active lints."""

#     # TODO: implement this class as a singleton.

#     CORE_LINTS: Dict[str, Callable[..., Lint]] = {}

#     def __init__(self, settings: Settings) -> None:
#         self.lint_constructors: Dict[str, Callable[..., Lint]] = {}
#         self.included_lints: Optional[Set[str]] = settings.included_lints
#         self.excluded_lints: Optional[Set[str]] = settings.excluded_lints

#         # Register lint classes
#         self.register(NonLinearExecution.slug, NonLinearExecution)

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
