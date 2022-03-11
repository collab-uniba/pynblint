""" Entry point of pynblint. Used when running pynblint from the command line. """

from pathlib import Path

import typer
from rich.console import Console

from . import loader
from .config import CellRenderingMode, settings
from .nb_linter import NotebookLinter
from .notebook import Notebook
from .repo_linter import RepoLinter
from .repository import GitHubRepository, LocalRepository, Repository

app = typer.Typer()
console = Console(force_terminal=True)


loader.load_core_modules()
loader.load_plugins(settings.plugins)


@app.command()
def main(
    source: str = typer.Argument(..., exists=True),
    from_github: bool = typer.Option(
        None, help="Whether to interpret the source as the URL of a GitHub repository."
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
    if render_full_cells:
        settings.cell_rendering_mode = CellRenderingMode.FULL

    if display_cell_index:
        settings.display_cell_index = True

    if initial_cells:
        settings.initial_cells = initial_cells

    if final_cells:
        settings.final_cells = final_cells

    # Main procedure
    console.print("\n")
    console.rule("PYNBLINT", characters="*")
    repo: Repository

    if from_github:
        # Analyze GitHub repository
        repo = GitHubRepository(source)
        repo_linter = RepoLinter(repo)
        console.print(repo_linter)

    else:
        path: Path = Path(source)

        if path.is_dir():
            # Analyze local uncompressed directory
            repo = LocalRepository(path)
            repo_linter = RepoLinter(repo)
            console.print(repo_linter)

        elif path.suffix == ".ipynb":
            # Analyze standalone notebook
            with open(path) as notebook_file:
                nb = Notebook(Path(notebook_file.name))
                nb_linter = NotebookLinter(nb)
                console.print(nb_linter)

        else:
            # Analyze local compressed directory
            repo = LocalRepository(path)
            repo_linter = RepoLinter(repo)
            console.print(repo_linter)


if __name__ == "__main__":
    app()
