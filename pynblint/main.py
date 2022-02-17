""" Entry point of pynblint. Used when running pynblint from the command line. """

from pathlib import Path

import typer
from rich.console import Console

from .config import CellRenderingMode, settings
from .nb_linting import NotebookLinter
from .notebook import Notebook
from .repo_linting import RepoLinter
from .repository import GitHubRepository, LocalRepository, Repository

app = typer.Typer()
console = Console()


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
):

    # Update settings
    if render_full_cells:
        settings.cell_rendering_mode = CellRenderingMode.FULL

    if display_cell_index:
        settings.display_cell_index = True

    # Main procedure
    console.rule("PYNBLINT", characters="*")
    repo: Repository

    if from_github:
        # Analyze GitHub repository
        repo = GitHubRepository(source)
        repo_linter = RepoLinter(repo)
        console.print(repo_linter.get_linting_results())

    else:
        path: Path = Path(source)

        if path.is_dir():
            # Analyze local uncompressed directory
            repo = LocalRepository(path)
            repo_linter = RepoLinter(repo)
            console.print(repo_linter.get_linting_results())

        elif path.suffix == ".ipynb":
            # Analyze standalone notebook
            with open(path) as notebook_file:
                nb = Notebook(Path(notebook_file.name))
                nb_linter = NotebookLinter(nb)
                console.print(nb_linter.get_linting_results())
                console.print(nb)

        else:
            # Analyze local compressed directory
            repo = LocalRepository(path)
            repo_linter = RepoLinter(repo)
            console.print(repo_linter.get_linting_results())


if __name__ == "__main__":
    app()
