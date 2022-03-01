"""Linting modules loader."""

import importlib
from typing import List

from . import nb_linting, repo_linting


def load_core_modules() -> None:
    nb_linting.initialize()
    repo_linting.initialize()


class PluginInterface:
    """A plugin has a single function called initialize."""

    @staticmethod
    def initialize() -> None:
        """Initialize the plugin."""


def import_module(name: str) -> PluginInterface:
    return importlib.import_module(name)  # type: ignore


def load_plugins(plugins: List[str]) -> None:
    """Load the plugins defined in the plugins list."""

    for plugin_name in plugins:
        plugin = import_module(plugin_name)
        plugin.initialize()
