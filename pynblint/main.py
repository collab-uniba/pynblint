""" Entry point of pynblint. Used when running pynblint from the command line. """

import json
import sys
from pathlib import Path
from typing import Union

import typer
from rich.console import Console

from . import loader
from .config import CellRenderingMode, settings
from .exceptions import ExportFormatNotSupportedError
from .nb_linter import NotebookLinter
from .notebook import Notebook
from .repo_linter import RepoLinter
from .repository import GitHubRepository, LocalRepository, Repository

app = typer.Typer()
console = Console(force_terminal=True)


@app.command()
def main(
    source: str = typer.Argument(..., exists=True),
    from_github: bool = typer.Option(
        None, help="Whether to interpret the source as the URL of a GitHub repository."
    ),
    output_file: Path = typer.Option(
        None,
        "--output",
        "--output-file",
        "-o",
        help="Path of the output file. Based on the extension of the specified filename"
        "Pynblint will chose the output format.\n"
        "Currently, the only supported export format is 'JSON' (extension: `.json`).",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Run pynblint non-interactively by always answering 'yes' "
        "to command-line prompts.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Analyze the supplied input silently "
        "(i.e., without writing to the standard output).",
    ),
    exclude: str = typer.Option(
        None,
        "--exclude",
        "-e",
        help="List of slugs of the linting rules to be ignored.\n"
        "Separate slugs with commas; do not use spaces.",
    ),
    include: str = typer.Option(
        None,
        "--include",
        "-i",
        help="List of slugs of the set of included linting rules.\n"
        "If you use this option, all the remaining linting rules will be ignored.\n"
        "Separate slugs with commas; do not use spaces.",
    ),
    hide_stats: bool = typer.Option(
        None,
        "--hide-stats",
        "-S",
        help='Hide the "STATISTICS" section from the output.',
    ),
    hide_recommendations: bool = typer.Option(
        None,
        "--hide-recommendations",
        "-R",
        help="Hide recommendations from the output.",
    ),
    render_full_cells: bool = typer.Option(
        None,
        help="Whether to render full cells or just the first & last line of each cell.",
    ),
    display_cell_index: bool = typer.Option(
        None,
        help="Whether to display cell index \
            (i.e., the zero-based position of the cell within the notebook) \
            above rendered cells.",
    ),
    initial_cells: int = typer.Option(
        None,
        help="The number of cells (from the notebook beginning) that Pynblint should "
        'consider as the "initial cells" of the notebook',
    ),
    final_cells: int = typer.Option(
        None,
        help="The number of cells (from the notebook ending) that Pynblint should "
        'consider as the "final cells" of the notebook',
    ),
    min_md_code_ratio: float = typer.Option(
        None,
        help="The minimum ratio of Markdown cells over code cells. "
        f"Defaults to {settings.min_md_code_ratio}.",
    ),
):

    # Update settings
    if exclude:
        settings.exclude = set(json.loads(exclude))

    if include:
        settings.include = set(json.loads(include))

    if hide_stats:
        settings.hide_stats = True

    if hide_recommendations:
        settings.hide_recommendations = True

    if render_full_cells:
        settings.cell_rendering_mode = CellRenderingMode.FULL

    if display_cell_index:
        settings.display_cell_index = True

    if initial_cells:
        settings.initial_cells = initial_cells

    if final_cells:
        settings.final_cells = final_cells

    if min_md_code_ratio:
        settings.min_md_code_ratio = min_md_code_ratio

    # Prevent accidental overwriting of previous output
    if output_file and output_file.is_file() and not yes:
        console.print("[red bold]The specified output file already exists.[/red bold]")
        ans = input("Do you want to overwrite it? (y/n): ")
        if ans.lower() != "y":
            sys.exit()

    # ============== #
    # Main procedure #
    # ============== #

    # Load all modules containing linting rules
    loader.load_core_modules()
    loader.load_plugins(settings.plugins)

    # Analyze the supplied input
    repo: Repository
    linter: Union[NotebookLinter, RepoLinter]

    if from_github:
        # Analyze GitHub repository
        repo = GitHubRepository(source)
        linter = RepoLinter(repo)

    else:
        path: Path = Path(source)

        if path.is_dir():
            # Analyze local uncompressed directory
            repo = LocalRepository(path)
            linter = RepoLinter(repo)

        elif path.suffix == ".ipynb":
            # Analyze standalone notebook
            with open(path) as notebook_file:
                nb = Notebook(Path(notebook_file.name))
                linter = NotebookLinter(nb)

        else:
            # Analyze local compressed directory
            repo = LocalRepository(path)
            linter = RepoLinter(repo)

    # Generate the output file if requested
    if output_file:
        if output_file.suffix == ".json":
            with open(output_file, "w") as f:
                json.dump(linter.as_dict(), f)
        else:
            raise ExportFormatNotSupportedError(
                f"The specified output file extension `{output_file.suffix}` "
                "is not supported yet."
            )

    # Print the output to the terminal
    if not quiet:
        console.print("\n")
        console.rule("PYNBLINT", characters="*")
        console.print(linter)


if __name__ == "__main__":
    app()
