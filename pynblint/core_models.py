import ast
import os
import re
import tempfile
import zipfile
from abc import ABC
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set

import git
import nbconvert
import nbformat
import rich
import toml
from isort.stdlibs.py39 import stdlib
from nbformat.notebooknode import NotebookNode
from rich.abc import RichRenderable
from rich.columns import Columns
from rich.console import Console, ConsoleOptions, RenderResult
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from yaml import safe_load

from .config import CellRenderingMode, settings
from .rich_extensions import NotebookMarkdown


class Repository(ABC):
    """
    This class stores data about a code repository.
    """

    def __init__(self, path: Path):

        # Repository info
        self.path = path

        # Extracted content
        self.notebooks: List[Notebook] = []  # List of Notebook objects
        self.dependecies_file_found: Dict[str, Path] = self.retrieve_file()
        self.declare_dependencies: set = self.get_requirement_from_file()

    def retrieve_notebooks(self):

        # Directories to ignore while traversing the tree
        dirs_ignore = [".ipynb_checkpoints"]

        for root, dirs, files in os.walk(self.path):
            # `dirs[:] = value` modifies dirs in-place
            dirs[:] = [d for d in dirs if d not in dirs_ignore]
            for f in files:
                if f.endswith(".ipynb"):
                    nb = Notebook(Path(root) / Path(f), self)
                    self.notebooks.append(nb)

    @property
    def is_git_repository(self):
        # Directories to ignore while traversing the tree
        dirs_ignore = [".ipynb_checkpoints"]
        versioned = False
        for _, dirs, _ in os.walk(self.path):
            # `dirs[:] = value` modifies dirs in-place
            dirs[:] = [d for d in dirs if d not in dirs_ignore]
            for d in dirs:
                if d == ".git":
                    versioned = True
        return versioned

    @property
    def large_file_paths(self) -> List[Path]:
        """Return the list of files whose size is above the fixed threshold.

        The threshold size for data files is defined in the settings.

        Returns:
            List[Path]: the list of large files.
        """
        large_files: List[Path] = []
        for dirpath, _, filenames in os.walk(self.path):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                if os.path.getsize(file_path) > settings.max_data_file_size:
                    large_files.append(file_path)
        return large_files

    def get_requirement_from_file(self) -> set:
        requirement_set = set()

        requirement_set.update(self._get_dependencies_from_txt())
        requirement_set.update(self._get_dependencies_from_setup())
        requirement_set.update(self._get_dependencies_from_yaml())
        requirement_set.update(self._get_dependencies_from_toml())
        requirement_set.update(self._get_dependencies_from_pipfile())

        return requirement_set

    def retrieve_file(self) -> Dict[str, Path]:
        path = Path()
        list_of_path: Dict[str, Path] = {}
        for root, dirs, files in os.walk(self.path):
            dirs[:] = [d for d in dirs]
            for f in files:
                if f.endswith("enviroment.yaml"):
                    path = Path(root) / Path(f)
                    list_of_path["enviroment.yaml"] = path
                elif f.endswith("Pipfile"):
                    path = Path(root) / Path(f)
                    list_of_path["Pipfile"] = path
                elif f.endswith("setup.py"):
                    path = Path(root) / Path(f)
                    list_of_path["setup.py"] = path
                elif f.endswith("pyproject.toml"):
                    path = Path(root) / Path(f)
                    list_of_path["pyproject.toml"] = path
                elif f.endswith("requirements.txt"):
                    path = Path(root) / Path(f)
                    list_of_path["requirements.txt"] = path
        return list_of_path

    def _get_dependencies_from_txt(self) -> set:
        """this function after fetching the location of the
        .txt file reads it and scans it for dependencies"""
        txt_dependencies = set()
        try:
            path = self.dependecies_file_found["requirements.txt"]
            if path is not None:
                with open(path, "r") as fi:
                    row_file = fi.read()
                    tmp = row_file.split("\n")
                    for item in tmp:
                        item.strip()
                    txt_dependencies.add(item.split("==")[0])
                    fi.close()

        except KeyError:
            return txt_dependencies

        return txt_dependencies

    def _get_dependencies_from_toml(self) -> set:
        toml_dependencies = set()
        try:
            path = self.dependecies_file_found["pyproject.toml"]
            if path is not None:
                data = toml.load(path)
                tmp_list = [
                    x.split("=")[0] for x in data["tool"]["poetry"]["dev-dependencies"]
                ]
                for i in tmp_list:
                    toml_dependencies.add(i)
        except KeyError:
            return toml_dependencies

        return toml_dependencies

    def _get_dependencies_from_yaml(self) -> set:
        yaml_dependencies = set()
        try:
            path = self.dependecies_file_found["enviroment.yaml"]
            if path is not None:
                with open(path, "r") as fi:
                    row_file = fi.read()
                    data = safe_load(row_file)
                    tmp_list = [x.split("==")[0] for x in data["requirements"]]
                    for i in tmp_list:
                        yaml_dependencies.add(i)
                fi.close()

        except KeyError:
            return yaml_dependencies

        return yaml_dependencies

    def _get_dependencies_from_pipfile(self) -> set:
        pip_dependencies = set()
        try:
            path = self.dependecies_file_found["Pipfile"]
            if path is not None:
                data = toml.load(path)
                tmp_list = [x.split("=")[0] for x in data["dev-packages"]]
                for i in tmp_list:
                    pip_dependencies.add(i)
        except KeyError:
            return pip_dependencies

        return pip_dependencies

    def _get_dependencies_from_setup(self) -> set:
        setup_dependencies = set()
        try:
            path = self.dependecies_file_found["setup.py"]
            if path is not None:
                with open(path, "r") as fi:
                    row_file = fi.read()
                    point = row_file.find("install_requires")
                    if point != -1:
                        tmp = row_file[point:-2]
                        tmp = tmp.replace("install_requires=[", "")
                        tmp = tmp.replace("]", "").strip()
                        tmp = tmp.replace('"', "").strip()
                        tmp = tmp.replace("<", "").strip()
                        tmp = tmp.replace(">", "").strip()
                        tmp_split = tmp.split(",")
                        for x in tmp_split:
                            tmp = x.split("=")[0]
                            setup_dependencies.add(tmp.strip())
                fi.close()
        except KeyError:
            return setup_dependencies

        return setup_dependencies

    def _get_core_dependecies(self) -> set:
        coredependecies = set()
        for name in sorted(stdlib):
            coredependecies.add(name)
        return coredependecies


class LocalRepository(Repository):
    """
    This class stores data about a local code repository.
    The `source_path` can point either to a local directory or a zip archive
    """

    def __init__(self, source_path: Path):

        self.source_path = source_path
        tmp_dir: Optional[tempfile.TemporaryDirectory] = None

        # Handle .zip archives
        if self.source_path.suffix == ".zip":

            # Create temp directory
            tmp_dir = tempfile.TemporaryDirectory()
            repo_path: Path = Path(tmp_dir.name)

            # Extract the zip file into the temp folder
            with zipfile.ZipFile(self.source_path, "r") as zip_file:
                zip_file.extractall(repo_path)

        # Handle local folders
        elif self.source_path.is_dir():
            repo_path = self.source_path

        else:
            raise ValueError(
                "The file at the specified path is neither a notebook (.ipynb) "
                "nor a compressed archive."
            )

        super().__init__(repo_path)
        self.retrieve_notebooks()

        # Clean up the temp directory if one was created
        if tmp_dir is not None:
            tmp_dir.cleanup()


class GitHubRepository(Repository):
    """
    This class stores data about a GitHub repository
    """

    def __init__(self, github_url: str):

        self.url = github_url

        # Clone the repo in a temp directory
        tmp_dir = tempfile.TemporaryDirectory()
        git.Repo.clone_from(  # type: ignore
            url=github_url, to_path=tmp_dir.name, depth=1
        )
        super().__init__(Path(tmp_dir.name) / github_url.split("/")[-1])

        # Analyze the repo
        self.retrieve_notebooks()

        # Clean up the temp directory
        tmp_dir.cleanup()


class CellType(str, Enum):
    MARKDOWN = "markdown"
    CODE = "code"
    RAW = "raw"
    OTHER = "other"


class Cell(RichRenderable):
    def __init__(self, cell_index: int, cell_dict: NotebookNode) -> None:
        """Pynblint's representation of a notebook cell."""

        self.cell_index: int = cell_index
        self._cell_dict: NotebookNode = cell_dict

        # Cell type
        self.cell_type: CellType
        if self._cell_dict["cell_type"] == "markdown":
            self.cell_type = CellType.MARKDOWN
        elif self._cell_dict["cell_type"] == "code":
            self.cell_type = CellType.CODE
        elif self._cell_dict["cell_type"] == "raw":
            self.cell_type = CellType.RAW
        else:
            self.cell_type = CellType.OTHER

        # Execution count
        if self.cell_type == CellType.CODE:
            self.exec_count: int = self._cell_dict["execution_count"]

        # Cell source and source excerpt (for cell visualization with Rich)
        self.cell_source: str = self._cell_dict["source"]
        self._source_excerpt: str = ""

        if settings.cell_rendering_mode == CellRenderingMode.COMPACT:
            cell_source_array = self.cell_source.split("\n")
            if len(cell_source_array) > 2:
                self._source_excerpt = "\n".join(
                    [cell_source_array[0], "\n[...]\n", cell_source_array[-1]]
                )
            else:
                self._source_excerpt = self.cell_source
        else:
            self._source_excerpt = self.cell_source

    @property
    def empty(self) -> bool:
        """Return ``True`` if the code cell is empty."""
        if self.cell_type == CellType.CODE:
            return (self.exec_count is None) and (len(self.cell_source) == 0)
        else:
            raise Exception("The `empty` property is defined only for code cells.")

    @property
    def non_executed(self) -> bool:
        """Return ``True`` if the code cell is not empty and has not been executed."""
        if self.cell_type == CellType.CODE:
            return (self.exec_count is None) and (len(self.cell_source) > 0)
        else:
            raise Exception(
                "The `non_executed` property is defined only for code cells."
            )

    @property
    def is_heading(self) -> bool:
        """Return ``True`` if the cell is an MD cell containing only MD headings."""
        if self.cell_type == CellType.MARKDOWN:
            pattern = re.compile(r"^\s*#{1,6}\s*[^#\n]*$")
            return all(
                pattern.match(line)
                for line in self.cell_source.splitlines()
                if line and (not line.isspace())
            )
        else:
            return False

    def as_dict(self, source: bool = True) -> Dict:
        cell_dict = {
            "index": self.cell_index,
            "type": str(self.cell_type),
        }
        if self.cell_type == CellType.CODE:
            cell_dict["execution_count"] = self.exec_count
        if source:
            cell_dict["source"] = self._source_excerpt
        return cell_dict

    def __rich__(self) -> Columns:

        if self.cell_type == CellType.CODE:
            counter = self.exec_count or " "
            if settings.display_cell_index:
                panel_title = f"Index: {self.cell_index}"
            else:
                panel_title = None
            rendered_cell = Columns(
                [
                    f"\nIn [{counter}]:",
                    Panel(
                        Syntax(
                            self._source_excerpt, "python", background_color="default"
                        ),
                        width=int(rich.get_console().size[0] * 0.85),
                        title=panel_title,
                    ),
                ]
            )
        else:
            rendered_cell = Columns(
                [
                    "        ",
                    Padding(NotebookMarkdown(self._source_excerpt), (1, 0, 1, 8)),
                ]
            )

        return rendered_cell


class Notebook(RichRenderable):
    """
    This class stores the representations of a notebook
    on which pynblint functions are called
    """

    def __init__(self, path: Path, repository: Optional[Repository] = None):
        self.path: Path = path
        self.repository: Optional[Repository] = repository

        # Read the notebook with nbformat
        with open(self.path) as f:
            nb_raw = f.read()
        self.nb_dict: NotebookNode = nbformat.reads(nb_raw, as_version=4)

        # Populate the list of Cells
        self.cells: List[Cell] = [
            Cell(cell_index, cell_dict)
            for cell_index, cell_dict in enumerate(self.nb_dict.cells)
        ]
        self.non_executed = all([cell.non_executed for cell in self.code_cells])

        # Convert the notebook to a Python script
        python_exporter = nbconvert.PythonExporter()
        self.script, _ = python_exporter.from_notebook_node(self.nb_dict)

        # Extract the Python abstract syntax tree
        # (or set `has_invalid_python_syntax` to True)
        self.has_invalid_python_syntax: bool = False
        try:
            self.ast = ast.parse(self.script)
        except SyntaxError:
            self.has_invalid_python_syntax = True

        # Get the set of imported Python packages
        if not self.has_invalid_python_syntax:
            self.imported_packages: Set = self._get_imported_packages()

    @property
    def code_cells(self) -> List[Cell]:
        code_cells = [cell for cell in self.cells if cell.cell_type == CellType.CODE]
        return code_cells

    @property
    def markdown_cells(self) -> List[Cell]:
        md_cells = [cell for cell in self.cells if cell.cell_type == CellType.MARKDOWN]
        return md_cells

    @property
    def initial_cells(self) -> List[Cell]:
        return self.cells[: settings.initial_cells]

    @property
    def final_cells(self) -> List[Cell]:
        return self.cells[-settings.final_cells :]  # noqa: E203

    def _get_imported_packages(self) -> Set:
        """Builds the set of packages and modules imported in the notebook.

        Sice it relies on the ``ast`` module, this function works only for notebooks
        with a valid Python syntax. Therefore, a ``ValueError`` exception is raised if
        this function is invoked on a notebook containing syntactic Python errors.

        Returns:
            Set: the set of packages and modules imported in the notebook.
        """

        if self.has_invalid_python_syntax:
            raise ValueError(
                "Imported packages cannot be parsed in notebooks with invalid "
                "Python syntax."
            )

        imported_packages: Set = set()
        for node in ast.walk(self.ast):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imported_packages.add(name.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level > 0:
                    # Relative imports always refer to the current package.
                    continue
                if node.module:
                    imported_packages.add(node.module.split(".")[0])
        return imported_packages

    def __len__(self) -> int:
        return len(self.cells)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        return self.cells
