"""Linting functions for notebooks."""
import ast
import re
from typing import List, Pattern

from . import lint_register as register
from .cell import Cell, CellType
from .config import settings
from .lint import LintDefinition, LintLevel
from .notebook import Notebook

# ============== #
# NOTEBOOK LEVEL #
# ============== #


def non_linear_execution(notebook: Notebook) -> bool:
    """Check linear execution order of notebook cells."""
    exec_counters: List[int] = [
        cell.exec_count for cell in notebook.code_cells if cell.exec_count
    ]
    sorted_counters = sorted(exec_counters)
    return exec_counters != sorted_counters


def notebook_too_long(notebook: Notebook) -> bool:
    """Check if the notebook is too long (i.e., if it contains too many cells)."""

    return len(notebook) > settings.max_cells_in_notebook


def untitled_notebook(notebook: Notebook) -> bool:
    """Check whether the notebook is untitled.

    I.e., if it was left with the default title: ``Untitled.ipynb``.
    """
    res = False
    pattern: Pattern[str] = re.compile(r"Untitled\d*.ipynb")
    if pattern.match(notebook.path.name):
        res = True
    return res


def notebook_named_with_unrestricted_charset(notebook: Notebook) -> bool:
    """Check if the notebook filename contains characters outside ``[A-Za-z0-9_.-]``.

    To be supported by all popular operating systems,
    notebook names should be restricted to the ``[A-Za-z0-9_.-]`` charset.
    """
    return not re.search("^[A-Za-z0-9_.-]+$", notebook.path.name)


def long_filename(notebook: Notebook) -> bool:
    """Check if the notebook title exceedes the fixed character threshold."""
    if settings.filename_max_length:
        return len(notebook.path.name) > settings.filename_max_length
    else:
        return False


def imports_beyond_first_cell(notebook: Notebook) -> bool:
    """Check if import statements are used beyond the first code cell."""

    code = notebook.script
    found_first_cell = False
    # when `found_first_cell` is True, it means we have found the first cell of code
    # that has to be ignored

    second_cell_not_reached = True
    # when set to False, we are actually reading instructions from the second cell of
    # code; from now on we need to analyze all the cells looking for import statements

    correct_position = True
    cell = ""
    program = code.split("\n")
    for line in program:
        if not found_first_cell:
            # it ignores all the lines before the first cell generated by
            # nbconvert(python# version ecc.)
            if line[0:5] == "# In[":
                found_first_cell = True
        elif not second_cell_not_reached:
            # starting from the second cell, it saves all the instructions until
            # it finds a new cell
            if line[0:5] != "# In[":
                cell = cell + "\n" + line
            else:
                tree = ast.parse(cell)
                # once it finds a new cell, it checks if there are any import statements
                # in the previous cell
                if sum(isinstance(exp, ast.Import) for exp in tree.body) > 0:
                    correct_position = False
                    break
        else:
            if line[0:5] == "# In[":
                # following instructions are from the second cell of code,
                # the first one we have to analyze
                second_cell_not_reached = False
    return not correct_position


def missing_h1_md_heading(notebook: Notebook) -> bool:
    """Check that the notebook has an H1 Markdown title in the initial cells.

    Args:
        notebook (Notebook): the notebook to be analyzed.

    Returns:
        bool: ``True`` if the notebook does not contain an H1 title in the selected set
            of initial cells; ``False`` otherwise.
    """
    md_rows = "\n".join(
        [
            cell.cell_source
            for cell in notebook.initial_cells
            if cell.cell_type == CellType.MARKDOWN
        ]
    )
    pattern = re.compile(r"^\s*#\s*[^#\n]*$")
    return not any([pattern.match(line) for line in md_rows.splitlines()])


def missing_opening_MD_text(notebook: Notebook) -> bool:
    """Check that descriptive MD cells are present among the first cells of a notebook.

    Markdown cells containing just Markdown headings do not count.

    Args:
        notebook (Notebook): the notebook to be analyzed.

    Returns:
        bool: ``True`` if the notebook has no MD cells among its fist cells;
            ``False`` otherwise.
    """
    return not any(
        cell.cell_type == CellType.MARKDOWN and not cell.is_heading
        for cell in notebook.initial_cells
    )


def missing_closing_MD_text(notebook: Notebook) -> bool:
    """Check that descriptive MD cells are present among the first cells of a notebook.

    Markdown cells containing just Markdown headings do not count.

    Args:
        notebook (Notebook): the notebook to be analyzed.

    Returns:
        bool: ``True`` if the notebook has no MD cells among its fist cells;
            ``False`` otherwise.
    """
    return not any(
        cell.cell_type == CellType.MARKDOWN and not cell.is_heading
        for cell in notebook.final_cells
    )


def duplicate_notebook_not_renamed(notebook: Notebook) -> bool:
    """Check if the duplicate notebook has not been renamed.

    I.e., if it was left with the default title:
    ``<source-notebook-name>-Copy<copy-number>.ipynb``.
    """
    res = False
    pattern: Pattern[str] = re.compile(r".*-Copy\d+.ipynb")
    if pattern.match(notebook.path.name):
        res = True
    return res


def too_few_MD_cells(notebook: Notebook) -> bool:
    """Check that the number of MD cells is adequate.

    Check that the number of MD cells is adequate with respect
    to the number of code cells.

    Args:
        notebook (Notebook): the notebook to be analyzed.

    Returns:
        bool: ``True`` if the notebook contains too few MD cells with respect
        to the existing code cells; ``False`` otherwise.
    """
    n_of_md_cells = len(notebook.markdown_cells)
    n_of_code_cells = len(notebook.code_cells)
    if n_of_code_cells:
        ratio = n_of_md_cells / n_of_code_cells
        return ratio < settings.min_md_code_ratio
    else:
        return False


# ========== #
# CELL LEVEL #
# ========== #


def non_executed_cells(notebook: Notebook) -> List[Cell]:
    """Check the existence of non executed cells and return their list."""
    return [cell for cell in notebook.code_cells if cell.non_executed]


def empty_cells(notebook: Notebook) -> List[Cell]:
    """Check the existence of empty cells and return their list."""
    return [cell for cell in notebook.code_cells if cell.empty]


def cells_too_long(notebook: Notebook) -> List[Cell]:
    """Check whether code cells in this notebook are too long."""
    return [
        cell
        for cell in notebook.code_cells
        if len(cell.cell_source.split("\n")) > settings.max_lines_in_code_cell
    ]


# ================= #
# LINT REGISTRATION #
# ================= #


notebook_level_lints: List[LintDefinition] = [
    LintDefinition(
        slug="non-linear-execution",
        description="Notebook cells have been executed in a non-linear order.",
        recommendation="Re-run your notebook top to bottom to ensure it is "
        "reproducible.",
        linting_function=non_linear_execution,
    ),
    LintDefinition(
        slug="notebook-too-long",
        description="The notebook is too long: the total number of cells exceeds "
        f"the fixed threshold ({settings.max_cells_in_notebook}).",
        recommendation="Split this notebook into two or more notebooks.",
        linting_function=notebook_too_long,
    ),
    LintDefinition(
        slug="untitled-notebook",
        description="The notebook still has the default title: "
        "Untitled<serial-number>.ipynb",
        recommendation="Give it a meaningful title to make it easy to recognize.",
        linting_function=untitled_notebook,
    ),
    LintDefinition(
        slug="non-portable-chars-in-nb-name",
        description="The notebook filename contains non-portable characters "
        "(i.e., characters outside the [A-Za-z0-9_.-] charset).",
        recommendation="Rename your notebook by using characters contained "
        "in the following portable charset: [A-Za-z0-9_.-].",
        linting_function=notebook_named_with_unrestricted_charset,
    ),
    LintDefinition(
        slug="notebook-name-too-long",
        description="The notebook filename is too long (i.e., it exceeds the "
        f"fixed threshold of {settings.filename_max_length} characters).",
        recommendation="Use a shorter filename and leverage Markdown titles to convey "
        "detailed information.",
        linting_function=long_filename,
    ),
    LintDefinition(
        slug="imports-beyond-first-cell",
        description="Import statements found beyond the first cell of the notebook.",
        recommendation="Move import statements to the first code cell to make "
        "your notebook dependencies more explicit.",
        linting_function=imports_beyond_first_cell,
    ),
    LintDefinition(
        slug="missing-h1-MD-heading",
        description="An H1 Markdown heading is missing from the initial cells "
        "of the notebook.",
        recommendation="Clarify the notebook subject by writing an H1 Markdown heading "
        "in one of the initial cells of your notebook.",
        linting_function=missing_h1_md_heading,
    ),
    LintDefinition(
        slug="missing-opening-MD-text",
        description="The initial notebook cells "
        f"(i.e., the first {settings.initial_cells} cells in the notebook) "
        "contain no Markdown text.",
        recommendation="Begin your notebook by describing what you intend to do "
        "in one or more introductory Markdown cells.",
        linting_function=missing_opening_MD_text,
    ),
    LintDefinition(
        slug="missing-closing-MD-text",
        description="The final notebook cells "
        f"(i.e., the last {settings.final_cells} cells in the notebook) "
        "contain no Markdown text.",
        recommendation="Conclude your notebook by describing what you have accomplished"
        " in one or more concluding Markdown cells.",
        linting_function=missing_closing_MD_text,
    ),
    LintDefinition(
        slug="too-few-MD-cells",
        description="The notebook contains too few Markdown cells compared to code "
        "cells (the ratio is below the fixed threshold of "
        f"{settings.min_md_code_ratio*100}%).",
        recommendation="Describe the steps of your computation by adding "
        "a few more Markdown cells.",
        linting_function=too_few_MD_cells,
    ),
    LintDefinition(
        slug="duplicate-notebook-not-renamed",
        description="The duplicate notebook still has the default title: "
        "<source-notebook-name>-Copy<copy-number>.ipynb",
        recommendation="Give it a meaningful title to make it easy to recognize.",
        linting_function=duplicate_notebook_not_renamed,
    ),
]

cell_level_lints: List[LintDefinition] = [
    LintDefinition(
        slug="non-executed-cells",
        description="Non-executed cells are present in the notebook.",
        recommendation="Re-run your notebook top to bottom to ensure that all cells "
        "are executed.",
        linting_function=non_executed_cells,
    ),
    LintDefinition(
        slug="empty-cells",
        description="Empty cells are present in the notebook.",
        recommendation="Keep your notebook clean by deleting unused cells.",
        linting_function=empty_cells,
        show_details=False,
    ),
    LintDefinition(
        slug="cell-too-long",
        description="One or more code cells in this notebook are too long "
        "(i.e., they exceed the fixed threshold "
        f"of {settings.max_lines_in_code_cell} lines).",
        recommendation="Consider consolidating your code outside the notebook "
        "by moving utility functions to a structured and tested codebase.\n"
        "Use notebooks to display results, not to compute them.",
        linting_function=cells_too_long,
    ),
]


def initialize() -> None:
    register.register_lints(LintLevel.NOTEBOOK, notebook_level_lints)
    register.register_lints(LintLevel.CELL, cell_level_lints)
