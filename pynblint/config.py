from enum import Enum
from typing import List, Optional, Set

from pydantic import BaseSettings


class CellRenderingMode(str, Enum):
    FULL = "full"
    COMPACT = "compact"


class Settings(BaseSettings):

    plugins: List[str] = []
    include: Optional[Set[str]] = None
    exclude: Optional[Set[str]] = None
    hide_stats: bool = False
    hide_recommendations: bool = False
    cell_rendering_mode: CellRenderingMode = CellRenderingMode.COMPACT
    result_details_indentation: int = 5
    display_cell_index: bool = False
    filename_max_length: int = 0
    max_cells_in_notebook: int = 50
    max_lines_in_code_cell: int = 30
    initial_cells: int = 3
    final_cells: int = 3
    min_md_code_ratio: float = 0.3
    max_data_file_size: int = 10 * 1000000  # 10MB

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
