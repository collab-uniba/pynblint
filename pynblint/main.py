""" Entry point of pynblint. Used when running pynblint from the command line. """

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .config import CellRenderingMode, settings
from .notebook import Notebook
from .repository import LocalRepository

app = typer.Typer()
console = Console()


@app.command()
def main(
    path: Path = typer.Argument(..., exists=True),
    render_full_cells: Optional[bool] = typer.Option(
        None,
        help="Whether to render full cells or just the first & last line of each cell.",
    ),
    display_cell_index: bool = typer.Option(
        None,
        help="Whether to display cell index \
            (i.e., the zero-based position of the cell within the notebook) \
            above rendered cells",
    ),
):

    # Update settings
    if render_full_cells:
        settings.cell_rendering_mode = CellRenderingMode.FULL

    if display_cell_index:
        settings.display_cell_index = True

    # Main procedure
    console.rule("PYNBLINT", characters="*")

    if path.is_dir:

        # Directory linting
        console.print("\n\nREPOSITORY LINTING\n")
        repo = LocalRepository(path)
        console.print(repo.get_repo_results())

    else:

        # Notebook linting
        console.print("\nNOTEBOOK LINTING\n")
        with open(path) as notebook_file:
            nb = Notebook(Path(notebook_file.name), notebook_name=path.name)
            console.print(nb.get_pynblint_results())
            console.print(nb)


if __name__ == "__main__":
    app()
