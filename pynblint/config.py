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
