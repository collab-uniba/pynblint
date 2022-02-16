from enum import Enum

from pydantic import BaseSettings


class CellRenderingMode(str, Enum):
    FULL = "full"
    COMPACT = "compact"


class Settings(BaseSettings):

    cell_rendering_mode: CellRenderingMode = CellRenderingMode.COMPACT
    display_cell_index: bool = False

    class Config:
        env_file = ".pynblint"
        env_file_encoding = "utf-8"


settings = Settings()
